# Security

Source: https://developers.openai.com/codex/security

Codex helps protect your code and data and reduces the risk of misuse.

By default, the agent runs with network access turned off. Locally, Codex uses an OS-enforced sandbox that limits what it can touch (typically to the current workspace), plus an approval policy that controls when it must stop and ask you before acting.

## Sandbox and approvals

Codex security controls come from two layers that work together:

- **Sandbox mode**: What Codex can do technically (for example, where it can write and whether it can reach the network) when it executes model-generated commands.
- **Approval policy**: When Codex must ask you before it executes an action (for example, leaving the sandbox, using the network, or running commands outside a trusted set).

Codex uses different sandbox modes depending on where you run it:

- **Codex cloud**: Runs in isolated OpenAI-managed containers, preventing access to your host system or unrelated data. You can expand access intentionally (for example, to install dependencies or allow specific domains) when needed. Network access is always enabled during the setup phase, which runs before the agent has access to your code.
- **Codex CLI / IDE extension**: OS-level mechanisms enforce sandbox policies. Defaults include no network access and write permissions limited to the active workspace. You can configure the sandbox, approval policy, and network settings based on your risk tolerance.

In the `Auto` preset (for example, `--full-auto`), Codex can read files, make edits, and run commands in the working directory automatically.

Codex asks for approval to edit files outside the workspace or to run commands that require network access. If you want to chat or plan without making changes, switch to `read-only` mode with the `/permissions` command.

Codex can also elicit approval for app (connector) tool calls that advertise side effects, even when the action isn’t a shell command or file change.

## Network access [Elevated Risk](https://help.openai.com/articles/20001061)

For Codex cloud, see [agent internet access](/codex/cloud/internet-access) to enable full internet access or a domain allow list.

For the Codex app, CLI, or IDE Extension, the default `workspace-write` sandbox mode keeps network access turned off unless you enable it in your configuration:

```
[sandbox_workspace_write]
network_access = true
```

