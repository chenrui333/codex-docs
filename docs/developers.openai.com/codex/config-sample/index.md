# Sample Configuration

Source: https://developers.openai.com/codex/config-sample

Use this example configuration as a starting point. It includes most keys Codex reads from `config.toml`, along with default behaviors, recommended values where helpful, and short notes.

For explanations and guidance, see:

- [Config basics](/codex/config-basic)
- [Advanced Config](/codex/config-advanced)
- [Config Reference](/codex/config-reference)
- [Sandbox and approvals](/codex/agent-approvals-security#sandbox-and-approvals)
- [Managed configuration](/codex/enterprise/managed-configuration)

Use the snippet below as a reference. Copy only the keys and sections you need into `~/.codex/config.toml` (or into a project-scoped `.codex/config.toml`), then adjust values for your setup.

```
# Codex example configuration (config.toml)
#
# This file lists the main keys Codex reads from config.toml, along with default
# behaviors, recommended examples, and concise explanations. Adjust as needed.
#
# Notes
# - Root keys must appear before tables in TOML.
# - Optional keys that default to "unset" are shown commented out with notes.
# - MCP servers, profiles, and model providers are examples; remove or edit.

################################################################################
# Core Model Selection
################################################################################

# Primary model used by Codex. Recommended example for most users: "gpt-5.4".
model = "gpt-5.4"

# Communication style for supported models. Allowed values: none | friendly | pragmatic
# personality = "pragmatic"

# Optional model override for /review. Default: unset (uses current session model).
# review_model = "gpt-5.4"

# Provider id selected from [model_providers]. Default: "openai".
model_provider = "openai"

# Default OSS provider for --oss sessions. When unset, Codex prompts. Default: unset.
# oss_provider = "ollama"

# Preferred service tier. `fast` is honored only when enabled in [features].
# service_tier = "flex"  # fast | flex

# Optional manual model metadata. When unset, Codex uses model or preset defaults.
# model_context_window = 128000       # tokens; default: auto for model
# model_auto_compact_token_limit = 64000  # tokens; unset uses model defaults
# tool_output_token_limit = 12000     # tokens stored per tool output
# model_catalog_json = "/absolute/path/to/models.json" # optional startup-only model catalog override
# background_terminal_max_timeout = 300000 # ms; max empty write_stdin poll window (default 5m)
# log_dir = "/absolute/path/to/codex-logs" # directory for Codex logs; default: "$CODEX_HOME/log"
# sqlite_home = "/absolute/path/to/codex-state" # optional SQLite-backed runtime state directory

################################################################################
# Reasoning & Verbosity (Responses API capable models)
################################################################################

# Reasoning effort: minimal | low | medium | high | xhigh
# model_reasoning_effort = "medium"

# Optional override used when Codex runs in plan mode: none | minimal | low | medium | high | xhigh
# plan_mode_reasoning_effort = "high"

# Reasoning summary: auto | concise | detailed | none
# model_reasoning_summary = "auto"

# Text verbosity for GPT-5 family (Responses API): low | medium | high
# model_verbosity = "medium"

# Force enable or disable reasoning summaries for current model.
# model_supports_reasoning_summaries = true

################################################################################
# Instruction Overrides
################################################################################

# Additional user instructions are injected before AGENTS.md. Default: unset.
# developer_instructions = ""

# Inline override for the history compaction prompt. Default: unset.
# compact_prompt = ""

# Override the default commit co-author trailer. Set to "" to disable it.
# commit_attribution = "Jane Doe <jane@example.com>"

# Override built-in base instructions with a file path. Default: unset.
# model_instructions_file = "/absolute/or/relative/path/to/instructions.txt"

# Load the compact prompt override from a file. Default: unset.
# experimental_compact_prompt_file = "/absolute/or/relative/path/to/compact_prompt.txt"

################################################################################
# Notifications
################################################################################

# External notifier program (argv array). When unset: disabled.
# notify = ["notify-send", "Codex"]

################################################################################
# Approval & Sandbox
################################################################################

# When to ask for command approval:
# - untrusted: only known-safe read-only commands auto-run; others prompt
# - on-request: model decides when to ask (default)
# - never: never prompt (risky)
# - { reject = { ... } }: auto-reject selected prompt categories
approval_policy = "on-request"
# Example granular auto-reject policy:
# approval_policy = { reject = { sandbox_approval = true, rules = false, mcp_elicitations = false } }

# Allow login-shell semantics for shell-based tools when they request `login = true`.
# Default: true. Set false to force non-login shells and reject explicit login-shell requests.
allow_login_shell = true

# Filesystem/network sandbox policy for tool calls:
# - read-only (default)
# - workspace-write
# - danger-full-access (no sandbox; extremely risky)
sandbox_mode = "read-only"

################################################################################
# Authentication & Login
################################################################################

# Where to persist CLI login credentials: file (default) | keyring | auto
cli_auth_credentials_store = "file"

# Base URL for ChatGPT auth flow (not OpenAI API).
chatgpt_base_url = "https://chatgpt.com/backend-api/"

# Restrict ChatGPT login to a specific workspace id. Default: unset.
# forced_chatgpt_workspace_id = "00000000-0000-0000-0000-000000000000"

# Force login mechanism when Codex would normally auto-select. Default: unset.
# Allowed values: chatgpt | api
# forced_login_method = "chatgpt"

# Preferred store for MCP OAuth credentials: auto (default) | file | keyring
mcp_oauth_credentials_store = "auto"
# Optional fixed port for MCP OAuth callback: 1-65535. Default: unset.
# mcp_oauth_callback_port = 4321
# Optional redirect URI override for MCP OAuth login (for example, remote devbox ingress).
# Custom callback paths are supported. `mcp_oauth_callback_port` still controls the listener port.
# mcp_oauth_callback_url = "https://devbox.example.internal/callback"

################################################################################
# Project Documentation Controls
################################################################################

# Max bytes from AGENTS.md to embed into first-turn instructions. Default: 32768
project_doc_max_bytes = 32768

# Ordered fallbacks when AGENTS.md is missing at a directory level. Default: []
project_doc_fallback_filenames = []

# Project root marker filenames used when searching parent directories. Default: [".git"]
# project_root_markers = [".git"]

################################################################################
# History & File Opener
################################################################################

# URI scheme for clickable citations: vscode (default) | vscode-insiders | windsurf | cursor | none
file_opener = "vscode"

################################################################################
# UI, Notifications, and Misc
################################################################################

# Suppress internal reasoning events from output. Default: false
hide_agent_reasoning = false

# Show raw reasoning content when available. Default: false
show_raw_agent_reasoning = false

# Disable burst-paste detection in the TUI. Default: false
disable_paste_burst = false

# Track Windows onboarding acknowledgement (Windows only). Default: false
windows_wsl_setup_acknowledged = false

# Check for updates on startup. Default: true
check_for_update_on_startup = true

################################################################################
# Web Search
################################################################################

# Web search mode: disabled | cached | live. Default: "cached"
# cached serves results from a web search cache (an OpenAI-maintained index).
# cached returns pre-indexed results; live fetches the most recent data.
# If you use --yolo or another full access sandbox setting, web search defaults to live.
web_search = "cached"

# Active profile name. When unset, no profile is applied.
# profile = "default"

# Suppress the warning shown when under-development feature flags are enabled.
# suppress_unstable_features_warning = true

################################################################################
# Agents (multi-agent roles and limits)
################################################################################

[agents]
# Maximum concurrently open agent threads. Default: 6
# max_threads = 6
# Maximum nested spawn depth. Root session starts at depth 0. Default: 1
# max_depth = 1
# Default timeout per worker for spawn_agents_on_csv jobs. When unset, the tool defaults to 1800 seconds.
# job_max_runtime_seconds = 1800

# [agents.reviewer]
# description = "Find correctness, security, and test risks in code."
# config_file = "./agents/reviewer.toml"  # relative to the config.toml that defines it
# nickname_candidates = ["Athena", "Ada"]

################################################################################
# Skills (per-skill overrides)
################################################################################

# Disable or re-enable a specific skill without deleting it.
[[skills.config]]
# path = "/path/to/skill/SKILL.md"
# enabled = false

################################################################################
# Sandbox settings (tables)
################################################################################

# Extra settings used only when sandbox_mode = "workspace-write".
[sandbox_workspace_write]
# Additional writable roots beyond the workspace (cwd). Default: []
writable_roots = []
# Allow outbound network access inside the sandbox. Default: false
network_access = false
# Exclude $TMPDIR from writable roots. Default: false
exclude_tmpdir_env_var = false
# Exclude /tmp from writable roots. Default: false
exclude_slash_tmp = false

################################################################################
# Shell Environment Policy for spawned processes (table)
################################################################################

[shell_environment_policy]
# inherit: all (default) | core | none
inherit = "all"
# Skip default excludes for names containing KEY/SECRET/TOKEN (case-insensitive). Default: false
ignore_default_excludes = false
# Case-insensitive glob patterns to remove (e.g., "AWS_*", "AZURE_*"). Default: []
exclude = []
# Explicit key/value overrides (always win). Default: {}
set = {}
# Whitelist; if non-empty, keep only matching vars. Default: []
include_only = []
# Experimental: run via user shell profile. Default: false
experimental_use_profile = false

################################################################################
# Managed network proxy settings
################################################################################

[permissions.network]
# enabled = true
# proxy_url = "http://127.0.0.1:43128"
# admin_url = "http://127.0.0.1:43129"
# enable_socks5 = false
# socks_url = "http://127.0.0.1:43130"
# enable_socks5_udp = false
# allow_upstream_proxy = false
# dangerously_allow_non_loopback_proxy = false
# dangerously_allow_non_loopback_admin = false
# dangerously_allow_all_unix_sockets = false
# mode = "limited"                           # limited | full
# allowed_domains = ["api.openai.com"]
# denied_domains = ["example.com"]
# allow_unix_sockets = ["/var/run/docker.sock"]
# allow_local_binding = false

################################################################################
# History (table)
################################################################################

[history]
# save-all (default) | none
persistence = "save-all"
# Maximum bytes for history file; oldest entries are trimmed when exceeded. Example: 5242880
# max_bytes = 5242880

################################################################################
# UI, Notifications, and Misc (tables)
################################################################################

[tui]
# Desktop notifications from the TUI: boolean or filtered list. Default: true
# Examples: false | ["agent-turn-complete", "approval-requested"]
notifications = false

# Notification mechanism for terminal alerts: auto | osc9 | bel. Default: "auto"
# notification_method = "auto"

# Enables welcome/status/spinner animations. Default: true
animations = true

# Show onboarding tooltips in the welcome screen. Default: true
show_tooltips = true

# Control alternate screen usage (auto skips it in Zellij to preserve scrollback).
# alternate_screen = "auto"

# Ordered list of footer status-line item IDs. When unset, Codex uses:
# ["model-with-reasoning", "context-remaining", "current-dir"].
# Set to [] to hide the footer.
# status_line = ["model", "context-remaining", "git-branch"]

# Syntax-highlighting theme (kebab-case). Use /theme in the TUI to preview and save.
# You can also add custom .tmTheme files under $CODEX_HOME/themes.
# theme = "catppuccin-mocha"

# Internal tooltip state keyed by model slug. Usually managed by Codex.
# [tui.model_availability_nux]
# "gpt-5.4" = 1

# Enable or disable analytics for this machine. When unset, Codex uses its default behavior.
[analytics]
enabled = true

# Control whether users can submit feedback from `/feedback`. Default: true
[feedback]
enabled = true

# In-product notices (mostly set automatically by Codex).
[notice]
# hide_full_access_warning = true
# hide_world_writable_warning = true
# hide_rate_limit_model_nudge = true
# hide_gpt5_1_migration_prompt = true
# "hide_gpt-5.1-codex-max_migration_prompt" = true
# model_migrations = { "gpt-4.1" = "gpt-5.1" }

################################################################################
# Centralized Feature Flags (preferred)
################################################################################

[features]
# Leave this table empty to accept defaults. Set explicit booleans to opt in/out.
# shell_tool = true
# apps = false
# apps_mcp_gateway = false
# unified_exec = false
# shell_snapshot = false
# multi_agent = false
# personality = true
# use_linux_sandbox_bwrap = false
# runtime_metrics = true
# powershell_utf8 = true
# child_agents_md = false
# sqlite = true
# fast_mode = true
# enable_request_compression = true
# image_generation = false
# skill_mcp_dependency_install = true
# skill_env_var_dependency_prompt = false
# default_mode_request_user_input = false
# artifact = false
# prevent_idle_sleep = false
# responses_websockets = false
# responses_websockets_v2 = false
# image_detail_original = false

################################################################################
# Define MCP servers under this table. Leave empty to disable.
################################################################################

[mcp_servers]

# --- Example: STDIO transport ---
# [mcp_servers.docs]
# enabled = true                       # optional; default true
# required = true                      # optional; fail startup/resume if this server cannot initialize
# command = "docs-server"                 # required
# args = ["--port", "4000"]               # optional
# env = { "API_KEY" = "value" }           # optional key/value pairs copied as-is
# env_vars = ["ANOTHER_SECRET"]            # optional: forward these from the parent env
# cwd = "/path/to/server"                 # optional working directory override
# startup_timeout_sec = 10.0               # optional; default 10.0 seconds
# # startup_timeout_ms = 10000              # optional alias for startup timeout (milliseconds)
# tool_timeout_sec = 60.0                  # optional; default 60.0 seconds
# enabled_tools = ["search", "summarize"]  # optional allow-list
# disabled_tools = ["slow-tool"]           # optional deny-list (applied after allow-list)
# scopes = ["read:docs"]                   # optional OAuth scopes
# oauth_resource = "https://docs.example.com/" # optional OAuth resource

# --- Example: Streamable HTTP transport ---
# [mcp_servers.github]
# enabled = true                          # optional; default true
# required = true                         # optional; fail startup/resume if this server cannot initialize
# url = "https://github-mcp.example.com/mcp"  # required
# bearer_token_env_var = "GITHUB_TOKEN"        # optional; Authorization: Bearer <token>
# http_headers = { "X-Example" = "value" }    # optional static headers
# env_http_headers = { "X-Auth" = "AUTH_ENV" } # optional headers populated from env vars
# startup_timeout_sec = 10.0                   # optional
# tool_timeout_sec = 60.0                      # optional
# enabled_tools = ["list_issues"]             # optional allow-list
# disabled_tools = ["delete_issue"]           # optional deny-list
# scopes = ["repo"]                           # optional OAuth scopes

################################################################################
# Model Providers
################################################################################

# Built-ins include:
# - openai
# - ollama
# - lmstudio

[model_providers]

# --- Example: OpenAI data residency with explicit base URL or headers ---
# [model_providers.openaidr]
# name = "OpenAI Data Residency"
# base_url = "https://us.api.openai.com/v1"        # example with 'us' domain prefix
# wire_api = "responses"                           # only supported value
# # requires_openai_auth = true                    # built-in OpenAI defaults to true
# # request_max_retries = 4                        # default 4; max 100
# # stream_max_retries = 5                         # default 5; max 100
# # stream_idle_timeout_ms = 300000                # default 300_000 (5m)
# # supports_websockets = true                     # optional
# # experimental_bearer_token = "sk-example"       # optional dev-only direct bearer token
# # http_headers = { "X-Example" = "value" }
# # env_http_headers = { "OpenAI-Organization" = "OPENAI_ORGANIZATION", "OpenAI-Project" = "OPENAI_PROJECT" }

# --- Example: Azure/OpenAI-compatible provider ---
# [model_providers.azure]
# name = "Azure"
# base_url = "https://YOUR_PROJECT_NAME.openai.azure.com/openai"
# wire_api = "responses"
# query_params = { api-version = "2025-04-01-preview" }
# env_key = "AZURE_OPENAI_API_KEY"
# env_key_instructions = "Set AZURE_OPENAI_API_KEY in your environment"
# # supports_websockets = false

# --- Example: Local OSS (e.g., Ollama-compatible) ---
# [model_providers.ollama]
# name = "Ollama"
# base_url = "http://localhost:11434/v1"
# wire_api = "responses"

################################################################################
# Apps / Connectors
################################################################################

# Optional per-app controls.
[apps]
# [_default] applies to all apps unless overridden per app.
# [apps._default]
# enabled = true
# destructive_enabled = true
# open_world_enabled = true
#
# [apps.google_drive]
# enabled = false
# destructive_enabled = false            # block destructive-hint tools for this app
# default_tools_enabled = true
# default_tools_approval_mode = "prompt" # auto | prompt | approve
#
# [apps.google_drive.tools."files/delete"]
# enabled = false
# approval_mode = "approve"

################################################################################
# Profiles (named presets)
################################################################################

[profiles]

# [profiles.default]
# model = "gpt-5.4"
# model_provider = "openai"
# approval_policy = "on-request"
# sandbox_mode = "read-only"
# service_tier = "flex"
# oss_provider = "ollama"
# model_reasoning_effort = "medium"
# plan_mode_reasoning_effort = "high"
# model_reasoning_summary = "auto"
# model_verbosity = "medium"
# personality = "pragmatic" # or "friendly" or "none"
# chatgpt_base_url = "https://chatgpt.com/backend-api/"
# model_catalog_json = "./models.json"
# model_instructions_file = "/absolute/or/relative/path/to/instructions.txt"
# experimental_compact_prompt_file = "./compact_prompt.txt"
# tools_view_image = true
# features = { unified_exec = false }

################################################################################
# Projects (trust levels)
################################################################################

[projects]
# Mark specific worktrees as trusted or untrusted.
# [projects."/absolute/path/to/project"]
# trust_level = "trusted"  # or "untrusted"

################################################################################
# Tools
################################################################################

[tools]
# view_image = true

################################################################################
# OpenTelemetry (OTEL) - disabled by default
################################################################################

[otel]
# Include user prompt text in logs. Default: false
log_user_prompt = false
# Environment label applied to telemetry. Default: "dev"
environment = "dev"
# Exporter: none (default) | otlp-http | otlp-grpc
exporter = "none"
# Trace exporter: none (default) | otlp-http | otlp-grpc
trace_exporter = "none"
# Metrics exporter: none | statsig | otlp-http | otlp-grpc
metrics_exporter = "statsig"

# Example OTLP/HTTP exporter configuration
# [otel.exporter."otlp-http"]
# endpoint = "https://otel.example.com/v1/logs"
# protocol = "binary"                         # "binary" | "json"

# [otel.exporter."otlp-http".headers]
# "x-otlp-api-key" = "${OTLP_TOKEN}"

# [otel.exporter."otlp-http".tls]
# ca-certificate = "certs/otel-ca.pem"
# client-certificate = "/etc/codex/certs/client.pem"
# client-private-key = "/etc/codex/certs/client-key.pem"

# Example OTLP/gRPC trace exporter configuration
# [otel.trace_exporter."otlp-grpc"]
# endpoint = "https://otel.example.com:4317"
# headers = { "x-otlp-meta" = "abc123" }

################################################################################
# Windows
################################################################################

[windows]
# Native Windows sandbox mode (Windows only): unelevated | elevated
sandbox = "unelevated"
```

