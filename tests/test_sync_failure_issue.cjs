const assert = require('node:assert/strict');
const test = require('node:test');

const issueHandler = require('../.github/scripts/sync-failure-issue.cjs');

function fakeClient(openIssues) {
  const calls = [];
  return {
    calls,
    github: {
      paginate: async () => openIssues,
      rest: {
        issues: {
          listForRepo: () => {},
          create: async (args) => calls.push(['create', args]),
          createComment: async (args) => calls.push(['comment', args]),
          update: async (args) => calls.push(['update', args]),
        },
      },
    },
  };
}

const context = {
  repo: { owner: 'example', repo: 'mirror' },
  runId: 123,
  serverUrl: 'https://github.example',
};

test('failure body keeps only the log tail', () => {
  const syncLog = Array.from({ length: 130 }, (_, index) => `line-${index}`).join('\n');
  const body = issueHandler.buildFailureBody({
    date: '2026-07-30',
    workflowRunUrl: 'https://example.test/run',
    syncLog,
    syncSummary: '{}',
    sourceCoverage: '{}',
    freshnessStatus: '{"status":"stale"}',
  });

  assert.doesNotMatch(body, /line-0\n/);
  assert.match(body, /line-129/);
  assert.match(body, /Freshness status/);
  assert.match(body, /"status":"stale"/);
});

test('failure adopts a legacy daily issue as the rolling incident', async () => {
  const client = fakeClient([
    { number: 49, title: 'Codex docs sync failed - 2026-07-09' },
  ]);

  await issueHandler.recordFailure({
    github: client.github,
    context,
    now: new Date('2026-07-30T12:00:00Z'),
    reader: () => '{}',
  });

  assert.equal(client.calls[0][0], 'update');
  assert.equal(client.calls[0][1].title, issueHandler.FAILURE_ISSUE_TITLE);
  assert.equal(client.calls[1][0], 'comment');
  assert.equal(client.calls[1][1].issue_number, 49);
});

test('failure creates the rolling incident when none is open', async () => {
  const client = fakeClient([]);

  await issueHandler.recordFailure({
    github: client.github,
    context,
    now: new Date('2026-07-30T12:00:00Z'),
    reader: () => '{}',
  });

  assert.equal(client.calls.length, 1);
  assert.equal(client.calls[0][0], 'create');
  assert.equal(client.calls[0][1].title, issueHandler.FAILURE_ISSUE_TITLE);
});

test('healthy sync comments on and closes the rolling incident', async () => {
  const client = fakeClient([
    { number: 49, title: issueHandler.FAILURE_ISSUE_TITLE },
  ]);

  await issueHandler.closeRecoveredFailure({
    github: client.github,
    context,
    now: new Date('2026-07-30T12:00:00Z'),
  });

  assert.equal(client.calls[0][0], 'comment');
  assert.match(client.calls[0][1].body, /recovered/);
  assert.deepEqual(
    {
      issue_number: client.calls[1][1].issue_number,
      state: client.calls[1][1].state,
      state_reason: client.calls[1][1].state_reason,
    },
    { issue_number: 49, state: 'closed', state_reason: 'completed' },
  );
});
