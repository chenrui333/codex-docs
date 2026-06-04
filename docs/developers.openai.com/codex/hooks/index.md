---
source_type: 'developers'
source_area: 'codex_cli_docs'
source_url: 'https://developers.openai.com/codex/hooks'
source_last_modified: '2026-05-22T20:25:51Z'
source_etag: 'W/"dbdc864dd3d2182dd9b998ddae96fe46"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0"]
---

# Hooks – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/hooks

Hooks are an extensibility framework for Codex. They allow
you to inject your own scripts into the agentic loop, enabling features such as:

- Send the conversation to a custom logging/analytics engine
- Scan your team’s prompts to block accidentally pasting API keys
- Summarize conversations to create persistent memories automatically
- Run a custom validation check when a conversation turn stops, enforcing standards
- Customize prompting when in a certain directory

Hooks are enabled by default. If you need to turn them off in `config.toml`,
set:

```
[features]
hooks = false
```

Use `hooks` as the canonical feature key. `codex_hooks` still works as a
deprecated alias.

Admins can force hooks off the same way in `requirements.toml` with
`[features].hooks = false`.

Runtime behavior to keep in mind:

- Matching hooks from multiple files all run.
- Multiple matching command hooks for the same event are launched concurrently,
  so one hook cannot prevent another matching hook from starting.
- Non-managed command hooks must be reviewed and trusted before they run.
- `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`,
  `PostCompact`, `UserPromptSubmit`, `SubagentStop`, and `Stop` run at turn
  scope. `SessionStart` and `SubagentStart` run at thread or subagent-start
  scope.

## Where Codex looks for hooks

Codex discovers hooks next to active config layers in either of these forms:

- `hooks.json`
- inline `[hooks]` tables inside `config.toml`