You can also control the [web search tool](https://platform.openai.com/docs/guides/tools-web-search) without granting full network access to spawned commands. Codex defaults to using a web search cache to access results. The cache is an OpenAI-maintained index of web results, so cached mode returns pre-indexed results instead of fetching live pages. This reduces exposure to prompt injection from arbitrary live content, but you should still treat web results as untrusted. If you are using `--yolo` or another [full access sandbox setting](#common-sandbox-and-approval-combinations), web search defaults to live results. Use `--search` or set `web_search = "live"` to allow live browsing, or set it to `"disabled"` to turn the tool off:

```
web_search = "cached"  # default
# web_search = "disabled"
# web_search = "live"  # same as --search
```

Use caution when enabling network access or web search in Codex. Prompt injection can cause the agent to fetch and follow untrusted instructions.

## Defaults and recommendations

- On launch, Codex detects whether the folder is version-controlled and recommends:
  - Version-controlled folders: `Auto` (workspace write + on-request approvals)
  - Non-version-controlled folders: `read-only`
- Depending on your setup, Codex may also start in `read-only` until you explicitly trust the working directory (for example, via an onboarding prompt or `/permissions`).
- The workspace includes the current directory and temporary directories like `/tmp`. Use the `/status` command to see which directories are in the workspace.
- To accept the defaults, run `codex`.
- You can set these explicitly:
  - `codex --sandbox workspace-write --ask-for-approval on-request`
  - `codex --sandbox read-only --ask-for-approval on-request`

### Protected paths in writable roots

In the default `workspace-write` sandbox policy, writable roots still include protected paths:

- `<writable_root>/.git` is protected as read-only whether it appears as a directory or file.
- If `<writable_root>/.git` is a pointer file (`gitdir: ...`), the resolved Git directory path is also protected as read-only.
- `<writable_root>/.agents` is protected as read-only when it exists as a directory.
- `<writable_root>/.codex` is protected as read-only when it exists as a directory.
- Protection is recursive, so everything under those paths is read-only.

### Run without approval prompts

You can disable approval prompts with `--ask-for-approval never` or `-a never` (shorthand).

This option works with all `--sandbox` modes, so you still control Codex’s level of autonomy. Codex makes a best effort within the constraints you set.

If you need Codex to read files, make edits, and run commands with network access without approval prompts, use `--sandbox danger-full-access` (or the `--dangerously-bypass-approvals-and-sandbox` flag). Use caution before doing so.

### Common sandbox and approval combinations

| Intent | Flags | Effect |
| --- | --- | --- |
| Auto (preset) | *no flags needed* or `--full-auto` | Codex can read files, make edits, and run commands in the workspace. Codex requires approval to edit outside the workspace or to access network. |
| Safe read-only browsing | `--sandbox read-only --ask-for-approval on-request` | Codex can read files and answer questions. Codex requires approval to make edits, run commands, or access network. |
| Read-only non-interactive (CI) | `--sandbox read-only --ask-for-approval never` | Codex can only read files; never asks for approval. |
| Automatically edit but ask for approval to run untrusted commands | `--sandbox workspace-write --ask-for-approval untrusted` | Codex can read and edit files but asks for approval before running untrusted commands. |
| Dangerous full access | `--dangerously-bypass-approvals-and-sandbox` (alias: `--yolo`) | [Elevated Risk](https://help.openai.com/articles/20001061) No sandbox; no approvals *(not recommended)* |

`--full-auto` is a convenience alias for `--sandbox workspace-write --ask-for-approval on-request`.

With `--ask-for-approval untrusted`, Codex runs only known-safe read operations automatically. Commands that can mutate state or trigger external execution paths (for example, destructive Git operations or Git output/config-override flags) require approval.

#### Configuration in `config.toml`

For the broader configuration workflow, see [Config basics](/codex/config-basic), [Advanced Config](/codex/config-advanced#approval-policies-and-sandbox-modes), and the [Configuration Reference](/codex/config-reference).

```
# Always ask for approval mode
approval_policy = "untrusted"
sandbox_mode    = "read-only"

# Optional: Allow network in workspace-write mode
[sandbox_workspace_write]
network_access = true
```

You can also save presets as profiles, then select them with `codex --profile <name>`:

```
[profiles.full_auto]
approval_policy = "on-request"
sandbox_mode    = "workspace-write"

[profiles.readonly_quiet]
approval_policy = "never"
sandbox_mode    = "read-only"
```

### Test the sandbox locally

To see what happens when a command runs under the Codex sandbox, use these Codex CLI commands:

```
# macOS
codex sandbox macos [--full-auto] [--log-denials] [COMMAND]...
# Linux
codex sandbox linux [--full-auto] [COMMAND]...
```

The `sandbox` command is also available as `codex debug`, and the platform helpers have aliases (for example `codex sandbox seatbelt` and `codex sandbox landlock`).

## OS-level sandbox

Codex enforces the sandbox differently depending on your OS:

- **macOS** uses Seatbelt policies and runs commands using `sandbox-exec` with a profile (`-p`) that corresponds to the `--sandbox` mode you selected.
- **Linux** uses `Landlock` plus `seccomp` by default. You can opt into the alternative Linux sandbox pipeline with `features.use_linux_sandbox_bwrap = true` (or `-c use_linux_sandbox_bwrap=true`).
- **Windows** uses the Linux sandbox implementation when running in [Windows Subsystem for Linux (WSL)](/codex/windows#windows-subsystem-for-linux). When running natively on Windows, you can enable an [experimental sandbox](/codex/windows#windows-experimental-sandbox) implementation.

If you use the Codex IDE extension on Windows, it supports WSL directly. Set the following in your VS Code settings to keep the agent inside WSL whenever it’s available:

```
{
  "chatgpt.runCodexInWindowsSubsystemForLinux": true
}
```

This ensures the IDE extension inherits Linux sandbox semantics for commands, approvals, and filesystem access even when the host OS is Windows. Learn more in the [Windows setup guide](/codex/windows).

The native Windows sandbox is experimental and has important limitations. For example, it can’t prevent writes in directories where the `Everyone` SID already has write permissions (for example, world-writable folders). See the [Windows setup guide](/codex/windows#windows-experimental-sandbox) for details and mitigation steps.

When you run Linux in a containerized environment such as Docker, the sandbox may not work if the host or container configuration doesn’t support the required `Landlock` and `seccomp` features.

In that case, configure your Docker container to provide the isolation you need, then run `codex` with `--sandbox danger-full-access` (or the `--dangerously-bypass-approvals-and-sandbox` flag) inside the container.

## Version control

Codex works best with a version control workflow:

- Work on a feature branch and keep `git status` clean before delegating. This keeps Codex patches easier to isolate and revert.
- Prefer patch-based workflows (for example, `git diff`/`git apply`) over editing tracked files directly. Commit frequently so you can roll back in small increments.
- Treat Codex suggestions like any other PR: run targeted verification, review diffs, and document decisions in commit messages for auditing.

## Monitoring and telemetry

Codex supports opt-in monitoring via OpenTelemetry (OTel) to help teams audit usage, investigate issues, and meet compliance requirements without weakening local security defaults. Telemetry is off by default; enable it explicitly in your configuration.

### Overview

- Codex turns off OTel export by default to keep local runs self-contained.
- When enabled, Codex emits structured log events covering conversations, API requests, SSE/WebSocket stream activity, user prompts (redacted by default), tool approval decisions, and tool results.
- Codex tags exported events with `service.name` (originator), CLI version, and an environment label to separate dev/staging/prod traffic.

### Enable OTel (opt-in)

Add an `[otel]` block to your Codex configuration (typically `~/.codex/config.toml`), choosing an exporter and whether to log prompt text.

```
[otel]
environment = "staging"   # dev | staging | prod
exporter = "none"          # none | otlp-http | otlp-grpc
log_user_prompt = false     # redact prompt text unless policy allows
```

- `exporter = "none"` leaves instrumentation active but doesn’t send data anywhere.
- To send events to your own collector, pick one of:

```
[otel]
exporter = { otlp-http = {
  endpoint = "https://otel.example.com/v1/logs",
  protocol = "binary",
  headers = { "x-otlp-api-key" = "${OTLP_TOKEN}" }
}}
```

```
[otel]
exporter = { otlp-grpc = {
  endpoint = "https://otel.example.com:4317",
  headers = { "x-otlp-meta" = "abc123" }
}}
```

Codex batches events and flushes them on shutdown. Codex exports only telemetry produced by its OTel module.

### Event categories

Representative event types include:

- `codex.conversation_starts` (model, reasoning settings, sandbox/approval policy)
- `codex.api_request` (attempt, status/success, duration, and error details)
- `codex.sse_event` (stream event kind, success/failure, duration, plus token counts on `response.completed`)
- `codex.websocket_request` and `codex.websocket_event` (request duration plus per-message kind/success/error)
- `codex.user_prompt` (length; content redacted unless explicitly enabled)
- `codex.tool_decision` (approved/denied, source: configuration vs. user)
- `codex.tool_result` (duration, success, output snippet)

Associated OTel metrics (counter plus duration histogram pairs) include `codex.api_request`, `codex.sse_event`, `codex.websocket.request`, `codex.websocket.event`, and `codex.tool.call` (with corresponding `.duration_ms` instruments).

For the full event catalog and configuration reference, see the [Codex configuration documentation on GitHub](https://github.com/openai/codex/blob/main/docs/config.md#otel).

### Security and privacy guidance

- Keep `log_user_prompt = false` unless policy explicitly permits storing prompt contents. Prompts can include source code and sensitive data.
- Route telemetry only to collectors you control; apply retention limits and access controls aligned with your compliance requirements.
- Treat tool arguments and outputs as sensitive. Favor redaction at the collector or SIEM when possible.
- Review local data retention settings (for example, `history.persistence` / `history.max_bytes`) if you don’t want Codex to save session transcripts under `CODEX_HOME`. See [Advanced Config](/codex/config-advanced#history-persistence) and [Configuration Reference](/codex/config-reference).
- If you run the CLI with network access turned off, OTel export can’t reach your collector. To export, allow network access in `workspace-write` mode for the OTel endpoint, or export from Codex cloud with the collector domain on your approved list.
- Review events periodically for approval/sandbox changes and unexpected tool executions.

OTel is optional and designed to complement, not replace, the sandbox and approval protections described above.

## Managed configuration

Enterprise admins can control local Codex behavior in two ways. For the exact key list, see the [`requirements.toml` section in Configuration Reference](/codex/config-reference#requirementstoml):

- **Requirements**: admin-enforced constraints that users can’t override.
- **Managed defaults**: starting values applied when Codex launches. Users can still change settings during a session; Codex reapplies managed defaults the next time it starts.

### Admin-enforced requirements (requirements.toml)

Requirements constrain security-sensitive settings (approval policy, sandbox mode, web search mode, and optionally which MCP servers you can enable). If a user explicitly selects a disallowed value (via `config.toml`, CLI flags, profiles, or in-session UI), Codex rejects the change. If a value isn’t explicitly set and the default conflicts with requirements, Codex falls back to a requirements-compliant default. If you configure an `mcp_servers` approved list, Codex enables an MCP server only when both its name and identity match an approved entry; otherwise, Codex turns it off.

#### Locations

- Linux/macOS (Unix): `/etc/codex/requirements.toml`
- macOS MDM: preference domain `com.openai.codex`, key `requirements_toml_base64`

#### Cloud requirements (Business and Enterprise)

When you sign in with ChatGPT on a Business or Enterprise plan, Codex can also
fetch admin-enforced requirements from the Codex service. This applies across
Codex surfaces, including the TUI, `codex exec`, and `codex app-server`.

Cloud requirements are currently best-effort. If the fetch fails or times out,
Codex continues without the cloud layer.

Requirements layer in this order (higher wins):

- macOS managed preferences (MDM; highest precedence)
- Cloud requirements (ChatGPT Business or Enterprise)
- `/etc/codex/requirements.toml`

Cloud requirements only fill unset requirement fields, so higher-precedence
managed layers still win when both specify the same constraint.

For backwards compatibility, Codex also interprets legacy `managed_config.toml` fields `approval_policy` and `sandbox_mode` as requirements (allowing only that single value).

#### Example requirements.toml

This example blocks `--ask-for-approval never` and `--sandbox danger-full-access` (including `--yolo`):

```
allowed_approval_policies = ["untrusted", "on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

You can also constrain web search mode:

```
allowed_web_search_modes = ["cached"] # "disabled" remains implicitly allowed
```

`allowed_web_search_modes = []` effectively allows only `"disabled"`.
For example, `allowed_web_search_modes = ["cached"]` prevents live web search even in `danger-full-access` sessions.

#### Enforce command rules from requirements

Admins can also enforce restrictive command rules from `requirements.toml`
using a `[rules]` table. These rules merge with regular `.rules` files, and the
most restrictive decision still wins.

Unlike `.rules`, requirements rules must specify `decision`, and that decision
must be `"prompt"` or `"forbidden"` (not `"allow"`).

```
[rules]
prefix_rules = [
  { pattern = [{ token = "rm" }], decision = "forbidden", justification = "Use git clean -fd instead." },
  { pattern = [{ token = "git" }, { any_of = ["push", "commit"] }], decision = "prompt", justification = "Require review before mutating history." },
]
```

To restrict which MCP servers Codex can enable, add an `mcp_servers` approved list. For stdio servers, match on `command`; for streamable HTTP servers, match on `url`:

```
[mcp_servers.docs]
identity = { command = "codex-mcp" }

[mcp_servers.remote]
identity = { url = "https://example.com/mcp" }
```

If `mcp_servers` is present but empty, Codex disables all MCP servers.

### Managed defaults (managed\_config.toml)

Managed defaults merge on top of a user’s local `config.toml` and take precedence over any CLI `--config` overrides, setting the starting values when Codex launches. Users can still change those settings during a session; Codex reapplies managed defaults the next time it starts.

Make sure your managed defaults meet your requirements; Codex rejects disallowed values.

#### Precedence and layering

Codex assembles the effective configuration in this order (top overrides bottom):

- Managed preferences (macOS MDM; highest precedence)
- `managed_config.toml` (system/managed file)
- `config.toml` (user’s base configuration)

CLI `--config key=value` overrides apply to the base, but managed layers override them. This means each run starts from the managed defaults even if you provide local flags.

Cloud requirements affect the requirements layer (not managed defaults). See
[Admin-enforced requirements](/codex/security#admin-enforced-requirements-requirementstoml)
for their precedence.

#### Locations

- Linux/macOS (Unix): `/etc/codex/managed_config.toml`
- Windows/non-Unix: `~/.codex/managed_config.toml`

If the file is missing, Codex skips the managed layer.

#### macOS managed preferences (MDM)

On macOS, admins can push a device profile that provides base64-encoded TOML payloads at:

- Preference domain: `com.openai.codex`
- Keys:
  - `config_toml_base64` (managed defaults)
  - `requirements_toml_base64` (requirements)

Codex parses these “managed preferences” payloads as TOML and applies them with the highest precedence.

### MDM setup workflow

Codex honors standard macOS MDM payloads, so you can distribute settings with tooling like `Jamf Pro`, `Fleet`, or `Kandji`. A lightweight deployment looks like:

1. Build the managed payload TOML and encode it with `base64` (no wrapping).
2. Drop the string into your MDM profile under the `com.openai.codex` domain at `config_toml_base64` (managed defaults) or `requirements_toml_base64` (requirements).
3. Push the profile, then ask users to restart Codex and confirm the startup config summary reflects the managed values.
4. When revoking or changing policy, update the managed payload; the CLI reads the refreshed preference the next time it launches.

Avoid embedding secrets or high-churn dynamic values in the payload. Treat the managed TOML like any other MDM setting under change control.

### Example managed\_config.toml

```
# Set conservative defaults
approval_policy = "on-request"
sandbox_mode    = "workspace-write"

[sandbox_workspace_write]
network_access = false             # keep network disabled unless explicitly allowed

[otel]
environment = "prod"
exporter = "otlp-http"            # point at your collector
log_user_prompt = false            # keep prompts redacted
# exporter details live under exporter tables; see Monitoring and telemetry above
```

### Recommended guardrails

- Prefer `workspace-write` with approvals for most users; reserve full access for controlled containers.
- Keep `network_access = false` unless your security review allows a collector or domains required by your workflows.
- Use managed configuration to pin OTel settings (exporter, environment), but keep `log_user_prompt = false` unless your policy explicitly allows storing prompt contents.
- Periodically audit diffs between local `config.toml` and managed policy to catch drift; managed layers should win over local flags and files.

