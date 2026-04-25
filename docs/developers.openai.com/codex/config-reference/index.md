---
source_type: 'developers'
source_url: 'https://developers.openai.com/codex/config-reference'
source_last_modified: '2026-04-25T06:28:27Z'
source_etag: 'W/"ffb92c54ab25499934ee4cce8f8b3a8b"'
codex_cli_versions: ["0.125.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0"]
---

# Configuration Reference – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/config-reference

Use this page as a searchable reference for Codex configuration files. For conceptual guidance and examples, start with [Config basics](/codex/config-basic) and [Advanced Config](/codex/config-advanced).

## `config.toml`

User-level configuration lives in `~/.codex/config.toml`. You can also add project-scoped overrides in `.codex/config.toml` files. Codex loads project-scoped config files only when you trust the project.

For sandbox and approval keys (`approval_policy`, `sandbox_mode`, and `sandbox_workspace_write.*`), pair this reference with [Sandbox and approvals](/codex/agent-approvals-security#sandbox-and-approvals), [Protected paths in writable roots](/codex/agent-approvals-security#protected-paths-in-writable-roots), and [Network access](/codex/agent-approvals-security#network-access).

| Key | Type / Values | Details |
| --- | --- | --- |
| `agents.<name>.config_file` | `string (path)` | Path to a TOML config layer for that role; relative paths resolve from the config file that declares the role. |
| `agents.<name>.description` | `string` | Role guidance shown to Codex when choosing and spawning that agent type. |
| `agents.<name>.nickname_candidates` | `array<string>` | Optional pool of display nicknames for spawned agents in that role. |
| `agents.job_max_runtime_seconds` | `number` | Default per-worker timeout for `spawn_agents_on_csv` jobs. When unset, the tool falls back to 1800 seconds per worker. |
| `agents.max_depth` | `number` | Maximum nesting depth allowed for spawned agent threads (root sessions start at depth 0; default: 1). |
| `agents.max_threads` | `number` | Maximum number of agent threads that can be open concurrently. Defaults to `6` when unset. |
| `allow_login_shell` | `boolean` | Allow shell-based tools to use login-shell semantics. Defaults to `true`; when `false`, `login = true` requests are rejected and omitted `login` defaults to non-login shells. |
| `analytics.enabled` | `boolean` | Enable or disable analytics for this machine/profile. When unset, the client default applies. |
| `approval_policy` | `untrusted | on-request | never | { granular = { sandbox_approval = bool, rules = bool, mcp_elicitations = bool, request_permissions = bool, skill_approval = bool } }` | Controls when Codex pauses for approval before executing commands. You can also use `approval_policy = { granular = { ... } }` to allow or auto-reject specific prompt categories while keeping other prompts interactive. `on-failure` is deprecated; use `on-request` for interactive runs or `never` for non-interactive runs. |
| `approval_policy.granular.mcp_elicitations` | `boolean` | When `true`, MCP elicitation prompts are allowed to surface instead of being auto-rejected. |
| `approval_policy.granular.request_permissions` | `boolean` | When `true`, prompts from the `request_permissions` tool are allowed to surface. |
| `approval_policy.granular.rules` | `boolean` | When `true`, approvals triggered by execpolicy `prompt` rules are allowed to surface. |
| `approval_policy.granular.sandbox_approval` | `boolean` | When `true`, sandbox escalation approval prompts are allowed to surface. |
| `approval_policy.granular.skill_approval` | `boolean` | When `true`, skill-script approval prompts are allowed to surface. |
| `approvals_reviewer` | `user | auto_review` | Who reviews eligible approval prompts under `on-request` or granular approval policies. Defaults to `user`; `auto_review` uses the reviewer subagent. This setting doesn't change sandboxing or review actions already allowed inside the sandbox. |
| `apps._default.destructive_enabled` | `boolean` | Default allow/deny for app tools with `destructive_hint = true`. |
| `apps._default.enabled` | `boolean` | Default app enabled state for all apps unless overridden per app. |
| `apps._default.open_world_enabled` | `boolean` | Default allow/deny for app tools with `open_world_hint = true`. |
| `apps.<id>.default_tools_approval_mode` | `auto | prompt | approve` | Default approval behavior for tools in this app unless a per-tool override exists. |
| `apps.<id>.default_tools_enabled` | `boolean` | Default enabled state for tools in this app unless a per-tool override exists. |
| `apps.<id>.destructive_enabled` | `boolean` | Allow or block tools in this app that advertise `destructive_hint = true`. |
| `apps.<id>.enabled` | `boolean` | Enable or disable a specific app/connector by id (default: true). |
| `apps.<id>.open_world_enabled` | `boolean` | Allow or block tools in this app that advertise `open_world_hint = true`. |
| `apps.<id>.tools.<tool>.approval_mode` | `auto | prompt | approve` | Per-tool approval behavior override for a single app tool. |
| `apps.<id>.tools.<tool>.enabled` | `boolean` | Per-tool enabled override for an app tool (for example `repos/list`). |
| `auto_review.policy` | `string` | Local Markdown policy instructions for automatic review. Managed `guardian_policy_config` takes precedence. Blank values are ignored. |
| `background_terminal_max_timeout` | `number` | Maximum poll window in milliseconds for empty `write_stdin` polls (background terminal polling). Default: `300000` (5 minutes). Replaces the older `background_terminal_timeout` key. |
| `chatgpt_base_url` | `string` | Override the base URL used during the ChatGPT login flow. |
| `check_for_update_on_startup` | `boolean` | Check for Codex updates on startup (set to false only when updates are centrally managed). |
| `cli_auth_credentials_store` | `file | keyring | auto` | Control where the CLI stores cached credentials (file-based auth.json vs OS keychain). |
| `commit_attribution` | `string` | Override the commit co-author trailer text. Set an empty string to disable automatic attribution. |
| `compact_prompt` | `string` | Inline override for the history compaction prompt. |
| `default_permissions` | `string` | Name of the default permissions profile to apply to sandboxed tool calls. |
| `developer_instructions` | `string` | Additional developer instructions injected into the session (optional). |
| `disable_paste_burst` | `boolean` | Disable burst-paste detection in the TUI. |
| `experimental_compact_prompt_file` | `string (path)` | Load the compaction prompt override from a file (experimental). |
| `experimental_use_unified_exec_tool` | `boolean` | Legacy name for enabling unified exec; prefer `[features].unified_exec` or `codex --enable unified_exec`. |
| `features.apps` | `boolean` | Enable ChatGPT Apps/connectors support (experimental). |
| `features.codex_hooks` | `boolean` | Enable lifecycle hooks loaded from `hooks.json` or inline `[hooks]` config. |
| `features.enable_request_compression` | `boolean` | Compress streaming request bodies with zstd when supported (stable; on by default). |
| `features.fast_mode` | `boolean` | Enable Fast mode selection and the `service_tier = "fast"` path (stable; on by default). |
| `features.memories` | `boolean` | Enable [Memories](/codex/memories) (off by default). |
| `features.multi_agent` | `boolean` | Enable multi-agent collaboration tools (`spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, and `close_agent`) (stable; on by default). |
| `features.personality` | `boolean` | Enable personality selection controls (stable; on by default). |
| `features.prevent_idle_sleep` | `boolean` | Prevent the machine from sleeping while a turn is actively running (experimental; off by default). |
| `features.shell_snapshot` | `boolean` | Snapshot shell environment to speed up repeated commands (stable; on by default). |
| `features.shell_tool` | `boolean` | Enable the default `shell` tool for running commands (stable; on by default). |
| `features.skill_mcp_dependency_install` | `boolean` | Allow prompting and installing missing MCP dependencies for skills (stable; on by default). |
| `features.undo` | `boolean` | Enable undo support (stable; off by default). |
| `features.unified_exec` | `boolean` | Use the unified PTY-backed exec tool (stable; enabled by default except on Windows). |
| `features.web_search` | `boolean` | Deprecated legacy toggle; prefer the top-level `web_search` setting. |
| `features.web_search_cached` | `boolean` | Deprecated legacy toggle. When `web_search` is unset, true maps to `web_search = "cached"`. |
| `features.web_search_request` | `boolean` | Deprecated legacy toggle. When `web_search` is unset, true maps to `web_search = "live"`. |
| `feedback.enabled` | `boolean` | Enable feedback submission via `/feedback` across Codex surfaces (default: true). |
| `file_opener` | `vscode | vscode-insiders | windsurf | cursor | none` | URI scheme used to open citations from Codex output (default: `vscode`). |
| `forced_chatgpt_workspace_id` | `string (uuid)` | Limit ChatGPT logins to a specific workspace identifier. |
| `forced_login_method` | `chatgpt | api` | Restrict Codex to a specific authentication method. |
| `hide_agent_reasoning` | `boolean` | Suppress reasoning events in both the TUI and `codex exec` output. |
| `history.max_bytes` | `number` | If set, caps the history file size in bytes by dropping oldest entries. |
| `history.persistence` | `save-all | none` | Control whether Codex saves session transcripts to history.jsonl. |
| `hooks` | `table` | Lifecycle hooks configured inline in `config.toml`. Uses the same event schema as `hooks.json`; see the Hooks guide for examples and supported events. |
| `instructions` | `string` | Reserved for future use; prefer `model_instructions_file` or `AGENTS.md`. |
| `log_dir` | `string (path)` | Directory where Codex writes log files (for example `codex-tui.log`); defaults to `$CODEX_HOME/log`. |
| `mcp_oauth_callback_port` | `integer` | Optional fixed port for the local HTTP callback server used during MCP OAuth login. When unset, Codex binds to an ephemeral port chosen by the OS. |
| `mcp_oauth_callback_url` | `string` | Optional redirect URI override for MCP OAuth login (for example, a devbox ingress URL). `mcp_oauth_callback_port` still controls the callback listener port. |
| `mcp_oauth_credentials_store` | `auto | file | keyring` | Preferred store for MCP OAuth credentials. |
| `mcp_servers.<id>.args` | `array<string>` | Arguments passed to the MCP stdio server command. |
| `mcp_servers.<id>.bearer_token_env_var` | `string` | Environment variable sourcing the bearer token for an MCP HTTP server. |
| `mcp_servers.<id>.command` | `string` | Launcher command for an MCP stdio server. |
| `mcp_servers.<id>.cwd` | `string` | Working directory for the MCP stdio server process. |
| `mcp_servers.<id>.disabled_tools` | `array<string>` | Deny list applied after `enabled_tools` for the MCP server. |
| `mcp_servers.<id>.enabled` | `boolean` | Disable an MCP server without removing its configuration. |
| `mcp_servers.<id>.enabled_tools` | `array<string>` | Allow list of tool names exposed by the MCP server. |
| `mcp_servers.<id>.env` | `map<string,string>` | Environment variables forwarded to the MCP stdio server. |
| `mcp_servers.<id>.env_http_headers` | `map<string,string>` | HTTP headers populated from environment variables for an MCP HTTP server. |
| `mcp_servers.<id>.env_vars` | `array<string | { name = string, source = "local" | "remote" }>` | Additional environment variables to whitelist for an MCP stdio server. String entries default to `source = "local"`; use `source = "remote"` only with executor-backed remote stdio. |
| `mcp_servers.<id>.experimental_environment` | `local | remote` | Experimental placement for an MCP server. `remote` starts stdio servers through a remote executor environment; streamable HTTP remote placement is not implemented. |
| `mcp_servers.<id>.http_headers` | `map<string,string>` | Static HTTP headers included with each MCP HTTP request. |
| `mcp_servers.<id>.oauth_resource` | `string` | Optional RFC 8707 OAuth resource parameter to include during MCP login. |
| `mcp_servers.<id>.required` | `boolean` | When true, fail startup/resume if this enabled MCP server cannot initialize. |
| `mcp_servers.<id>.scopes` | `array<string>` | OAuth scopes to request when authenticating to that MCP server. |
| `mcp_servers.<id>.startup_timeout_ms` | `number` | Alias for `startup_timeout_sec` in milliseconds. |
| `mcp_servers.<id>.startup_timeout_sec` | `number` | Override the default 10s startup timeout for an MCP server. |
| `mcp_servers.<id>.tool_timeout_sec` | `number` | Override the default 60s per-tool timeout for an MCP server. |
| `mcp_servers.<id>.url` | `string` | Endpoint for an MCP streamable HTTP server. |
| `memories.consolidation_model` | `string` | Optional model override for global memory consolidation. |
| `memories.disable_on_external_context` | `boolean` | When `true`, threads that use external context such as MCP tool calls, web search, or tool search are kept out of memory generation. Defaults to `false`. Legacy alias: `memories.no_memories_if_mcp_or_web_search`. |
| `memories.extract_model` | `string` | Optional model override for per-thread memory extraction. |
| `memories.generate_memories` | `boolean` | When `false`, newly created threads are not stored as memory-generation inputs. Defaults to `true`. |
| `memories.max_raw_memories_for_consolidation` | `number` | Maximum recent raw memories retained for global consolidation. Defaults to `256` and is capped at `4096`. |
| `memories.max_rollout_age_days` | `number` | Maximum age of threads considered for memory generation. Defaults to `30` and is clamped to `0`-`90`. |
| `memories.max_rollouts_per_startup` | `number` | Maximum rollout candidates processed per startup pass. Defaults to `16` and is capped at `128`. |
| `memories.max_unused_days` | `number` | Maximum days since a memory was last used before it becomes ineligible for consolidation. Defaults to `30` and is clamped to `0`-`365`. |
| `memories.min_rollout_idle_hours` | `number` | Minimum idle time before a thread is considered for memory generation. Defaults to `6` and is clamped to `1`-`48`. |
| `memories.use_memories` | `boolean` | When `false`, Codex skips injecting existing memories into future sessions. Defaults to `true`. |
| `model` | `string` | Model to use (e.g., `gpt-5.5`). |
| `model_auto_compact_token_limit` | `number` | Token threshold that triggers automatic history compaction (unset uses model defaults). |
| `model_catalog_json` | `string (path)` | Optional path to a JSON model catalog loaded on startup. Profile-level `profiles.<name>.model_catalog_json` can override this per profile. |
| `model_context_window` | `number` | Context window tokens available to the active model. |
| `model_instructions_file` | `string (path)` | Replacement for built-in instructions instead of `AGENTS.md`. |
| `model_provider` | `string` | Provider id from `model_providers` (default: `openai`). |
| `model_providers.<id>` | `table` | Custom provider definition. Built-in provider IDs (`openai`, `ollama`, and `lmstudio`) are reserved and cannot be overridden. |
| `model_providers.<id>.auth` | `table` | Command-backed bearer token configuration for a custom provider. Do not combine with `env_key`, `experimental_bearer_token`, or `requires_openai_auth`. |
| `model_providers.<id>.auth.args` | `array<string>` | Arguments passed to the token command. |
| `model_providers.<id>.auth.command` | `string` | Command to run when Codex needs a bearer token. The command must print the token to stdout. |
| `model_providers.<id>.auth.cwd` | `string (path)` | Working directory for the token command. |
| `model_providers.<id>.auth.refresh_interval_ms` | `number` | How often Codex proactively refreshes the token in milliseconds (default: 300000). Set to `0` to refresh only after an authentication retry. |
| `model_providers.<id>.auth.timeout_ms` | `number` | Maximum token command runtime in milliseconds (default: 5000). |
| `model_providers.<id>.base_url` | `string` | API base URL for the model provider. |
| `model_providers.<id>.env_http_headers` | `map<string,string>` | HTTP headers populated from environment variables when present. |
| `model_providers.<id>.env_key` | `string` | Environment variable supplying the provider API key. |
| `model_providers.<id>.env_key_instructions` | `string` | Optional setup guidance for the provider API key. |
| `model_providers.<id>.experimental_bearer_token` | `string` | Direct bearer token for the provider (discouraged; use `env_key`). |
| `model_providers.<id>.http_headers` | `map<string,string>` | Static HTTP headers added to provider requests. |
| `model_providers.<id>.name` | `string` | Display name for a custom model provider. |
| `model_providers.<id>.query_params` | `map<string,string>` | Extra query parameters appended to provider requests. |
| `model_providers.<id>.request_max_retries` | `number` | Retry count for HTTP requests to the provider (default: 4). |
| `model_providers.<id>.requires_openai_auth` | `boolean` | The provider uses OpenAI authentication (defaults to false). |
| `model_providers.<id>.stream_idle_timeout_ms` | `number` | Idle timeout for SSE streams in milliseconds (default: 300000). |
| `model_providers.<id>.stream_max_retries` | `number` | Retry count for SSE streaming interruptions (default: 5). |
| `model_providers.<id>.supports_websockets` | `boolean` | Whether that provider supports the Responses API WebSocket transport. |
| `model_providers.<id>.wire_api` | `responses` | Protocol used by the provider. `responses` is the only supported value, and it is the default when omitted. |
| `model_reasoning_effort` | `minimal | low | medium | high | xhigh` | Adjust reasoning effort for supported models (Responses API only; `xhigh` is model-dependent). |
| `model_reasoning_summary` | `auto | concise | detailed | none` | Select reasoning summary detail or disable summaries entirely. |
| `model_supports_reasoning_summaries` | `boolean` | Force Codex to send or not send reasoning metadata. |
| `model_verbosity` | `low | medium | high` | Optional GPT-5 Responses API verbosity override; when unset, the selected model/preset default is used. |
| `notice.hide_full_access_warning` | `boolean` | Track acknowledgement of the full access warning prompt. |
| `notice.hide_gpt-5.1-codex-max_migration_prompt` | `boolean` | Track acknowledgement of the gpt-5.1-codex-max migration prompt. |
| `notice.hide_gpt5_1_migration_prompt` | `boolean` | Track acknowledgement of the GPT-5.1 migration prompt. |
| `notice.hide_rate_limit_model_nudge` | `boolean` | Track opt-out of the rate limit model switch reminder. |
| `notice.hide_world_writable_warning` | `boolean` | Track acknowledgement of the Windows world-writable directories warning. |
| `notice.model_migrations` | `map<string,string>` | Track acknowledged model migrations as old->new mappings. |
| `notify` | `array<string>` | Command invoked for notifications; receives a JSON payload from Codex. |
| `openai_base_url` | `string` | Base URL override for the built-in `openai` model provider. |
| `oss_provider` | `lmstudio | ollama` | Default local provider used when running with `--oss` (defaults to prompting if unset). |
| `otel.environment` | `string` | Environment tag applied to emitted OpenTelemetry events (default: `dev`). |
| `otel.exporter` | `none | otlp-http | otlp-grpc` | Select the OpenTelemetry exporter and provide any endpoint metadata. |
| `otel.exporter.<id>.endpoint` | `string` | Exporter endpoint for OTEL logs. |
| `otel.exporter.<id>.headers` | `map<string,string>` | Static headers included with OTEL exporter requests. |
| `otel.exporter.<id>.protocol` | `binary | json` | Protocol used by the OTLP/HTTP exporter. |
| `otel.exporter.<id>.tls.ca-certificate` | `string` | CA certificate path for OTEL exporter TLS. |
| `otel.exporter.<id>.tls.client-certificate` | `string` | Client certificate path for OTEL exporter TLS. |
| `otel.exporter.<id>.tls.client-private-key` | `string` | Client private key path for OTEL exporter TLS. |
| `otel.log_user_prompt` | `boolean` | Opt in to exporting raw user prompts with OpenTelemetry logs. |
| `otel.metrics_exporter` | `none | statsig | otlp-http | otlp-grpc` | Select the OpenTelemetry metrics exporter (defaults to `statsig`). |
| `otel.trace_exporter` | `none | otlp-http | otlp-grpc` | Select the OpenTelemetry trace exporter and provide any endpoint metadata. |
| `otel.trace_exporter.<id>.endpoint` | `string` | Trace exporter endpoint for OTEL logs. |
| `otel.trace_exporter.<id>.headers` | `map<string,string>` | Static headers included with OTEL trace exporter requests. |
| `otel.trace_exporter.<id>.protocol` | `binary | json` | Protocol used by the OTLP/HTTP trace exporter. |
| `otel.trace_exporter.<id>.tls.ca-certificate` | `string` | CA certificate path for OTEL trace exporter TLS. |
| `otel.trace_exporter.<id>.tls.client-certificate` | `string` | Client certificate path for OTEL trace exporter TLS. |
| `otel.trace_exporter.<id>.tls.client-private-key` | `string` | Client private key path for OTEL trace exporter TLS. |
| `permissions.<name>.filesystem` | `table` | Named filesystem permission profile. Each key is an absolute path or special token such as `:minimal` or `:project_roots`. |
| `permissions.<name>.filesystem.":project_roots".<subpath-or-glob>` | `"read" | "write" | "none"` | Scoped filesystem access relative to the detected project roots. Use `"."` for the root itself; glob subpaths such as `"**/*.env"` can deny reads with `"none"`. |
| `permissions.<name>.filesystem.<path-or-glob>` | `"read" | "write" | "none" | table` | Grant direct access for a path, glob pattern, or special token, or scope nested entries under that root. Use `"none"` to deny reads for matching paths. |
| `permissions.<name>.filesystem.glob_scan_max_depth` | `number` | Maximum depth for expanding deny-read glob patterns on platforms that snapshot matches before sandbox startup. Must be at least `1` when set. |
| `permissions.<name>.network.allow_local_binding` | `boolean` | Permit local bind/listen operations through the managed proxy. |
| `permissions.<name>.network.allow_upstream_proxy` | `boolean` | Allow the managed proxy to chain to another upstream proxy. |
| `permissions.<name>.network.dangerously_allow_all_unix_sockets` | `boolean` | Allow the proxy to use arbitrary Unix sockets instead of the default restricted set. |
| `permissions.<name>.network.dangerously_allow_non_loopback_proxy` | `boolean` | Permit non-loopback bind addresses for the managed proxy listener. |
| `permissions.<name>.network.domains` | `map<string, allow | deny>` | Domain rules for the managed proxy. Use domain names or wildcard patterns as keys, with `allow` or `deny` values. |
| `permissions.<name>.network.enable_socks5` | `boolean` | Expose a SOCKS5 listener when this permissions profile enables the managed network proxy. |
| `permissions.<name>.network.enable_socks5_udp` | `boolean` | Allow UDP over the SOCKS5 listener when enabled. |
| `permissions.<name>.network.enabled` | `boolean` | Enable network access for this named permissions profile. |
| `permissions.<name>.network.mode` | `limited | full` | Network proxy mode used for subprocess traffic. |
| `permissions.<name>.network.proxy_url` | `string` | HTTP proxy endpoint used when this permissions profile enables the managed network proxy. |
| `permissions.<name>.network.socks_url` | `string` | SOCKS5 proxy endpoint used by this permissions profile. |
| `permissions.<name>.network.unix_sockets` | `map<string, allow | none>` | Unix socket rules for the managed proxy. Use socket paths as keys, with `allow` or `none` values. |
| `personality` | `none | friendly | pragmatic` | Default communication style for models that advertise `supportsPersonality`; can be overridden per thread/turn or via `/personality`. |
| `plan_mode_reasoning_effort` | `none | minimal | low | medium | high | xhigh` | Plan-mode-specific reasoning override. When unset, Plan mode uses its built-in preset default. |
| `profile` | `string` | Default profile applied at startup (equivalent to `--profile`). |
| `profiles.<name>.*` | `various` | Profile-scoped overrides for any of the supported configuration keys. |
| `profiles.<name>.analytics.enabled` | `boolean` | Profile-scoped analytics enablement override. |
| `profiles.<name>.experimental_use_unified_exec_tool` | `boolean` | Legacy name for enabling unified exec; prefer `[features].unified_exec`. |
| `profiles.<name>.model_catalog_json` | `string (path)` | Profile-scoped model catalog JSON path override (applied on startup only; overrides the top-level `model_catalog_json` for that profile). |
| `profiles.<name>.model_instructions_file` | `string (path)` | Profile-scoped replacement for the built-in instruction file. |
| `profiles.<name>.oss_provider` | `lmstudio | ollama` | Profile-scoped OSS provider for `--oss` sessions. |
| `profiles.<name>.personality` | `none | friendly | pragmatic` | Profile-scoped communication style override for supported models. |
| `profiles.<name>.plan_mode_reasoning_effort` | `none | minimal | low | medium | high | xhigh` | Profile-scoped Plan-mode reasoning override. |
| `profiles.<name>.service_tier` | `flex | fast` | Profile-scoped service tier preference for new turns. |
| `profiles.<name>.tools_view_image` | `boolean` | Enable or disable the `view_image` tool in that profile. |
| `profiles.<name>.web_search` | `disabled | cached | live` | Profile-scoped web search mode override (default: `"cached"`). |
| `profiles.<name>.windows.sandbox` | `unelevated | elevated` | Profile-scoped Windows sandbox mode override. |
| `project_doc_fallback_filenames` | `array<string>` | Additional filenames to try when `AGENTS.md` is missing. |
| `project_doc_max_bytes` | `number` | Maximum bytes read from `AGENTS.md` when building project instructions. |
| `project_root_markers` | `array<string>` | List of project root marker filenames; used when searching parent directories for the project root. |
| `projects.<path>.trust_level` | `string` | Mark a project or worktree as trusted or untrusted (`"trusted"` | `"untrusted"`). Untrusted projects skip project-scoped `.codex/` layers, including project-local config, hooks, and rules. |
| `review_model` | `string` | Optional model override used by `/review` (defaults to the current session model). |
| `sandbox_mode` | `read-only | workspace-write | danger-full-access` | Sandbox policy for filesystem and network access during command execution. |
| `sandbox_workspace_write.exclude_slash_tmp` | `boolean` | Exclude `/tmp` from writable roots in workspace-write mode. |
| `sandbox_workspace_write.exclude_tmpdir_env_var` | `boolean` | Exclude `$TMPDIR` from writable roots in workspace-write mode. |
| `sandbox_workspace_write.network_access` | `boolean` | Allow outbound network access inside the workspace-write sandbox. |
| `sandbox_workspace_write.writable_roots` | `array<string>` | Additional writable roots when `sandbox_mode = "workspace-write"`. |
| `service_tier` | `flex | fast` | Preferred service tier for new turns. |
| `shell_environment_policy.exclude` | `array<string>` | Glob patterns for removing environment variables after the defaults. |
| `shell_environment_policy.experimental_use_profile` | `boolean` | Use the user shell profile when spawning subprocesses. |
| `shell_environment_policy.ignore_default_excludes` | `boolean` | Keep variables containing KEY/SECRET/TOKEN before other filters run. |
| `shell_environment_policy.include_only` | `array<string>` | Whitelist of patterns; when set only matching variables are kept. |
| `shell_environment_policy.inherit` | `all | core | none` | Baseline environment inheritance when spawning subprocesses. |
| `shell_environment_policy.set` | `map<string,string>` | Explicit environment overrides injected into every subprocess. |
| `show_raw_agent_reasoning` | `boolean` | Surface raw reasoning content when the active model emits it. |
| `skills.config` | `array<object>` | Per-skill enablement overrides stored in config.toml. |
| `skills.config.<index>.enabled` | `boolean` | Enable or disable the referenced skill. |
| `skills.config.<index>.path` | `string (path)` | Path to a skill folder containing `SKILL.md`. |
| `sqlite_home` | `string (path)` | Directory where Codex stores the SQLite-backed state DB used by agent jobs and other resumable runtime state. |
| `suppress_unstable_features_warning` | `boolean` | Suppress the warning that appears when under-development feature flags are enabled. |
| `tool_output_token_limit` | `number` | Token budget for storing individual tool/function outputs in history. |
| `tool_suggest.discoverables` | `array<table>` | Allow tool suggestions for additional discoverable connectors or plugins. Each entry uses `type = "connector"` or `"plugin"` and an `id`. |
| `tools.view_image` | `boolean` | Enable the local-image attachment tool `view_image`. |
| `tools.web_search` | `boolean | { context_size = "low|medium|high", allowed_domains = [string], location = { country, region, city, timezone } }` | Optional web search tool configuration. The legacy boolean form is still accepted, but the object form lets you set search context size, allowed domains, and approximate user location. |
| `tui` | `table` | TUI-specific options such as enabling inline desktop notifications. |
| `tui.alternate_screen` | `auto | always | never` | Control alternate screen usage for the TUI (default: auto; auto skips it in Zellij to preserve scrollback). |
| `tui.animations` | `boolean` | Enable terminal animations (welcome screen, shimmer, spinner) (default: true). |
| `tui.model_availability_nux.<model>` | `integer` | Internal startup-tooltip state keyed by model slug. |
| `tui.notification_condition` | `unfocused | always` | Control whether TUI notifications fire only when the terminal is unfocused or regardless of focus. Defaults to `unfocused`. |
| `tui.notification_method` | `auto | osc9 | bel` | Notification method for terminal notifications (default: auto). |
| `tui.notifications` | `boolean | array<string>` | Enable TUI notifications; optionally restrict to specific event types. |
| `tui.show_tooltips` | `boolean` | Show onboarding tooltips in the TUI welcome screen (default: true). |
| `tui.status_line` | `array<string> | null` | Ordered list of TUI footer status-line item identifiers. `null` disables the status line. |
| `tui.terminal_title` | `array<string> | null` | Ordered list of terminal window/tab title item identifiers. Defaults to `["spinner", "project"]`; `null` disables title updates. |
| `tui.theme` | `string` | Syntax-highlighting theme override (kebab-case theme name). |
| `web_search` | `disabled | cached | live` | Web search mode (default: `"cached"`; cached uses an OpenAI-maintained index and does not fetch live pages; if you use `--yolo` or another full access sandbox setting, it defaults to `"live"`). Use `"live"` to fetch the most recent data from the web, or `"disabled"` to remove the tool. |
| `windows_wsl_setup_acknowledged` | `boolean` | Track Windows onboarding acknowledgement (Windows only). |
| `windows.sandbox` | `unelevated | elevated` | Windows-only native sandbox mode when running Codex natively on Windows. |
| `windows.sandbox_private_desktop` | `boolean` | Run the final sandboxed child process on a private desktop by default on native Windows. Set `false` only for compatibility with the older `Winsta0\\Default` behavior. |

Key

`agents.<name>.config_file`

Type / Values

`string (path)`

Details

Path to a TOML config layer for that role; relative paths resolve from the config file that declares the role.

Key

`agents.<name>.description`

Type / Values

`string`

Details

Role guidance shown to Codex when choosing and spawning that agent type.

Key

`agents.<name>.nickname_candidates`

Type / Values

`array<string>`

Details

Optional pool of display nicknames for spawned agents in that role.

Key

`agents.job_max_runtime_seconds`

Type / Values

`number`

Details

Default per-worker timeout for `spawn_agents_on_csv` jobs. When unset, the tool falls back to 1800 seconds per worker.

Key

`agents.max_depth`

Type / Values

`number`

Details

Maximum nesting depth allowed for spawned agent threads (root sessions start at depth 0; default: 1).

Key

`agents.max_threads`

Type / Values

`number`

Details

Maximum number of agent threads that can be open concurrently. Defaults to `6` when unset.

Key

`allow_login_shell`

Type / Values

`boolean`

Details

Allow shell-based tools to use login-shell semantics. Defaults to `true`; when `false`, `login = true` requests are rejected and omitted `login` defaults to non-login shells.

Key

`analytics.enabled`

Type / Values

`boolean`

Details

Enable or disable analytics for this machine/profile. When unset, the client default applies.

Key

`approval_policy`

Type / Values

`untrusted | on-request | never | { granular = { sandbox_approval = bool, rules = bool, mcp_elicitations = bool, request_permissions = bool, skill_approval = bool } }`

Details

Controls when Codex pauses for approval before executing commands. You can also use `approval_policy = { granular = { ... } }` to allow or auto-reject specific prompt categories while keeping other prompts interactive. `on-failure` is deprecated; use `on-request` for interactive runs or `never` for non-interactive runs.

Key

`approval_policy.granular.mcp_elicitations`

Type / Values

`boolean`

Details

When `true`, MCP elicitation prompts are allowed to surface instead of being auto-rejected.

Key

`approval_policy.granular.request_permissions`

Type / Values

`boolean`

Details

When `true`, prompts from the `request_permissions` tool are allowed to surface.

Key

`approval_policy.granular.rules`

Type / Values

`boolean`

Details

When `true`, approvals triggered by execpolicy `prompt` rules are allowed to surface.

Key

`approval_policy.granular.sandbox_approval`

Type / Values

`boolean`

Details

When `true`, sandbox escalation approval prompts are allowed to surface.

Key

`approval_policy.granular.skill_approval`

Type / Values

`boolean`

Details

When `true`, skill-script approval prompts are allowed to surface.

Key

`approvals_reviewer`

Type / Values

`user | auto_review`

Details

Who reviews eligible approval prompts under `on-request` or granular approval policies. Defaults to `user`; `auto_review` uses the reviewer subagent. This setting doesn't change sandboxing or review actions already allowed inside the sandbox.

Key

`apps._default.destructive_enabled`

Type / Values

`boolean`

Details

Default allow/deny for app tools with `destructive_hint = true`.

Key

`apps._default.enabled`

Type / Values

`boolean`

Details

Default app enabled state for all apps unless overridden per app.

Key

`apps._default.open_world_enabled`

Type / Values

`boolean`

Details

Default allow/deny for app tools with `open_world_hint = true`.

Key

`apps.<id>.default_tools_approval_mode`

Type / Values

`auto | prompt | approve`

Details

Default approval behavior for tools in this app unless a per-tool override exists.

Key

`apps.<id>.default_tools_enabled`

Type / Values

`boolean`

Details

Default enabled state for tools in this app unless a per-tool override exists.

Key

`apps.<id>.destructive_enabled`

Type / Values

`boolean`

Details

Allow or block tools in this app that advertise `destructive_hint = true`.

Key

`apps.<id>.enabled`

Type / Values

`boolean`

Details

Enable or disable a specific app/connector by id (default: true).

Key

`apps.<id>.open_world_enabled`

Type / Values

`boolean`

Details

Allow or block tools in this app that advertise `open_world_hint = true`.

Key

`apps.<id>.tools.<tool>.approval_mode`

Type / Values

`auto | prompt | approve`

Details

Per-tool approval behavior override for a single app tool.

Key

`apps.<id>.tools.<tool>.enabled`

Type / Values

`boolean`

Details

Per-tool enabled override for an app tool (for example `repos/list`).

Key

`auto_review.policy`

Type / Values

`string`

Details

Local Markdown policy instructions for automatic review. Managed `guardian_policy_config` takes precedence. Blank values are ignored.

Key

`background_terminal_max_timeout`

Type / Values

`number`

Details

Maximum poll window in milliseconds for empty `write_stdin` polls (background terminal polling). Default: `300000` (5 minutes). Replaces the older `background_terminal_timeout` key.

Key

`chatgpt_base_url`

Type / Values

`string`

Details

Override the base URL used during the ChatGPT login flow.

Key

`check_for_update_on_startup`

Type / Values

`boolean`

Details

Check for Codex updates on startup (set to false only when updates are centrally managed).

Key

`cli_auth_credentials_store`

Type / Values

`file | keyring | auto`

Details

Control where the CLI stores cached credentials (file-based auth.json vs OS keychain).

Key

`commit_attribution`

Type / Values

`string`

Details

Override the commit co-author trailer text. Set an empty string to disable automatic attribution.

Key

`compact_prompt`

Type / Values

`string`

Details

Inline override for the history compaction prompt.

Key

`default_permissions`

Type / Values

`string`

Details

Name of the default permissions profile to apply to sandboxed tool calls.

Key

`developer_instructions`

Type / Values

`string`

Details

Additional developer instructions injected into the session (optional).

Key

`disable_paste_burst`

Type / Values

`boolean`

Details

Disable burst-paste detection in the TUI.

Key

`experimental_compact_prompt_file`

Type / Values

`string (path)`

Details

Load the compaction prompt override from a file (experimental).

Key

`experimental_use_unified_exec_tool`

Type / Values

`boolean`

Details

Legacy name for enabling unified exec; prefer `[features].unified_exec` or `codex --enable unified_exec`.

Key

`features.apps`

Type / Values

`boolean`

Details

Enable ChatGPT Apps/connectors support (experimental).

Key

`features.codex_hooks`

Type / Values

`boolean`

Details

Enable lifecycle hooks loaded from `hooks.json` or inline `[hooks]` config.

Key

`features.enable_request_compression`

Type / Values

`boolean`

Details

Compress streaming request bodies with zstd when supported (stable; on by default).

Key

`features.fast_mode`

Type / Values

`boolean`

Details

Enable Fast mode selection and the `service_tier = "fast"` path (stable; on by default).

Key

`features.memories`

Type / Values

`boolean`

Details

Enable [Memories](/codex/memories) (off by default).

Key

`features.multi_agent`

Type / Values

`boolean`

Details

Enable multi-agent collaboration tools (`spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, and `close_agent`) (stable; on by default).

Key

`features.personality`

Type / Values

`boolean`

Details

Enable personality selection controls (stable; on by default).

Key

`features.prevent_idle_sleep`

Type / Values

`boolean`

Details

Prevent the machine from sleeping while a turn is actively running (experimental; off by default).

Key

`features.shell_snapshot`

Type / Values

`boolean`

Details

Snapshot shell environment to speed up repeated commands (stable; on by default).

Key

`features.shell_tool`

Type / Values

`boolean`

Details

Enable the default `shell` tool for running commands (stable; on by default).

Key

`features.skill_mcp_dependency_install`

Type / Values

`boolean`

Details

Allow prompting and installing missing MCP dependencies for skills (stable; on by default).

Key

`features.undo`

Type / Values

`boolean`

Details

Enable undo support (stable; off by default).

Key

`features.unified_exec`

Type / Values

`boolean`

Details

Use the unified PTY-backed exec tool (stable; enabled by default except on Windows).

Key

`features.web_search`

Type / Values

`boolean`

Details

Deprecated legacy toggle; prefer the top-level `web_search` setting.

Key

`features.web_search_cached`

Type / Values

`boolean`

Details

Deprecated legacy toggle. When `web_search` is unset, true maps to `web_search = "cached"`.

Key

`features.web_search_request`

Type / Values

`boolean`

Details

Deprecated legacy toggle. When `web_search` is unset, true maps to `web_search = "live"`.

Key

`feedback.enabled`

Type / Values

`boolean`

Details

Enable feedback submission via `/feedback` across Codex surfaces (default: true).

Key

`file_opener`

Type / Values

`vscode | vscode-insiders | windsurf | cursor | none`

Details

URI scheme used to open citations from Codex output (default: `vscode`).

Key

`forced_chatgpt_workspace_id`

Type / Values

`string (uuid)`

Details

Limit ChatGPT logins to a specific workspace identifier.

Key

`forced_login_method`

Type / Values

`chatgpt | api`

Details

Restrict Codex to a specific authentication method.

Key

`hide_agent_reasoning`

Type / Values

`boolean`

Details

Suppress reasoning events in both the TUI and `codex exec` output.

Key

`history.max_bytes`

Type / Values

`number`

Details

If set, caps the history file size in bytes by dropping oldest entries.

Key

`history.persistence`

Type / Values

`save-all | none`

Details

Control whether Codex saves session transcripts to history.jsonl.

Key

`hooks`

Type / Values

`table`

Details

Lifecycle hooks configured inline in `config.toml`. Uses the same event schema as `hooks.json`; see the Hooks guide for examples and supported events.

Key

`instructions`

Type / Values

`string`

Details

Reserved for future use; prefer `model_instructions_file` or `AGENTS.md`.

Key

`log_dir`

Type / Values

`string (path)`

Details

Directory where Codex writes log files (for example `codex-tui.log`); defaults to `$CODEX_HOME/log`.

Key

`mcp_oauth_callback_port`

Type / Values

`integer`

Details

Optional fixed port for the local HTTP callback server used during MCP OAuth login. When unset, Codex binds to an ephemeral port chosen by the OS.

Key

`mcp_oauth_callback_url`

Type / Values

`string`

Details

Optional redirect URI override for MCP OAuth login (for example, a devbox ingress URL). `mcp_oauth_callback_port` still controls the callback listener port.

Key

`mcp_oauth_credentials_store`

Type / Values

`auto | file | keyring`

Details

Preferred store for MCP OAuth credentials.

Key

`mcp_servers.<id>.args`

Type / Values

`array<string>`

Details

Arguments passed to the MCP stdio server command.

Key

`mcp_servers.<id>.bearer_token_env_var`

Type / Values

`string`

Details

Environment variable sourcing the bearer token for an MCP HTTP server.

Key

`mcp_servers.<id>.command`

Type / Values

`string`

Details

Launcher command for an MCP stdio server.

Key

`mcp_servers.<id>.cwd`

Type / Values

`string`

Details

Working directory for the MCP stdio server process.

Key

`mcp_servers.<id>.disabled_tools`

Type / Values

`array<string>`

Details

Deny list applied after `enabled_tools` for the MCP server.

Key

`mcp_servers.<id>.enabled`

Type / Values

`boolean`

Details

Disable an MCP server without removing its configuration.

Key

`mcp_servers.<id>.enabled_tools`

Type / Values

`array<string>`

Details

Allow list of tool names exposed by the MCP server.

Key

`mcp_servers.<id>.env`

Type / Values

`map<string,string>`

Details

Environment variables forwarded to the MCP stdio server.

Key

`mcp_servers.<id>.env_http_headers`

Type / Values

`map<string,string>`

Details

HTTP headers populated from environment variables for an MCP HTTP server.

Key

`mcp_servers.<id>.env_vars`

Type / Values

`array<string | { name = string, source = "local" | "remote" }>`

Details

Additional environment variables to whitelist for an MCP stdio server. String entries default to `source = "local"`; use `source = "remote"` only with executor-backed remote stdio.

Key

`mcp_servers.<id>.experimental_environment`

Type / Values

`local | remote`

Details

Experimental placement for an MCP server. `remote` starts stdio servers through a remote executor environment; streamable HTTP remote placement is not implemented.

Key

`mcp_servers.<id>.http_headers`

Type / Values

`map<string,string>`

Details

Static HTTP headers included with each MCP HTTP request.

Key

`mcp_servers.<id>.oauth_resource`

Type / Values

`string`

Details

Optional RFC 8707 OAuth resource parameter to include during MCP login.

Key

`mcp_servers.<id>.required`

Type / Values

`boolean`

Details

When true, fail startup/resume if this enabled MCP server cannot initialize.

Key

`mcp_servers.<id>.scopes`

Type / Values

`array<string>`

Details

OAuth scopes to request when authenticating to that MCP server.

Key

`mcp_servers.<id>.startup_timeout_ms`

Type / Values

`number`

Details

Alias for `startup_timeout_sec` in milliseconds.

Key

`mcp_servers.<id>.startup_timeout_sec`

Type / Values

`number`

Details

Override the default 10s startup timeout for an MCP server.

Key

`mcp_servers.<id>.tool_timeout_sec`

Type / Values

`number`

Details

Override the default 60s per-tool timeout for an MCP server.

Key

`mcp_servers.<id>.url`

Type / Values

`string`

Details

Endpoint for an MCP streamable HTTP server.

Key

`memories.consolidation_model`

Type / Values

`string`

Details

Optional model override for global memory consolidation.

Key

`memories.disable_on_external_context`

Type / Values

`boolean`

Details

When `true`, threads that use external context such as MCP tool calls, web search, or tool search are kept out of memory generation. Defaults to `false`. Legacy alias: `memories.no_memories_if_mcp_or_web_search`.

Key

`memories.extract_model`

Type / Values

`string`

Details

Optional model override for per-thread memory extraction.

Key

`memories.generate_memories`

Type / Values

`boolean`

Details

When `false`, newly created threads are not stored as memory-generation inputs. Defaults to `true`.

Key

`memories.max_raw_memories_for_consolidation`

Type / Values

`number`

Details

Maximum recent raw memories retained for global consolidation. Defaults to `256` and is capped at `4096`.

Key

`memories.max_rollout_age_days`

Type / Values

`number`

Details

Maximum age of threads considered for memory generation. Defaults to `30` and is clamped to `0`-`90`.

Key

`memories.max_rollouts_per_startup`

Type / Values

`number`

Details

Maximum rollout candidates processed per startup pass. Defaults to `16` and is capped at `128`.

Key

`memories.max_unused_days`

Type / Values

`number`

Details

Maximum days since a memory was last used before it becomes ineligible for consolidation. Defaults to `30` and is clamped to `0`-`365`.

Key

`memories.min_rollout_idle_hours`

Type / Values

`number`

Details

Minimum idle time before a thread is considered for memory generation. Defaults to `6` and is clamped to `1`-`48`.

Key

`memories.use_memories`

Type / Values

`boolean`

Details

When `false`, Codex skips injecting existing memories into future sessions. Defaults to `true`.

Key

`model`

Type / Values

`string`

Details

Model to use (e.g., `gpt-5.5`).

Key

`model_auto_compact_token_limit`

Type / Values

`number`

Details

Token threshold that triggers automatic history compaction (unset uses model defaults).

Key

`model_catalog_json`

Type / Values

`string (path)`

Details

Optional path to a JSON model catalog loaded on startup. Profile-level `profiles.<name>.model_catalog_json` can override this per profile.

Key

`model_context_window`

Type / Values

`number`

Details

Context window tokens available to the active model.

Key

`model_instructions_file`

Type / Values

`string (path)`

Details

Replacement for built-in instructions instead of `AGENTS.md`.

Key

`model_provider`

Type / Values

`string`

Details

Provider id from `model_providers` (default: `openai`).

Key

`model_providers.<id>`

Type / Values

`table`

Details

Custom provider definition. Built-in provider IDs (`openai`, `ollama`, and `lmstudio`) are reserved and cannot be overridden.

Key

`model_providers.<id>.auth`

Type / Values

`table`

Details

Command-backed bearer token configuration for a custom provider. Do not combine with `env_key`, `experimental_bearer_token`, or `requires_openai_auth`.

Key

`model_providers.<id>.auth.args`

Type / Values

`array<string>`

Details

Arguments passed to the token command.

Key

`model_providers.<id>.auth.command`

Type / Values

`string`

Details

Command to run when Codex needs a bearer token. The command must print the token to stdout.

Key

`model_providers.<id>.auth.cwd`

Type / Values

`string (path)`

Details

Working directory for the token command.

Key

`model_providers.<id>.auth.refresh_interval_ms`

Type / Values

`number`

Details

How often Codex proactively refreshes the token in milliseconds (default: 300000). Set to `0` to refresh only after an authentication retry.

Key

`model_providers.<id>.auth.timeout_ms`

Type / Values

`number`

Details

Maximum token command runtime in milliseconds (default: 5000).

Key

`model_providers.<id>.base_url`

Type / Values

`string`

Details

API base URL for the model provider.

Key

`model_providers.<id>.env_http_headers`

Type / Values

`map<string,string>`

Details

HTTP headers populated from environment variables when present.

Key

`model_providers.<id>.env_key`

Type / Values

`string`

Details

Environment variable supplying the provider API key.

Key

`model_providers.<id>.env_key_instructions`

Type / Values

`string`

Details

Optional setup guidance for the provider API key.

Key

`model_providers.<id>.experimental_bearer_token`

Type / Values

`string`

Details

Direct bearer token for the provider (discouraged; use `env_key`).

Key

`model_providers.<id>.http_headers`

Type / Values

`map<string,string>`

Details

Static HTTP headers added to provider requests.

Key

`model_providers.<id>.name`

Type / Values

`string`

Details

Display name for a custom model provider.

Key

`model_providers.<id>.query_params`

Type / Values

`map<string,string>`

Details

Extra query parameters appended to provider requests.

Key

`model_providers.<id>.request_max_retries`

Type / Values

`number`

Details

Retry count for HTTP requests to the provider (default: 4).

Key

`model_providers.<id>.requires_openai_auth`

Type / Values

`boolean`

Details

The provider uses OpenAI authentication (defaults to false).

Key

`model_providers.<id>.stream_idle_timeout_ms`

Type / Values

`number`

Details

Idle timeout for SSE streams in milliseconds (default: 300000).

Key

`model_providers.<id>.stream_max_retries`

Type / Values

`number`

Details

Retry count for SSE streaming interruptions (default: 5).

Key

`model_providers.<id>.supports_websockets`

Type / Values

`boolean`

Details

Whether that provider supports the Responses API WebSocket transport.

Key

`model_providers.<id>.wire_api`

Type / Values

`responses`

Details

Protocol used by the provider. `responses` is the only supported value, and it is the default when omitted.

Key

`model_reasoning_effort`

Type / Values

`minimal | low | medium | high | xhigh`

Details

Adjust reasoning effort for supported models (Responses API only; `xhigh` is model-dependent).

Key

`model_reasoning_summary`

Type / Values

`auto | concise | detailed | none`

Details

Select reasoning summary detail or disable summaries entirely.

Key

`model_supports_reasoning_summaries`

Type / Values

`boolean`

Details

Force Codex to send or not send reasoning metadata.

Key

`model_verbosity`

Type / Values

`low | medium | high`

Details

Optional GPT-5 Responses API verbosity override; when unset, the selected model/preset default is used.

Key

`notice.hide_full_access_warning`

Type / Values

`boolean`

Details

Track acknowledgement of the full access warning prompt.

Key

`notice.hide_gpt-5.1-codex-max_migration_prompt`

Type / Values

`boolean`

Details

Track acknowledgement of the gpt-5.1-codex-max migration prompt.

Key

`notice.hide_gpt5_1_migration_prompt`

Type / Values

`boolean`

Details

Track acknowledgement of the GPT-5.1 migration prompt.

Key

`notice.hide_rate_limit_model_nudge`

Type / Values

`boolean`

Details

Track opt-out of the rate limit model switch reminder.

Key

`notice.hide_world_writable_warning`

Type / Values

`boolean`

Details

Track acknowledgement of the Windows world-writable directories warning.

Key

`notice.model_migrations`

Type / Values

`map<string,string>`

Details

Track acknowledged model migrations as old->new mappings.

Key

`notify`

Type / Values

`array<string>`

Details

Command invoked for notifications; receives a JSON payload from Codex.

Key

`openai_base_url`

Type / Values

`string`

Details

Base URL override for the built-in `openai` model provider.

Key

`oss_provider`

Type / Values

`lmstudio | ollama`

Details

Default local provider used when running with `--oss` (defaults to prompting if unset).

Key

`otel.environment`

Type / Values

`string`

Details

Environment tag applied to emitted OpenTelemetry events (default: `dev`).

Key

`otel.exporter`

Type / Values

`none | otlp-http | otlp-grpc`

Details

Select the OpenTelemetry exporter and provide any endpoint metadata.

Key

`otel.exporter.<id>.endpoint`

Type / Values

`string`

Details

Exporter endpoint for OTEL logs.

Key

`otel.exporter.<id>.headers`

Type / Values

`map<string,string>`

Details

Static headers included with OTEL exporter requests.

Key

`otel.exporter.<id>.protocol`

Type / Values

`binary | json`

Details

Protocol used by the OTLP/HTTP exporter.

Key

`otel.exporter.<id>.tls.ca-certificate`

Type / Values

`string`

Details

CA certificate path for OTEL exporter TLS.

Key

`otel.exporter.<id>.tls.client-certificate`

Type / Values

`string`

Details

Client certificate path for OTEL exporter TLS.

Key

`otel.exporter.<id>.tls.client-private-key`

Type / Values

`string`

Details

Client private key path for OTEL exporter TLS.

Key

`otel.log_user_prompt`

Type / Values

`boolean`

Details

Opt in to exporting raw user prompts with OpenTelemetry logs.

Key

`otel.metrics_exporter`

Type / Values

`none | statsig | otlp-http | otlp-grpc`

Details

Select the OpenTelemetry metrics exporter (defaults to `statsig`).

Key

`otel.trace_exporter`

Type / Values

`none | otlp-http | otlp-grpc`

Details

Select the OpenTelemetry trace exporter and provide any endpoint metadata.

Key

`otel.trace_exporter.<id>.endpoint`

Type / Values

`string`

Details

Trace exporter endpoint for OTEL logs.

Key

`otel.trace_exporter.<id>.headers`

Type / Values

`map<string,string>`

Details

Static headers included with OTEL trace exporter requests.

Key

`otel.trace_exporter.<id>.protocol`

Type / Values

`binary | json`

Details

Protocol used by the OTLP/HTTP trace exporter.

Key

`otel.trace_exporter.<id>.tls.ca-certificate`

Type / Values

`string`

Details

CA certificate path for OTEL trace exporter TLS.

Key

`otel.trace_exporter.<id>.tls.client-certificate`

Type / Values

`string`

Details

Client certificate path for OTEL trace exporter TLS.

Key

`otel.trace_exporter.<id>.tls.client-private-key`

Type / Values

`string`

Details

Client private key path for OTEL trace exporter TLS.

Key

`permissions.<name>.filesystem`

Type / Values

`table`

Details

Named filesystem permission profile. Each key is an absolute path or special token such as `:minimal` or `:project_roots`.

Key

`permissions.<name>.filesystem.":project_roots".<subpath-or-glob>`

Type / Values

`"read" | "write" | "none"`

Details

Scoped filesystem access relative to the detected project roots. Use `"."` for the root itself; glob subpaths such as `"**/*.env"` can deny reads with `"none"`.

Key

`permissions.<name>.filesystem.<path-or-glob>`

Type / Values

`"read" | "write" | "none" | table`

Details

Grant direct access for a path, glob pattern, or special token, or scope nested entries under that root. Use `"none"` to deny reads for matching paths.

Key

`permissions.<name>.filesystem.glob_scan_max_depth`

Type / Values

`number`

Details

Maximum depth for expanding deny-read glob patterns on platforms that snapshot matches before sandbox startup. Must be at least `1` when set.

Key

`permissions.<name>.network.allow_local_binding`

Type / Values

`boolean`

Details

Permit local bind/listen operations through the managed proxy.

Key

`permissions.<name>.network.allow_upstream_proxy`

Type / Values

`boolean`

Details

Allow the managed proxy to chain to another upstream proxy.

Key

`permissions.<name>.network.dangerously_allow_all_unix_sockets`

Type / Values

`boolean`

Details

Allow the proxy to use arbitrary Unix sockets instead of the default restricted set.

Key

`permissions.<name>.network.dangerously_allow_non_loopback_proxy`

Type / Values

`boolean`

Details

Permit non-loopback bind addresses for the managed proxy listener.

Key

`permissions.<name>.network.domains`

Type / Values

`map<string, allow | deny>`

Details

Domain rules for the managed proxy. Use domain names or wildcard patterns as keys, with `allow` or `deny` values.

Key

`permissions.<name>.network.enable_socks5`

Type / Values

`boolean`

Details

Expose a SOCKS5 listener when this permissions profile enables the managed network proxy.

Key

`permissions.<name>.network.enable_socks5_udp`

Type / Values

`boolean`

Details

Allow UDP over the SOCKS5 listener when enabled.

Key

`permissions.<name>.network.enabled`

Type / Values

`boolean`

Details

Enable network access for this named permissions profile.

Key

`permissions.<name>.network.mode`

Type / Values

`limited | full`

Details

Network proxy mode used for subprocess traffic.

Key

`permissions.<name>.network.proxy_url`

Type / Values

`string`

Details

HTTP proxy endpoint used when this permissions profile enables the managed network proxy.

Key

`permissions.<name>.network.socks_url`

Type / Values

`string`

Details

SOCKS5 proxy endpoint used by this permissions profile.

Key

`permissions.<name>.network.unix_sockets`

Type / Values

`map<string, allow | none>`

Details

Unix socket rules for the managed proxy. Use socket paths as keys, with `allow` or `none` values.

Key

`personality`

Type / Values

`none | friendly | pragmatic`

Details

Default communication style for models that advertise `supportsPersonality`; can be overridden per thread/turn or via `/personality`.

Key

`plan_mode_reasoning_effort`

Type / Values

`none | minimal | low | medium | high | xhigh`

Details

Plan-mode-specific reasoning override. When unset, Plan mode uses its built-in preset default.

Key

`profile`

Type / Values

`string`

Details

Default profile applied at startup (equivalent to `--profile`).

Key

`profiles.<name>.*`

Type / Values

`various`

Details

Profile-scoped overrides for any of the supported configuration keys.

Key

`profiles.<name>.analytics.enabled`

Type / Values

`boolean`

Details

Profile-scoped analytics enablement override.

Key

`profiles.<name>.experimental_use_unified_exec_tool`

Type / Values

`boolean`

Details

Legacy name for enabling unified exec; prefer `[features].unified_exec`.

Key

`profiles.<name>.model_catalog_json`

Type / Values

`string (path)`

Details

Profile-scoped model catalog JSON path override (applied on startup only; overrides the top-level `model_catalog_json` for that profile).

Key

`profiles.<name>.model_instructions_file`

Type / Values

`string (path)`

Details

Profile-scoped replacement for the built-in instruction file.

Key

`profiles.<name>.oss_provider`

Type / Values

`lmstudio | ollama`

Details

Profile-scoped OSS provider for `--oss` sessions.

Key

`profiles.<name>.personality`

Type / Values

`none | friendly | pragmatic`

Details

Profile-scoped communication style override for supported models.

Key

`profiles.<name>.plan_mode_reasoning_effort`

Type / Values

`none | minimal | low | medium | high | xhigh`

Details

Profile-scoped Plan-mode reasoning override.

Key

`profiles.<name>.service_tier`

Type / Values

`flex | fast`

Details

Profile-scoped service tier preference for new turns.

Key

`profiles.<name>.tools_view_image`

Type / Values

`boolean`

Details

Enable or disable the `view_image` tool in that profile.

Key

`profiles.<name>.web_search`

Type / Values

`disabled | cached | live`

Details

Profile-scoped web search mode override (default: `"cached"`).

Key

`profiles.<name>.windows.sandbox`

Type / Values

`unelevated | elevated`

Details

Profile-scoped Windows sandbox mode override.

Key

`project_doc_fallback_filenames`

Type / Values

`array<string>`

Details

Additional filenames to try when `AGENTS.md` is missing.

Key

`project_doc_max_bytes`

Type / Values

`number`

Details

Maximum bytes read from `AGENTS.md` when building project instructions.

Key

`project_root_markers`

Type / Values

`array<string>`

Details

List of project root marker filenames; used when searching parent directories for the project root.

Key

`projects.<path>.trust_level`

Type / Values

`string`

Details

Mark a project or worktree as trusted or untrusted (`"trusted"` | `"untrusted"`). Untrusted projects skip project-scoped `.codex/` layers, including project-local config, hooks, and rules.

Key

`review_model`

Type / Values

`string`

Details

Optional model override used by `/review` (defaults to the current session model).

Key

`sandbox_mode`

Type / Values

`read-only | workspace-write | danger-full-access`

Details

Sandbox policy for filesystem and network access during command execution.

Key

`sandbox_workspace_write.exclude_slash_tmp`

Type / Values

`boolean`

Details

Exclude `/tmp` from writable roots in workspace-write mode.

Key

`sandbox_workspace_write.exclude_tmpdir_env_var`

Type / Values

`boolean`

Details

Exclude `$TMPDIR` from writable roots in workspace-write mode.

Key

`sandbox_workspace_write.network_access`

Type / Values

`boolean`

Details

Allow outbound network access inside the workspace-write sandbox.

Key

`sandbox_workspace_write.writable_roots`

Type / Values

`array<string>`

Details

Additional writable roots when `sandbox_mode = "workspace-write"`.

Key

`service_tier`

Type / Values

`flex | fast`

Details

Preferred service tier for new turns.

Key

`shell_environment_policy.exclude`

Type / Values

`array<string>`

Details

Glob patterns for removing environment variables after the defaults.

Key

`shell_environment_policy.experimental_use_profile`

Type / Values

`boolean`

Details

Use the user shell profile when spawning subprocesses.

Key

`shell_environment_policy.ignore_default_excludes`

Type / Values

`boolean`

Details

Keep variables containing KEY/SECRET/TOKEN before other filters run.

Key

`shell_environment_policy.include_only`

Type / Values

`array<string>`

Details

Whitelist of patterns; when set only matching variables are kept.

Key

`shell_environment_policy.inherit`

Type / Values

`all | core | none`

Details

Baseline environment inheritance when spawning subprocesses.

Key

`shell_environment_policy.set`

Type / Values

`map<string,string>`

Details

Explicit environment overrides injected into every subprocess.

Key

`show_raw_agent_reasoning`

Type / Values

`boolean`

Details

Surface raw reasoning content when the active model emits it.

Key

`skills.config`

Type / Values

`array<object>`

Details

Per-skill enablement overrides stored in config.toml.

Key

`skills.config.<index>.enabled`

Type / Values

`boolean`

Details

Enable or disable the referenced skill.

Key

`skills.config.<index>.path`

Type / Values

`string (path)`

Details

Path to a skill folder containing `SKILL.md`.

Key

`sqlite_home`

Type / Values

`string (path)`

Details

Directory where Codex stores the SQLite-backed state DB used by agent jobs and other resumable runtime state.

Key

`suppress_unstable_features_warning`

Type / Values

`boolean`

Details

Suppress the warning that appears when under-development feature flags are enabled.

Key

`tool_output_token_limit`

Type / Values

`number`

Details

Token budget for storing individual tool/function outputs in history.

Key

`tool_suggest.discoverables`

Type / Values

`array<table>`

Details

Allow tool suggestions for additional discoverable connectors or plugins. Each entry uses `type = "connector"` or `"plugin"` and an `id`.

Key

`tools.view_image`

Type / Values

`boolean`

Details

Enable the local-image attachment tool `view_image`.

Key

`tools.web_search`

Type / Values

`boolean | { context_size = "low|medium|high", allowed_domains = [string], location = { country, region, city, timezone } }`

Details

Optional web search tool configuration. The legacy boolean form is still accepted, but the object form lets you set search context size, allowed domains, and approximate user location.

Key

`tui`

Type / Values

`table`

Details

TUI-specific options such as enabling inline desktop notifications.

Key

`tui.alternate_screen`

Type / Values

`auto | always | never`

Details

Control alternate screen usage for the TUI (default: auto; auto skips it in Zellij to preserve scrollback).

Key

`tui.animations`

Type / Values

`boolean`

Details

Enable terminal animations (welcome screen, shimmer, spinner) (default: true).

Key

`tui.model_availability_nux.<model>`

Type / Values

`integer`

Details

Internal startup-tooltip state keyed by model slug.

Key

`tui.notification_condition`

Type / Values

`unfocused | always`

Details

Control whether TUI notifications fire only when the terminal is unfocused or regardless of focus. Defaults to `unfocused`.

Key

`tui.notification_method`

Type / Values

`auto | osc9 | bel`

Details

Notification method for terminal notifications (default: auto).

Key

`tui.notifications`

Type / Values

`boolean | array<string>`

Details

Enable TUI notifications; optionally restrict to specific event types.

Key

`tui.show_tooltips`

Type / Values

`boolean`

Details

Show onboarding tooltips in the TUI welcome screen (default: true).

Key

`tui.status_line`

Type / Values

`array<string> | null`

Details

Ordered list of TUI footer status-line item identifiers. `null` disables the status line.

Key

`tui.terminal_title`

Type / Values

`array<string> | null`

Details

Ordered list of terminal window/tab title item identifiers. Defaults to `["spinner", "project"]`; `null` disables title updates.

Key

`tui.theme`

Type / Values

`string`

Details

Syntax-highlighting theme override (kebab-case theme name).

Key

`web_search`

Type / Values

`disabled | cached | live`

Details

Web search mode (default: `"cached"`; cached uses an OpenAI-maintained index and does not fetch live pages; if you use `--yolo` or another full access sandbox setting, it defaults to `"live"`). Use `"live"` to fetch the most recent data from the web, or `"disabled"` to remove the tool.

Key

`windows_wsl_setup_acknowledged`

Type / Values

`boolean`

Details

Track Windows onboarding acknowledgement (Windows only).

Key

`windows.sandbox`

Type / Values

`unelevated | elevated`

Details

Windows-only native sandbox mode when running Codex natively on Windows.

Key

`windows.sandbox_private_desktop`

Type / Values

`boolean`

Details

Run the final sandboxed child process on a private desktop by default on native Windows. Set `false` only for compatibility with the older `Winsta0\\Default` behavior.

Expand to view all

You can find the latest JSON schema for `config.toml` [here](/codex/config-schema.json).

To get autocompletion and diagnostics when editing `config.toml` in VS Code or Cursor, you can install the [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml) extension and add this line to the top of your `config.toml`:

```
#:schema https://developers.openai.com/codex/config-schema.json
```

Note: Rename `experimental_instructions_file` to `model_instructions_file`. Codex deprecates the old key; update existing configs to the new name.

## `requirements.toml`

`requirements.toml` is an admin-enforced configuration file that constrains security-sensitive settings users can’t override. For details, locations, and examples, see [Admin-enforced requirements](/codex/enterprise/managed-configuration#admin-enforced-requirements-requirementstoml).

For ChatGPT Business and Enterprise users, Codex can also apply cloud-fetched
requirements. See the security page for precedence details.

Use `[features]` in `requirements.toml` to pin feature flags by the same
canonical keys that `config.toml` uses. Omitted keys remain unconstrained.

| Key | Type / Values | Details |
| --- | --- | --- |
| `allowed_approval_policies` | `array<string>` | Allowed values for `approval_policy` (for example `untrusted`, `on-request`, `never`, and `granular`). |
| `allowed_approvals_reviewers` | `array<string>` | Allowed values for `approvals_reviewer`, such as `user` and `auto_review`. |
| `allowed_sandbox_modes` | `array<string>` | Allowed values for `sandbox_mode`. |
| `allowed_web_search_modes` | `array<string>` | Allowed values for `web_search` (`disabled`, `cached`, `live`). `disabled` is always allowed; an empty list effectively allows only `disabled`. |
| `feature_requirements` | `table` | Alias for `features` in `requirements.toml`. Use it to pin feature values by canonical feature key. |
| `feature_requirements.browser_use` | `boolean` | Set to `false` in `requirements.toml` to disable Browser Use and Browser Agent availability. You can also set `features.browser_use`. |
| `feature_requirements.computer_use` | `boolean` | Set to `false` in `requirements.toml` to disable Computer Use availability and related install or enablement flows. You can also set `features.computer_use`. |
| `feature_requirements.in_app_browser` | `boolean` | Set to `false` in `requirements.toml` to disable the in-app browser pane. You can also set `features.in_app_browser`. |
| `features` | `table` | Pinned feature values keyed by the canonical names from `config.toml`'s `[features]` table. |
| `features.<name>` | `boolean` | Require a specific canonical feature key to stay enabled or disabled. |
| `guardian_policy_config` | `string` | Managed Markdown policy instructions for automatic review. This takes precedence over local `[auto_review].policy`. Blank values are ignored. |
| `hooks` | `table` | Admin-enforced managed lifecycle hooks. Requires a managed hook directory and uses the same event schema as inline `[hooks]` in `config.toml`. |
| `hooks.<Event>` | `array<table>` | Matcher groups for a hook event such as `PreToolUse`, `PostToolUse`, `PermissionRequest`, `SessionStart`, `UserPromptSubmit`, or `Stop`. |
| `hooks.<Event>[].hooks` | `array<table>` | Hook handlers for a matcher group. Command hooks are currently supported; prompt and agent hook handlers are parsed but skipped. |
| `hooks.managed_dir` | `string (absolute path)` | Directory containing managed hook scripts on macOS and Linux. Codex validates that it is absolute and exists before loading managed hooks. |
| `hooks.windows_managed_dir` | `string (absolute path)` | Directory containing managed hook scripts on Windows. Codex validates that it is absolute and exists before loading managed hooks. |
| `mcp_servers` | `table` | Allowlist of MCP servers that may be enabled. Both the server name (`<id>`) and its identity must match for the MCP server to be enabled. Any configured MCP server not in the allowlist (or with a mismatched identity) is disabled. |
| `mcp_servers.<id>.identity` | `table` | Identity rule for a single MCP server. Set either `command` (stdio) or `url` (streamable HTTP). |
| `mcp_servers.<id>.identity.command` | `string` | Allow an MCP stdio server when its `mcp_servers.<id>.command` matches this command. |
| `mcp_servers.<id>.identity.url` | `string` | Allow an MCP streamable HTTP server when its `mcp_servers.<id>.url` matches this URL. |
| `permissions.filesystem.deny_read` | `array<string>` | Admin-enforced filesystem read denials. Entries can be paths or glob patterns, and users cannot weaken them with local config. |
| `remote_sandbox_config` | `array<table>` | Host-specific sandbox requirements. The first entry whose `hostname_patterns` match the resolved host name overrides top-level `allowed_sandbox_modes` for that requirements source. Host-specific entries currently override sandbox modes only. |
| `remote_sandbox_config[].allowed_sandbox_modes` | `array<string>` | Allowed sandbox modes to apply when this host-specific entry matches. |
| `remote_sandbox_config[].hostname_patterns` | `array<string>` | Case-insensitive host name patterns. Supports `*` for any sequence of characters and `?` for one character. |
| `rules` | `table` | Admin-enforced command rules merged with `.rules` files. Requirements rules must be restrictive. |
| `rules.prefix_rules` | `array<table>` | List of enforced prefix rules. Each rule must include `pattern` and `decision`. |
| `rules.prefix_rules[].decision` | `prompt | forbidden` | Required. Requirements rules can only prompt or forbid (not allow). |
| `rules.prefix_rules[].justification` | `string` | Optional non-empty rationale surfaced in approval prompts or rejection messages. |
| `rules.prefix_rules[].pattern` | `array<table>` | Command prefix expressed as pattern tokens. Each token sets either `token` or `any_of`. |
| `rules.prefix_rules[].pattern[].any_of` | `array<string>` | A list of allowed alternative tokens at this position. |
| `rules.prefix_rules[].pattern[].token` | `string` | A single literal token at this position. |

Key

`allowed_approval_policies`

Type / Values

`array<string>`

Details

Allowed values for `approval_policy` (for example `untrusted`, `on-request`, `never`, and `granular`).

Key

`allowed_approvals_reviewers`

Type / Values

`array<string>`

Details

Allowed values for `approvals_reviewer`, such as `user` and `auto_review`.

Key

`allowed_sandbox_modes`

Type / Values

`array<string>`

Details

Allowed values for `sandbox_mode`.

Key

`allowed_web_search_modes`

Type / Values

`array<string>`

Details

Allowed values for `web_search` (`disabled`, `cached`, `live`). `disabled` is always allowed; an empty list effectively allows only `disabled`.

Key

`feature_requirements`

Type / Values

`table`

Details

Alias for `features` in `requirements.toml`. Use it to pin feature values by canonical feature key.

Key

`feature_requirements.browser_use`

Type / Values

`boolean`

Details

Set to `false` in `requirements.toml` to disable Browser Use and Browser Agent availability. You can also set `features.browser_use`.

Key

`feature_requirements.computer_use`

Type / Values

`boolean`

Details

Set to `false` in `requirements.toml` to disable Computer Use availability and related install or enablement flows. You can also set `features.computer_use`.

Key

`feature_requirements.in_app_browser`

Type / Values

`boolean`

Details

Set to `false` in `requirements.toml` to disable the in-app browser pane. You can also set `features.in_app_browser`.

Key

`features`

Type / Values

`table`

Details

Pinned feature values keyed by the canonical names from `config.toml`'s `[features]` table.

Key

`features.<name>`

Type / Values

`boolean`

Details

Require a specific canonical feature key to stay enabled or disabled.

Key

`guardian_policy_config`

Type / Values

`string`

Details

Managed Markdown policy instructions for automatic review. This takes precedence over local `[auto_review].policy`. Blank values are ignored.

Key

`hooks`

Type / Values

`table`

Details

Admin-enforced managed lifecycle hooks. Requires a managed hook directory and uses the same event schema as inline `[hooks]` in `config.toml`.

Key

`hooks.<Event>`

Type / Values

`array<table>`

Details

Matcher groups for a hook event such as `PreToolUse`, `PostToolUse`, `PermissionRequest`, `SessionStart`, `UserPromptSubmit`, or `Stop`.

Key

`hooks.<Event>[].hooks`

Type / Values

`array<table>`

Details

Hook handlers for a matcher group. Command hooks are currently supported; prompt and agent hook handlers are parsed but skipped.

Key

`hooks.managed_dir`

Type / Values

`string (absolute path)`

Details

Directory containing managed hook scripts on macOS and Linux. Codex validates that it is absolute and exists before loading managed hooks.

Key

`hooks.windows_managed_dir`

Type / Values

`string (absolute path)`

Details

Directory containing managed hook scripts on Windows. Codex validates that it is absolute and exists before loading managed hooks.

Key

`mcp_servers`

Type / Values

`table`

Details

Allowlist of MCP servers that may be enabled. Both the server name (`<id>`) and its identity must match for the MCP server to be enabled. Any configured MCP server not in the allowlist (or with a mismatched identity) is disabled.

Key

`mcp_servers.<id>.identity`

Type / Values

`table`

Details

Identity rule for a single MCP server. Set either `command` (stdio) or `url` (streamable HTTP).

Key

`mcp_servers.<id>.identity.command`

Type / Values

`string`

Details

Allow an MCP stdio server when its `mcp_servers.<id>.command` matches this command.

Key

`mcp_servers.<id>.identity.url`

Type / Values

`string`

Details

Allow an MCP streamable HTTP server when its `mcp_servers.<id>.url` matches this URL.

Key

`permissions.filesystem.deny_read`

Type / Values

`array<string>`

Details

Admin-enforced filesystem read denials. Entries can be paths or glob patterns, and users cannot weaken them with local config.

Key

`remote_sandbox_config`

Type / Values

`array<table>`

Details

Host-specific sandbox requirements. The first entry whose `hostname_patterns` match the resolved host name overrides top-level `allowed_sandbox_modes` for that requirements source. Host-specific entries currently override sandbox modes only.

Key

`remote_sandbox_config[].allowed_sandbox_modes`

Type / Values

`array<string>`

Details

Allowed sandbox modes to apply when this host-specific entry matches.

Key

`remote_sandbox_config[].hostname_patterns`

Type / Values

`array<string>`

Details

Case-insensitive host name patterns. Supports `*` for any sequence of characters and `?` for one character.

Key

`rules`

Type / Values

`table`

Details

Admin-enforced command rules merged with `.rules` files. Requirements rules must be restrictive.

Key

`rules.prefix_rules`

Type / Values

`array<table>`

Details

List of enforced prefix rules. Each rule must include `pattern` and `decision`.

Key

`rules.prefix_rules[].decision`

Type / Values

`prompt | forbidden`

Details

Required. Requirements rules can only prompt or forbid (not allow).

Key

`rules.prefix_rules[].justification`

Type / Values

`string`

Details

Optional non-empty rationale surfaced in approval prompts or rejection messages.

Key

`rules.prefix_rules[].pattern`

Type / Values

`array<table>`

Details

Command prefix expressed as pattern tokens. Each token sets either `token` or `any_of`.

Key

`rules.prefix_rules[].pattern[].any_of`

Type / Values

`array<string>`

Details

A list of allowed alternative tokens at this position.

Key

`rules.prefix_rules[].pattern[].token`

Type / Values

`string`

Details

A single literal token at this position.

Expand to view all

