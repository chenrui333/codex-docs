const assert = require('node:assert/strict');
const test = require('node:test');
const handler = require('../.github/scripts/sync-failure-issue.cjs');
const context = { repo: { owner: 'example', repo: 'mirror' }, runId: 123, serverUrl: 'https://github.example' };
function client(initial = []) {
  const issues = [...initial], calls = [];
  return { issues, calls, github: {
    paginate: async () => issues.filter((issue) => issue.state !== 'closed'),
    rest: { issues: {
      listForRepo() {},
      create: async (args) => { calls.push(['create', args]); issues.push({ ...args, number: issues.length + 1 }); },
      createComment: async (args) => calls.push(['comment', args]),
      update: async (args) => { calls.push(['update', args]); Object.assign(issues.find((issue) => issue.number === args.issue_number), args); },
    } },
  } };
}
function reader(error = 'Read timed out (read timeout=30.0)', url = 'https://learn.example/child.xml') {
  return (path) => path === 'sync.log'
    ? `INFO start\nERROR Source transaction failed: ${JSON.stringify({ source: 'learn', stage: 'sitemap_fetch', state: 'sitemap_unavailable', url, error })}\n`
    : '{"failure_count":0}';
}
async function fail(c, options = {}) {
  await handler.recordFailure({ github: c.github, context, now: new Date('2026-09-18T12:00:00Z'), reader: reader(), ...options });
}
test('first failure creates bounded current diagnostics with first/latest seen and run link', async () => {
  const c = client(); await fail(c);
  assert.deepEqual(c.calls.map(([type]) => type), ['create']);
  const body = c.issues[0].body;
  assert.match(body, /First seen: 2026-09-18T12:00:00.000Z/);
  assert.match(body, /Latest seen:/); assert.match(body, /actions\/runs\/123/);
  assert.match(body, /timeout/); assert.match(body, /last successful transaction/);
  assert.ok(body.length < 3000);
});
test('same semantic failure updates body without comment and retains first seen', async () => {
  const c = client(); await fail(c);
  await fail(c, { reader: reader('Read timed out (read timeout=90.0)'), now: new Date('2026-09-19T00:00:00Z') });
  assert.deepEqual(c.calls.map(([type]) => type), ['create', 'update']);
  assert.match(c.issues[0].body, /First seen: 2026-09-18/);
  assert.match(c.issues[0].body, /Latest seen: 2026-09-19/);
});
test('materially changed failure adds one small transition comment', async () => {
  const c = client(); await fail(c); await fail(c, { reader: reader('Malformed XML') });
  assert.deepEqual(c.calls.map(([type]) => type), ['create', 'comment', 'update']);
  assert.ok(c.calls[1][1].body.length < 500);
  await fail(c, { reader: reader('Malformed XML') });
  assert.equal(c.calls.filter(([type]) => type === 'comment').length, 1);
});
test('legacy issue is adopted in place without another diagnostic comment', async () => {
  const c = client([{ number: 49, title: 'Codex docs sync failed - 2026-07-09', created_at: '2026-07-09T00:00:00Z', body: 'legacy' }]);
  await fail(c); assert.equal(c.calls.length, 1); assert.equal(c.calls[0][0], 'update');
  assert.equal(c.issues[0].title, handler.FAILURE_ISSUE_TITLE);
  assert.match(c.issues[0].body, /First seen: 2026-07-09/);
});
test('recovery comments once and closes; reoccurrence starts a new incident', async () => {
  const c = client(); await fail(c);
  await handler.closeRecoveredFailure({ github: c.github, context });
  await handler.closeRecoveredFailure({ github: c.github, context });
  assert.equal(c.calls.filter(([type]) => type === 'comment').length, 1);
  assert.equal(c.issues[0].state, 'closed');
  await fail(c); assert.equal(c.issues.length, 2);
});
test('missing diagnostic files produce a stable unknown failure', async () => {
  const c = client(); const missing = () => { throw new Error('ENOENT'); };
  await fail(c, { reader: missing }); await fail(c, { reader: missing });
  assert.deepEqual(c.calls.map(([type]) => type), ['create', 'update']);
  assert.match(c.issues[0].body, /diagnostics unavailable/);
});
test('very large logs, errors, and duplicate records stay bounded', async () => {
  const c = client(); const log = 'noise\n'.repeat(400000) + reader('x'.repeat(100000))('sync.log');
  await fail(c, { reader: (path) => path === 'sync.log' ? log : '{}' });
  assert.ok(c.issues[0].body.length < 8000);
});
test('fingerprint ignores ordering, duplicates, URL queries, and retry details', () => {
  const a = reader()('sync.log'), b = reader('HTTP 503', 'https://example.test/other')('sync.log');
  const first = handler.diagnosticState({ syncLog: a + b });
  const second = handler.diagnosticState({ syncLog: b + a + a });
  assert.equal(first.fingerprint, second.fingerprint);
  assert.equal(handler.diagnosticState({ syncLog: reader(undefined, 'https://learn.example/child.xml?token=redacted')('sync.log') }).fingerprint,
    handler.diagnosticState({ syncLog: a }).fingerprint);
});
test('current failure log takes precedence over stale canonical reports', () => {
  const state = handler.diagnosticState({ syncLog: reader()('sync.log'), syncSummary: '{"failures":[{"source":"old"}]}' });
  assert.equal(state.failures[0].source, 'learn');
});
test('freshness failures and unstructured workflow errors have useful fallback identity', () => {
  assert.equal(handler.diagnosticState({ freshnessStatus: '{"checks":[{"name":"provenance","status":"fail"}]}' }).failures[0].source, 'freshness');
  assert.equal(handler.diagnosticState({ syncLog: 'ERROR connection refused' }).failures[0].error_class, 'connection');
});
