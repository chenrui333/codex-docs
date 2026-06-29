---
source_type: 'developers'
source_area: 'codex_cli_docs'
source_url: 'https://developers.openai.com/codex/cli/reference'
source_last_modified: '2026-06-18T18:36:15Z'
source_etag: 'W/"83a603cdecc95497b4dc3c16e5de02f7"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4"]
---

# Command line options – Codex CLI | OpenAI Developers

Source: https://developers.openai.com/codex/cli/reference

## How to read this reference

This page catalogs every documented Codex CLI command and flag. Use the interactive tables to search by key or description. Each section indicates whether the option is stable or experimental and calls out risky combinations.

The CLI inherits most defaults from `~/.codex/config.toml`. Any
`-c key=value` overrides you pass at the command line take
precedence for that invocation. See [Config
basics](/codex/config-basic#configuration-precedence) for more information.

## Global flags

| Key | Type / Values | Details |
| --- | --- | --- |
| `--add-dir` | `path` | Grant additional directories write access alongside the main workspace. Repeat for multiple paths. |
| `--ask-for-approval, -a` | `untrusted | on-request | never` | Control when Codex pauses for human approval before running a command. `on-failure` is deprecated; prefer `on-request` for interactive runs or `never` for non-interactive runs. |
| `--cd, -C` | `path` | Set the working directory for the agent before it starts processing your request. |
| `--config, -c` | `key=value` | Override configuration values. Values parse as TOML if possible; otherwise the literal string is used. |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | `boolean` | Run every command without approvals or sandboxing. Only use inside an externally hardened environment. |
| `--dangerously-bypass-hook-trust` | `boolean` | Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources. |
| `--disable` | `feature` | Force-disable a feature flag (translates to `-c features.<name>=false`). Repeatable. |
| `--enable` | `feature` | Force-enable a feature flag (translates to `-c features.<name>=true`). Repeatable. |
| `--image, -i` | `path[,path...]` | Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag. |
| `--model, -m` | `string` | Override the model set in configuration (for example `gpt-5.4`). |
| `--no-alt-screen` | `boolean` | Disable alternate screen mode for the TUI (overrides `tui.alternate_screen` for this run). |
| `--oss` | `boolean` | Use the local open source model provider (equivalent to `-c model_provider="oss"`). Validates that Ollama is running. |
| `--profile, -p` | `string` | Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config. |
| `--remote` | `ws://host:port | wss://host:port | unix:// | unix://PATH` | Connect to a remote app-server endpoint over WebSocket or a Unix socket. Supported for `codex`, `codex resume`, `codex fork`, `codex archive`, `codex delete`, and `codex unarchive`; other subcommands reject remote mode. |
| `--remote-auth-token-env` | `ENV_VAR` | Read a bearer token from this environment variable and send it when connecting with `--remote`. Requires `--remote`; tokens are only sent over `wss://` URLs or local-only `ws://` URLs. |
| `--sandbox, -s` | `read-only | workspace-write | danger-full-access` | Select the sandbox policy for model-generated shell commands. |
| `--search` | `boolean` | Enable live web search (sets `web_search = "live"` instead of the default `"cached"`). |
| `--strict-config` | `boolean` | Error when `config.toml` contains fields this Codex version does not recognize. Supported by runtime commands such as `codex`, `exec`, `review`, `resume`, `fork`, `app-server`, `mcp-server`, and `exec-server`. |
| `PROMPT` | `string` | Optional text instruction to start the session. Omit to launch the TUI without a pre-filled message. |

Key

`--add-dir`

Type / Values

`path`

Details

Grant additional directories write access alongside the main workspace. Repeat for multiple paths.

Key

`--ask-for-approval, -a`

Type / Values

`untrusted | on-request | never`

Details

Control when Codex pauses for human approval before running a command. `on-failure` is deprecated; prefer `on-request` for interactive runs or `never` for non-interactive runs.

Key

`--cd, -C`

Type / Values

`path`

Details

Set the working directory for the agent before it starts processing your request.

Key

`--config, -c`

Type / Values

`key=value`

Details

Override configuration values. Values parse as TOML if possible; otherwise the literal string is used.

Key

`--dangerously-bypass-approvals-and-sandbox, --yolo`

Type / Values

`boolean`

Details

Run every command without approvals or sandboxing. Only use inside an externally hardened environment.

Key

`--dangerously-bypass-hook-trust`

Type / Values

`boolean`

Details

Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources.

Key

`--disable`

Type / Values

`feature`

Details

Force-disable a feature flag (translates to `-c features.<name>=false`). Repeatable.

Key

`--enable`

Type / Values

`feature`

Details

Force-enable a feature flag (translates to `-c features.<name>=true`). Repeatable.

Key

`--image, -i`

Type / Values

`path[,path...]`

Details

Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag.

Key

`--model, -m`

Type / Values

`string`

Details

Override the model set in configuration (for example `gpt-5.4`).

Key

`--no-alt-screen`

Type / Values

`boolean`

Details

Disable alternate screen mode for the TUI (overrides `tui.alternate_screen` for this run).

Key

`--oss`

Type / Values

`boolean`

Details

Use the local open source model provider (equivalent to `-c model_provider="oss"`). Validates that Ollama is running.

Key

`--profile, -p`

Type / Values

`string`

Details

Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config.

Key

`--remote`

Type / Values

`ws://host:port | wss://host:port | unix:// | unix://PATH`

Details

Connect to a remote app-server endpoint over WebSocket or a Unix socket. Supported for `codex`, `codex resume`, `codex fork`, `codex archive`, `codex delete`, and `codex unarchive`; other subcommands reject remote mode.

Key

`--remote-auth-token-env`

Type / Values

`ENV_VAR`

Details

Read a bearer token from this environment variable and send it when connecting with `--remote`. Requires `--remote`; tokens are only sent over `wss://` URLs or local-only `ws://` URLs.

Key

`--sandbox, -s`

Type / Values

`read-only | workspace-write | danger-full-access`

Details

Select the sandbox policy for model-generated shell commands.

Key

`--search`

Type / Values

`boolean`

Details

Enable live web search (sets `web_search = "live"` instead of the default `"cached"`).

Key

`--strict-config`

Type / Values

`boolean`

Details

Error when `config.toml` contains fields this Codex version does not recognize. Supported by runtime commands such as `codex`, `exec`, `review`, `resume`, `fork`, `app-server`, `mcp-server`, and `exec-server`.

Key

`PROMPT`

Type / Values

`string`

Details

Optional text instruction to start the session. Omit to launch the TUI without a pre-filled message.

Expand to view all

These options apply to the base `codex` command. Most propagate to commands;
see the notes above or the relevant command help for exceptions. For propagated
flags, follow the relevant command help. For example, `codex exec --oss ...`
applies `--oss` to `exec`.

## Command overview

The Maturity column uses feature maturity labels such as Experimental, Beta,
and Stable. See [Feature Maturity](/codex/feature-maturity) for how to
interpret these labels.

| Key | Maturity | Details |
| --- | --- | --- |
| [`codex`](/codex/cli/reference#codex-interactive) | Stable | Launch the terminal UI. Accepts the global flags above plus an optional prompt or image attachments. |
| [`codex app`](/codex/cli/reference#codex-app) | Stable | Launch the Codex desktop app on macOS or Windows. On macOS, Codex can open a workspace path; on Windows, Codex prints the path to open. |
| [`codex app-server`](/codex/cli/reference#codex-app-server) | Experimental | Launch the Codex app server for local development or debugging over stdio, WebSocket, or a Unix socket. |
| [`codex apply`](/codex/cli/reference#codex-apply) | Stable | Apply the latest diff generated by a Codex Cloud task to your local working tree. Alias: `codex a`. |
| [`codex archive`](/codex/cli/reference#codex-archive-and-codex-unarchive) | Stable | Archive a saved interactive session by session ID or session name. |
| [`codex cloud`](/codex/cli/reference#codex-cloud) | Experimental | Browse or execute Codex Cloud tasks from the terminal without opening the TUI. Alias: `codex cloud-tasks`. |
| [`codex completion`](/codex/cli/reference#codex-completion) | Stable | Generate shell completion scripts for Bash, Zsh, Fish, or PowerShell. |
| [`codex debug app-server send-message-v2`](/codex/cli/reference#codex-debug-app-server-send-message-v2) | Experimental | Debug app-server by sending a single V2 message through the built-in test client. |
| [`codex debug models`](/codex/cli/reference#codex-debug-models) | Experimental | Print the raw model catalog Codex sees, including an option to inspect only the bundled catalog. |
| [`codex delete`](/codex/cli/reference#codex-delete) | Stable | Permanently delete a saved interactive session by session ID or session name. |
| [`codex doctor`](/codex/cli/reference#codex-doctor) | Stable | Generate a diagnostic report for local installation, config, auth, runtime, Git, terminal, app-server, and thread inventory issues. |
| [`codex exec`](/codex/cli/reference#codex-exec) | Stable | Run Codex non-interactively. Alias: `codex e`. Stream results to stdout or JSONL and optionally resume previous sessions. |
| [`codex execpolicy`](/codex/cli/reference#codex-execpolicy) | Experimental | Evaluate execpolicy rule files and see whether a command would be allowed, prompted, or blocked. |
| [`codex features`](/codex/cli/reference#codex-features) | Stable | List feature flags and persistently enable or disable them in `config.toml`. |
| [`codex fork`](/codex/cli/reference#codex-fork) | Stable | Fork a previous interactive session into a new thread, preserving the original transcript. |
| [`codex login`](/codex/cli/reference#codex-login) | Stable | Authenticate Codex using ChatGPT OAuth, device auth, an API key, or an access token piped over stdin. |
| [`codex logout`](/codex/cli/reference#codex-logout) | Stable | Remove stored authentication credentials. |
| [`codex mcp`](/codex/cli/reference#codex-mcp) | Experimental | Manage Model Context Protocol servers (list, add, remove, authenticate). |
| [`codex mcp-server`](/codex/cli/reference#codex-mcp-server) | Experimental | Run Codex itself as an MCP server over stdio. Useful when another agent consumes Codex. |
| [`codex plugin`](/codex/cli/reference#codex-plugin) | Experimental | Install, list, and remove plugins from configured marketplace sources. |
| [`codex plugin marketplace`](/codex/cli/reference#codex-plugin-marketplace) | Experimental | Add, list, upgrade, or remove plugin marketplaces from Git or local sources. |
| [`codex remote-control`](/codex/cli/reference#codex-remote-control) | Experimental | Ensure the local app-server daemon is running with remote-control support enabled. |
| [`codex resume`](/codex/cli/reference#codex-resume) | Stable | Continue a previous interactive session by ID or resume the most recent conversation. |
| [`codex sandbox`](/codex/cli/reference#codex-sandbox) | Experimental | Run arbitrary commands inside Codex-provided macOS, Linux, or Windows sandboxes. |
| [`codex unarchive`](/codex/cli/reference#codex-archive-and-codex-unarchive) | Stable | Restore an archived interactive session by session ID or session name. |
| [`codex update`](/codex/cli/reference#codex-update) | Stable | Check for and apply a Codex CLI update when the installed release supports self-update. |

Key

[`codex`](/codex/cli/reference#codex-interactive)

Maturity

Stable

Details

Launch the terminal UI. Accepts the global flags above plus an optional prompt or image attachments.

Key

[`codex app`](/codex/cli/reference#codex-app)

Maturity

Stable

Details

Launch the Codex desktop app on macOS or Windows. On macOS, Codex can open a workspace path; on Windows, Codex prints the path to open.

Key

[`codex app-server`](/codex/cli/reference#codex-app-server)

Maturity

Experimental

Details

Launch the Codex app server for local development or debugging over stdio, WebSocket, or a Unix socket.

Key

[`codex apply`](/codex/cli/reference#codex-apply)

Maturity

Stable

Details

Apply the latest diff generated by a Codex Cloud task to your local working tree. Alias: `codex a`.

Key

[`codex archive`](/codex/cli/reference#codex-archive-and-codex-unarchive)

Maturity

Stable

Details

Archive a saved interactive session by session ID or session name.

Key

[`codex cloud`](/codex/cli/reference#codex-cloud)

Maturity

Experimental

Details

Browse or execute Codex Cloud tasks from the terminal without opening the TUI. Alias: `codex cloud-tasks`.

Key

[`codex completion`](/codex/cli/reference#codex-completion)

Maturity

Stable

Details

Generate shell completion scripts for Bash, Zsh, Fish, or PowerShell.

Key

[`codex debug app-server send-message-v2`](/codex/cli/reference#codex-debug-app-server-send-message-v2)

Maturity

Experimental

Details

Debug app-server by sending a single V2 message through the built-in test client.

Key

[`codex debug models`](/codex/cli/reference#codex-debug-models)

Maturity

Experimental

Details

Print the raw model catalog Codex sees, including an option to inspect only the bundled catalog.

Key

[`codex delete`](/codex/cli/reference#codex-delete)

Maturity

Stable

Details

Permanently delete a saved interactive session by session ID or session name.

Key

[`codex doctor`](/codex/cli/reference#codex-doctor)

Maturity

Stable

Details

Generate a diagnostic report for local installation, config, auth, runtime, Git, terminal, app-server, and thread inventory issues.

Key

[`codex exec`](/codex/cli/reference#codex-exec)

Maturity

Stable

Details

Run Codex non-interactively. Alias: `codex e`. Stream results to stdout or JSONL and optionally resume previous sessions.

Key

[`codex execpolicy`](/codex/cli/reference#codex-execpolicy)

Maturity

Experimental

Details

Evaluate execpolicy rule files and see whether a command would be allowed, prompted, or blocked.

Key

[`codex features`](/codex/cli/reference#codex-features)

Maturity

Stable

Details

List feature flags and persistently enable or disable them in `config.toml`.

Key

[`codex fork`](/codex/cli/reference#codex-fork)

Maturity

Stable

Details

Fork a previous interactive session into a new thread, preserving the original transcript.

Key

[`codex login`](/codex/cli/reference#codex-login)

Maturity

Stable

Details

Authenticate Codex using ChatGPT OAuth, device auth, an API key, or an access token piped over stdin.

Key

[`codex logout`](/codex/cli/reference#codex-logout)

Maturity

Stable

Details

Remove stored authentication credentials.

Key

[`codex mcp`](/codex/cli/reference#codex-mcp)

Maturity

Experimental

Details

Manage Model Context Protocol servers (list, add, remove, authenticate).

Key

[`codex mcp-server`](/codex/cli/reference#codex-mcp-server)

Maturity

Experimental

Details

Run Codex itself as an MCP server over stdio. Useful when another agent consumes Codex.

Key

[`codex plugin`](/codex/cli/reference#codex-plugin)

Maturity

Experimental

Details

Install, list, and remove plugins from configured marketplace sources.

Key

[`codex plugin marketplace`](/codex/cli/reference#codex-plugin-marketplace)

Maturity

Experimental

Details

Add, list, upgrade, or remove plugin marketplaces from Git or local sources.

Key

[`codex remote-control`](/codex/cli/reference#codex-remote-control)

Maturity

Experimental

Details

Ensure the local app-server daemon is running with remote-control support enabled.

Key

[`codex resume`](/codex/cli/reference#codex-resume)

Maturity

Stable

Details

Continue a previous interactive session by ID or resume the most recent conversation.

Key

[`codex sandbox`](/codex/cli/reference#codex-sandbox)

Maturity

Experimental

Details

Run arbitrary commands inside Codex-provided macOS, Linux, or Windows sandboxes.

Key

[`codex unarchive`](/codex/cli/reference#codex-archive-and-codex-unarchive)

Maturity

Stable

Details

Restore an archived interactive session by session ID or session name.

Key

[`codex update`](/codex/cli/reference#codex-update)

Maturity

Stable

Details

Check for and apply a Codex CLI update when the installed release supports self-update.

Expand to view all

## Command details

### `codex` (interactive)

Running `codex` with no subcommand launches the interactive terminal UI (TUI). The agent accepts the global flags above plus image attachments. Web search defaults to cached mode; use `--search` to switch to live browsing. For low-friction local work, use `--sandbox workspace-write --ask-for-approval on-request`.

Use `--remote ws://host:port` or `--remote wss://host:port` to connect the TUI to an app server started with `codex app-server --listen ws://IP:PORT`. For a local Unix socket, use `--remote unix://` for the default socket or `--remote unix://PATH` for an explicit path. Add `--remote-auth-token-env <ENV_VAR>` when the server requires a bearer token for WebSocket authentication.

### `codex app-server`

Launch the Codex app server locally. This is primarily for development and debugging and may change without notice.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--analytics-default-enabled` | `boolean` | Defaults analytics to enabled for first-party app-server clients unless the user opts out in config. |
| `--listen` | `stdio:// | ws://IP:PORT | unix:// | unix://PATH | off` | Transport listener URL. Use `stdio://` for JSONL, `ws://IP:PORT` for a TCP WebSocket endpoint, `unix://` for the default Unix socket, `unix://PATH` for a custom Unix socket, or `off` to disable the local transport. |
| `--stdio` | `boolean` | Use stdio transport. Equivalent to `--listen stdio://` and mutually exclusive with `--listen`. |
| `--ws-audience` | `string` | Expected `aud` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`. |
| `--ws-auth` | `capability-token | signed-bearer-token` | Authentication mode for app-server WebSocket clients. If omitted, WebSocket auth is disabled; non-local listeners warn during startup. |
| `--ws-issuer` | `string` | Expected `iss` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`. |
| `--ws-max-clock-skew-seconds` | `number` | Clock skew allowance when validating signed bearer token `exp` and `nbf` claims. Requires `--ws-auth signed-bearer-token`. |
| `--ws-shared-secret-file` | `absolute path` | File containing the HMAC shared secret used to validate signed JWT bearer tokens. Required with `--ws-auth signed-bearer-token`. |
| `--ws-token-file` | `absolute path` | File containing the shared capability token. Use with `--ws-auth capability-token` unless you provide `--ws-token-sha256` instead. |
| `--ws-token-sha256` | `hexadecimal SHA-256 digest` | Expected SHA-256 digest for capability-token authentication. Use instead of `--ws-token-file` when the client token comes from another source. |

Key

`--analytics-default-enabled`

Type / Values

`boolean`

Details

Defaults analytics to enabled for first-party app-server clients unless the user opts out in config.

Key

`--listen`

Type / Values

`stdio:// | ws://IP:PORT | unix:// | unix://PATH | off`

Details

Transport listener URL. Use `stdio://` for JSONL, `ws://IP:PORT` for a TCP WebSocket endpoint, `unix://` for the default Unix socket, `unix://PATH` for a custom Unix socket, or `off` to disable the local transport.

Key

`--stdio`

Type / Values

`boolean`

Details

Use stdio transport. Equivalent to `--listen stdio://` and mutually exclusive with `--listen`.

Key

`--ws-audience`

Type / Values

`string`

Details

Expected `aud` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`.

Key

`--ws-auth`

Type / Values

`capability-token | signed-bearer-token`

Details

Authentication mode for app-server WebSocket clients. If omitted, WebSocket auth is disabled; non-local listeners warn during startup.

Key

`--ws-issuer`

Type / Values

`string`

Details

Expected `iss` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`.

Key

`--ws-max-clock-skew-seconds`

Type / Values

`number`

Details

Clock skew allowance when validating signed bearer token `exp` and `nbf` claims. Requires `--ws-auth signed-bearer-token`.

Key

`--ws-shared-secret-file`

Type / Values

`absolute path`

Details

File containing the HMAC shared secret used to validate signed JWT bearer tokens. Required with `--ws-auth signed-bearer-token`.

Key

`--ws-token-file`

Type / Values

`absolute path`

Details

File containing the shared capability token. Use with `--ws-auth capability-token` unless you provide `--ws-token-sha256` instead.

Key

`--ws-token-sha256`

Type / Values

`hexadecimal SHA-256 digest`

Details

Expected SHA-256 digest for capability-token authentication. Use instead of `--ws-token-file` when the client token comes from another source.

`codex app-server --listen stdio://` keeps the default JSONL-over-stdio behavior, and `codex app-server --stdio` is an alias for that transport. `--listen ws://IP:PORT` enables WebSocket transport for app-server clients. The server accepts `ws://` listen URLs; use TLS termination or a secure proxy when clients connect with `wss://`. Use `--listen unix://` to accept WebSocket handshakes on Codex’s default Unix socket, or `--listen unix:///absolute/path.sock` to choose a socket path. If you generate schemas for client bindings, add `--experimental` to include gated fields and methods.

### `codex remote-control`

Ensure the app-server daemon is running with remote-control support enabled.
Managed remote-control clients and SSH remote workflows use this command; it’s
not a replacement for `codex app-server --listen` when you are building a local
protocol client.

### `codex app`

Launch Codex Desktop from the terminal on macOS or Windows. On macOS, Codex can open a specific workspace path; on Windows, Codex prints the path to open.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--download-url` | `url` | Advanced override for the Codex desktop installer URL used during install. |
| `PATH` | `path` | Workspace path for Codex Desktop. On macOS, Codex opens this path; on Windows, Codex prints the path. |

Key

`--download-url`

Type / Values

`url`

Details

Advanced override for the Codex desktop installer URL used during install.

Key

`PATH`

Type / Values

`path`

Details

Workspace path for Codex Desktop. On macOS, Codex opens this path; on Windows, Codex prints the path.

`codex app` opens an installed Codex Desktop app, or starts the installer when
the app is missing. On macOS, Codex opens the provided workspace path; on
Windows, it prints the path to open after installation.

### `codex debug app-server send-message-v2`

Send one message through app-server’s V2 thread/turn flow using the built-in app-server test client.

| Key | Type / Values | Details |
| --- | --- | --- |
| `USER_MESSAGE` | `string` | Message text sent to app-server through the built-in V2 test-client flow. |

Key

`USER_MESSAGE`

Type / Values

`string`

Details

Message text sent to app-server through the built-in V2 test-client flow.

This debug flow initializes with `experimentalApi: true`, starts a thread, sends a turn, and streams server notifications. Use it to reproduce and inspect app-server protocol behavior locally.

### `codex debug models`

Print the raw model catalog Codex sees as JSON.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--bundled` | `boolean` | Skip refresh and print only the model catalog bundled with the current Codex binary. |

Key

`--bundled`

Type / Values

`boolean`

Details

Skip refresh and print only the model catalog bundled with the current Codex binary.

Use `--bundled` when you want to inspect only the catalog bundled with the current binary, without refreshing from the remote models endpoint.

### `codex apply`

Apply the most recent diff from a Codex cloud task to your local repository. You must authenticate and have access to the task.

| Key | Type / Values | Details |
| --- | --- | --- |
| `TASK_ID` | `string` | Identifier of the Codex Cloud task whose diff should be applied. |

Key

`TASK_ID`

Type / Values

`string`

Details

Identifier of the Codex Cloud task whose diff should be applied.

Codex prints the patched files and exits non-zero if `git apply` fails (for example, due to conflicts).

### `codex archive` and `codex unarchive`

Archive or restore a saved interactive session by session ID or session name.
Use these commands when you want to clean up the session picker without deleting
the transcript. Session IDs take precedence over session names.

```
codex archive <SESSION>
codex unarchive <SESSION>
```

| Key | Type / Values | Details |
| --- | --- | --- |
| `--remote` | `ws://host:port | wss://host:port | unix:// | unix://PATH` | Connect to a remote app-server endpoint before changing archive state. |
| `--remote-auth-token-env` | `ENV_VAR` | Read a bearer token from this environment variable when `--remote` requires authentication. |
| `SESSION` | `session ID | session name` | Saved session to archive or restore. Session IDs take precedence over session names. |

Key

`--remote`

Type / Values

`ws://host:port | wss://host:port | unix:// | unix://PATH`

Details

Connect to a remote app-server endpoint before changing archive state.

Key

`--remote-auth-token-env`

Type / Values

`ENV_VAR`

Details

Read a bearer token from this environment variable when `--remote` requires authentication.

Key

`SESSION`

Type / Values

`session ID | session name`

Details

Saved session to archive or restore. Session IDs take precedence over session names.

### `codex delete`

Permanently delete a saved interactive session by session ID or session name.
Use this only when you want to remove the transcript instead of hiding it from
active session lists.

```
codex delete <SESSION>
codex delete <SESSION_UUID> --force
```

| Key | Type / Values | Details |
| --- | --- | --- |
| `--force` | `boolean` | Delete without prompting. The session argument must be a UUID; names still require interactive confirmation. |
| `--remote` | `ws://host:port | wss://host:port | unix:// | unix://PATH` | Connect to a remote app-server endpoint before deleting the session. |
| `--remote-auth-token-env` | `ENV_VAR` | Read a bearer token from this environment variable when `--remote` requires authentication. |
| `SESSION` | `session ID | session name` | Saved session to delete. Session IDs take precedence over session names. |

Key

`--force`

Type / Values

`boolean`

Details

Delete without prompting. The session argument must be a UUID; names still require interactive confirmation.

Key

`--remote`

Type / Values

`ws://host:port | wss://host:port | unix:// | unix://PATH`

Details

Connect to a remote app-server endpoint before deleting the session.

Key

`--remote-auth-token-env`

Type / Values

`ENV_VAR`

Details

Read a bearer token from this environment variable when `--remote` requires authentication.

Key

`SESSION`

Type / Values

`session ID | session name`

Details

Saved session to delete. Session IDs take precedence over session names.

Use `--force` only with a session UUID. Named sessions still require
confirmation so Codex doesn’t delete a repeated or ambiguous name without a prompt.

### `codex cloud`

Interact with Codex cloud tasks from the terminal. The default command opens an interactive picker; `codex cloud exec` submits a task directly, and `codex cloud list` returns recent tasks for scripting or quick inspection.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--attempts` | `1-4` | Number of assistant attempts (best-of-N) Codex Cloud should run. |
| `--env` | `ENV_ID` | Target Codex Cloud environment identifier (required). Use `codex cloud` to list options. |
| `QUERY` | `string` | Task prompt. If omitted, Codex prompts interactively for details. |

Key

`--attempts`

Type / Values

`1-4`

Details

Number of assistant attempts (best-of-N) Codex Cloud should run.

Key

`--env`

Type / Values

`ENV_ID`

Details

Target Codex Cloud environment identifier (required). Use `codex cloud` to list options.

Key

`QUERY`

Type / Values

`string`

Details

Task prompt. If omitted, Codex prompts interactively for details.

Authentication follows the same credentials as the main CLI. Codex exits non-zero if the task submission fails.

#### `codex cloud list`

List recent cloud tasks with optional filtering and pagination.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--cursor` | `string` | Pagination cursor returned by a previous request. |
| `--env` | `ENV_ID` | Filter tasks by environment identifier. |
| `--json` | `boolean` | Emit machine-readable JSON instead of plain text. |
| `--limit` | `1-20` | Maximum number of tasks to return. |

Key

`--cursor`

Type / Values

`string`

Details

Pagination cursor returned by a previous request.

Key

`--env`

Type / Values

`ENV_ID`

Details

Filter tasks by environment identifier.

Key

`--json`

Type / Values

`boolean`

Details

Emit machine-readable JSON instead of plain text.

Key

`--limit`

Type / Values

`1-20`

Details

Maximum number of tasks to return.

Plain-text output prints a task URL followed by status details. Use `--json` for automation. The JSON payload contains a `tasks` array plus an optional `cursor` value. Each task includes `id`, `url`, `title`, `status`, `updated_at`, `environment_id`, `environment_label`, `summary`, `is_review`, and `attempt_total`.

### `codex completion`

Generate shell completion scripts and redirect the output to the appropriate location, for example `codex completion zsh > "${fpath[1]}/_codex"`.

| Key | Type / Values | Details |
| --- | --- | --- |
| `SHELL` | `bash | zsh | fish | power-shell | elvish` | Shell to generate completions for. Output prints to stdout. |

Key

`SHELL`

Type / Values

`bash | zsh | fish | power-shell | elvish`

Details

Shell to generate completions for. Output prints to stdout.

### `codex doctor`

Generate a local diagnostic report before filing a support issue or
while investigating a broken Codex installation. The report checks installation,
configuration, authentication, runtime, Git, terminal, app-server, and thread
inventory health.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--all` | `boolean` | Expand long lists in the detailed human-readable report. |
| `--ascii` | `boolean` | Use ASCII status labels and separators in human-readable output. |
| `--json` | `boolean` | Emit a redacted machine-readable support report. |
| `--no-color` | `boolean` | Disable ANSI color in human-readable output. |
| `--summary` | `boolean` | Show grouped check rows and the final count summary only. |

Key

`--all`

Type / Values

`boolean`

Details

Expand long lists in the detailed human-readable report.

Key

`--ascii`

Type / Values

`boolean`

Details

Use ASCII status labels and separators in human-readable output.

Key

`--json`

Type / Values

`boolean`

Details

Emit a redacted machine-readable support report.

Key

`--no-color`

Type / Values

`boolean`

Details

Disable ANSI color in human-readable output.

Key

`--summary`

Type / Values

`boolean`

Details

Show grouped check rows and the final count summary only.

### `codex features`

Manage feature flags stored in `$CODEX_HOME/config.toml`. The `enable` and
`disable` commands persist changes so they apply to future sessions. The
`features` subcommand doesn’t accept `--profile`.

| Key | Type / Values | Details |
| --- | --- | --- |
| `Disable subcommand` | `codex features disable <feature>` | Persistently disable a feature flag in `$CODEX_HOME/config.toml`. |
| `Enable subcommand` | `codex features enable <feature>` | Persistently enable a feature flag in `$CODEX_HOME/config.toml`. |
| `List subcommand` | `codex features list` | Show known feature flags, their maturity stage, and their effective state. |

Key

`Disable subcommand`

Type / Values

`codex features disable <feature>`

Details

Persistently disable a feature flag in `$CODEX_HOME/config.toml`.

Key

`Enable subcommand`

Type / Values

`codex features enable <feature>`

Details

Persistently enable a feature flag in `$CODEX_HOME/config.toml`.

Key

`List subcommand`

Type / Values

`codex features list`

Details

Show known feature flags, their maturity stage, and their effective state.

### `codex exec`

Use `codex exec` (or the short form `codex e`) for scripted or CI-style runs that should finish without human interaction.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--cd, -C` | `path` | Set the workspace root before executing the task. |
| `--color` | `always | never | auto` | Control ANSI color in stdout. |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | `boolean` | Bypass approval prompts and sandboxing. Dangerous—only use inside an isolated runner. |
| `--dangerously-bypass-hook-trust` | `boolean` | Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources. |
| `--ephemeral` | `boolean` | Run without persisting session rollout files to disk. |
| `--full-auto` | `boolean` | Deprecated compatibility flag. Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used. |
| `--ignore-rules` | `boolean` | Do not load user or project execpolicy `.rules` files for this run. |
| `--ignore-user-config` | `boolean` | Do not load `$CODEX_HOME/config.toml`. Authentication still uses `CODEX_HOME`. |
| `--image, -i` | `path[,path...]` | Attach images to the first message. Repeatable; supports comma-separated lists. |
| `--json, --experimental-json` | `boolean` | Print newline-delimited JSON events instead of formatted text. |
| `--model, -m` | `string` | Override the configured model for this run. |
| `--oss` | `boolean` | Use the local open source provider (requires a running Ollama instance). |
| `--output-last-message, -o` | `path` | Write the assistant’s final message to a file. Useful for downstream scripting. |
| `--output-schema` | `path` | JSON Schema file describing the expected final response shape. Codex validates tool output against it. |
| `--profile, -p` | `string` | Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config. |
| `--sandbox, -s` | `read-only | workspace-write | danger-full-access` | Sandbox policy for model-generated commands. Defaults to configuration. |
| `--skip-git-repo-check` | `boolean` | Allow running outside a Git repository (useful for one-off directories). |
| `-c, --config` | `key=value` | Inline configuration override for the non-interactive run (repeatable). |
| `PROMPT` | `string | - (read stdin)` | Initial instruction for the task. Use `-` to pipe the prompt from stdin. |
| `Resume subcommand` | `codex exec resume [SESSION_ID]` | Resume an exec session by ID or add `--last` to continue the most recent session from the current working directory. Add `--all` to consider sessions from any directory. Accepts an optional follow-up prompt. |

Key

`--cd, -C`

Type / Values

`path`

Details

Set the workspace root before executing the task.

Key

`--color`

Type / Values

`always | never | auto`

Details

Control ANSI color in stdout.

Key

`--dangerously-bypass-approvals-and-sandbox, --yolo`

Type / Values

`boolean`

Details

Bypass approval prompts and sandboxing. Dangerous—only use inside an isolated runner.

Key

`--dangerously-bypass-hook-trust`

Type / Values

`boolean`

Details

Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources.

Key

`--ephemeral`

Type / Values

`boolean`

Details

Run without persisting session rollout files to disk.

Key

`--full-auto`

Type / Values

`boolean`

Details

Deprecated compatibility flag. Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used.

Key

`--ignore-rules`

Type / Values

`boolean`

Details

Do not load user or project execpolicy `.rules` files for this run.

Key

`--ignore-user-config`

Type / Values

`boolean`

Details

Do not load `$CODEX_HOME/config.toml`. Authentication still uses `CODEX_HOME`.

Key

`--image, -i`

Type / Values

`path[,path...]`

Details

Attach images to the first message. Repeatable; supports comma-separated lists.

Key

`--json, --experimental-json`

Type / Values

`boolean`

Details

Print newline-delimited JSON events instead of formatted text.

Key

`--model, -m`

Type / Values

`string`

Details

Override the configured model for this run.

Key

`--oss`

Type / Values

`boolean`

Details

Use the local open source provider (requires a running Ollama instance).

Key

`--output-last-message, -o`

Type / Values

`path`

Details

Write the assistant’s final message to a file. Useful for downstream scripting.

Key

`--output-schema`

Type / Values

`path`

Details

JSON Schema file describing the expected final response shape. Codex validates tool output against it.

Key

`--profile, -p`

Type / Values

`string`

Details

Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config.

Key

`--sandbox, -s`

Type / Values

`read-only | workspace-write | danger-full-access`

Details

Sandbox policy for model-generated commands. Defaults to configuration.

Key

`--skip-git-repo-check`

Type / Values

`boolean`

Details

Allow running outside a Git repository (useful for one-off directories).

Key

`-c, --config`

Type / Values

`key=value`

Details

Inline configuration override for the non-interactive run (repeatable).

Key

`PROMPT`

Type / Values

`string | - (read stdin)`

Details

Initial instruction for the task. Use `-` to pipe the prompt from stdin.

Key

`Resume subcommand`

Type / Values

`codex exec resume [SESSION_ID]`

Details

Resume an exec session by ID or add `--last` to continue the most recent session from the current working directory. Add `--all` to consider sessions from any directory. Accepts an optional follow-up prompt.

Expand to view all

Codex writes formatted output by default. Add `--json` to receive newline-delimited JSON events (one per state change). The optional `resume` subcommand lets you continue non-interactive tasks. Use `--last` to pick the most recent session from the current working directory, or add `--all` to search across all sessions:

| Key | Type / Values | Details |
| --- | --- | --- |
| `--all` | `boolean` | Include sessions outside the current working directory when selecting the most recent session. |
| `--image, -i` | `path[,path...]` | Attach one or more images to the follow-up prompt. Separate multiple paths with commas or repeat the flag. |
| `--last` | `boolean` | Resume the most recent conversation from the current working directory. |
| `PROMPT` | `string | - (read stdin)` | Optional follow-up instruction sent immediately after resuming. |
| `SESSION_ID` | `uuid` | Resume the specified session. Omit and use `--last` to continue the most recent session. |

Key

`--all`

Type / Values

`boolean`

Details

Include sessions outside the current working directory when selecting the most recent session.

Key

`--image, -i`

Type / Values

`path[,path...]`

Details

Attach one or more images to the follow-up prompt. Separate multiple paths with commas or repeat the flag.

Key

`--last`

Type / Values

`boolean`

Details

Resume the most recent conversation from the current working directory.

Key

`PROMPT`

Type / Values

`string | - (read stdin)`

Details

Optional follow-up instruction sent immediately after resuming.

Key

`SESSION_ID`

Type / Values

`uuid`

Details

Resume the specified session. Omit and use `--last` to continue the most recent session.

### `codex execpolicy`

Check `execpolicy` rule files before you save them. `codex execpolicy check` accepts one or more `--rules` flags (for example, files under `~/.codex/rules`) and emits JSON showing the strictest decision and any matching rules. Add `--pretty` to format the output. The `execpolicy` command is currently in preview.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--pretty` | `boolean` | Pretty-print the JSON result. |
| `--rules, -r` | `path (repeatable)` | Path to an execpolicy rule file to evaluate. Provide multiple flags to combine rules across files. |
| `COMMAND...` | `var-args` | Command to be checked against the specified policies. |

Key

`--pretty`

Type / Values

`boolean`

Details

Pretty-print the JSON result.

Key

`--rules, -r`

Type / Values

`path (repeatable)`

Details

Path to an execpolicy rule file to evaluate. Provide multiple flags to combine rules across files.

Key

`COMMAND...`

Type / Values

`var-args`

Details

Command to be checked against the specified policies.

### `codex login`

Authenticate the CLI with a ChatGPT account, API key, or access token. With no flags, Codex opens a browser for the ChatGPT OAuth flow.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--device-auth` | `boolean` | Use OAuth device code flow instead of launching a browser window. |
| `--with-access-token` | `boolean` | Read an access token from stdin (for example `printenv CODEX_ACCESS_TOKEN | codex login --with-access-token`). |
| `--with-api-key` | `boolean` | Read an API key from stdin (for example `printenv OPENAI_API_KEY | codex login --with-api-key`). |
| `status subcommand` | `codex login status` | Print the active authentication mode and exit with 0 when logged in. |

Key

`--device-auth`

Type / Values

`boolean`

Details

Use OAuth device code flow instead of launching a browser window.

Key

`--with-access-token`

Type / Values

`boolean`

Details

Read an access token from stdin (for example `printenv CODEX_ACCESS_TOKEN | codex login --with-access-token`).

Key

`--with-api-key`

Type / Values

`boolean`

Details

Read an API key from stdin (for example `printenv OPENAI_API_KEY | codex login --with-api-key`).

Key

`status subcommand`

Type / Values

`codex login status`

Details

Print the active authentication mode and exit with 0 when logged in.

`codex login status` exits with `0` when credentials are present, which is helpful in automation scripts.

### `codex logout`

Remove saved credentials for both API key and ChatGPT authentication. This command has no flags.

### `codex mcp`

Manage Model Context Protocol server entries stored in `~/.codex/config.toml`.

| Key | Type / Values | Details |
| --- | --- | --- |
| `add <name>` | `-- <command...> | --url <value>` | Register a server using a stdio launcher command or a streamable HTTP URL. Supports `--env KEY=VALUE` for stdio transports. |
| `get <name>` | `--json` | Show a specific server configuration. `--json` prints the raw config entry. |
| `list` | `--json` | List configured MCP servers. Add `--json` for machine-readable output. |
| `login <name>` | `--scopes scope1,scope2` | Start an OAuth login for a streamable HTTP server (servers that support OAuth only). |
| `logout <name>` |  | Remove stored OAuth credentials for a streamable HTTP server. |
| `remove <name>` |  | Delete a stored MCP server definition. |

Key

`add <name>`

Type / Values

`-- <command...> | --url <value>`

Details

Register a server using a stdio launcher command or a streamable HTTP URL. Supports `--env KEY=VALUE` for stdio transports.

Key

`get <name>`

Type / Values

`--json`

Details

Show a specific server configuration. `--json` prints the raw config entry.

Key

`list`

Type / Values

`--json`

Details

List configured MCP servers. Add `--json` for machine-readable output.

Key

`login <name>`

Type / Values

`--scopes scope1,scope2`

Details

Start an OAuth login for a streamable HTTP server (servers that support OAuth only).

Key

`logout <name>`

Details

Remove stored OAuth credentials for a streamable HTTP server.

Key

`remove <name>`

Details

Delete a stored MCP server definition.

The `add` subcommand supports both stdio and streamable HTTP transports:

| Key | Type / Values | Details |
| --- | --- | --- |
| `--bearer-token-env-var` | `ENV_VAR` | Environment variable whose value is sent as a bearer token when connecting to a streamable HTTP server. |
| `--env KEY=VALUE` | `repeatable` | Environment variable assignments applied when launching a stdio server. |
| `--oauth-client-id` | `CLIENT_ID` | OAuth client identifier for a streamable HTTP MCP server. Requires `--url`. |
| `--oauth-resource` | `RESOURCE` | OAuth resource parameter to include during login for a streamable HTTP MCP server. Requires `--url`. |
| `--url` | `https://…` | Register a streamable HTTP server instead of stdio. Mutually exclusive with `COMMAND...`. |
| `COMMAND...` | `stdio transport` | Executable plus arguments to launch the MCP server. Provide after `--`. |

Key

`--bearer-token-env-var`

Type / Values

`ENV_VAR`

Details

Environment variable whose value is sent as a bearer token when connecting to a streamable HTTP server.

Key

`--env KEY=VALUE`

Type / Values

`repeatable`

Details

Environment variable assignments applied when launching a stdio server.

Key

`--oauth-client-id`

Type / Values

`CLIENT_ID`

Details

OAuth client identifier for a streamable HTTP MCP server. Requires `--url`.

Key

`--oauth-resource`

Type / Values

`RESOURCE`

Details

OAuth resource parameter to include during login for a streamable HTTP MCP server. Requires `--url`.

Key

`--url`

Type / Values

`https://…`

Details

Register a streamable HTTP server instead of stdio. Mutually exclusive with `COMMAND...`.

Key

`COMMAND...`

Type / Values

`stdio transport`

Details

Executable plus arguments to launch the MCP server. Provide after `--`.

OAuth actions (`login`, `logout`) only work with streamable HTTP servers (and only when the server supports OAuth).

### `codex plugin`

Install, list, and remove plugins from configured marketplaces.

| Key | Type / Values | Details |
| --- | --- | --- |
| `add <plugin[@marketplace]>` | `[--marketplace, -m NAME] [--json]` | Install a plugin from a configured marketplace. Use `--marketplace` or `-m` when the plugin argument omits `@marketplace`. |
| `list` | `[--marketplace, -m NAME] [--available --json] [--json]` | List installed plugins. With `--json`, output has `installed` and `available` arrays; `--available` includes uninstalled marketplace plugins and requires `--json`. |
| `marketplace` |  | Manage configured marketplace sources. See `codex plugin marketplace` below. |
| `remove <plugin[@marketplace]>` | `[--marketplace, -m NAME] [--json]` | Remove an installed plugin from local config and cache. Use `--json` for automation-friendly output. |

Key

`add <plugin[@marketplace]>`

Type / Values

`[--marketplace, -m NAME] [--json]`

Details

Install a plugin from a configured marketplace. Use `--marketplace` or `-m` when the plugin argument omits `@marketplace`.

Key

`list`

Type / Values

`[--marketplace, -m NAME] [--available --json] [--json]`

Details

List installed plugins. With `--json`, output has `installed` and `available` arrays; `--available` includes uninstalled marketplace plugins and requires `--json`.

Key

`marketplace`

Details

Manage configured marketplace sources. See `codex plugin marketplace` below.

Key

`remove <plugin[@marketplace]>`

Type / Values

`[--marketplace, -m NAME] [--json]`

Details

Remove an installed plugin from local config and cache. Use `--json` for automation-friendly output.

`codex plugin add --json` prints `pluginId`, `name`, `marketplaceName`,
`version`, `installedPath`, and `authPolicy`. `codex plugin list --json` prints
`installed` and `available` arrays. Entries include `pluginId`, `name`,
`marketplaceName`, `version`, `installed`, `enabled`, `source`, `installPolicy`,
`authPolicy`, and, when available, `marketplaceSource` with the configured
marketplace source type and value. `codex plugin remove --json` prints
`pluginId`, `name`, and `marketplaceName`.

### `codex plugin marketplace`

Manage plugin marketplace sources that Codex can browse and install from.

| Key | Type / Values | Details |
| --- | --- | --- |
| `add <source>` | `[--ref REF] [--sparse PATH] [--json]` | Install a plugin marketplace from GitHub shorthand, a Git URL, an SSH URL, or a local marketplace root directory. `--sparse` is supported only for Git sources and can be repeated. |
| `list` | `[--json]` | Show plugin marketplaces Codex is currently considering and the root path for each marketplace. |
| `remove <marketplace-name>` | `[--json]` | Remove a configured plugin marketplace. |
| `upgrade [marketplace-name]` | `[--json]` | Refresh one configured Git marketplace, or all configured Git marketplaces when no name is provided. |

Key

`add <source>`

Type / Values

`[--ref REF] [--sparse PATH] [--json]`

Details

Install a plugin marketplace from GitHub shorthand, a Git URL, an SSH URL, or a local marketplace root directory. `--sparse` is supported only for Git sources and can be repeated.

Key

`list`

Type / Values

`[--json]`

Details

Show plugin marketplaces Codex is currently considering and the root path for each marketplace.

Key

`remove <marketplace-name>`

Type / Values

`[--json]`

Details

Remove a configured plugin marketplace.

Key

`upgrade [marketplace-name]`

Type / Values

`[--json]`

Details

Refresh one configured Git marketplace, or all configured Git marketplaces when no name is provided.

`codex plugin marketplace add` accepts GitHub shorthand such as `owner/repo` or
`owner/repo@ref`, HTTP or HTTPS Git URLs, SSH Git URLs, and local marketplace
root directories. Use `--ref` to pin a Git ref, and repeat `--sparse PATH` to
use a sparse checkout for Git-backed marketplace repositories.

`codex plugin marketplace list` prints in-scope marketplace names and roots,
including implicitly discovered default marketplaces and configured marketplace
snapshots.

Add `--json` to marketplace add, list, upgrade, or remove commands for
automation-friendly output. Marketplace add JSON includes `marketplaceName`,
`installedRoot`, and `alreadyAdded`; list JSON includes a `marketplaces` array
with `name`, `root`, and optional `marketplaceSource`; upgrade JSON includes
`selectedMarketplaces`, `upgradedRoots`, and `errors`; remove JSON includes
`marketplaceName` and `installedRoot`.

### `codex mcp-server`

Run Codex as an MCP server over stdio so that other tools can connect. This command inherits global configuration overrides and exits when the downstream client closes the connection.

### `codex resume`

Continue an interactive session by ID or resume the most recent conversation. `codex resume` scopes `--last` to the current working directory unless you pass `--all`. It accepts the same global flags as `codex`, including model and sandbox overrides.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--all` | `boolean` | Include sessions outside the current working directory when selecting the most recent session. |
| `--last` | `boolean` | Skip the picker and resume the most recent conversation from the current working directory. |
| `SESSION_ID` | `uuid` | Resume the specified session. Omit and use `--last` to continue the most recent session. |

Key

`--all`

Type / Values

`boolean`

Details

Include sessions outside the current working directory when selecting the most recent session.

Key

`--last`

Type / Values

`boolean`

Details

Skip the picker and resume the most recent conversation from the current working directory.

Key

`SESSION_ID`

Type / Values

`uuid`

Details

Resume the specified session. Omit and use `--last` to continue the most recent session.

### `codex fork`

Fork a previous interactive session into a new thread. By default, `codex fork` opens the session picker; add `--last` to fork your most recent session instead.

| Key | Type / Values | Details |
| --- | --- | --- |
| `--all` | `boolean` | Show sessions beyond the current working directory in the picker. |
| `--last` | `boolean` | Skip the picker and fork the most recent conversation automatically. |
| `SESSION_ID` | `uuid` | Fork the specified session. Omit and use `--last` to fork the most recent session. |

Key

`--all`

Type / Values

`boolean`

Details

Show sessions beyond the current working directory in the picker.

Key

`--last`

Type / Values

`boolean`

Details

Skip the picker and fork the most recent conversation automatically.

Key

`SESSION_ID`

Type / Values

`uuid`

Details

Fork the specified session. Omit and use `--last` to fork the most recent session.

### `codex sandbox`

Use the sandbox helper to run a command under the same policies Codex uses internally.

#### macOS seatbelt

| Key | Type / Values | Details |
| --- | --- | --- |
| `--allow-unix-socket` | `path` | Allow the sandboxed command to bind or connect Unix sockets rooted at this path. Repeat to allow multiple paths. |
| `--cd, -C` | `DIR` | Working directory used for profile resolution and command execution. Requires `--permissions-profile`. |
| `--config, -c` | `key=value` | Pass configuration overrides into the sandboxed run (repeatable). |
| `--include-managed-config` | `boolean` | Include managed requirements while resolving an explicit permissions profile. Requires `--permissions-profile`. |
| `--log-denials` | `boolean` | Capture macOS sandbox denials with `log stream` while the command runs and print them after exit. |
| `--permissions-profile, -P` | `NAME` | Apply a named permissions profile from the active configuration stack. |
| `--profile, -p` | `NAME` | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `COMMAND...` | `var-args` | Shell command to execute under macOS Seatbelt. Everything after `--` is forwarded. |

Key

`--allow-unix-socket`

Type / Values

`path`

Details

Allow the sandboxed command to bind or connect Unix sockets rooted at this path. Repeat to allow multiple paths.

Key

`--cd, -C`

Type / Values

`DIR`

Details

Working directory used for profile resolution and command execution. Requires `--permissions-profile`.

Key

`--config, -c`

Type / Values

`key=value`

Details

Pass configuration overrides into the sandboxed run (repeatable).

Key

`--include-managed-config`

Type / Values

`boolean`

Details

Include managed requirements while resolving an explicit permissions profile. Requires `--permissions-profile`.

Key

`--log-denials`

Type / Values

`boolean`

Details

Capture macOS sandbox denials with `log stream` while the command runs and print them after exit.

Key

`--permissions-profile, -P`

Type / Values

`NAME`

Details

Apply a named permissions profile from the active configuration stack.

Key

`--profile, -p`

Type / Values

`NAME`

Details

Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config.

Key

`COMMAND...`

Type / Values

`var-args`

Details

Shell command to execute under macOS Seatbelt. Everything after `--` is forwarded.

#### Linux Landlock

| Key | Type / Values | Details |
| --- | --- | --- |
| `--cd, -C` | `DIR` | Working directory used for profile resolution and command execution. Requires `--permissions-profile`. |
| `--config, -c` | `key=value` | Configuration overrides applied before launching the sandbox (repeatable). |
| `--include-managed-config` | `boolean` | Include managed requirements while resolving an explicit permissions profile. Requires `--permissions-profile`. |
| `--permissions-profile, -P` | `NAME` | Apply a named permissions profile from the active configuration stack. |
| `--profile, -p` | `NAME` | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `COMMAND...` | `var-args` | Command to execute under Landlock + seccomp. Provide the executable after `--`. |

Key

`--cd, -C`

Type / Values

`DIR`

Details

Working directory used for profile resolution and command execution. Requires `--permissions-profile`.

Key

`--config, -c`

Type / Values

`key=value`

Details

Configuration overrides applied before launching the sandbox (repeatable).

Key

`--include-managed-config`

Type / Values

`boolean`

Details

Include managed requirements while resolving an explicit permissions profile. Requires `--permissions-profile`.

Key

`--permissions-profile, -P`

Type / Values

`NAME`

Details

Apply a named permissions profile from the active configuration stack.

Key

`--profile, -p`

Type / Values

`NAME`

Details

Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config.

Key

`COMMAND...`

Type / Values

`var-args`

Details

Command to execute under Landlock + seccomp. Provide the executable after `--`.

#### Windows

| Key | Type / Values | Details |
| --- | --- | --- |
| `--cd, -C` | `DIR` | Working directory used for profile resolution and command execution. Requires `--permissions-profile`. |
| `--config, -c` | `key=value` | Configuration overrides applied before launching the sandbox (repeatable). |
| `--include-managed-config` | `boolean` | Include managed requirements while resolving an explicit permissions profile. Requires `--permissions-profile`. |
| `--permissions-profile, -P` | `NAME` | Apply a named permissions profile from the active configuration stack. |
| `--profile, -p` | `NAME` | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `COMMAND...` | `var-args` | Command to execute under the native Windows sandbox. Provide the executable after `--`. |

Key

`--cd, -C`

Type / Values

`DIR`

Details

Working directory used for profile resolution and command execution. Requires `--permissions-profile`.

Key

`--config, -c`

Type / Values

`key=value`

Details

Configuration overrides applied before launching the sandbox (repeatable).

Key

`--include-managed-config`

Type / Values

`boolean`

Details

Include managed requirements while resolving an explicit permissions profile. Requires `--permissions-profile`.

Key

`--permissions-profile, -P`

Type / Values

`NAME`

Details

Apply a named permissions profile from the active configuration stack.

Key

`--profile, -p`

Type / Values

`NAME`

Details

Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config.

Key

`COMMAND...`

Type / Values

`var-args`

Details

Command to execute under the native Windows sandbox. Provide the executable after `--`.

### `codex update`

Check for and apply a Codex CLI update when the installed release supports self-update. Debug builds print a message telling you to install a release build instead.

## Flag combinations and safety tips

- Use `--sandbox workspace-write` for unattended local work that can stay inside the workspace, and avoid `--dangerously-bypass-approvals-and-sandbox` unless you are inside a dedicated sandbox VM.
- When you need to grant Codex write access to more directories, prefer `--add-dir` rather than forcing `--sandbox danger-full-access`.
- Pair `--json` with `--output-last-message` in CI to capture machine-readable progress and a final natural-language summary.

## Related resources

- [Codex CLI overview](/codex/cli): installation, upgrades, and quick tips.
- [Config basics](/codex/config-basic): persist defaults like the model and provider.
- [Advanced Config](/codex/config-advanced): profiles, providers, sandbox tuning, and integrations.
- [AGENTS.md](/codex/guides/agents-md): conceptual overview of Codex agent capabilities and best practices.

