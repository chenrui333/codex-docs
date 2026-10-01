const assert = require('node:assert/strict');
const test = require('node:test');
const { nextVersion, safeBranch, creationForbidden, propose } = require('../.github/scripts/version-proposal.cjs');
const context = { repo: { owner: 'example', repo: 'mirror' }, runId: 1, serverUrl: 'https://github.example' };
const forbidden = Object.assign(new Error('GitHub Actions is not permitted to create or approve pull requests.'), { status: 403 });
function fake({ issues = [], prs = [], error } = {}) {
  const calls = [];
  return { calls, github: { paginate: async (fn) => fn === 'issues' ? issues : prs, rest: {
    issues: { listForRepo: 'issues', create: async (args) => calls.push(['issue', args]), update: async (args) => calls.push(['update', args]) },
    pulls: { list: 'pulls', create: async (args) => { calls.push(['pr', args]); if (error) throw error; return { data: { html_url: 'https://example/pr/1' } }; } },
  } } };
}
const tracking = { number: 48, title: 'VERSION bump proposal: v0.1.1' };
const invoke = (client, options = {}) => propose({ github: client.github, context, current: '0.1.0', prepare: () => ({ ready: true }), ...options });
test('computes semantic bumps and rejects invalid input', () => {
  assert.equal(nextVersion('0.1.0'), '0.1.1'); assert.equal(nextVersion('0.1.9', 'minor'), '0.2.0');
  assert.equal(nextVersion('0.1.9', 'major'), '1.0.0');
  for (const value of ['v1.0.0', '1.2', '01.2.3', '1.2.3\n', '9007199254740992.0.0']) assert.throws(() => nextVersion(value));
  assert.throws(() => nextVersion('1.2.3', 'bad'));
});
test('only intended automation-owned VERSION-only branches are refreshable', () => {
  const state = { files: ['VERSION'], version: '0.1.1', next: '0.1.1', current: '0.1.0', mergeBaseVersion: '0.1.0', authors: ['github-actions[bot]@users.noreply.github.com'] };
  assert.equal(safeBranch(state), true);
  for (const change of [{ files: ['VERSION', 'README.md'] }, { authors: ['human@example.test'] }, { authors: [] }, { version: '9.0.0' }, { mergeBaseVersion: '0.0.9' }])
    assert.equal(safeBranch({ ...state, ...change }), false);
});
test('creates PR and resolves tracking issue', async () => {
  const c = fake({ issues: [tracking] }); const result = await invoke(c);
  assert.equal(result.status, 'created'); assert.equal(c.calls[0][0], 'pr');
  assert.equal(c.calls[1][1].state, 'closed');
});
test('existing branch or title PR prevents branch writes and resolves issue', async () => {
  for (const pr of [{ title: 'renamed', head: { ref: 'chore/version-bump-v0.1.1', repo: { full_name: 'example/mirror' } } },
    { title: 'chore: bump VERSION to v0.1.1', head: { ref: 'old-version-branch', repo: { full_name: 'example/mirror' } } }]) {
    const c = fake({ issues: [tracking], prs: [{ ...pr, html_url: 'https://example/pr' }] });
    assert.equal((await invoke(c, { prepare: () => assert.fail('unexpected branch write') })).status, 'existing');
    assert.equal(c.calls[0][1].state, 'closed');
  }
});
test('disabled PR creation updates one concise issue without comments', async () => {
  const c = fake({ issues: [tracking], error: forbidden });
  assert.equal((await invoke(c)).status, 'creation_disabled');
  assert.deepEqual(c.calls.map(([type]) => type), ['pr', 'update']);
  assert.match(c.calls[1][1].body, /chore\/version-bump-v0.1.1/); assert.match(c.calls[1][1].body, /maintainer/);
  assert.ok(c.calls[1][1].body.length < 1500);
  const first = fake({ error: forbidden }); await invoke(first); assert.equal(first.calls[1][0], 'issue');
});
test('unrelated branch requires human review and is never used for a PR', async () => {
  const c = fake(); assert.equal((await invoke(c, { prepare: () => ({ ready: false, reason: 'unrelated human work' }) })).status, 'manual_review');
  assert.deepEqual(c.calls.map(([type]) => type), ['issue']);
});
test('unexpected API failures remain visible failures', async () => {
  for (const error of [Object.assign(new Error('Resource not accessible'), { status: 403 }), Object.assign(new Error('rate limit'), { status: 429 }), new Error('network')]) {
    assert.equal(creationForbidden(error), false); await assert.rejects(invoke(fake({ error })), error);
  }
});
test('main VERSION advancement resolves old proposal tracking', async () => {
  const c = fake({ issues: [tracking] }); await invoke(c, { current: '0.1.1' });
  assert.equal(c.calls[0][1].state, 'closed'); assert.match(c.calls[0][1].body, /main now contains VERSION 0.1.1/);
});

