const { readFileSync } = require('node:fs');

const FAILURE_ISSUE_TITLE = 'Codex docs sync failure';
const LEGACY_FAILURE_TITLE = /^Codex docs sync failed - \d{4}-\d{2}-\d{2}$/;

function readText(path, reader = readFileSync) {
  try {
    return reader(path, 'utf8');
  } catch {
    return '';
  }
}

function tailLines(text, lineCount) {
  return text.split(/\r?\n/).slice(-lineCount).join('\n');
}

function runUrl(context) {
  return `${context.serverUrl}/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}`;
}

function buildFailureBody({ date, workflowRunUrl, syncLog, syncSummary, sourceCoverage }) {
  const syncLogTail = tailLines(syncLog, 120).slice(-12000) || '(no log available)';
  const summary = syncSummary.slice(-12000) || '(no sync summary available)';
  const coverage = sourceCoverage.slice(-12000) || '(no source coverage available)';

  return [
    `Automated docs sync failed or recorded source failures on ${date}.`,
    '',
    `Workflow run: ${workflowRunUrl}`,
    '',
    '### Sync summary',
    '```json',
    summary,
    '```',
    '',
    '### Source coverage',
    '```json',
    coverage,
    '```',
    '',
    '### Sync log tail',
    '```text',
    syncLogTail,
    '```',
  ].join('\n');
}

function buildRecoveryBody({ date, workflowRunUrl }) {
  return [
    `Automated docs sync recovered on ${date}; closing this rolling incident.`,
    '',
    `Workflow run: ${workflowRunUrl}`,
  ].join('\n');
}

async function findOpenFailureIssue({ github, context }) {
  const openIssues = await github.paginate(github.rest.issues.listForRepo, {
    owner: context.repo.owner,
    repo: context.repo.repo,
    state: 'open',
    per_page: 100,
  });
  const issues = openIssues.filter((issue) => !issue.pull_request);
  return (
    issues.find((issue) => issue.title === FAILURE_ISSUE_TITLE) ||
    issues.find((issue) => LEGACY_FAILURE_TITLE.test(issue.title)) ||
    null
  );
}

async function recordFailure({ github, context, reader = readFileSync, now = new Date() }) {
  const date = now.toISOString().split('T')[0];
  const body = buildFailureBody({
    date,
    workflowRunUrl: runUrl(context),
    syncLog: readText('sync.log', reader),
    syncSummary: readText('docs/sync_summary.json', reader),
    sourceCoverage: readText('docs/source_coverage.json', reader),
  });
  const issue = await findOpenFailureIssue({ github, context });
  const repository = { owner: context.repo.owner, repo: context.repo.repo };

  if (!issue) {
    await github.rest.issues.create({
      ...repository,
      title: FAILURE_ISSUE_TITLE,
      body,
      labels: ['bug'],
    });
    return;
  }

  if (issue.title !== FAILURE_ISSUE_TITLE) {
    await github.rest.issues.update({
      ...repository,
      issue_number: issue.number,
      title: FAILURE_ISSUE_TITLE,
    });
  }
  await github.rest.issues.createComment({
    ...repository,
    issue_number: issue.number,
    body,
  });
}

async function closeRecoveredFailure({ github, context, now = new Date() }) {
  const issue = await findOpenFailureIssue({ github, context });
  if (!issue) {
    return;
  }
  const date = now.toISOString().split('T')[0];
  const repository = { owner: context.repo.owner, repo: context.repo.repo };
  await github.rest.issues.createComment({
    ...repository,
    issue_number: issue.number,
    body: buildRecoveryBody({ date, workflowRunUrl: runUrl(context) }),
  });
  await github.rest.issues.update({
    ...repository,
    issue_number: issue.number,
    state: 'closed',
    state_reason: 'completed',
  });
}

module.exports = {
  FAILURE_ISSUE_TITLE,
  buildFailureBody,
  buildRecoveryBody,
  closeRecoveredFailure,
  findOpenFailureIssue,
  recordFailure,
  tailLines,
};
