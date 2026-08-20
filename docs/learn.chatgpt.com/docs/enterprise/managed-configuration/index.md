---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/managed-configuration'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0"]
---

# Managed configuration

Source: https://learn.chatgpt.com/docs/enterprise/managed-configuration

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Managed configuration controls supported local runtime behavior for covered capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension. Supported requirements can differ by client and version. Managed configuration doesn't grant ChatGPT workspace access, assign seats, or replace workspace role-based access control (RBAC). Use [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions) for workspace feature access and this page for local runtime policy.

Enterprise admins can control supported local client behavior in two ways:

- **Requirements**: admin-enforced constraints that users can't override.
- **Managed defaults**: starting values applied when a supported client launches. Users can still change settings during a run; the client reapplies managed defaults the next time it starts.

## Admin-enforced requirements (requirements.toml)

Requirements constrain security-sensitive settings (approval policy, approvals reviewer, automatic review policy, sandbox mode, permission profiles, web search mode, managed hooks, which MCP servers users can enable, and which user-configured plugin marketplace sources they can add, install from, or refresh). When resolving configuration (for example from `config.toml`, [profile files](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles), or CLI config overrides), if a value conflicts with an enforced rule, the local client falls back to a compatible value and notifies the user. If you configure an `mcp_servers` allowlist, the client enables an MCP server only when both its name and identity match an approved entry; otherwise, the client disables it.