Installed plugins can also bundle lifecycle config through their plugin
manifest or a default `hooks/hooks.json` file. See [Build
plugins](/codex/plugins/build#bundled-mcp-servers-and-lifecycle-config) for the
plugin packaging rules.

In practice, the four most useful locations are:

- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `<repo>/.codex/hooks.json`
- `<repo>/.codex/config.toml`

If more than one hook source exists, Codex loads all matching hooks.
Higher-precedence config layers don’t replace lower-precedence hooks.
If a single layer contains both `hooks.json` and inline `[hooks]`, Codex
merges them and warns at startup. Prefer one representation per layer.

Codex can also discover hooks bundled with enabled plugins. Plugin-bundled
hooks load alongside other hook sources and use the same trust-review flow as
other non-managed hooks.

Project-local hooks load only when the project `.codex/` layer is trusted. In
untrusted projects, Codex still loads user and system hooks from their own
active config layers.

## Review and trust hooks

Codex lists configured hooks before deciding which ones can run. Before a
non-managed command hook can run, Codex requires you to review and trust the
exact hook definition. Codex records trust against the hook’s current hash, so
new or changed hooks are marked for review and skipped until trusted.

Use `/hooks` in the CLI to inspect hook sources, review new or changed hooks,
trust hooks, or disable individual non-managed hooks. If hooks need review at
startup, Codex prints a warning that tells you to open `/hooks`.

Managed hooks from system, MDM, cloud, or `requirements.toml` sources are marked
as managed, trusted by policy, and can’t be disabled from the user hook browser.

For one-off automation that already vets hook sources outside Codex, pass
`--dangerously-bypass-hook-trust` to run enabled hooks without requiring
persisted hook trust for that invocation.

## Config shape

Hooks are organized in three levels:

- A hook event such as `PreToolUse`, `PostToolUse`, `PreCompact`,
  `SubagentStart`, or `Stop`
- A matcher group that decides when that event matches
- One or more hook handlers that run when the matcher group matches

```
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/session_start.py",
            "statusMessage": "Loading session notes"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py\"",
            "statusMessage": "Checking Bash command"
          }
        ]
      }
    ],
    "PermissionRequest": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/permission_request.py\"",
            "statusMessage": "Checking approval request"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/post_tool_use_review.py\"",
            "statusMessage": "Reviewing Bash output"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/user_prompt_submit_data_flywheel.py\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/stop_continue.py\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Notes:

- `timeout` is in seconds.
- If `timeout` is omitted, Codex uses `600` seconds.
- `statusMessage` is optional.
- `commandWindows` is an optional Windows-only command override. In TOML, use
  `command_windows` or `commandWindows`.
- `async` is parsed, but async command hooks aren’t supported yet. Codex skips
  handlers with `async: true`.
- Only `type: "command"` handlers run today. `prompt` and `agent` handlers are
  parsed but skipped.
- Commands run with the session `cwd` as their working directory.
- For repo-local hooks, prefer resolving from the git root instead of using a
  relative path such as `.codex/hooks/...`. Codex may be started from a
  subdirectory, and a git-root-based path keeps the hook location stable.

Equivalent inline TOML in `config.toml`:

```
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py"'
timeout = 30
statusMessage = "Checking Bash command"

[[hooks.PostToolUse]]
matcher = "^Bash$"

[[hooks.PostToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/post_tool_use_review.py"'
timeout = 30
statusMessage = "Reviewing Bash output"
```

## Managed hooks from `requirements.toml`

Enterprise-managed requirements can also define hooks inline under `[hooks]`.
This is useful when admins want to enforce the hook configuration while
delivering the actual scripts through MDM or another device-management system.
To enforce managed hooks even for users who disabled hooks locally, pin
`[features].hooks = true` in `requirements.toml` alongside `[hooks]`. To ignore
user, project, session, and plugin hooks while still allowing administrator
managed hooks, set `allow_managed_hooks_only = true`.

```
allow_managed_hooks_only = true

[features]
hooks = true

[hooks]
managed_dir = "/enterprise/hooks"
windows_managed_dir = 'C:\enterprise\hooks'

[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = "python3 /enterprise/hooks/pre_tool_use_policy.py"
command_windows = 'py -3 C:\enterprise\hooks\pre_tool_use_policy.py'
timeout = 30
statusMessage = "Checking managed Bash command"
```

Notes for managed hooks:

- `managed_dir` is used on macOS and Linux.
- `windows_managed_dir` is used on Windows.
- Codex doesn’t distribute the scripts in `managed_dir`; your enterprise
  tooling must install and update them separately.
- Managed hook commands should use absolute script paths under the configured
  managed directory.
- `allow_managed_hooks_only = true` skips hooks from user, project, session, and
  plugin sources, but still loads managed hooks from `requirements.toml` and
  other managed config layers.

## Plugin-bundled hooks

When a plugin is enabled, Codex can load lifecycle hooks from that plugin
alongside user, project, and managed hooks.

By default, Codex looks for `hooks/hooks.json` inside the plugin root. A plugin
manifest can override that default with a `hooks` entry in
`.codex-plugin/plugin.json`. The manifest entry can be a `./`-prefixed path, an
array of `./`-prefixed paths, an inline hooks object, or an array of inline
hooks objects.

```
{
  "name": "repo-policy",
  "hooks": "./hooks/hooks.json"
}
```

Manifest hook paths are resolved relative to the plugin root and must stay
inside that root. If a manifest defines `hooks`, Codex uses those manifest
entries instead of the default `hooks/hooks.json`.

Plugin hook commands receive these environment variables:

- `PLUGIN_ROOT` is a Codex-specific extension that points to the installed
  plugin root.
- `PLUGIN_DATA` is a Codex-specific extension that points to the plugin’s
  writable data directory.
- Codex also sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for
  compatibility with existing plugin hooks.

Plugin hooks use the same event schema as other hooks. Installing or enabling a
plugin doesn’t automatically trust its hooks; Codex skips plugin-bundled hooks
until you review and trust the current hook definition.

## Matcher patterns

The `matcher` field is a regex string that filters when hooks fire. Use `"*"`,
`""`, or omit `matcher` entirely to match every occurrence of a supported
event.

Only some current Codex events honor `matcher`:

| Event | What `matcher` filters | Notes |
| --- | --- | --- |
| `PermissionRequest` | tool name | Support includes `Bash`, `apply_patch`\*, and MCP tool names |
| `PostToolUse` | tool name | Support includes `Bash`, `apply_patch`\*, and MCP tool names |
| `PostCompact` | compaction trigger | Values are `manual` or `auto` |
| `PreCompact` | compaction trigger | Values are `manual` or `auto` |
| `PreToolUse` | tool name | Support includes `Bash`, `apply_patch`\*, and MCP tool names |
| `SessionStart` | start source | Values are `startup`, `resume`, `clear`, and `compact` |
| `SubagentStart` | subagent type | Values depend on the subagent that starts |
| `SubagentStop` | subagent type | Values depend on the subagent that stops |
| `UserPromptSubmit` | not supported | Any configured `matcher` is ignored for this event |
| `Stop` | not supported | Any configured `matcher` is ignored for this event |

\*For `apply_patch`, `matcher` values can also use `Edit` or `Write`.

Examples:

- `Bash`
- `^apply_patch$`
- `Edit|Write`
- `mcp__filesystem__read_file`
- `mcp__filesystem__.*`
- `startup|resume|clear|compact`
- `manual|auto`

## Common input fields

Every command hook receives one JSON object on `stdin`.

These are the shared fields you will usually use:

| Field | Type | Meaning |
| --- | --- | --- |
| `session_id` | `string` | Current Codex session id. Subagent hooks use the parent session id. |
| `transcript_path` | `string | null` | Path to the session transcript file, if any |
| `cwd` | `string` | Working directory for the session |
| `hook_event_name` | `string` | Current hook event name |
| `model` | `string` | Codex-specific extension. Active model slug |

Turn-scoped hooks list `turn_id` as a Codex-specific extension in their
event-specific tables.

`SessionStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`,
`UserPromptSubmit`, `SubagentStart`, `SubagentStop`, and `Stop` also include
`permission_mode`, which describes the current permission mode as `default`,
`acceptEdits`, `plan`, `dontAsk`, or `bypassPermissions`.

`transcript_path` points to a conversation transcript for convenience, but the
transcript format is not a stable interface for hooks and may change over time.

If you need the full wire format, see [Schemas](#schemas).

## Common output fields

`SessionStart`, `PreCompact`, `PostCompact`, `UserPromptSubmit`,
`SubagentStop`, and `Stop` support these shared JSON fields. `SubagentStart`
accepts the same shape for `systemMessage` and hook-specific context, but
`continue: false` doesn’t stop the subagent:

```
{
  "continue": true,
  "stopReason": "optional",
  "systemMessage": "optional",
  "suppressOutput": false
}
```

| Field | Effect |
| --- | --- |
| `continue` | If `false`, marks that hook run as stopped |
| `stopReason` | Recorded as the reason for stopping |
| `systemMessage` | Surfaced as a warning in the UI or event stream |
| `suppressOutput` | Parsed today but not yet implemented |

Exit `0` with no output is treated as success and Codex continues.

`PreToolUse` and `PermissionRequest` support `systemMessage`, but `continue`,
`stopReason`, and `suppressOutput` aren’t currently supported for those events.
If a `PreToolUse` hook returns one of those unsupported fields, Codex marks
that hook run as failed, reports the error, and continues the tool call.

`PostToolUse` supports `systemMessage`, `continue: false`, and `stopReason`.
`suppressOutput` is parsed but not currently supported for that event.

## Hooks

### SessionStart

`matcher` is applied to `source` for this event.

Fields in addition to [Common input fields](#common-input-fields):

| Field | Type | Meaning |
| --- | --- | --- |
| `source` | `string` | How the session started: `startup`, `resume`, `clear`, or `compact` |

Plain text on `stdout` is added as extra developer context.

JSON on `stdout` supports [Common output fields](#common-output-fields) and this
hook-specific shape:

```
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Load the workspace conventions before editing."
  }
}
```

That `additionalContext` text is added as extra developer context.

### SubagentStart

`matcher` is applied to `agent_type` for this event.

Fields in addition to [Common input fields](#common-input-fields):

| Field | Type | Meaning |
| --- | --- | --- |
| `turn_id` | `string` | Codex-specific extension. Active Codex turn id |
| `agent_id` | `string` | Identifier for the subagent |
| `agent_type` | `string` | Subagent type or profile |
| `permission_mode` | `string` | Current permission mode |

Plain text on `stdout` is added as extra developer context for the subagent.

JSON on `stdout` supports `systemMessage` and this hook-specific shape:

```
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Review the repository test conventions first."
  }
}
```

That `additionalContext` text is added as extra developer context for the
subagent. `continue: false` is parsed for compatibility, but it doesn’t stop the
subagent from starting.

### PreToolUse

`PreToolUse` can intercept Bash, file edits performed through `apply_patch`,
and MCP tool calls. It’s still a guardrail rather than a complete enforcement
boundary because Codex can often perform equivalent work through another
supported tool path.

This doesn’t intercept all shell calls yet, only the simple ones. The newer
`unified_exec` mechanism allows richer streaming stdin/stdout handling of
shell, but interception is incomplete. Similarly, this doesn’t intercept
`WebSearch` or other non-shell, non-MCP tool calls.

`matcher` is applied to `tool_name` and matcher aliases. For file edits through
`apply_patch`, `matcher` values can use `apply_patch`, `Edit`, or `Write`; hook input
still reports `tool_name: "apply_patch"`.

Fields in addition to [Common input fields](#common-input-fields):

| Field | Type | Meaning |
| --- | --- | --- |
| `turn_id` | `string` | Codex-specific extension. Active Codex turn id |
| `tool_name` | `string` | Canonical hook tool name, such as `Bash`, `apply_patch`, or an MCP name like `mcp__fs__read` |
| `tool_use_id` | `string` | Tool-call id for this invocation |
| `tool_input` | `JSON value` | Tool-specific input. `Bash` and `apply_patch` use `tool_input.command` while MCP tools send all arguments. |

Plain text on `stdout` is ignored.

JSON on `stdout` can use `systemMessage`. To deny a supported tool call, return
this hook-specific shape:

```
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook."
  }
}
```

Codex also accepts this older block shape:

```
{
  "decision": "block",
  "reason": "Destructive command blocked by hook."
}
```

You can also use exit code `2` and write the blocking reason to `stderr`.

To add model-visible context without blocking, return
`hookSpecificOutput.additionalContext`:

```
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "The pending command touches generated files."
  }
}
```

To rewrite a supported tool call without blocking, return
`permissionDecision: "allow"` with `updatedInput`:

```
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "command": "echo rewritten"
    }
  }
}
```

For Bash commands and `apply_patch`, `updatedInput` must include a string
`command` field. For MCP tools, `updatedInput` is the replacement arguments
object. Return `updatedInput` only with `permissionDecision: "allow"`; other
`updatedInput` shapes are reported as errors.

`permissionDecision: "ask"`, legacy `decision: "approve"`, `continue: false`,
`stopReason`, and `suppressOutput` are parsed but not supported yet. Codex marks
the hook run as failed, reports the error, and continues the tool call.

### PermissionRequest

`PermissionRequest` runs when Codex is about to ask for approval, such as a
shell escalation or managed-network approval. It can allow the request, deny
the request, or decline to decide and let the normal approval prompt continue.
It doesn’t run for commands that don’t need approval.

`matcher` is applied to `tool_name` and matcher aliases. Current canonical
values include `Bash`, `apply_patch`, and MCP tool names such as
`mcp__server__tool`; `apply_patch` also matches `Edit` and `Write`.

Fields in addition to [Common input fields](#common-input-fields):

| Field | Type | Meaning |
| --- | --- | --- |
| `turn_id` | `string` | Codex-specific extension. Active Codex turn id |
| `tool_name` | `string` | Canonical hook tool name, such as `Bash`, `apply_patch`, or an MCP name like `mcp__fs__read` |
| `tool_input` | `JSON value` | Tool-specific input. `Bash` and `apply_patch` use `tool_input.command` while MCP tools send all the args. |
| `tool_input.description` | `string | null` | Human-readable approval reason, when Codex has one |

Plain text on `stdout` is ignored.

Some tool inputs may include a human-readable description, but don’t rely on a
`tool_input.description` field for every tool.

To approve the request, return:

```
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow"
    }
  }
}
```

To deny the request, return:

```
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "deny",
      "message": "Blocked by repository policy."
    }
  }
}
```

If multiple matching hooks return decisions, any `deny` wins. Otherwise, an
`allow` lets the request proceed without surfacing the approval prompt. If no
matching hook decides, Codex uses the normal approval flow.

Don’t return `updatedInput`, `updatedPermissions`, or `interrupt` for
`PermissionRequest`; those fields are reserved for future behavior and fail
closed today.

### PostToolUse

`PostToolUse` runs after supported tools produce output, including Bash,
`apply_patch`, and MCP tool calls. For Bash, it also runs after commands that
exit with a non-zero status. It can’t undo side effects from the tool that
already ran.

This doesn’t intercept all shell calls yet, only the simple ones. The newer
`unified_exec` mechanism allows richer streaming stdin/stdout handling of
shell, but interception is incomplete. Similarly, this doesn’t intercept
`WebSearch` or other non-shell, non-MCP tool calls.

`matcher` is applied to `tool_name` and matcher aliases. For file edits through
`apply_patch`, `matcher` values can use `apply_patch`, `Edit`, or `Write`; hook input
still reports `tool_name: "apply_patch"`.

Fields in addition to [Common input fields](#common-input-fields):

| Field | Type | Meaning |
| --- | --- | --- |
| `turn_id` | `string` | Codex-specific extension. Active Codex turn id |
| `tool_name` | `string` | Canonical hook tool name, such as `Bash`, `apply_patch`, or an MCP name like `mcp__fs__read` |
| `tool_use_id` | `string` | Tool-call id for this invocation |
| `tool_input` | `JSON value` | Tool-specific input. `Bash` and `apply_patch` use `tool_input.command` while MCP tools send all arguments. |
| `tool_response` | `JSON value` | Tool-specific output. For MCP tools, this is the MCP call result. |

Plain text on `stdout` is ignored.

JSON on `stdout` can use `systemMessage` and this hook-specific shape:

```
{
  "decision": "block",
  "reason": "The Bash output needs review before continuing.",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "The command updated generated files."
  }
}
```

That `additionalContext` text is added as extra developer context.

For this event, `decision: "block"` doesn’t undo the completed Bash command.
Instead, Codex records the feedback, replaces the tool result with that
feedback, and continues the model from the hook-provided message.

You can also use exit code `2` and write the feedback reason to `stderr`.

To stop normal processing of the original tool result after the command has
already run, return `continue: false`. Codex will replace the tool result with
your feedback or stop text and continue from there.

`updatedMCPToolOutput` and `suppressOutput` are parsed but not supported yet.
Codex marks the hook run as failed, reports the error, and continues normal
processing of the tool result.

### PreCompact

`PreCompact` runs before Codex compacts the conversation. `matcher` is applied
to `trigger`, whose values are `manual` and `auto`.

Fields in addition to [Common input fields](#common-input-fields):

| Field | Type | Meaning |
| --- | --- | --- |
| `turn_id` | `string` | Codex-specific extension. Active Codex turn id |
| `trigger` | `string` | What triggered compaction: `manual` or `auto` |

Plain text on `stdout` is ignored.

JSON on `stdout` supports [Common output fields](#common-output-fields). If a
matching `PreCompact` hook returns `continue: false`, Codex stops before
compacting.

### PostCompact

`PostCompact` runs after Codex compacts the conversation. `matcher` is applied
to `trigger`, whose values are `manual` and `auto`.

Fields in addition to [Common input fields](#common-input-fields):

| Field | Type | Meaning |
| --- | --- | --- |
| `turn_id` | `string` | Codex-specific extension. Active Codex turn id |
| `trigger` | `string` | What triggered compaction: `manual` or `auto` |

Plain text on `stdout` is ignored.

JSON on `stdout` supports [Common output fields](#common-output-fields). If a
matching `PostCompact` hook returns `continue: false`, Codex stops after
compacting.

### UserPromptSubmit

`matcher` isn’t currently used for this event.

Fields in addition to [Common input fields](#common-input-fields):

| Field | Type | Meaning |
| --- | --- | --- |
| `turn_id` | `string` | Codex-specific extension. Active Codex turn id |
| `prompt` | `string` | User prompt that’s about to be sent |

Plain text on `stdout` is added as extra developer context.

JSON on `stdout` supports [Common output fields](#common-output-fields) and
this hook-specific shape:

```
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Ask for a clearer reproduction before editing files."
  }
}
```

That `additionalContext` text is added as extra developer context.

To block the prompt, return:

```
{
  "decision": "block",
  "reason": "Ask for confirmation before doing that."
}
```

You can also use exit code `2` and write the blocking reason to `stderr`.

### SubagentStop

`matcher` is applied to `agent_type` for this event.

Fields in addition to [Common input fields](#common-input-fields):

| Field | Type | Meaning |
| --- | --- | --- |
| `turn_id` | `string` | Codex-specific extension. Active Codex turn id |
| `agent_id` | `string` | Identifier for the subagent |
| `agent_type` | `string` | Subagent type or profile |
| `agent_transcript_path` | `string | null` | Path to the subagent transcript file, if any |
| `stop_hook_active` | `boolean` | Whether this subagent was already continued |
| `last_assistant_message` | `string | null` | Latest subagent assistant message, if available |

`SubagentStop` expects JSON on `stdout` when it exits `0`. Plain text output is
invalid for this event.

JSON on `stdout` supports [Common output fields](#common-output-fields). To ask
Codex to continue the subagent flow, return:

```
{
  "decision": "block",
  "reason": "Run one more focused pass inside the subagent."
}
```

You can also use exit code `2` and write the continuation reason to `stderr`.

If any matching `SubagentStop` hook returns `continue: false`, that takes
precedence over continuation decisions from other matching `SubagentStop`
hooks.

### Stop

`matcher` isn’t currently used for this event.

Fields in addition to [Common input fields](#common-input-fields):

| Field | Type | Meaning |
| --- | --- | --- |
| `turn_id` | `string` | Codex-specific extension. Active Codex turn id |
| `stop_hook_active` | `boolean` | Whether this turn was already continued by `Stop` |
| `last_assistant_message` | `string | null` | Latest assistant message text, if available |

`Stop` expects JSON on `stdout` when it exits `0`. Plain text output is invalid
for this event.

JSON on `stdout` supports [Common output fields](#common-output-fields). To keep
Codex going, return:

```
{
  "decision": "block",
  "reason": "Run one more pass over the failing tests."
}
```

You can also use exit code `2` and write the continuation reason to `stderr`.

For this event, `decision: "block"` doesn’t reject the turn. Instead, it tells
Codex to continue and automatically creates a new continuation prompt that acts
as a new user prompt, using your `reason` as that prompt text.

If any matching `Stop` hook returns `continue: false`, that takes precedence
over continuation decisions from other matching `Stop` hooks.

## Schemas

The linked `main` branch schemas may include hook fields that are not in the
current release. Use this page as the release behavior reference.

If you need the exact current wire format, see the generated schemas in the
[Codex GitHub repository](https://github.com/openai/codex/tree/main/codex-rs/hooks/schema/generated).

