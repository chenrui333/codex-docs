const { readFileSync } = require('node:fs');
const { createHash } = require('node:crypto');

const FAILURE_ISSUE_TITLE = 'Codex docs sync failure';
const LEGACY_FAILURE_TITLE = /^Codex docs sync failed - \d{4}-\d{2}-\d{2}$/;
const MARKER = /<!-- sync-incident: (\{[^\n]+\}) -->/;

function readText(path, reader = readFileSync) {
  try { return reader(path, 'utf8'); } catch { return ''; }
}
function parseJson(text) {
  try { return JSON.parse(text); } catch { return null; }
}
function bounded(value, limit = 300) {
  return String(value ?? '').replace(/\r/g, '').slice(0, limit);
}
function tailLines(text, count) {
  return text.split(/\r?\n/).slice(-count).join('\n');
}
function runUrl(context) {
  return `${context.serverUrl}/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}`;
}
function errorClass(error) {
  const text = String(error || '').toLowerCase();
  if (/timed?\s*out|timeout/.test(text)) return 'timeout';
  if (/429|rate.limit/.test(text)) return 'rate_limit';
  if (/\b5\d\d\b/.test(text)) return 'http_5xx';
  if (/\b4\d\d\b/.test(text)) return 'http_4xx';
  if (/connection|dns|resolve/.test(text)) return 'connection';
  if (/malformed|content.type|empty response|parse|invalid json/.test(text)) return 'invalid_content';
  return bounded(text.replace(/0x[\da-f]+|\b\d+\b/g, '#').replace(/\s+/g, ' '), 120) || 'unknown';
}
function failureKey(failure) {
  let url = bounded(failure.url, 1000);
  try { const parsed = new URL(url); parsed.search = ''; parsed.hash = ''; url = parsed.href; } catch { /* non-HTTP source */ }
  return {
    source: bounded(failure.source), stage: bounded(failure.stage),
    state: bounded(failure.state), url, error_class: errorClass(failure.error),
  };
}
function diagnosticState({ syncLog = '', syncSummary = '', sourceCoverage = '', freshnessStatus = '' }) {
  // Strict failures leave canonical reports unchanged. Prefer this run's structured log.
  const log = syncLog.slice(-1024 * 1024);
  let failures = log.split(/\r?\n/).flatMap((line) => {
    const match = line.match(/Source transaction failed: (\{.*\})/);
    const value = match && parseJson(match[1]);
    return value && typeof value === 'object' ? [value] : [];
  });
  if (!failures.length) {
    const summary = parseJson(syncSummary);
    failures = Array.isArray(summary?.failures) ? summary.failures.filter((item) => item && typeof item === 'object') : [];
  }
  if (!failures.length) {
    const freshness = parseJson(freshnessStatus);
    failures = (Array.isArray(freshness?.checks) ? freshness.checks : [])
      .filter((check) => check.status === 'fail')
      .map((check) => ({ source: 'freshness', stage: check.name, state: 'failed', error: 'invariant failed' }));
  }
  if (!failures.length) {
    const error = tailLines(log, 30).split('\n').filter((line) => /error|failed|exception/i.test(line)).pop();
    failures = [{ source: 'workflow', stage: 'sync', state: 'failed', error: error || 'diagnostics unavailable' }];
  }
  const unique = [...new Set(failures.map((failure) => JSON.stringify(failureKey(failure))))].sort();
  return {
    fingerprint: createHash('sha256').update(unique.join('\n')).digest('hex'),
    failures: unique.map((value) => JSON.parse(value)),
    reports: {
      summary: parseJson(syncSummary) ? 'available (may be last successful state)' : 'missing or invalid',
      coverage: parseJson(sourceCoverage) ? 'available (may be last successful state)' : 'missing or invalid',
    },
  };
}
function buildFailureBody({ date, firstSeen = date, workflowRunUrl, state, ...diagnostics }) {
  state ||= diagnosticState(diagnostics);
  const metadata = { fingerprint: state.fingerprint, first_seen: firstSeen };
  return [
    `<!-- sync-incident: ${JSON.stringify(metadata)} -->`,
    'Automated documentation sync is failing.', '',
    `First seen: ${firstSeen}`, `Latest seen: ${date}`,
    `Latest workflow run and diagnostic artifacts: ${workflowRunUrl}`, '',
    `Failure fingerprint: \`${state.fingerprint}\``, '',
    '### Current failures', '```json',
    JSON.stringify(state.failures.slice(0, 8), null, 2).slice(0, 6000), '```',
    ...(state.failures.length > 8 ? [`${state.failures.length - 8} additional failures are available in the workflow log.`] : []),
    '', 'Canonical coverage, summary, and freshness artifacts can describe the last successful transaction; they are not proof that this attempt succeeded.',
    `Summary: ${state.reports.summary}; coverage: ${state.reports.coverage}.`,
  ].join('\n');
}
function buildRecoveryBody({ date, workflowRunUrl }) {
  return `Automated docs sync recovered on ${date}; closing this rolling incident.\n\nWorkflow run: ${workflowRunUrl}`;
}
async function findOpenFailureIssue({ github, context }) {
  const issues = await github.paginate(github.rest.issues.listForRepo, {
    ...context.repo, state: 'open', per_page: 100,
  });
  return issues.find((issue) => !issue.pull_request && issue.title === FAILURE_ISSUE_TITLE)
    || issues.find((issue) => !issue.pull_request && LEGACY_FAILURE_TITLE.test(issue.title)) || null;
}
async function recordFailure({ github, context, reader = readFileSync, now = new Date() }) {
  const issue = await findOpenFailureIssue({ github, context });
  const previous = parseJson(issue?.body?.match(MARKER)?.[1] || '');
  const date = now.toISOString();
  const firstSeen = previous?.first_seen || issue?.created_at || date;
  const state = diagnosticState({
    syncLog: readText('sync.log', reader), syncSummary: readText('docs/sync_summary.json', reader),
    sourceCoverage: readText('docs/source_coverage.json', reader), freshnessStatus: readText('docs/freshness.json', reader),
  });
  const body = buildFailureBody({ date, firstSeen, workflowRunUrl: runUrl(context), state });
  if (!issue) {
    await github.rest.issues.create({ ...context.repo, title: FAILURE_ISSUE_TITLE, body, labels: ['bug'] });
    return;
  }
  // Adopting a legacy issue needs no additional copy of its already-large diagnostics.
  if (previous?.fingerprint && previous.fingerprint !== state.fingerprint) {
    await github.rest.issues.createComment({ ...context.repo, issue_number: issue.number,
      body: `Failure changed on ${date}: \`${previous.fingerprint}\` → \`${state.fingerprint}\`.\n\nWorkflow run: ${runUrl(context)}` });
  }
  await github.rest.issues.update({ ...context.repo, issue_number: issue.number, title: FAILURE_ISSUE_TITLE, body });
}
async function closeRecoveredFailure({ github, context, now = new Date() }) {
  const issue = await findOpenFailureIssue({ github, context });
  if (!issue) return;
  await github.rest.issues.createComment({ ...context.repo, issue_number: issue.number,
    body: buildRecoveryBody({ date: now.toISOString(), workflowRunUrl: runUrl(context) }) });
  await github.rest.issues.update({ ...context.repo, issue_number: issue.number, state: 'closed', state_reason: 'completed' });
}
module.exports = { FAILURE_ISSUE_TITLE, buildFailureBody, buildRecoveryBody, closeRecoveredFailure,
  findOpenFailureIssue, recordFailure, tailLines, diagnosticState };