Requirements can also constrain [feature flags](https://learn.chatgpt.com/docs/config-file/config-basic#feature-flags) via the `[features]` table in `requirements.toml`. Note that features aren't always security-sensitive, but enterprises can pin values if desired. Omitted keys remain unconstrained.

For Codex 0.138.0 or later, prefer [permission profiles](https://learn.chatgpt.com/docs/permissions)
with `allowed_permission_profiles` and managed `default_permissions`. Use
`allowed_sandbox_modes` only for legacy deployments that still configure
`sandbox_mode`.

For the exact key list, see the [`requirements.toml` section in Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml).

### Locations and precedence

Each supported local client composes requirements from lower to higher precedence:

1. System `requirements.toml` (`/etc/codex/requirements.toml` on Unix systems,
   including Linux and macOS, or `%ProgramData%\OpenAI\Codex\requirements.toml`
   on Windows).
2. Enterprise-managed requirements delivered in the cloud config bundle.
3. Legacy `managed_config.toml` fields that the local client reinterprets as requirements.
4. macOS managed preferences (MDM) delivered through
   `com.openai.codex:requirements_toml_base64`.

Higher-precedence layers override ordinary scalar and list values from lower
layers. Tables merge by key, while requirements such as rules, hooks, and
filesystem restrictions have field-specific composition behavior. Use the
[`requirements.toml` reference](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml)
for the current schema instead of assuming that every field merges the same
way.

For backward compatibility, supported local clients reinterpret the legacy
`approval_policy`, `approvals_reviewer`, and `sandbox_mode` fields as
requirements. This conversion adds compatibility choices where necessary; use
`requirements.toml` for explicit allowlists.

### Cloud-managed requirements

When a user signs in with ChatGPT on a supported plan, supported local clients
can receive admin-enforced requirements associated with the workspace. This is
a delivery channel for `requirements.toml`-compatible policy. It doesn't grant
workspace access or replace workspace RBAC.

Open [Managed configuration](https://chatgpt.com/codex/settings/managed-configs)
to create and assign cloud-managed requirements. For example, this policy limits
approval and sandbox choices and prompts before a supported shell entry point
runs:

```toml
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]

[rules]
prefix_rules = [
  { pattern = [{ any_of = ["bash", "sh", "zsh"] }], decision = "prompt", justification = "Require explicit approval for shell entry points" },
]
```

Confirm that every managed client version supports the keys you select, and
test the policy with a small group before an organization-wide assignment. Use
the configuration reference for the current schema and the administration
surface for current assignment behavior.

The service selects the enterprise-managed requirement layers that apply to the
signed-in identity. The local client evaluates those layers with the other
requirements sources described in [Locations and precedence](#locations-and-precedence).
Use the current administration surface for workspace-side creation and
assignment. Don't rely on a copied group-matching algorithm; the administration
service owns that behavior and can change it independently of the local
requirements format.

For supported keys and examples, see
[Example requirements.toml](#example-requirementstoml) and the
[`requirements.toml` reference](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml).

#### How local clients apply cloud-managed requirements

When a user starts a supported local client and signs in with ChatGPT on a
supported plan, the client first checks for a valid, identity-matched cache
entry. If no valid entry is available, the client fetches the applicable bundle
with retries and writes a signed cache entry on success. If the request fails or
times out and no valid cache is available, the cloud config bundle load returns
an error rather than silently starting without the cloud-managed requirements
layer.

After cache resolution, the client composes the cloud requirements with the
other requirements layers described above. A background refresh can update the
cache for a later start; it doesn't replace the requirements already loaded
into the current process.

### Confirm the admin and employee experience

Assign a person to own each managed policy, record which users or groups should
receive it, and document the business reason for any filesystem, network,
approval, or permission-profile restriction.

Before expanding the rollout, test an approved workflow and an intentionally
disallowed workflow with a representative user. Verify the effective settings
in the supported client rather than assuming a workspace role or group alone
enforces the local restriction.

### Example requirements.toml

This example blocks `--ask-for-approval never` and `--sandbox danger-full-access` (including `--yolo`):

```toml
allowed_approval_policies = ["untrusted", "on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

### Disable Appshots

To disable Appshots for managed users, set the top-level `allow_appshots` requirement:

```toml
allow_appshots = false
```

Where Appshots are available, `allow_appshots = false` disables them. If you
omit the key, requirements don't constrain Appshots, and normal product
availability checks apply. App-server clients that read effective requirements
through `configRequirements/read` receive the same restriction as
`allowAppshots`; an omitted or `null` `allowAppshots` value doesn't disable
Appshots.

### Disable device remote control

To disable [device remote control](https://learn.chatgpt.com/docs/remote-connections#pick-up-work-from-another-device)
for managed users, set the top-level `allow_remote_control` requirement:

```toml
allow_remote_control = false
```

Where device remote control is supported, `allow_remote_control = false`
disables it. If you omit the key, requirements don't constrain device remote
control, and normal product availability checks apply. This requirement doesn't
disable SSH remote connections.

### Control available permission profiles

Use `allowed_permission_profiles` to control which built-in and custom
[permission profiles](https://learn.chatgpt.com/docs/permissions) users can select. This is the
permission-profile counterpart to `allowed_sandbox_modes`; use the allowlist that
matches how your users select permissions.

Permission-profile allowlists require Codex 0.138.0 or later. Codex 0.137.0 and
earlier ignore `allowed_permission_profiles` and managed
`default_permissions`.

Use the permission-profile examples below only after every managed client runs a
supporting release. Don't deploy managed custom profiles until the fleet upgrade
is complete.

When present, the table is the complete list of allowed profiles. It allows
profiles set to `true` and denies profiles omitted or set to `false`, including
built-ins added in future Codex versions.

#### Allow the standard profiles

This policy allows read-only and workspace access, but not full access:

```toml
default_permissions = ":workspace"

[allowed_permission_profiles]
":read-only" = true
":workspace" = true
# ":danger-full-access" is omitted, so it is denied.
```

#### Add a managed least-privilege default

Admins can define a custom profile in the same requirements source. Use
organization-specific profile names that won't collide with names in users'
loaded config. Custom names can't start with `:` or use the reserved `filesystem`
name.

Don't deploy managed custom profiles to clients running Codex 0.137.0 or
earlier. Those clients recognize the profile table but not the managed default
that selects it.

For example:

```toml
default_permissions = "acme_review_only"

[allowed_permission_profiles]
":read-only" = true
":workspace" = true
acme_review_only = true
# ":danger-full-access" is intentionally omitted, so it is denied.

[permissions.acme_review_only]
description = "Review code without modifying the workspace."
extends = ":read-only"
```

#### Allow only enterprise-defined profiles

Omit all built-ins when users should select only admin-defined profiles:

```toml
default_permissions = "acme_workspace"

[allowed_permission_profiles]
acme_workspace = true

[permissions.acme_workspace]
description = "Workspace access with sensitive files denied."
extends = ":workspace"

[permissions.acme_workspace.filesystem]
glob_scan_max_depth = 3

[permissions.acme_workspace.filesystem.":workspace_roots"]
"**/*.env" = "deny"
```

The custom profile can extend `:workspace` even though users can't select the
built-in `:workspace` profile directly.

#### Turn off a profile allowed by another source

Permission allowlists combine by profile name. Because cloud requirements have
higher precedence than system requirements, cloud requirements can use `false`
to turn off a profile allowed by the system file.

Cloud requirements:

```toml
default_permissions = ":read-only"

[allowed_permission_profiles]
":read-only" = true
":workspace" = false
```

System requirements:

```toml
[allowed_permission_profiles]
":read-only" = true
":workspace" = true  # Not honored because cloud requirements set this to false.
```

Set `default_permissions` explicitly to an allowed profile. If it's omitted,
the local runtime defaults to `:workspace` only when both `:workspace` and
`:read-only` are explicitly allowed. When `allowed_permission_profiles` is
absent, managed requirements don't restrict which profile names users can
select. Every entry must name a built-in profile or a custom profile defined in
a loaded config or requirements source. Define custom profiles in managed
requirements to control their behavior centrally.

### Override sandbox requirements by host

Use `[[remote_sandbox_config]]` when one managed policy should apply different
sandbox requirements on different hosts. For example, you can keep a stricter
default for laptops while allowing workspace writes on matching dev boxes or CI
runners. Host-specific entries currently override `allowed_sandbox_modes` only:

```toml
allowed_sandbox_modes = ["read-only"]

[[remote_sandbox_config]]
hostname_patterns = ["*.devbox.example.com", "runner-??.ci.example.com"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

The local runtime compares each `hostname_patterns` entry against the
best-effort resolved host name. It prefers the fully qualified domain name when
available and falls back to the local host name. Matching is case-insensitive;
`*` matches any sequence of characters, and `?` matches one character.

The first matching `[[remote_sandbox_config]]` entry wins within the same
requirements source. If no entry matches, the local runtime keeps the top-level
`allowed_sandbox_modes`. Host name matching is for policy selection only; don't
treat it as authenticated device proof.

You can also constrain web search mode:

```toml
allowed_web_search_modes = ["cached"] # "disabled" remains implicitly allowed
```

`allowed_web_search_modes = []` allows only `"disabled"`.
For example, `allowed_web_search_modes = ["cached"]` prevents live web search even in `danger-full-access` sessions.

### Configure network access requirements

<WarningTip>
  `[experimental_network]` is experimental and may change. Do not enable these
  requirements broadly across an enterprise deployment without validating them
  on the local client versions and operating systems your users run. Windows
  support is still limited; avoid applying this policy to Windows users unless
  you have tested it in your environment.
</WarningTip>

Use `[experimental_network]` in `requirements.toml` when administrators should
define network access requirements centrally. These requirements are separate
from the user `features.network_proxy` toggle: they can configure sandbox
networking without that feature flag, but they don't grant command network
access when the active sandbox keeps networking off. Set
`experimental_network.enabled = true` to activate the managed proxy; an
allowlist alone does not make the proxy active.

```toml
experimental_network.enabled = true
experimental_network.allowed_domains = [
  "api.openai.com",
  "*.example.com",
]
experimental_network.denied_domains = [
  "blocked.example.com",
  "*.exfil.example.com",
]
```

Use `experimental_network.managed_allowed_domains_only = true` only when you
also define administrator-owned `allowed_domains` and want that allowlist to be
exclusive. If it's `true` without managed allow rules, user-added domain allow
rules don't remain effective.

The domain syntax, local/private destination rules, deny-over-allow behavior,
and DNS rebinding limitations are the same as the sandbox networking behavior
described in [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security#network-isolation).

These requirements apply only to local commands that run inside the sandbox.
They do not route or filter web search, apps and connectors, MCP servers,
browser or Computer Use activity, Codex service requests, or Codex cloud
traffic. Use the controls for each surface:

- Use `allowed_web_search_modes` to restrict web search.
- Use `features.apps = false` to disable app and connector integrations, and
  `features.plugins = false` to disable plugins where supported.
- Use the managed `mcp_servers` approved list to restrict MCP servers.
- Use feature requirements such as `browser_use`, `in_app_browser`, and
  `computer_use` to restrict browser and computer-use capabilities.
- Configure Codex cloud network access in its cloud environment settings.

A command domain allowlist does not replace these capability-specific
controls.

### Pin feature flags

You can also pin [feature flags](https://learn.chatgpt.com/docs/config-file/config-basic#feature-flags) for users
receiving a managed `requirements.toml`:

```toml
[features]
personality = true
unified_exec = false

# Disable surface-specific features when needed.
browser_use = false
browser_use_full_cdp_access = false
browser_use_external = false
in_app_browser = false
in_app_updates = false
computer_use = false
```

Use the canonical feature keys from `config.toml`'s `[features]` table for
runtime features. The local runtime normalizes recognized features to meet these
pins and rejects conflicting writes to `config.toml` or profile file feature
settings.

<a id="disable-codex-feature-surfaces"></a>

- `in_app_browser = false` disables the built-in browser pane.
- `in_app_updates = false` disables the ChatGPT desktop app's own updater on
  restart, where supported. It doesn't affect external package deployment or
  extend support for older app versions. For setup and rollout guidance, see
  [Manage app updates](https://learn.chatgpt.com/docs/enterprise/manage-app-updates).
- `browser_use = false` disables Computer Use in browsers and Browser Agent availability.
- `browser_use_full_cdp_access = false` disables full CDP access in the local
  runtime, including Browser Developer mode, and prevents the ChatGPT desktop
  app from enabling the corresponding setting.
- `browser_use_external = false` disables external Browser Use.
- `computer_use = false` disables Computer Use, Record & Replay, and related
  install or setup flows.

If you omit these keys, policy allows the features, subject to normal client,
platform, and rollout availability.

### Restrict locked computer use

To prevent [Computer Use](https://learn.chatgpt.com/docs/computer-use#locked-use) from operating
after a managed Mac locks, add this requirement:

```toml
[computer_use]
allow_locked_computer_use = false
```

This requirement doesn't enable Computer Use. It only prevents locked use on
macOS. If you omit it, requirements don't constrain locked use; normal product
availability and the user's local setting still apply.

### Configure automatic review policy

Use `allowed_approvals_reviewers` to require or allow automatic review. Set it
to `["auto_review"]` to require automatic review, or include `"user"` when users
can choose manual approval.

Set `guardian_policy_config` to replace the tenant-specific section of the
automatic review policy. The local runtime still uses the built-in reviewer
template and output contract. Managed `guardian_policy_config` takes precedence
over local `[auto_review].policy`.

```toml
allowed_approval_policies = ["on-request"]
allowed_approvals_reviewers = ["auto_review"]

guardian_policy_config = """
## Environment Profile
- Trusted internal destinations include github.com/my-org, artifacts.example.com,
  and internal CI systems.

## Tenant Risk Taxonomy and Allow/Deny Rules
- Treat uploads to unapproved third-party file-sharing services as high risk.
- Deny actions that expose credentials or private source code to untrusted
  destinations.
"""
```

### Enforce deny-read requirements

Admins can deny reads for exact paths or glob patterns with
`[permissions.filesystem]`. Users can't weaken these requirements with local
configuration.

```toml
[permissions.filesystem]
deny_read = [
  # values can be absolute paths...
  "/**/*.env",
  # ...or relative to $HOME/%USERPROFILE% using `~`.
  "~/.ssh",
  # But relative paths starting with `./` are not allowed.
]
```

When deny-read requirements are present, the local runtime rejects full-access
permissions and keeps local execution in a read-only or workspace sandbox so it
can enforce them. On native Windows, managed `deny_read` applies to direct file
tools; shell subprocess reads don't use this sandbox rule.

### Enforce managed hooks from requirements

Admins can also define managed lifecycle hooks directly in `requirements.toml`.
Use `[hooks]` for the hook configuration itself, and point `managed_dir` at the
directory where your MDM or endpoint-management tooling installs the referenced
scripts.

To enforce managed hooks even for users who turned hooks off locally, pin
`[features].hooks = true` alongside `[hooks]`. To skip user, project, session,
and plugin hooks while still allowing managed hooks, set
`allow_managed_hooks_only = true`.

```toml
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

Notes:

- The local runtime enforces the hook configuration from `requirements.toml`,
  but it doesn't distribute the scripts in `managed_dir`.
- Deliver those scripts with your MDM or device-management solution.
- Managed hook commands should reference absolute script paths under the
  configured managed directory.
- `allow_managed_hooks_only = true` skips hooks from user, project, session, and
  plugin sources, but still loads hooks from `requirements.toml` and other
  managed config layers.

### Enforce command rules from requirements

Admins can also enforce restrictive command rules from `requirements.toml`
using a `[rules]` table. These rules merge with regular `.rules` files, and the
most restrictive decision still wins.

Unlike `.rules`, requirements rules must specify `decision`, and that decision
must be `"prompt"` or `"forbidden"` (not `"allow"`).

```toml
[rules]
prefix_rules = [
  { pattern = [{ token = "rm" }], decision = "forbidden", justification = "Use git clean -fd instead." },
  { pattern = [{ token = "git" }, { any_of = ["push", "commit"] }], decision = "prompt", justification = "Require review before mutating history." },
]
```

To restrict which MCP servers a local client can enable, add an `mcp_servers`
approved list. For stdio servers, match on `command`; for streamable HTTP
servers, match on `url`:

```toml
[mcp_servers.docs]
identity = { command = "codex-mcp" }

[mcp_servers.remote]
identity = { url = "https://example.com/mcp" }
```

The string form of `identity.command` matches only the configured `command`. It
doesn't inspect `args`, `cwd`, `env`, or `env_vars`.

To constrain a complete stdio invocation, match the executable and each
positional argument:

```toml
[mcp_servers.internal.identity]
command = { executable = "/usr/local/bin/codex-mcp", args = [
  { match = "exact", value = "serve" },
  { match = "prefix", value = "--workspace=" },
] }
```

The executable, argument count, and argument order must match. Argument and URL
rules support `exact`, `prefix`, and full-value `regex` matching. Structured
command rules still don't inspect `cwd`, `env`, or `env_vars`. Plugin-bundled
MCP servers use the same identity shapes under
`plugins.<plugin>.mcp_servers.<server>`.

If `mcp_servers` is present but empty, the local client disables all MCP servers.

### Control plugin availability

To turn off plugins in supported local clients, set `features.plugins` to
`false` in `requirements.toml`:

```toml
features.plugins = false
```

This setting also applies when users sign in to Codex with an API key. See the
[`features.plugins`
reference](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml) for the
supported configuration.

### Restrict plugin marketplace sources

To restrict operations on user-configured marketplace sources, set
`restrict_to_allowed_sources = true` and define one or more source rules:

```toml
[marketplaces]
restrict_to_allowed_sources = true

[marketplaces.allowed_sources.company_plugins]
source = "git"
url = "https://github.com/example/company-plugins.git"
ref = "main"

[marketplaces.allowed_sources.internal_git]
source = "host_pattern"
host_pattern = '^git\.example\.com$'

[marketplaces.allowed_sources.local_plugins]
source = "local"
path = "/opt/company/codex-plugins"
```

Git rules match the normalized repository URL and, when present, an exact
`ref`. Host patterns are regular expressions matched against the lowercase Git
host; use `^` and `$` for a whole-host match. Local rules require an absolute,
normalized path. See the [`requirements.toml` reference](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml)
for the full schema and merge behavior.

These requirements reject unmatched marketplace add, plugin install, and
configured Git marketplace refresh operations for user-configured sources.
Codex-managed OpenAI marketplaces remain available when their source and
reserved name match. The requirements don't filter already configured user
marketplaces or their plugins at runtime.

These source restrictions apply only where a local client supports plugin
marketplace operations: ChatGPT and Codex in the desktop app, and Codex CLI.
They don't control plugin use in ChatGPT on the web or mobile, and they don't
add plugins to the IDE extension.

## Managed defaults (`managed_config.toml`)

Managed defaults set the configuration a supported local client starts with. At
startup, they override the user's local `config.toml` and any CLI `--config`
overrides. Users can still change those settings during the current run, and the
defaults apply again the next time the client starts.

If a managed default, macOS MDM profile, or saved configuration pins `gpt-5.4`
or `gpt-5.4-mini` for users signed in with ChatGPT, update it before August 31, 2026. Replace `gpt-5.4` with `gpt-5.6-terra` and `gpt-5.4-mini` with
`gpt-5.6-luna`. The OpenAI API and Codex authenticated with your own API key
aren't affected. See [workspace model
availability](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability#prepare-for-the-gpt-54-retirement).

Make sure your managed defaults meet your requirements; the local runtime
rejects disallowed values.

### Precedence and layering

The local runtime assembles the effective configuration in this order (top
overrides bottom):

- Managed preferences (macOS MDM; highest precedence)
- `managed_config.toml` (system/managed file)
- `config.toml` (user's base configuration)

CLI `--config key=value` overrides apply to the base, but managed layers override them. This means each run starts from the managed defaults even if you provide local flags.

Cloud-managed requirements affect the requirements layer (not managed defaults). See the Admin-enforced requirements section above for precedence.

### Locations

- Linux/macOS (Unix): `/etc/codex/managed_config.toml`
- Windows/non-Unix: `~/.codex/managed_config.toml`

If the file is missing, the local runtime skips the managed layer.

### macOS managed preferences (MDM)

On macOS, admins can push a device profile that provides base64-encoded TOML payloads at:

- Preference domain: `com.openai.codex`
- Keys:
  - `config_toml_base64` (managed defaults)
  - `requirements_toml_base64` (requirements)

The local runtime parses these "managed preferences" payloads as TOML. For
managed defaults (`config_toml_base64`), managed preferences have the highest
precedence. For requirements (`requirements_toml_base64`), precedence follows
the cloud-managed requirements order described above. The same
requirements-side `[features]` table works in `requirements_toml_base64`; use
canonical feature keys there as well.

### MDM setup workflow

The local runtime honors standard macOS MDM payloads, so you can distribute
settings with tooling like `Jamf Pro`, `Fleet`, or `Kandji`. A lightweight
deployment looks like:

1. Build the managed payload TOML and encode it with `base64` (no wrapping).
2. Drop the string into your MDM profile under the `com.openai.codex` domain at `config_toml_base64` (managed defaults) or `requirements_toml_base64` (requirements).
3. Push the profile, then ask users to restart the supported local client and
   confirm the startup config summary reflects the managed values.
4. When revoking or changing policy, update the managed payload; the client
   reads the refreshed preference the next time it launches.

Avoid embedding secrets or high-churn dynamic values in the payload. Treat the managed TOML like any other MDM setting under change control.

### Example managed_config.toml

```toml
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