const { execFileSync } = require('node:child_process');
const { mkdtempSync, writeFileSync, rmSync } = require('node:fs');
const { tmpdir } = require('node:os');
const { join } = require('node:path');
const { prepareBranch } = require('../.github/scripts/version-proposal.cjs');
function repository() {
  const root = mkdtempSync(join(tmpdir(), 'version-proposal-'));
  const remote = join(root, 'remote.git'), work = join(root, 'work');
  const exec = (cwd, ...args) => execFileSync('git', ['-c', 'commit.gpgsign=false', '-c', 'maintenance.auto=false', '-c', 'gc.auto=0', ...args], { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  exec(root, 'init', '--bare', remote); exec(root, 'clone', remote, work);
  const git = (...args) => exec(work, ...args);
  git('switch', '--orphan', 'main'); git('config', 'user.name', 'github-actions[bot]');
  git('config', 'user.email', 'github-actions[bot]@users.noreply.github.com');
  writeFileSync(join(work, 'VERSION'), '0.1.0\n'); git('add', '.'); git('commit', '-s', '-m', 'initial'); git('push', 'origin', 'main');
  return { root, work, git, dispose: () => rmSync(root, { recursive: true, force: true, maxRetries: 3, retryDelay: 100 }) };
}
const branch = 'chore/version-bump-v0.1.1';
function prepare(repo, runGit = repo.git) {
  return prepareBranch({ branch, current: '0.1.0', next: '0.1.1', title: 'chore: bump VERSION to v0.1.1', runGit,
    writeVersion: (value) => writeFileSync(join(repo.work, 'VERSION'), `${value}\n`) });
}
function checkoutMain(repo) { repo.git('switch', 'main'); repo.git('branch', '-D', branch); }
test('real git creates one branch, refreshes it by fast-forward, and repeats safely', () => {
  const repo = repository();
  try {
    assert.equal(prepare(repo).ready, true);
    const first = repo.git('rev-parse', 'HEAD');
    assert.match(repo.git('log', '-1', '--format=%B'), /Signed-off-by:/);
    checkoutMain(repo);
    writeFileSync(join(repo.work, 'README.md'), 'new main content\n'); repo.git('add', '.'); repo.git('commit', '-s', '-m', 'main moved'); repo.git('push', 'origin', 'main');
    assert.equal(prepare(repo).ready, true);
    const refreshed = repo.git('rev-parse', 'HEAD'); assert.notEqual(refreshed, first);
    assert.equal(repo.git('merge-base', first, refreshed), first);
    assert.equal(repo.git('diff', '--name-only', 'main...HEAD'), 'VERSION');
    assert.match(repo.git('log', '-1', '--format=%B'), /Signed-off-by:/);
    checkoutMain(repo); assert.equal(prepare(repo).ready, true); assert.equal(repo.git('rev-parse', 'HEAD'), refreshed);
  } finally { repo.dispose(); }
});
test('real git refuses unrelated branch content', () => {
  const repo = repository();
  try {
    prepare(repo); writeFileSync(join(repo.work, 'human.txt'), 'preserve\n'); repo.git('add', '.'); repo.git('commit', '-s', '-m', 'other work'); repo.git('push', 'origin', branch);
    const before = repo.git('rev-parse', 'HEAD'); checkoutMain(repo);
    assert.equal(prepare(repo).ready, false);
    assert.equal(repo.git('ls-remote', 'origin', `refs/heads/${branch}`).split(/\s+/)[0], before);
  } finally { repo.dispose(); }
});
test('stale main and concurrent proposal writers fail without overwriting remote', () => {
  for (const changed of ['main', branch]) {
    const repo = repository();
    try {
      assert.throws(() => prepare(repo, (...args) => {
        if (args[0] === 'ls-remote' && args.at(-1) === `refs/heads/${changed}`)
          return `${'f'.repeat(40)}\trefs/heads/${changed}`;
        return repo.git(...args);
      }));
      assert.equal(repo.git('ls-remote', 'origin', `refs/heads/${branch}`), '');
    } finally { repo.dispose(); }
  }
});
