---
source_type: 'learn'
source_area: 'learn_app_server'
source_url: 'https://learn.chatgpt.com/docs/app-server'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Codex App Server

Source: https://learn.chatgpt.com/docs/app-server

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex app-server is the interface Codex uses to power rich clients (for example, the Codex VS Code extension). Use it when you want a deep integration inside your own product: authentication, conversation history, approvals, and streamed agent events. The app-server implementation is open source in the Codex GitHub repository ([openai/codex/codex-rs/app-server](https://github.com/openai/codex/tree/main/codex-rs/app-server)). See the [Open Source](https://learn.chatgpt.com/docs/open-source) page for the full list of open-source Codex components.

If you are automating jobs or running Codex in CI, use the
  [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk) instead.

## Connect the CLI terminal UI

Remote terminal UI mode lets you run app-server on one machine and connect the
Codex CLI terminal interface from another. Start a WebSocket listener:

```bash
codex app-server --listen ws://127.0.0.1:4500
```

Then connect the terminal UI:

```bash
codex --remote ws://127.0.0.1:4500
```

For a non-local connection, configure WebSocket authentication and put the
connection behind TLS. Store the bearer token in an environment variable and
pass its name instead of putting the token on the command line:

```bash
export CODEX_REMOTE_TOKEN="$(cat "$HOME/.codex/app-server-token")"
codex --remote wss://remote-host:4500 \
  --remote-auth-token-env CODEX_REMOTE_TOKEN
```

The `--remote` option accepts `ws://`, `wss://`, `unix://`, and
`unix://PATH` endpoints. Use plain WebSockets only for localhost or an SSH
port-forwarded connection.

## Connect a remote Code Mode host

By default, app-server starts a local Code Mode host. To share a remote host
across threads in the same app-server process, pass the remote host's HTTP/2
gRPC endpoint to `--code-mode-host`.

```bash
codex app-server --code-mode-host https://code-mode.example.com
```

Use HTTPS for a remote host to protect tool arguments and results. Use HTTP
only on loopback or through a secure tunnel. The URL accepts a hostname and
optional port. Omit credentials, paths, query strings, and fragments. Use
`--listen` to configure the separate connection from clients to app-server.

## Protocol

Like [MCP](https://modelcontextprotocol.io/), `codex app-server` supports bidirectional communication using JSON-RPC 2.0 messages (with the `"jsonrpc":"2.0"` header omitted on the wire).

Supported transports:

- `stdio` (`--listen stdio://`, default): newline-delimited JSON (JSONL).
- `websocket` (`--listen ws://IP:PORT`, experimental and unsupported): one
  JSON-RPC message per WebSocket text frame.
- Unix socket (`--listen unix://` or `--listen unix://PATH`): WebSocket
  connections over Codex's default app-server control socket or a custom Unix
  socket path, using the standard HTTP Upgrade handshake.
- `off` (`--listen off`): don't expose a local transport.

When you run with `--listen ws://IP:PORT`, the same listener also serves basic
HTTP health probes:

- `GET /readyz` returns `200 OK` once the listener accepts new connections.
- `GET /healthz` returns `200 OK` when the request doesn't include an `Origin`
  header.
- Requests with an `Origin` header are rejected with `403 Forbidden`.

WebSocket transport is experimental and unsupported. Local listeners such as
`ws://127.0.0.1:PORT` are appropriate for localhost and SSH port-forwarding
workflows. Non-loopback WebSocket listeners currently allow unauthenticated
connections by default during rollout, so configure WebSocket auth before
exposing one remotely.

Supported WebSocket auth flags:

- `--ws-auth capability-token --ws-token-file /absolute/path`
- `--ws-auth capability-token --ws-token-sha256 HEX`
- `--ws-auth signed-bearer-token --ws-shared-secret-file /absolute/path`

For signed bearer tokens, you can also set `--ws-issuer`, `--ws-audience`, and
`--ws-max-clock-skew-seconds`. Clients present the credential as
`Authorization: Bearer <token>` during the WebSocket handshake, and app-server
enforces auth before JSON-RPC `initialize`.

Prefer `--ws-token-file` over passing raw bearer tokens on the command line. Use
`--ws-token-sha256` only when the client keeps the raw high-entropy token in a
separate local secret store; the hash is only a verifier, and clients still need
the original token.

In WebSocket mode, app-server uses bounded queues. When request ingress is full,
the server rejects new requests with JSON-RPC error code `-32001` and message
`"Server overloaded; retry later."` Clients should retry with an exponentially
increasing delay and jitter.

## Message schema

Requests include `method`, `params`, and `id`.

The request examples use [GPT-6.1 Sol](https://learn.chatgpt.com/docs/models#gpt-6.1-sol), which requires access
for the signed-in account or workspace. Use [`model/list`](#list-models-modellist)
to select an available model if needed.

```json
{ "method": "thread/start", "id": 10, "params": { "model": "gpt-6.1-sol" } }
```

Responses echo the `id` with either `result` or `error`:

```json
{ "id": 10, "result": { "thread": { "id": "thr_123" } } }
```

```json
{ "id": 10, "error": { "code": 123, "message": "Something went wrong" } }
```

Notifications omit `id` and use only `method` and `params`:

```json
{ "method": "turn/started", "params": { "turn": { "id": "turn_456" } } }
```

You can generate a TypeScript schema or a JSON Schema bundle from the CLI. Each output is specific to the Codex version you ran, so the generated artifacts match that version exactly:

```bash
codex app-server generate-ts --out ./schemas
codex app-server generate-json-schema --out ./schemas
```

## Getting started

1. Start the server with `codex app-server` (default stdio transport),
   `codex app-server --listen ws://127.0.0.1:4500` (TCP WebSocket), or
   `codex app-server --listen unix://` (default Unix socket).
2. Connect a client over the selected transport, then send `initialize` followed by the `initialized` notification.
3. Start a thread and a turn, then keep reading notifications from the active transport stream.

The following examples use the `stdio` transport:

Start an app-server conversation

```typescript
const proc = spawn("codex", ["app-server"], {
  stdio: ["pipe", "pipe", "inherit"],
});
const rl = readline.createInterface({ input: proc.stdout });
const send = (message: unknown) => {
  proc.stdin.write(`${JSON.stringify(message)}\n`);
};
let threadId: string | null = null;
rl.on("line", (line) => {
  const msg = JSON.parse(line) as any;
  console.log("server:", msg);
  if (msg.id === 0 && msg.result) {
    send({ method: "initialized", params: {} });
    send({
      method: "thread/start",
      id: 1,
      params: { model: "gpt-6.1-sol" },
    });
  }
  if (msg.method === "turn/completed") {
    if (msg.params?.turn?.status !== "completed") {
      console.error(msg.params?.turn?.error ?? "The turn did not complete.");
      process.exitCode = 1;
    }
    proc.stdin.end();
    rl.close();
  }
  if (msg.error) {
    console.error(msg.error);
    process.exitCode = 1;
    proc.stdin.end();
    rl.close();
  }
  if (msg.id === 1 && msg.result?.thread?.id && !threadId) {
    threadId = msg.result.thread.id;
    send({
      method: "turn/start",
      id: 2,
      params: {
        threadId,
        input: [{ type: "text", text: "Summarize this repo." }],
      },
    });
  }
});
send({
  method: "initialize",
  id: 0,
  params: {
    clientInfo: {
      name: "my_product",
      title: "My Product",
      version: "0.1.0",
    },
  },
});
proc.on("error", (error) => {
  console.error(error);
  process.exitCode = 1;
  rl.close();
});
proc.on("exit", (code) => {
  if (code !== 0) process.exitCode = code ?? 1;
});
```

```go
package main

otherwise, the server returns an unsupported-method error.

Pass an opaque `nextCursor` from a previous response to continue paging. To
start after a known item, pass an item anchor and a non-empty `turnId`:

```json
{ "method": "thread/items/list", "id": 21, "params": {
  "threadId": "thr_123",
  "turnId": "turn_456",
  "cursor": { "type": "item", "itemId": "item_123" },
  "sortDirection": "asc",
  "limit": 50
} }
{ "id": 21, "result": {
  "data": [],
  "nextCursor": null,
  "backwardsCursor": null
} }
```

Item anchors exclude the anchor itself: ascending order returns newer items,
and descending order returns older items. The item must belong to the
requested turn's visible history. Missing `turnId`, an empty item ID, or an
unknown or out-of-scope item returns invalid params (`-32602`). Continue with
the returned string `nextCursor`. Each result entry contains `turnId`, `item`,
and optional recorded start and completion timestamps.

### List threads (with pagination & filters)

`thread/list` lets you render a history UI. Results default to newest-first by `createdAt`. Filters apply before pagination. Pass any combination of:

- `cursor` - opaque string from a prior response; omit for the first page.
- `limit` - server defaults to a reasonable page size if unset.
- `sortKey` - `created_at` (default), `updated_at`, `recency_at`, or `section_position`. To use `section_position`, supply a non-null `sectionId`.
- `sortDirection` - `asc` or `desc`. If you omit `sortDirection`, `section_position` sorts in ascending order and time-based keys sort in descending order.
- `sectionId` - pass a section ID to list its threads or `null` for unassigned threads. Omit the field to include threads from all sections and unassigned threads.
- `excludedThreadIds` - omit up to 100 thread IDs. Duplicate IDs count toward the 100-ID cap. The server excludes matching threads before applying the page limit. Send the same exclusions with each cursor.
- `modelProviders` - restrict results to specific providers. Pass `[]` to include all providers. If you omit this field or pass `null`, the server uses the configured provider unless you filter by a thread relationship, in which case it includes all providers.
- `sourceKinds` - restrict results to specific thread sources. When omitted or `[]`, the server defaults to interactive sources only: `cli` and `vscode`.
- `archived` - when `true`, list archived threads only. When `false` or omitted, list non-archived threads (default).
- `cwd` - restrict results to threads whose session current working directory exactly matches this path, or one of the paths in an array. Relative paths resolve from the app-server process working directory.
- `useStateDbOnly` - when `true`, return state database results without scanning JSONL thread logs to repair metadata. Omit it or pass `false` for the default scan-and-repair behavior.
- `searchTerm` - restrict results to threads whose extracted title contains this case-sensitive text fragment.
- `parentThreadId` - restrict results to direct child threads of the given parent thread. This filter is experimental and requires `capabilities.experimentalApi = true`.
- `ancestorThreadId` - restrict results to spawned descendants of the given thread at any depth. This filter is experimental and requires `capabilities.experimentalApi = true`; don't combine it with `parentThreadId`.

`sourceKinds` accepts the following values:

- `cli`
- `vscode`
- `exec`
- `appServer`
- `subAgent`
- `subAgentReview`
- `subAgentCompact`
- `subAgentThreadSpawn`
- `subAgentOther`
- `unknown`

Example:

```json
{ "method": "thread/list", "id": 20, "params": {
  "cursor": null,
  "limit": 25,
  "sortKey": "created_at"
} }
{ "id": 20, "result": {
  "data": [
    { "id": "thr_a", "preview": "Create a TUI", "ephemeral": false, "section": { "id": "01984de2-8f74-7c91-a3b2-5c5e937cf318", "name": "Pinned", "appearance": null }, "modelProvider": "openai", "createdAt": 1730831111, "updatedAt": 1730831111, "name": "TUI prototype", "status": { "type": "notLoaded" } },
    { "id": "thr_b", "preview": "Fix tests", "ephemeral": false, "section": null, "modelProvider": "openai", "createdAt": 1730750000, "updatedAt": 1730750000, "status": { "type": "notLoaded" } }
  ],
  "nextCursor": "opaque-token-or-null"
} }
```

When `nextCursor` is `null`, you have reached the final page.

### Organize threads into sections

Create a named section with `threadSection/create` and use the returned
`section.id` in `thread/section/move`. Pass `beforeThreadId` to insert the
thread before another thread in the section, or omit it to append. Pass
`sectionId: null` to remove a thread from its section. Use `threadSection/list`,
`threadSection/update`, and `threadSection/delete` to page through, rename,
and remove custom sections. To pin a thread, move it to the built-in Pinned
section returned by `threadSection/list`.

### Manage thread attachments

Use attachments to associate resources such as pull requests with a stored
thread. You can manage these references without resuming the thread.

- `thread/attachment/add` takes `threadId`, `attachmentType`, `identityKey`, and a JSON `payload`. Adding the same type and key to the same thread again returns the existing attachment.
- `thread/attachment/list` pages through a thread's attachments. To find threads that reference a resource, call `thread/attachmentOwner/list` with its `attachmentType` and `identityKey`.
- `thread/attachment/remove` takes `threadId`, `attachmentType`, and `identityKey`. The underlying resource stays available.
- `thread/attachment/updated` reports a `created` or `deleted` operation when the association changes.

### Update stored thread metadata

Use `thread/metadata/update` to patch stored thread metadata without resuming the
thread. Pass the Git fields you want to update in `gitInfo`. Omit a field
to keep its value or pass `null` to clear it.

```json
{ "method": "thread/metadata/update", "id": 21, "params": {
  "threadId": "thr_123",
  "gitInfo": { "branch": "feature/sidebar-pr" }
} }
{ "id": 21, "result": {
  "thread": {
    "id": "thr_123",
    "gitInfo": { "sha": null, "branch": "feature/sidebar-pr", "originUrl": null }
  }
} }
```

### Track thread status changes

`thread/status/changed` is emitted whenever a loaded thread's runtime status changes. The payload includes `threadId` and the new `status`.

```json
{
  "method": "thread/status/changed",
  "params": {
    "threadId": "thr_123",
    "status": { "type": "active", "activeFlags": ["waitingOnApproval"] }
  }
}
```

### List loaded threads

`thread/loaded/list` returns thread IDs currently loaded in memory.

```json
{ "method": "thread/loaded/list", "id": 21 }
{ "id": 21, "result": { "data": ["thr_123", "thr_456"] } }
```

### Unsubscribe from a loaded thread

`thread/unsubscribe` removes the current connection's subscription to a thread. The response status is one of:

- `unsubscribed` when the connection was subscribed and is now removed.
- `notSubscribed` when the connection wasn't subscribed to that thread.
- `notLoaded` when the thread isn't loaded.

After the last subscriber leaves, app-server unloads the thread once it has
been idle for 60 seconds by default. Set
[`thread_unload_delay_secs`](https://learn.chatgpt.com/docs/config-file/config-reference) to change the
interval. When it unloads the thread, app-server emits `thread/status/changed`
with status `notLoaded` and a `thread/closed` notification.

```json
{ "method": "thread/unsubscribe", "id": 22, "params": { "threadId": "thr_123" } }
{ "id": 22, "result": { "status": "unsubscribed" } }
```

If the thread later expires:

```json
{ "method": "thread/status/changed", "params": {
    "threadId": "thr_123",
    "status": { "type": "notLoaded" }
} }
{ "method": "thread/closed", "params": { "threadId": "thr_123" } }
```

### Archive a thread

Use `thread/archive` to move the persisted thread log (stored as a JSONL file on disk) into the archived sessions directory. Archiving a thread also attempts to archive spawned descendant threads that aren't already archived.

```json
{ "method": "thread/archive", "id": 22, "params": { "threadId": "thr_b" } }
{ "id": 22, "result": {} }
{ "method": "thread/archived", "params": { "threadId": "thr_b" } }
{ "method": "thread/archived", "params": { "threadId": "thr_child" } }
```

Archived threads won't appear in future calls to `thread/list` unless you pass `archived: true`. The server emits one `thread/archived` notification for each thread it actually archives; if a spawned descendant can't be archived, the request can still succeed without an archived notification for that descendant.

### Delete a thread

Use `thread/delete` to permanently delete a persisted active or archived thread
and its spawned descendant threads. The server removes existing rollout files and
associated metadata before returning success; missing rollout files are treated
as already deleted. Ephemeral root threads can't be deleted.

```json
{ "method": "thread/delete", "id": 23, "params": { "threadId": "thr_b" } }
{ "id": 23, "result": {} }
{ "method": "thread/deleted", "params": { "threadId": "thr_b" } }
{ "method": "thread/deleted", "params": { "threadId": "thr_child" } }
```

### Unarchive a thread

Use `thread/unarchive` to move an archived thread rollout back into the active sessions directory.

```json
{ "method": "thread/unarchive", "id": 24, "params": { "threadId": "thr_b" } }
{ "id": 24, "result": { "thread": { "id": "thr_b", "name": "Bug bash notes" } } }
{ "method": "thread/unarchived", "params": { "threadId": "thr_b" } }
```

### Trigger thread compaction

Use `thread/compact/start` to trigger manual history compaction for a thread. The request returns immediately with `{}`.

App-server emits progress as standard `turn/*` and `item/*` notifications on the same `threadId`, including a `contextCompaction` item lifecycle (`item/started` then `item/completed`).

```json
{ "method": "thread/compact/start", "id": 25, "params": { "threadId": "thr_b" } }
{ "id": 25, "result": {} }
```

### Run a thread shell command

Use `thread/shellCommand` for user-initiated shell commands that belong to a thread. The request returns immediately with `{}` while progress streams through standard `turn/*` and `item/*` notifications.

This API runs outside the sandbox with full access and doesn't inherit the thread sandbox policy. Clients should expose it only for explicit user-initiated commands.

If the thread already has an active turn, the command runs as an auxiliary action on that turn and its formatted output is injected into the turn's message stream. If the thread is idle, app-server starts a standalone turn for the shell command.

Set `timeoutMs` to limit execution time in milliseconds. Omitting it or passing
`null` uses the one-hour default. `0` requests an immediate timeout; negative
values are rejected. The timeout doesn't delay the immediate RPC acknowledgement.

```json
{ "method": "thread/shellCommand", "id": 26, "params": { "threadId": "thr_b", "command": "git status --short", "timeoutMs": 10000 } }
{ "id": 26, "result": {} }
```

### Clean background terminals

Use `thread/backgroundTerminals/clean` to stop all running background terminals associated with a thread. This method is experimental and requires `capabilities.experimentalApi = true`.

```json
{ "method": "thread/backgroundTerminals/clean", "id": 27, "params": { "threadId": "thr_b" } }
{ "id": 27, "result": {} }
```

Use `thread/backgroundTerminals/list` to inspect running background terminals
for a loaded thread. The request supports standard `cursor` and `limit`
pagination, and the returned `processId` is the app-server process id. This
method is experimental and requires `capabilities.experimentalApi = true`:

```json
{ "method": "thread/backgroundTerminals/list", "id": 28, "params": { "threadId": "thr_b" } }
{ "id": 28, "result": { "data": [
  {
    "itemId": "item_456",
    "processId": "42",
    "command": "python3 -m http.server",
    "cwd": "/workspace",
    "osPid": null,
    "cpuPercent": null,
    "rssKb": null
  }
], "nextCursor": null } }
```

Use `thread/backgroundTerminals/terminate` with that `processId` to stop one
background terminal. This method is experimental and requires
`capabilities.experimentalApi = true`:

```json
{ "method": "thread/backgroundTerminals/terminate", "id": 29, "params": { "threadId": "thr_b", "processId": "42" } }
{ "id": 29, "result": { "terminated": true } }
```

### Revert thread history

Use `thread/revert` to remove `beforeTurnId` and every later turn from a
persistent paginated thread's conversation history. It doesn't revert local
file changes. Resume the thread first if it isn't loaded. Ephemeral threads
and threads with legacy history aren't supported.

```json
{ "method": "thread/revert", "id": 30, "params": { "threadId": "thr_b", "beforeTurnId": "turn_456" } }
{ "id": 30, "result": {
  "thread": { "id": "thr_b", "ephemeral": false, "turns": [] },
  "turnsBackwardsCursor": "retained-turn-cursor-or-null",
  "itemsBackwardsCursor": "retained-item-cursor-or-null"
} }
{ "method": "thread/reverted", "params": { "threadId": "thr_b" } }
```

The returned `thread.turns` is always empty. Use the returned cursors with
`thread/turns/list` or `thread/items/list` and `sortDirection: "desc"` to load
retained history, including the cursor's anchor.

`thread/rollback` has been removed and returns an unknown-method error.
Existing rollback markers in older saved threads remain readable.

## Turns

The `input` field accepts a list of items:

- `{ "type": "text", "text": "Explain this diff" }`
- `{ "type": "image", "url": "https://.../design.png" }`
- `{ "type": "localImage", "path": "/tmp/screenshot.png" }`

You can override configuration settings per turn (model, effort, `cwd`, sandbox policy, summary). When specified, these settings become the defaults for later turns on the same thread. `outputSchema` applies only to the current turn. For `sandboxPolicy.type = "externalSandbox"`, set `networkAccess` to `restricted` or `enabled`; for `workspaceWrite`, `networkAccess` remains a boolean.

For `turn/start.collaborationMode`, `settings.developer_instructions: null` means "use built-in instructions for the selected mode" rather than clearing mode instructions.

### Sandbox read access (`ReadOnlyAccess`)

`sandboxPolicy` supports explicit read-access controls:

- `readOnly`: optional `access` (`{ "type": "fullAccess" }` by default, or restricted roots).
- `workspaceWrite`: optional `readOnlyAccess` (`{ "type": "fullAccess" }` by default, or restricted roots).

Restricted read access shape:

```json
{
  "type": "restricted",
  "includePlatformDefaults": true,
  "readableRoots": ["/Users/me/shared-read-only"]
}
```

On macOS, `includePlatformDefaults: true` appends a curated platform-default Seatbelt policy for restricted-read sessions. This improves tool compatibility without broadly allowing all of `/System`.

Examples:

```json
{ "type": "readOnly", "access": { "type": "fullAccess" } }
```

```json
{
  "type": "workspaceWrite",
  "writableRoots": ["/Users/me/project"],
  "readOnlyAccess": {
    "type": "restricted",
    "includePlatformDefaults": true,
    "readableRoots": ["/Users/me/shared-read-only"]
  },
  "networkAccess": false
}
```

### Start a turn

```json
{ "method": "turn/start", "id": 30, "params": {
  "threadId": "thr_123",
  "input": [ { "type": "text", "text": "Run tests" } ],
  "cwd": "/Users/me/project",
  "approvalPolicy": "on-request",
  "sandboxPolicy": {
    "type": "workspaceWrite",
    "writableRoots": ["/Users/me/project"],
    "networkAccess": true
  },
  "model": "gpt-6.1-sol",
  "effort": "medium",
  "summary": "concise",
  "outputSchema": {
    "type": "object",
    "properties": { "answer": { "type": "string" } },
    "required": ["answer"],
    "additionalProperties": false
  }
} }
{ "id": 30, "result": { "turn": { "id": "turn_456", "status": "inProgress", "items": [], "error": null } } }
```

Set `serviceTierForTurn` to override the service tier for one new turn. Use
`"default"` for standard speed, or omit the field to inherit the thread's tier.
To change the tier for this turn and later turns, set `serviceTier`.

To start a turn with output from a tool your client ran, pass `toolOutput`
with a nonempty `name`, an optional `namespace`, and an `output` string or
array of content items. Set `input` to an empty array; you can't combine
`toolOutput` with nonempty user input.

```json
{
  "method": "turn/start",
  "id": 31,
  "params": {
    "threadId": "thr_123",
    "input": [],
    "toolOutput": {
      "name": "run_tests",
      "namespace": null,
      "output": "All 42 tests passed."
    }
  }
}
```

The output remains tool output in the conversation and appears as a
`functionCallOutput` item in notifications and persisted history. If a regular
turn is already active, Codex queues the output for that turn.

### Inject items into a thread

Use `thread/inject_items` to append prebuilt Responses API items to a loaded thread's prompt history without starting a user turn. These items are persisted to the rollout and included in subsequent model requests.

```json
{ "method": "thread/inject_items", "id": 31, "params": {
  "threadId": "thr_123",
  "items": [
    {
      "type": "message",
      "role": "assistant",
      "content": [{ "type": "output_text", "text": "Previously computed context." }]
    }
  ]
} }
{ "id": 31, "result": {} }
```

### Steer an active turn

Use `turn/steer` to append more user input to the active in-flight turn.

- Include `expectedTurnId`; it must match the active turn id.
- The request fails if there is no active turn on the thread.
- `turn/steer` doesn't emit a new `turn/started` notification.
- `turn/steer` doesn't accept turn-level overrides (`model`, `cwd`, `sandboxPolicy`, or `outputSchema`).

```json
{ "method": "turn/steer", "id": 32, "params": {
  "threadId": "thr_123",
  "input": [ { "type": "text", "text": "Actually focus on failing tests first." } ],
  "expectedTurnId": "turn_456"
} }
{ "id": 32, "result": { "turnId": "turn_456" } }
```

### Start a turn (invoke a skill)

Invoke a skill explicitly by including `$<skill-name>` in the text input and adding a `skill` input item alongside it.

```json
{ "method": "turn/start", "id": 33, "params": {
  "threadId": "thr_123",
  "input": [
    { "type": "text", "text": "$skill-creator Add a new skill for triaging flaky CI and include step-by-step usage." },
    { "type": "skill", "name": "skill-creator", "path": "/Users/me/.codex/skills/skill-creator/SKILL.md" }
  ]
} }
{ "id": 33, "result": { "turn": { "id": "turn_457", "status": "inProgress", "items": [], "error": null } } }
```

### Interrupt a turn

```json
{ "method": "turn/interrupt", "id": 31, "params": { "threadId": "thr_123", "turnId": "turn_456" } }
{ "id": 31, "result": {} }
```

On success, the turn finishes with `status: "interrupted"`.

## Review

`review/start` runs the Codex reviewer for a thread and streams review items. Targets include:

- `uncommittedChanges`
- `baseBranch` (diff against a branch)
- `commit` (review a specific commit)
- `custom` (free-form instructions)

`review/start` runs the review on the supplied thread. Omit `delivery` or pass
`"inline"`. To run a separate review, use `thread/fork` to include the existing
history or `thread/start` for a fresh thread. Then call `review/start` with the
new thread ID.

Example request/response:

```json
{ "method": "review/start", "id": 40, "params": {
  "threadId": "thr_123",
  "delivery": "inline",
  "target": { "type": "commit", "sha": "1234567deadbeef", "title": "Polish tui colors" }
} }
{ "id": 40, "result": {
  "turn": {
    "id": "turn_900",
    "status": "inProgress",
    "items": [
      { "type": "userMessage", "id": "turn_900", "content": [ { "type": "text", "text": "Review commit 1234567: Polish tui colors" } ] }
    ],
    "error": null
  },
  "reviewThreadId": "thr_123"
} }
```

Codex streams the usual `turn/started` notification followed by an `item/started` with an `enteredReviewMode` item:

```json
{
  "method": "item/started",
  "params": {
    "item": {
      "type": "enteredReviewMode",
      "id": "turn_900",
      "review": "current changes"
    }
  }
}
```

When the reviewer finishes, the server emits `item/started` and `item/completed` containing an `exitedReviewMode` item with the final review text:

```json
{
  "method": "item/completed",
  "params": {
    "item": {
      "type": "exitedReviewMode",
      "id": "turn_900",
      "review": "Looks solid overall..."
    }
  }
}
```

Use this notification to render the reviewer output in your client.

## Process execution

`process/*` is an experimental, explicit process-control API. It requires
`capabilities.experimentalApi = true` and runs outside Codex's sandbox. Use it
only when your client intentionally exposes local process control without a
sandbox.

Start a process with `process/spawn` and provide a `processHandle`, then use
that handle for stdin, resize, and kill requests. Output streams through
`process/outputDelta` notifications and completion streams through
`process/exited`.

```json
{ "method": "process/spawn", "id": 48, "params": {
  "command": ["python3", "-m", "pytest", "-q"],
  "processHandle": "pytest-1",
  "cwd": "/Users/me/project",
  "tty": true
} }
{ "id": 48, "result": {} }
{ "method": "process/outputDelta", "params": {
  "processHandle": "pytest-1",
  "stream": "stdout",
  "deltaBase64": "Li4u"
} }
{ "method": "process/exited", "params": {
  "processHandle": "pytest-1",
  "exitCode": 0
} }
```

Use `process/writeStdin` with `deltaBase64`, `closeStdin`, or both to send
input. Use `process/resizePty` for PTY resize events and `process/kill` to
terminate a running process.

## Command execution

`command/exec` runs a single command (`argv` array) under the server sandbox without creating a thread.

```json
{ "method": "command/exec", "id": 50, "params": {
  "command": ["ls", "-la"],
  "cwd": "/Users/me/project",
  "sandboxPolicy": { "type": "workspaceWrite" },
  "timeoutMs": 10000
} }
{ "id": 50, "result": { "exitCode": 0, "stdout": "...", "stderr": "" } }
```

Use `sandboxPolicy.type = "externalSandbox"` if you already sandbox the server process and want Codex to skip its own sandbox enforcement. For external sandbox mode, set `networkAccess` to `restricted` (default) or `enabled`. For `readOnly` and `workspaceWrite`, use the same optional `access` / `readOnlyAccess` structure shown above.

Notes:

- The server rejects empty `command` arrays.
- `sandboxPolicy` accepts the same shape used by `turn/start` (for example, `dangerFullAccess`, `readOnly`, `workspaceWrite`, `externalSandbox`).
- When omitted, `timeoutMs` falls back to the server default.
- Set `tty: true` for PTY-backed sessions, and use `processId` when you plan to follow up with `command/exec/write`, `command/exec/resize`, or `command/exec/terminate`.
- Set `streamStdoutStderr: true` to receive `command/exec/outputDelta` notifications while the command is running.

### Read admin requirements (`configRequirements/read`)

Use `configRequirements/read` to inspect the effective admin requirements loaded from `requirements.toml` and/or MDM.

```json
{ "method": "configRequirements/read", "id": 52, "params": {} }
{ "id": 52, "result": {
  "requirements": {
    "allowedApprovalPolicies": ["on-request", "never"],
    "allowedSandboxModes": ["read-only", "workspace-write"],
    "featureRequirements": {
      "unified_exec": false
    }
  }
} }
```

`result.requirements` is `null` when no requirements are configured.
When `result.supportsIndependentSpeedModes` is `true`, the `fast_mode` and
`ultrafast_mode` requirements apply independently. Older servers omit this
field and use `fast_mode` for both. For supported keys and values, see the
[`requirements.toml` reference](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml).

### Windows sandbox setup (`windowsSandbox/setupStart`)

Call `windowsSandbox/readiness` before prompting for setup. Both MXC and a
configured legacy sandbox can return `ready`. If the legacy sandbox returns
`updateRequired`, call `windowsSandbox/setupStart` to start setup
asynchronously. The readiness check returns `notConfigured` if the Windows
sandbox is disabled or the host runs another operating system.

```json
{ "method": "windowsSandbox/setupStart", "id": 53, "params": { "mode": "elevated" } }
{ "id": 53, "result": { "started": true } }
```

App-server starts setup in the background and later emits a completion notification:

```json
{
  "method": "windowsSandbox/setupCompleted",
  "params": { "mode": "elevated", "success": true, "error": null }
}
```

Modes:

- `elevated` - run the elevated Windows sandbox setup path.
- `unelevated` - run the legacy setup/preflight path.

## Filesystem

The v2 filesystem APIs operate on absolute paths. Use `fs/watch` when a client needs to invalidate UI state after a file or directory changes.

```json
{ "method": "fs/watch", "id": 54, "params": {
  "watchId": "0195ec6b-1d6f-7c2e-8c7a-56f2c4a8b9d1",
  "path": "/Users/me/project/.git/HEAD"
} }
{ "id": 54, "result": { "path": "/Users/me/project/.git/HEAD" } }
{ "method": "fs/changed", "params": {
  "watchId": "0195ec6b-1d6f-7c2e-8c7a-56f2c4a8b9d1",
  "changedPaths": ["/Users/me/project/.git/HEAD"]
} }
{ "method": "fs/unwatch", "id": 55, "params": {
  "watchId": "0195ec6b-1d6f-7c2e-8c7a-56f2c4a8b9d1"
} }
{ "id": 55, "result": {} }
```

Watching a file emits `fs/changed` for that file path, including updates delivered by replace or rename operations.

## Events

Event notifications are the server-initiated stream for thread lifecycles, turn lifecycles, and the items within them. After you start or resume a thread, keep reading the active transport stream for `thread/started`, `thread/archived`, `thread/unarchived`, `thread/closed`, `thread/status/changed`, `turn/*`, `item/*`, and `serverRequest/resolved` notifications.

### Notification opt-out

Clients can suppress specific notifications per connection by sending exact method names in `initialize.params.capabilities.optOutNotificationMethods`.

- Exact-match only: `item/agentMessage/delta` suppresses only that method.
- Unknown method names are ignored.
- Applies to the current `thread/*`, `turn/*`, `item/*`, and related v2 notifications.
- Doesn't apply to requests, responses, or errors.

### Fuzzy file search events (experimental)

The fuzzy file search session API emits per-query notifications:

- `fuzzyFileSearch/sessionUpdated` - `{ sessionId, query, files }` with the current matches for the active query.
- `fuzzyFileSearch/sessionCompleted` - `{ sessionId }` once indexing and matching for that query completes.

### Warning events

- `configWarning` - `{ summary, details?, path?, range? }` for recoverable
  configuration or initialization problems.
- `warning` - `{ threadId?, message }` for non-fatal runtime warnings.

### Windows sandbox setup events

- `windowsSandbox/setupCompleted` - `{ mode, success, error }` emitted after a `windowsSandbox/setupStart` request finishes.

### Turn events

- `turn/started` - `{ turn }` with the turn id, empty `items`, and `status: "inProgress"`.
- `turn/completed` - `{ turn }` where `turn.status` is `completed`, `interrupted`, or `failed`; failures carry `{ error: { message, codexErrorInfo?, additionalDetails? } }`.
- `turn/diff/updated` - `{ threadId, turnId, diff }` with the latest aggregated unified diff across every file change in the turn.
- `turn/plan/updated` - `{ turnId, explanation?, plan }` whenever the agent shares or changes its plan; each `plan` entry is `{ step, status }` with `status` in `pending`, `inProgress`, or `completed`.
- `hook/started` and `hook/completed` - `{ threadId, turnId?, run }` when a synchronous lifecycle hook starts and when its final run summary is available. These notifications aren't emitted for asynchronous hooks.
- `model/safetyBuffering/updated` - `{ threadId, turnId, model, useCases, reasons, showBufferingUi, fasterModel }` when a response enters transient safety buffering.
- `model/rerouted` - `{ threadId, turnId, fromModel, toModel, reason }` when the service routes a request to another model.
- `model/verification` - `{ threadId, turnId, verifications }` when the service requires additional account verification.
- `thread/tokenUsage/updated` - usage updates for the active thread.

`turn/diff/updated` and `turn/plan/updated` currently include empty `items` arrays even when item events stream. Use `item/*` notifications as the source of truth for turn items.

### Items

`ThreadItem` is the tagged union carried in turn responses and `item/*` notifications. Common item types include:

- `userMessage` - `{id, content}` where `content` is a list of user inputs (`text`, `image`, or `localImage`).
- `functionCallOutput` - `{id, name, namespace, output}` for standalone tool output supplied through `turn/start.toolOutput`. `namespace` can be `null`.
- `agentMessage` - `{id, text, phase?}` containing the accumulated agent reply. When present, `phase` uses Responses API wire values (`commentary`, `partial_answer`, `final_answer`). A `partial_answer` is stable answer text that may be followed by more output or tools.
- `plan` - `{id, text}` containing proposed plan text in plan mode. Treat the final `plan` item from `item/completed` as authoritative.
- `reasoning` - `{id, summary, content}` where `summary` holds streamed reasoning summaries and `content` holds raw reasoning blocks.
- `commandExecution` - `{id, command, cwd, status, commandActions, aggregatedOutput?, exitCode?, durationMs?}`.
- `fileChange` - `{id, changes, status}` describing proposed edits; `changes` list `{path, kind, diff}`.
- `mcpToolCall` - Records the call's `id`, `server`, `tool`, `status`, and `arguments`.
  The call also includes `appContext`, `mcpAppUi`, `pluginId`, `readOnlyHint`, `result`, `error`, and `durationMs`. Each of these fields can be `null`. The legacy `mcpAppResourceUri` field is optional.
  For trusted MCP apps, `appContext` contains `connectorId`. Its other fields (`linkId`, `resourceUri`, `appName`, and `actionName`) can be `null`.
  When the tool descriptor specifies a resource URI and a display mode (`inline` or `fullscreen`), `mcpAppUi` contains `resourceUri` and `preferredModelDisplayMode`. For calls saved without this presentation metadata, app-server returns `null` for `mcpAppUi`.
- `dynamicToolCall` - `{id, tool, arguments, status, contentItems?, success?, durationMs?}` for client-executed dynamic tool invocations.
- `collabToolCall` - `{id, tool, status, senderThreadId, receiverThreadId?, newThreadId?, prompt?, agentStatus?}`.
- `webSearch` - `{id, query, action?}` for web search requests issued by the agent.
- `imageView` - `{id, path}` emitted when the agent invokes the image viewer tool.
- `enteredReviewMode` - `{id, review}` sent when the reviewer starts.
- `exitedReviewMode` - `{id, review}` emitted when the reviewer finishes.
- `contextCompaction` - `{id}` emitted when Codex compacts the conversation history.

For `webSearch.action`, the action `type` can be `search` (`query?`, `queries?`), `openPage` (`url?`), or `findInPage` (`url?`, `pattern?`).

The app server deprecates the legacy `thread/compacted` notification; use the `contextCompaction` item instead.

All items emit two shared lifecycle events:

- `item/started` - emits the full `item` when a new unit of work begins; the `item.id` matches the `itemId` used by deltas.
- `item/completed` - sends the final `item` once work finishes; treat this as the authoritative state.

### Item deltas

- `item/agentMessage/delta` - appends streamed text for the agent message.
- `item/plan/delta` - streams proposed plan text. The final `plan` item may not exactly equal the concatenated deltas.
- `item/reasoning/summaryTextDelta` - streams readable reasoning summaries; `summaryIndex` increments when a new summary section opens.
- `item/reasoning/summaryPartAdded` - marks a boundary between reasoning summary sections.
- `item/reasoning/textDelta` - streams raw reasoning text (when supported by the model).
- `item/commandExecution/outputDelta` - streams stdout/stderr for a command; append deltas in order.
- `item/fileChange/outputDelta` - deprecated compatibility notification for legacy `apply_patch` text output. Current app-server versions no longer emit it; use `fileChange` items and `turn/diff/updated` instead.

## Errors

When app-server rejects new work during graceful shutdown, it returns a JSON-RPC
error with code `-32600` and `data.reason` set to `serverShuttingDown`.

The `error` notification includes a nested `error` object with a `message`
and optional `additionalDetails`. Its `codexErrorInfo` field can be `null`.
If `willRetry` is `true`, the server retries and the turn stays active. A turn
that fails finishes with `status: "failed"`. Common `codexErrorInfo` values include
`contextWindowExceeded`, `usageLimitExceeded`, `badRequest`, `unauthorized`,
and `sandboxError`. For upstream request failures, the value can be an
object such as `{ "httpConnectionFailed": { "httpStatusCode": 503 } }`.

## Approvals

Depending on a user's Codex settings, command execution and file changes may require approval. The app-server sends a server-initiated JSON-RPC request to the client, and the client responds with a decision payload.

- Command execution decisions: `accept`, `acceptForSession`, `decline`, `cancel`, or `{ "acceptWithExecpolicyAmendment": { "execpolicy_amendment": ["cmd", "..."] } }`.
- File change decisions: `accept`, `acceptForSession`, `decline`, `cancel`.

- Requests include `threadId` and `turnId` - use them to scope UI state to the active conversation.
- The server resumes or declines the work and ends the item with `item/completed`.

### Command execution approvals

Order of messages:

1. `item/started` shows the pending `commandExecution` item with `command`, `cwd`, and other fields.
2. `item/commandExecution/requestApproval` includes `itemId`, `threadId`, `turnId`, optional `reason`, optional `command`, optional `cwd`, optional `commandActions`, optional `proposedExecpolicyAmendment`, optional `networkApprovalContext`, and optional `availableDecisions`. When `initialize.params.capabilities.experimentalApi = true`, the payload can also include experimental `additionalPermissions` describing requested per-command sandbox access. Any filesystem paths inside `additionalPermissions` are absolute on the wire.
3. Client responds with one of the command execution approval decisions above.
4. `serverRequest/resolved` confirms that the pending request has been answered or cleared.
5. `item/completed` returns the final `commandExecution` item with `status: completed | failed | declined`.

When `networkApprovalContext` is present, the prompt is for managed network access (not a general shell-command approval). The current v2 schema exposes the target `host` and `protocol`; clients should render a network-specific prompt and not rely on `command` being a user-meaningful shell command preview.

Codex groups concurrent network approval prompts by destination (`host`, protocol, and port). The app-server may therefore send one prompt that unblocks multiple queued requests to the same destination, while different ports on the same host are treated separately.

### File change approvals

Order of messages:

1. `item/started` emits a `fileChange` item with proposed `changes` and `status: "inProgress"`.
2. `item/fileChange/requestApproval` includes `itemId`, `threadId`, `turnId`, optional `reason`, and optional `grantRoot`.
3. Client responds with one of the file change approval decisions above.
4. `serverRequest/resolved` confirms that the pending request has been answered or cleared.
5. `item/completed` returns the final `fileChange` item with `status: completed | failed | declined`.

### `tool/requestUserInput`

When the client responds to `item/tool/requestUserInput`, app-server emits `serverRequest/resolved` with `{ threadId, requestId }`. If the pending request is cleared by turn start, turn completion, or turn interruption before the client answers, the server emits the same notification for that cleanup.

Request params include `autoResolutionMs` as an integer millisecond timeout or
`null`. When present, host clients can resolve the prompt automatically after that
interval if the user doesn't answer.

### Permission requests

The built-in `request_permissions` tool sends
`item/permissions/requestApproval` with the `threadId`, `turnId`, `itemId`,
`environmentId`, `cwd`, optional `reason`, and requested network or filesystem
permissions. Respond with `permissions` containing only the granted subset.
Set `scope` to `"session"` to persist the grant for later turns in the same
session; omit it or use `"turn"` for a turn-scoped grant. Permissions that
weren't requested are ignored.

### MCP server elicitation requests

An MCP server can interrupt a turn with `mcpServer/elicitation/request`. The
request includes `threadId`, an optional `turnId`, `serverName`, and one of
these request shapes:

- `mode: "form"` or `mode: "openai/form"`, with `message` and
  `requestedSchema`.
- `mode: "url"`, with `message`, `url`, and `elicitationId`.

Respond with `action: "accept"` and the requested `content`, or with
`action: "decline"` or `"cancel"` and `content: null`. App-server then emits
`serverRequest/resolved`. To receive the `openai/form` variant, opt in with
`initialize.params.capabilities.mcpServerOpenaiFormElicitation`.

### Dynamic tool calls (experimental)

`dynamicTools` on `thread/start` and the corresponding `item/tool/call` request or response flow are experimental APIs.

Dynamic tool names and namespace names must follow Responses API naming
constraints. Avoid reserved namespace names used by built-in Codex tools.

When a dynamic tool is invoked during a turn, app-server emits:

1. `item/started` with `item.type = "dynamicToolCall"`, `status = "inProgress"`, plus `tool` and `arguments`.
2. `item/tool/call` as a server request to the client.
3. The client response payload with returned content items.
4. `item/completed` with `item.type = "dynamicToolCall"`, the final `status`, and any returned `contentItems` or `success` value.

### MCP tool-call approvals (apps)

App (connector) tool calls can also require approval. When an app tool call has side effects, the server may elicit approval with `tool/requestUserInput` and options such as **Accept**, **Decline**, and **Cancel**. Destructive tool annotations always trigger approval even when the tool also advertises less-privileged hints. If the user declines or cancels, the related `mcpToolCall` item completes with an error instead of running the tool.

## Skills

Invoke a skill by including `$<skill-name>` in the user text input. Add a `skill` input item (recommended) so the server injects full skill instructions instead of relying on the model to resolve the name.

```json
{
  "method": "turn/start",
  "id": 101,
  "params": {
    "threadId": "thread-1",
    "input": [
      {
        "type": "text",
        "text": "$skill-creator Add a new skill for triaging flaky CI."
      },
      {
        "type": "skill",
        "name": "skill-creator",
        "path": "/Users/me/.codex/skills/skill-creator/SKILL.md"
      }
    ]
  }
}
```

If you omit the `skill` item, the model will still parse the `$<skill-name>` marker and try to locate the skill, which can add latency.

Example:

```text
$skill-creator Add a new skill for triaging flaky CI and include step-by-step usage.
```

Use `skills/list` to fetch available skills (optionally scoped by `cwds`, with `forceReload`). You can also include `perCwdExtraUserRoots` to scan extra absolute paths as `user` scope for specific `cwd` values. App-server ignores entries whose `cwd` isn't present in `cwds`. `skills/list` may reuse a cached result per `cwd`; set `forceReload: true` to refresh from disk. When present, the server reads `interface` and `dependencies` from `SKILL.json`.

```json
{ "method": "skills/list", "id": 25, "params": {
  "cwds": ["/Users/me/project", "/Users/me/other-project"],
  "forceReload": true,
  "perCwdExtraUserRoots": [
    {
      "cwd": "/Users/me/project",
      "extraUserRoots": ["/Users/me/shared-skills"]
    }
  ]
} }
{ "id": 25, "result": {
  "data": [{
    "cwd": "/Users/me/project",
    "skills": [
      {
        "name": "skill-creator",
        "description": "Create or update a Codex skill",
        "enabled": true,
        "interface": {
          "displayName": "Skill Creator",
          "shortDescription": "Create or update a Codex skill"
        },
        "dependencies": {
          "tools": [
            {
              "type": "env_var",
              "value": "GITHUB_TOKEN",
              "description": "GitHub API token"
            },
            {
              "type": "mcp",
              "value": "github",
              "transport": "streamable_http",
              "url": "https://example.com/mcp"
            }
          ]
        }
      }
    ],
    "errors": []
  }]
} }
```

The server also emits `skills/changed` notifications when watched local skill files change. Treat this as an invalidation signal and rerun `skills/list` with your current params when needed.

To enable or disable a skill by path:

```json
{
  "method": "skills/config/write",
  "id": 26,
  "params": {
    "path": "/Users/me/.codex/skills/skill-creator/SKILL.md",
    "enabled": false
  }
}
```

## Apps (connectors)

Use `app/installed` to read the latest committed installed app runtime snapshot.
Each result includes the app `id`, `runtimeName` (or `null`), effective
`enabled` state, and `callable` state. An app is callable only when effective
configuration enables it and at least one model-visible tool complies with the
app and tool policies.

```json
{
  "method": "app/installed",
  "id": 49,
  "params": {
    "threadId": "thread-1",
    "forceRefresh": false
  }
}
{
  "id": 49,
  "result": {
    "apps": [
      {
        "id": "demo-app",
        "runtimeName": "Demo App",
        "enabled": true,
        "callable": true
      }
    ]
  }
}
```

Omit `threadId` to use the global configuration instead of a loaded thread's
configuration. Set `forceRefresh: true` to refresh the connector runtime
snapshot before reading it. When global or workspace policy blocks app access,
an observed app can still appear with `enabled` and `callable` set to `false`.

Use `app/list` to fetch available apps. In the CLI/TUI, `/apps` is the user-facing picker; in custom clients, call `app/list` directly. Each entry includes both `isAccessible` (available to the user) and `isEnabled` (enabled in `config.toml`) so clients can distinguish install/access from local enabled state. App entries can also include optional `branding`, `appMetadata`, and `labels` fields.

```json
{ "method": "app/list", "id": 50, "params": {
  "cursor": null,
  "limit": 50,
  "threadId": "thread-1",
  "forceRefetch": false
} }
{ "id": 50, "result": {
  "data": [
    {
      "id": "demo-app",
      "name": "Demo App",
      "description": "Example connector for documentation.",
      "logoUrl": "https://example.com/demo-app.png",
      "logoUrlDark": null,
      "distributionChannel": null,
      "branding": null,
      "appMetadata": null,
      "labels": null,
      "installUrl": "https://chatgpt.com/apps/demo-app/demo-app",
      "isAccessible": true,
      "isEnabled": true
    }
  ],
  "nextCursor": null
} }
```

If you provide `threadId`, app feature gating (`features.apps`) uses that thread's config snapshot. When omitted, app-server uses the latest global config.

`app/list` returns after both accessible apps and directory apps load. Set `forceRefetch: true` to bypass app caches and fetch fresh data. Cache entries are only replaced when refreshes succeed.

The server also emits `app/list/updated` notifications whenever either source (accessible apps or directory apps) finishes loading. Each notification includes the latest merged app list.

```json
{
  "method": "app/list/updated",
  "params": {
    "data": [
      {
        "id": "demo-app",
        "name": "Demo App",
        "description": "Example connector for documentation.",
        "logoUrl": "https://example.com/demo-app.png",
        "logoUrlDark": null,
        "distributionChannel": null,
        "branding": null,
        "appMetadata": null,
        "labels": null,
        "installUrl": "https://chatgpt.com/apps/demo-app/demo-app",
        "isAccessible": true,
        "isEnabled": true
      }
    ]
  }
}
```

Use `app/read` when you already know the app ids and need app metadata rather
than installed runtime state. Pass at most 100 `appIds`. The server keeps only
the first occurrence of each repeated id and preserves that order in both
`apps` and `missingAppIds`. Unknown or inaccessible apps are returned in
`missingAppIds` without failing the entire request.

```json
{
  "method": "app/read",
  "id": 52,
  "params": {
    "appIds": ["demo-app", "missing-app"],
    "includeTools": true
  }
}
{
  "id": 52,
  "result": {
    "apps": [
      {
        "id": "demo-app",
        "name": "Demo App",
        "description": "Example connector for documentation.",
        "iconUrl": null,
        "iconUrlDark": null,
        "distributionChannel": null,
        "installUrl": null,
        "pluginDisplayNames": [],
        "toolSummaries": [
          {
            "name": "search",
            "title": "Search",
            "description": "Search the app.",
            "isEnabled": true,
            "disabledReason": null,
            "isReadOnly": true
          }
        ]
      }
    ],
    "missingAppIds": ["missing-app"]
  }
}
```

Set `includeTools: true` to request display-only public tool summaries. The
metadata response doesn't include installed app runtime state or authorize a
tool call; use `app/installed` to check effective `enabled` and `callable`
state.

Invoke an app by inserting `$<app-slug>` in the text input and adding a `mention` input item with the `app://<id>` path (recommended).

```json
{
  "method": "turn/start",
  "id": 51,
  "params": {
    "threadId": "thread-1",
    "input": [
      {
        "type": "text",
        "text": "$demo-app Pull the latest updates from the team."
      },
      {
        "type": "mention",
        "name": "Demo App",
        "path": "app://demo-app"
      }
    ]
  }
}
```

### Config RPC examples for app settings

Use `config/read`, `config/value/write`, and `config/batchWrite` to inspect or update app controls in `config.toml`.

Read the effective app config shape (including `_default` and per-tool overrides):

```json
{ "method": "config/read", "id": 60, "params": { "includeLayers": false } }
{ "id": 60, "result": {
  "config": {
    "apps": {
      "_default": {
        "enabled": true,
        "destructive_enabled": true,
        "open_world_enabled": true,
        "approvals_reviewer": "user",
        "default_tools_approval_mode": "auto"
      },
      "google_drive": {
        "enabled": true,
        "destructive_enabled": false,
        "approvals_reviewer": "auto_review",
        "default_tools_approval_mode": "prompt",
        "tools": {
          "files/delete": { "enabled": false, "approval_mode": "approve" }
        }
      }
    }
  }
} }
```

`apps._default.approvals_reviewer` sets the reviewer for all apps unless a
per-app value overrides it. When both are omitted, the app inherits the
top-level `approvals_reviewer` value. Use `apps.<id>.tools.<tool>.approvals_reviewer`
to choose the reviewer for one tool. `apps._default.default_tools_approval_mode`
sets the fallback approval mode for tools without a per-app or per-tool
override. Managed approval-mode requirements override tool approval-mode
settings.

Update a single app setting:

```json
{
  "method": "config/value/write",
  "id": 61,
  "params": {
    "keyPath": "apps.google_drive.default_tools_approval_mode",
    "value": "prompt",
    "mergeStrategy": "replace"
  }
}
```

Apply multiple app edits atomically:

```json
{
  "method": "config/batchWrite",
  "id": 62,
  "params": {
    "edits": [
      {
        "keyPath": "apps._default.destructive_enabled",
        "value": false,
        "mergeStrategy": "upsert"
      },
      {
        "keyPath": "apps.google_drive.tools.files/delete.approval_mode",
        "value": "approve",
        "mergeStrategy": "upsert"
      }
    ]
  }
}
```

### Detect and import external agent config

Use `externalAgentConfig/detect` to discover external-agent artifacts that can be migrated, then pass the selected entries to `externalAgentConfig/import`.

Detection example:

```json
{ "method": "externalAgentConfig/detect", "id": 63, "params": {
  "includeHome": true,
  "cwds": ["/Users/me/project"]
} }
{ "id": 63, "result": {
  "items": [
    {
      "itemType": "AGENTS_MD",
      "description": "Import /Users/me/project/CLAUDE.md to /Users/me/project/AGENTS.md.",
      "cwd": "/Users/me/project"
    },
    {
      "itemType": "SKILLS",
      "description": "Copy skill folders from /Users/me/.claude/skills to /Users/me/.agents/skills.",
      "cwd": null
    }
  ]
} }
```

Import example:

```json
{ "method": "externalAgentConfig/import", "id": 64, "params": {
  "migrationItems": [
    {
      "itemType": "AGENTS_MD",
      "description": "Import /Users/me/project/CLAUDE.md to /Users/me/project/AGENTS.md.",
      "cwd": "/Users/me/project"
    }
  ],
  "source": "claude-code"
} }
{ "id": 64, "result": { "importId": "8ae96ff3-3425-4f4c-8772-b6fd61502868" } }
```

The optional top-level `source` import parameter labels the product that
produced the selected migration items.

The server emits `externalAgentConfig/import/progress` as item types complete,
and `externalAgentConfig/import/completed` after all synchronous and background
imports finish. These notifications include the same `importId` from the
response and `itemTypeResults` with per-type `successes` and `failures`.
Completion may arrive immediately after the response or after background remote
imports complete.

```json
{ "method": "externalAgentConfig/import/progress", "params": {
  "importId": "8ae96ff3-3425-4f4c-8772-b6fd61502868",
  "itemTypeResults": [
    {
      "itemType": "AGENTS_MD",
      "successes": [
        { "itemType": "AGENTS_MD", "cwd": "/Users/me/project", "source": null, "target": "/Users/me/project/AGENTS.md" }
      ],
      "failures": []
    }
  ]
} }
{ "method": "externalAgentConfig/import/completed", "params": {
  "importId": "8ae96ff3-3425-4f4c-8772-b6fd61502868",
  "itemTypeResults": [
    {
      "itemType": "AGENTS_MD",
      "successes": [
        { "itemType": "AGENTS_MD", "cwd": "/Users/me/project", "source": null, "target": "/Users/me/project/AGENTS.md" }
      ],
      "failures": []
    }
  ]
} }
```

Read prior completed imports:

```json
{ "method": "externalAgentConfig/import/readHistories", "id": 65 }
{ "id": 65, "result": { "data": [
  {
    "importId": "8ae96ff3-3425-4f4c-8772-b6fd61502868",
    "completedAtMs": 1781784000000,
    "successes": [
      { "itemType": "AGENTS_MD", "cwd": "/Users/me/project", "source": null, "target": "/Users/me/project/AGENTS.md" }
    ],
    "failures": []
  }
] } }
```

Supported `itemType` values are `AGENTS_MD`, `CONFIG`, `SKILLS`, `PLUGINS`,
`MCP_SERVER_CONFIG`, `SUBAGENTS`, `HOOKS`, `COMMANDS`, and `SESSIONS`. For
`PLUGINS` items, `details.plugins` lists each `marketplaceName` and the
`pluginNames` Codex can try to migrate. Detection returns only items that still
have work to do. For example, Codex skips AGENTS migration when `AGENTS.md`
already exists and is non-empty, and skill imports don't overwrite existing
skill directories.

When detecting plugins from `.claude/settings.json`, Codex reads configured
marketplace sources from `extraKnownMarketplaces`. If `enabledPlugins` contains
plugins from `claude-plugins-official` but the marketplace source is missing,
Codex infers `anthropics/claude-plugins-official` as the source.

## Auth endpoints

If you’ve built a local or open-source application using Codex app-server authentication, you can continue using it, though we recommend migrating to Sign in with ChatGPT so users have greater control over and visibility into their usage. See developer docs for Sign in with ChatGPT [here](https://developers.openai.com/siwc), and our implementation cookbook [here](https://developers.openai.com/cookbook/articles/sign-in-with-chatgpt). App-server authentication has never been permitted for commercial or hosted services. We launched Sign in with ChatGPT to support these use cases, and we’re excited to see what you build. Join our partner waitlist [here](https://openai.com/form/sign-in-with-chatgpt-interest/).

The JSON-RPC auth/account surface exposes request/response methods plus server-initiated notifications (no `id`). Use these to determine auth state, start or cancel logins, logout, inspect ChatGPT rate limits, and notify workspace owners about depleted credits or usage limits.

### Authentication modes

Codex supports these authentication modes. `account/updated.authMode` shows the active mode and includes the current ChatGPT `planType` when available. `account/read` also reports account and plan details.

- **API key (`apikey`)** - the caller supplies an OpenAI API key with `type: "apiKey"`, and Codex stores it for API requests.
- **ChatGPT managed (`chatgpt`)** - Codex owns the ChatGPT OAuth flow, persists tokens, and refreshes them automatically. Start with `type: "chatgpt"` for the browser flow or `type: "chatgptDeviceCode"` for the device-code flow.
- **ChatGPT external tokens (`chatgptAuthTokens`)** - experimental and intended for host apps that already own the user's ChatGPT auth lifecycle. The host app supplies an `accessToken`, `chatgptAccountId`, and optional `chatgptPlanType` directly, and must refresh the token when asked.
- **Amazon Bedrock** - `account/read` reports Bedrock accounts as `type: "amazonBedrock"` and indicates whether credentials come from a Codex-managed Bedrock API key (`credentialSource: "codexManaged"`) or the external AWS credential chain (`credentialSource: "awsManaged"`). `account/updated.authMode` uses `bedrockApiKey` for Codex-managed Bedrock API keys.

### API overview

- `account/read` - fetch current account info; optionally refresh tokens.
- `account/login/start` - begin login with `apiKey`, `chatgpt`, or `chatgptDeviceCode`. Experimental login types include `chatgptAuthTokens`, `amazonBedrock`, and `amazonBedrockAccessKeys`.
- `account/bedrock/setup` (experimental) - configure Amazon Bedrock with an AWS profile or environment credentials.
- `account/login/completed` (notify) - emitted when a login attempt finishes (success or error).
- `account/login/cancel` - cancel a pending managed ChatGPT login by `loginId`.
- `account/logout` - sign out; triggers `account/updated`.
- `account/updated` (notify) - emitted whenever auth mode changes (`authMode`: `apikey`, `chatgpt`, `chatgptAuthTokens`, `agentIdentity`, `personalAccessToken`, `bedrockApiKey`, or `null`) and includes `planType` when available.
- `account/chatgptAuthTokens/refresh` (server request) - request fresh externally managed ChatGPT tokens after an authorization error.
- `account/rateLimits/read` - fetch ChatGPT rate limits.
- `account/rateLimits/updated` (notify) - emitted whenever a user's ChatGPT rate limits change.
- `account/sendAddCreditsNudgeEmail` - ask ChatGPT to email a workspace owner about depleted credits or a reached usage limit.
- `account/rateLimitResetCredit/consume` - consume one earned rate-limit reset using a caller-provided `idempotencyKey` value.
- `account/usage/read` - fetch ChatGPT account token-activity summaries and daily buckets.
- `account/workspaceMessages/read` - fetch active workspace messages, including notification headlines when available.
- `mcpServer/oauthLogin/completed` (notify) - emitted after a `mcpServer/oauth/login` flow finishes; payload includes `{ name, threadId, loginId?, success, error? }`. Older servers omit `loginId`. `threadId` can be `null` for app-scoped or plugin OAuth flows.
- `mcpServer/startupStatus/updated` (notify) - emitted when a configured MCP server's startup status changes; payload includes `{ threadId, name, status, error, failureReason }`. `threadId` is `null` for app-scoped startup. On failed startup, `failureReason: "reauthenticationRequired"` means stored OAuth credentials expired and couldn't be refreshed, so the client should offer to reconnect the server.

### Select Amazon Bedrock Runtime

Set `capabilities.experimentalApi` to `true` during initialization. Pass
`providerId: "amazon-bedrock-runtime"` to `account/bedrock/setup` or to
`account/login/start` with type `amazonBedrock` or `amazonBedrockAccessKeys`.
Omitting `providerId` or passing `null` selects Bedrock Mantle (`amazon-bedrock`).

### Sign in to a configured gateway

If your client handles gateway sign-in, set `capabilities.explicitGatewayOauth` to
`true` during initialization. On each connection, call `account/gatewayOAuth/read`
successfully before sending authenticated requests. Pass `modelProvider` to check
or sign in to a specific gateway. Omit it to use the current provider.

For device-code sign-in, check that `account/gatewayOAuth/read` returns
`supportsDeviceAuth: true`. Call `account/gatewayOAuth/login` with the same
`modelProvider` and `deviceAuth: true`. A `null` prompt means the server reused
or refreshed the credential. Otherwise, show `prompt.verificationUrl` and
`prompt.userCode`, then wait for `account/gatewayOAuth/changed` with the
matching `loginId` to report whether sign-in succeeded.

### 1) Check auth state

Request:

```json
{ "method": "account/read", "id": 1, "params": { "refreshToken": false } }
```

Response examples:

```json
{ "id": 1, "result": { "account": null, "requiresOpenaiAuth": false } }
```

```json
{ "id": 1, "result": { "account": null, "requiresOpenaiAuth": true } }
```

```json
{
  "id": 1,
  "result": { "account": { "type": "apiKey" }, "requiresOpenaiAuth": true }
}
```

```json
{
  "id": 1,
  "result": {
    "account": {
      "type": "amazonBedrock",
      "credentialSource": "codexManaged"
    },
    "requiresOpenaiAuth": false
  }
}
```

```json
{
  "id": 1,
  "result": {
    "account": {
      "type": "amazonBedrock",
      "credentialSource": "awsManaged"
    },
    "requiresOpenaiAuth": false
  }
}
```

```json
{
  "id": 1,
  "result": {
    "account": {
      "type": "chatgpt",
      "email": "user@example.com",
      "planType": "pro"
    },
    "requiresOpenaiAuth": true
  }
}
```

Field notes:

- `refreshToken` (boolean): set `true` to force a token refresh in managed ChatGPT mode. In external token mode (`chatgptAuthTokens`), app-server ignores this flag.
- `email` is `null` when the ChatGPT account doesn't have an email address.
- `requiresOpenaiAuth` reflects the active provider; when `false`, Codex can run without OpenAI credentials.
- Amazon Bedrock reports `credentialSource: "codexManaged"` when it uses a
  Bedrock API key managed by Codex. It reports `credentialSource: "awsManaged"`
  for the external AWS credential path. This identifies the selected credential
  source; it doesn't validate that the AWS credential chain can resolve
  credentials.

### 2) Log in with an API key

1. Send:

```json
   {
     "method": "account/login/start",
     "id": 2,
     "params": { "type": "apiKey", "apiKey": "sk-..." }
   }
```

2. Expect:

```json
   { "id": 2, "result": { "type": "apiKey" } }
```

3. Notifications:

```json
   {
     "method": "account/login/completed",
     "params": { "loginId": null, "success": true, "error": null }
   }
```

```json
   {
     "method": "account/updated",
     "params": { "authMode": "apikey", "planType": null }
   }
```

### 3) Log in with ChatGPT (browser flow)

1. Start:

```json
   {
     "method": "account/login/start",
     "id": 3,
     "params": {
       "type": "chatgpt",
       "useHostedLoginSuccessPage": true,
       "appBrand": "chatgpt"
     }
   }
```

   By default, a successful browser callback redirects to a local success page.
   Set `useHostedLoginSuccessPage: true` to use the hosted success page when
   organization setup isn't required. With hosted success enabled, `appBrand`
   can be `"codex"` or `"chatgpt"`; omitted or `null` values default to
   `"codex"`.

```json
   {
     "id": 3,
     "result": {
       "type": "chatgpt",
       "loginId": "<uuid>",
       "authUrl": "https://chatgpt.com/...&redirect_uri=http%3A%2F%2Flocalhost%3A<port>%2Fauth%2Fcallback"
     }
   }
```

2. Open `authUrl` in a browser; the app-server hosts the local callback.
3. Wait for notifications:

```json
   {
     "method": "account/login/completed",
     "params": { "loginId": "<uuid>", "success": true, "error": null }
   }
```

```json
   {
     "method": "account/updated",
     "params": { "authMode": "chatgpt", "planType": "plus" }
   }
```

### 3b) Log in with ChatGPT (device-code flow)

Use this flow when your client owns the sign-in ceremony or when a browser callback is brittle.

1. Start:

```json
   {
     "method": "account/login/start",
     "id": 4,
     "params": { "type": "chatgptDeviceCode" }
   }
```

```json
   {
     "id": 4,
     "result": {
       "type": "chatgptDeviceCode",
       "loginId": "<uuid>",
       "verificationUrl": "https://auth.openai.com/codex/device",
       "userCode": "ABCD-1234"
     }
   }
```

2. Show `verificationUrl` and `userCode` to the user; the frontend owns the UX.
3. Wait for notifications:

```json
   {
     "method": "account/login/completed",
     "params": { "loginId": "<uuid>", "success": true, "error": null }
   }
```

```json
   {
     "method": "account/updated",
     "params": { "authMode": "chatgpt", "planType": "plus" }
   }
```

### 3c) Log in with externally managed ChatGPT tokens (`chatgptAuthTokens`)

Use this experimental mode only when a host application owns the user's ChatGPT auth lifecycle and supplies tokens directly. Clients must set `capabilities.experimentalApi = true` during `initialize` before using this login type.

1. Send:

```json
   {
     "method": "account/login/start",
     "id": 7,
     "params": {
       "type": "chatgptAuthTokens",
       "accessToken": "<jwt>",
       "chatgptAccountId": "org-123",
       "chatgptPlanType": "business"
     }
   }
```

2. Expect:

```json
   { "id": 7, "result": { "type": "chatgptAuthTokens" } }
```

3. Notifications:

```json
   {
     "method": "account/login/completed",
     "params": { "loginId": null, "success": true, "error": null }
   }
```

```json
   {
     "method": "account/updated",
     "params": { "authMode": "chatgptAuthTokens", "planType": "business" }
   }
```

When the server receives a `401 Unauthorized`, it may request refreshed tokens from the host app:

```json
{
  "method": "account/chatgptAuthTokens/refresh",
  "id": 8,
  "params": { "reason": "unauthorized", "previousAccountId": "org-123" }
}
{ "id": 8, "result": { "accessToken": "<jwt>", "chatgptAccountId": "org-123", "chatgptPlanType": "business" } }
```

The server retries the original request after a successful refresh response. Requests time out after about 10 seconds.

### 4) Cancel a ChatGPT login

```json
{ "method": "account/login/cancel", "id": 4, "params": { "loginId": "<uuid>" } }
{ "method": "account/login/completed", "params": { "loginId": "<uuid>", "success": false, "error": "..." } }
```

### 5) Logout

```json
{ "method": "account/logout", "id": 5 }
{ "id": 5, "result": {} }
{ "method": "account/updated", "params": { "authMode": null, "planType": null } }
```

### 6) Rate limits (ChatGPT)

```json
{ "method": "account/rateLimits/read", "id": 6 }
{ "id": 6, "result": {
  "rateLimits": {
    "limitId": "codex",
    "limitName": null,
    "primary": { "usedPercent": 25, "windowDurationMins": 15, "resetsAt": 1730947200 },
    "secondary": null,
    "rateLimitReachedType": null
  },
  "rateLimitsByLimitId": {
    "codex": {
      "limitId": "codex",
      "limitName": null,
      "primary": { "usedPercent": 25, "windowDurationMins": 15, "resetsAt": 1730947200 },
      "secondary": null,
      "rateLimitReachedType": null
    },
    "codex_other": {
      "limitId": "codex_other",
      "limitName": "codex_other",
      "primary": { "usedPercent": 42, "windowDurationMins": 60, "resetsAt": 1730950800 },
      "secondary": null,
      "rateLimitReachedType": null
    }
  },
  "rateLimitResetCredits": {
    "availableCount": 2,
    "credits": [{
      "id": "RateLimitResetCredit_1",
      "resetType": "codexRateLimits",
      "status": "available",
      "grantedAt": 1781654400,
      "expiresAt": 1784246400,
      "title": "Rate-limit reset",
      "description": "Reset an eligible Codex rate-limit window."
    }]
  }
} }
{ "method": "account/rateLimits/updated", "params": {
  "rateLimits": {
    "limitId": "codex",
    "primary": { "usedPercent": 31, "windowDurationMins": 15, "resetsAt": 1730948100 }
  }
} }
```

Field notes:

- `rateLimits` is the backward-compatible single-bucket view.
- `rateLimitsByLimitId` (when present) is the multi-bucket view keyed by metered `limit_id` (for example `codex`).
- `limitId` is the metered bucket identifier.
- `limitName` is an optional user-facing label for the bucket.
- `usedPercent` is current usage within the quota window.
- `windowDurationMins` is the quota window length.
- `resetsAt` is a Unix timestamp (seconds) for the next reset.
- `planType` is included when the server returns the ChatGPT plan associated with a bucket.
- `credits` is included when the server returns remaining workspace credit details.
- `rateLimitReachedType` identifies the server-classified limit state when one has been reached.
- `rateLimitResetCredits` contains the available earned-reset count when the service provides it; otherwise it's `null`.
- `rateLimitResetCredits.credits` is `null` when only the count is known. An empty array means the service fetched details and returned no available credits. The service can cap the detail rows, so `availableCount` is authoritative.
- Each detail row includes an opaque `id`, `resetType`, `status`, `grantedAt`, `expiresAt` (which can be `null`), `title` (which can be `null`), and `description` (which can be `null`).
- Fetch `account/rateLimits/read` after consuming a reset.

### 7) Token usage (ChatGPT)

Use `account/usage/read` to fetch ChatGPT token-activity summary fields and
optional daily buckets.

```json
{ "method": "account/usage/read", "id": 7 }
{ "id": 7, "result": {
  "summary": {
    "lifetimeTokens": 1234567,
    "peakDailyTokens": 45678,
    "longestRunningTurnSec": 540,
    "currentStreakDays": 8,
    "longestStreakDays": 14
  },
  "dailyUsageBuckets": [
    { "startDate": "2026-06-18", "tokens": 12345 }
  ]
} }
```

Field notes:

- `summary` values may be `null` when the service hasn't returned that metric.
- `dailyUsageBuckets` may be `null`; when present, each bucket includes `startDate` and `tokens`.
- The endpoint requires authentication backed by Codex services. ChatGPT,
  external ChatGPT tokens, agent identity, and personal access token auth work;
  API-key-only and Bedrock auth don't.

### 8) Earned rate-limit resets (ChatGPT)

Use `account/rateLimitResetCredit/consume` to consume one earned reset.

```json
{ "method": "account/rateLimitResetCredit/consume", "id": 8, "params": { "idempotencyKey": "8ae96ff3-3425-4f4c-8772-b6fd61502868", "creditId": "RateLimitResetCredit_1" } }
{ "id": 8, "result": { "outcome": "reset" } }
```

Field notes:

- `idempotencyKey` must be non-empty. Use a UUID for each logical redemption attempt and reuse the same value when retrying that attempt.
- `creditId` is optional. When provided, it must be a non-empty opaque ID from `account/rateLimits/read`. When omitted, the service selects the next available credit.
- `reset` means a credit was consumed.
- `alreadyRedeemed` means the same redemption completed previously. Treat it as an idempotent success and refresh account limits.
- `nothingToReset` means there is no eligible rate-limit window to reset.
- `noCredit` means the account has no earned reset credits available.
- Fetch `account/rateLimits/read` after consuming a reset instead of inferring updated windows from this response.

### 9) Notify a workspace owner about a limit

Use `account/sendAddCreditsNudgeEmail` to ask ChatGPT to email a workspace owner when credits are depleted or a usage limit has been reached.

```json
{ "method": "account/sendAddCreditsNudgeEmail", "id": 9, "params": { "creditType": "credits" } }
{ "id": 9, "result": { "status": "sent" } }
```

Use `creditType: "credits"` when workspace credits are depleted, or `creditType: "usage_limit"` when the workspace usage limit has been reached. If the owner was already notified recently, the response status is `cooldown_active`.

### 10) Workspace messages (ChatGPT)

Use `account/workspaceMessages/read` to fetch active messages for the current
workspace, including notification headlines when available.

```json
{ "method": "account/workspaceMessages/read", "id": 10 }
{ "id": 10, "result": { "featureEnabled": true, "messages": [
  { "messageId": "msg_123", "messageType": "headline", "messageBody": "Workspace maintenance starts at 5pm.", "createdAt": 1781395200, "archivedAt": null }
] } }
```
