const { execFileSync } = require('node:child_process');

const BOT = 'github-actions[bot]';
const EMAIL = 'github-actions[bot]@users.noreply.github.com';
const ISSUE_PREFIX = 'VERSION bump proposal: v';
function git(...args) { return execFileSync('git', args, { encoding: 'utf8' }).trim(); }
function nextVersion(current, level = 'patch') {
  if (!/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/.test(current)) throw new Error('Invalid VERSION');
  const parts = current.split('.').map(Number);
  const index = ['major', 'minor', 'patch'].indexOf(level);
  if (index < 0 || parts.some((part) => !Number.isSafeInteger(part))) throw new Error('Invalid bump level or version');
  parts[index] += 1;
  if (!Number.isSafeInteger(parts[index])) throw new Error('Version overflow');
  for (let i = index + 1; i < 3; i++) parts[i] = 0;
  return parts.join('.');
}
function compareVersions(a, b) {
  const left = a.split('.').map(Number), right = b.split('.').map(Number);
  for (let i = 0; i < 3; i++) if (left[i] !== right[i]) return left[i] - right[i];
  return 0;
}
function safeBranch({ files, version, authors, mergeBaseVersion, current, next }) {
  return files.length === 1 && files[0] === 'VERSION' && version === next
    && mergeBaseVersion === current && authors.length > 0 && authors.every((author) => author === EMAIL);
}
function prepareBranch({ branch, current, next, title, runGit = git, writeVersion = (value) => require('node:fs').writeFileSync('VERSION', `${value}\n`) }) {
  const base = runGit('rev-parse', 'HEAD');
  const remote = runGit('ls-remote', '--heads', 'origin', `refs/heads/${branch}`);
  runGit('config', '--local', 'user.name', BOT);
  runGit('config', '--local', 'user.email', EMAIL);
  if (remote) {
    const observed = remote.split(/\s+/)[0];
    runGit('fetch', '--no-tags', 'origin', `refs/heads/${branch}`);
    const head = runGit('rev-parse', 'FETCH_HEAD');
    if (head !== observed) throw new Error('Proposal branch moved during inspection; retry');
    const mergeBase = runGit('merge-base', base, head);
    const safe = safeBranch({
      files: runGit('diff', '--name-only', `${mergeBase}..${head}`).split('\n').filter(Boolean),
      version: runGit('show', `${head}:VERSION`),
      authors: runGit('log', '--format=%ae', `${base}..${head}`).split('\n').filter(Boolean),
      mergeBaseVersion: runGit('show', `${mergeBase}:VERSION`), current, next,
    });
    if (!safe) return { ready: false, reason: 'Existing branch is not an automation-owned VERSION-only proposal for this base. Review it manually; no branch content was changed.' };
    runGit('switch', '--create', branch, head);
    // Refresh by a signed-off merge, never by force-pushing over an existing ref.
    if (mergeBase !== base) {
      runGit('merge', '--no-ff', '--no-commit', base);
      runGit('commit', '-s', '-m', `chore: refresh VERSION proposal for v${next}`);
    }
  } else {
    runGit('switch', '--create', branch, base);
    writeVersion(next);
    runGit('add', 'VERSION');
    runGit('commit', '-s', '-m', title);
  }
  const latestBase = runGit('ls-remote', '--heads', 'origin', 'refs/heads/main').split(/\s+/)[0];
  if (latestBase !== base) throw new Error('main moved during proposal generation; retry from current main');
  // Normal fast-forward push rejects any concurrent branch writer.
  runGit('push', 'origin', `HEAD:refs/heads/${branch}`);
  return { ready: true };
}
function creationForbidden(error) {
  return error.status === 403 && /GitHub Actions is not permitted to create or approve pull requests/i.test(error.message);
}
async function propose({ github, context, level = 'patch', prepare = prepareBranch, current = git('show', 'HEAD:VERSION') }) {
  const next = nextVersion(current, level);
  const branch = `chore/version-bump-v${next}`, title = `chore: bump VERSION to v${next}`;
  const repository = context.repo;
  const runUrl = `${context.serverUrl}/${repository.owner}/${repository.repo}/actions/runs/${context.runId}`;
  const issues = (await github.paginate(github.rest.issues.listForRepo, { ...repository, state: 'open', per_page: 100 }))
    .filter((issue) => !issue.pull_request && issue.title.startsWith(ISSUE_PREFIX));
  async function resolve(issue, resolution) {
    await github.rest.issues.update({ ...repository, issue_number: issue.number, state: 'closed', state_reason: 'completed',
      body: `${resolution}\n\nWorkflow run: ${runUrl}` });
  }
  for (const issue of issues) {
    const version = issue.title.slice(ISSUE_PREFIX.length);
    if (/^\d+\.\d+\.\d+$/.test(version) && compareVersions(version, current) <= 0)
      await resolve(issue, `Resolved: main now contains VERSION ${current}.`);
  }
  const tracking = issues.find((issue) => issue.title === ISSUE_PREFIX + next);
  const pulls = await github.paginate(github.rest.pulls.list, { ...repository, state: 'open', base: 'main', per_page: 100 });
  const existing = pulls.find((pr) => pr.head?.repo?.full_name === `${repository.owner}/${repository.repo}`
    && (pr.head.ref === branch || pr.title === title));
  if (existing) {
    if (tracking) await resolve(tracking, `Resolved by pull request: ${existing.html_url}`);
    return { status: 'existing', url: existing.html_url };
  }
  async function track(reason) {
    const body = [
      `VERSION proposal: ${current} → ${next}.`, '', `Branch: \`${branch}\``,
      `Compare: ${context.serverUrl}/${repository.owner}/${repository.repo}/compare/main...${branch}`,
      `Latest workflow run: ${runUrl}`, '', reason,
    ].join('\n');
    if (tracking) await github.rest.issues.update({ ...repository, issue_number: tracking.number, body });
    else await github.rest.issues.create({ ...repository, title: ISSUE_PREFIX + next, body });
  }
  const prepared = prepare({ branch, current, next, title });
  if (!prepared.ready) { await track(prepared.reason); return { status: 'manual_review' }; }
  let pr;
  try {
    ({ data: pr } = await github.rest.pulls.create({ ...repository, base: 'main', head: branch, title,
      body: `## Summary\n\nBump the repository tooling release from v${current} to v${next}. Merging updates VERSION; the release workflow publishes v${next}.` }));
  } catch (error) {
    if (!creationForbidden(error)) throw error;
    await track('GitHub rejected PR creation because Actions-created pull requests are disabled. A maintainer can open a PR from this exact branch, or enable “Allow GitHub Actions to create and approve pull requests” under Settings → Actions → General, then rerun this workflow. No repository setting was changed.');
    return { status: 'creation_disabled' };
  }
  if (tracking) await resolve(tracking, `Resolved by pull request: ${pr.html_url}`);
  return { status: 'created', url: pr.html_url };
}
module.exports = { nextVersion, safeBranch, prepareBranch, creationForbidden, propose };
