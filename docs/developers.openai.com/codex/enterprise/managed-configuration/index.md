---
source_type: 'developers'
source_area: 'codex_enterprise'
source_url: 'https://developers.openai.com/codex/enterprise/managed-configuration'
source_last_modified: '2026-06-16T15:40:49Z'
source_etag: 'W/"7822808797f9dea493c71f03e4c89d7d"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0"]
---

# Managed configuration – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/enterprise/managed-configuration

Enterprise admins can control local Codex behavior in two ways:

- **Requirements**: admin-enforced constraints that users can’t override.
- **Managed defaults**: starting values applied when Codex launches. Users can still change settings during a session; Codex reapplies managed defaults the next time it starts.

## Admin-enforced requirements (requirements.toml)

Requirements constrain security-sensitive settings (approval policy, approvals reviewer, automatic review policy, sandbox mode, permission profiles, web search mode, managed hooks, and optionally which MCP servers users can enable). When resolving configuration (for example from `config.toml`, [profile files](/codex/config-advanced#profiles), or CLI config overrides), if a value conflicts with an enforced rule, Codex falls back to a compatible value and notifies the user. If you configure an `mcp_servers` allowlist, Codex enables an MCP server only when both its name and identity match an approved entry; otherwise, Codex disables it.

Requirements can also constrain [feature flags](/codex/config-basic/#feature-flags) via the `[features]` table in `requirements.toml`. Note that features aren’t always security-sensitive, but enterprises can pin values if desired. Omitted keys remain unconstrained.

For Codex 0.138.0 or later, prefer [permission profiles](/codex/permissions)
with `allowed_permission_profiles` and managed `default_permissions`. Use
`allowed_sandbox_modes` only for legacy deployments that still configure
`sandbox_mode`.

For the exact key list, see the [`requirements.toml` section in Configuration Reference](/codex/config-reference#requirementstoml).

### Locations and precedence

Codex checks requirement sources in this order. If the same setting appears more
than once, the first value wins:

1. Cloud-managed requirements (ChatGPT Business or Enterprise)
2. macOS managed preferences (MDM) via `com.openai.codex:requirements_toml_base64`
3. System `requirements.toml` (`/etc/codex/requirements.toml` on Unix systems, including Linux/macOS, or `%ProgramData%\OpenAI\Codex\requirements.toml` on Windows)

Codex checks these sources from top to bottom. For ordinary settings and lists,
it uses the first value it finds. A later source can still provide a setting
that earlier sources leave unset.

Tables combine one entry at a time. For `allowed_permission_profiles`, a later
source can add profile names that earlier sources don’t mention. If two sources
set the same profile name, the earlier source wins.

For backwards compatibility, Codex also interprets legacy `managed_config.toml` fields `approval_policy` and `sandbox_mode` as requirements (allowing only that single value).

### Cloud-managed requirements

When you sign in with ChatGPT on a Business or Enterprise plan, Codex can also fetch admin-enforced requirements from the Codex service. This is another source of `requirements.toml`-compatible requirements. This applies across Codex surfaces, including the CLI, App, and IDE Extension.

#### Configure cloud-managed requirements

Go to the [Codex managed-config page](https://chatgpt.com/codex/settings/managed-configs).

Create a new managed requirements file using the same format and keys as `requirements.toml`.

```
enforce_residency = "us"
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]

[rules]
prefix_rules = [
  { pattern = [{ any_of = ["bash", "sh", "zsh"] }], decision = "prompt", justification = "Require explicit approval for shell entrypoints" },
]
```

Save the configuration. Once saved, the updated managed requirements apply immediately for matching users.
For more examples, see [Example requirements.toml](#example-requirementstoml).

#### Assign requirements to groups

Admins can configure different managed requirements for different user groups, and also set a default fallback requirements policy.

If a user matches more than one group-specific rule, the first matching rule applies. Codex doesn’t fill unset fields from later matching group rules.

For example, if the first matching group rule sets only `allowed_sandbox_modes = ["read-only"]` and a later matching group rule sets `allowed_approval_policies = ["on-request"]`, Codex applies only the first matching group rule and doesn’t fill `allowed_approval_policies` from the later rule.

#### How Codex applies cloud-managed requirements locally

When a user starts Codex and signs in with ChatGPT on a Business or Enterprise plan, Codex applies managed requirements on a best-effort basis. Codex first checks for a valid, unexpired local managed requirements cache entry and uses it if available. If the cache is missing, expired, corrupted, or doesn’t match the current auth identity, Codex attempts to fetch managed requirements from the service (with retries) and writes a new signed cache entry on success. If no valid cached entry is available and the fetch fails or times out, Codex continues without the managed requirements layer.

After cache resolution, Codex enforces managed requirements as part of the normal requirements layering described above.

### Example requirements.toml

This example blocks `--ask-for-approval never` and `--sandbox danger-full-access` (including `--yolo`):

```
allowed_approval_policies = ["untrusted", "on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

### Disable Appshots

To disable Appshots for managed users, set the top-level `allow_appshots` requirement:

```
allow_appshots = false
```

Codex treats only `allow_appshots = false` as disabling Appshots. If the key is omitted, Appshots remain unconstrained by requirements and use normal product availability checks. App-server clients that read effective requirements through `configRequirements/read` receive the same restriction as `allowAppshots`; an omitted or `null` `allowAppshots` value doesn’t disable Appshots.

### Disable device remote control

To disable [device remote control](/codex/remote-connections#pick-up-work-from-another-device)
for managed users, set the top-level `allow_remote_control` requirement:

```
allow_remote_control = false
```

Codex treats only `allow_remote_control = false` as disabling device remote
control. If the key is omitted, device remote control remains unconstrained by
requirements and uses normal product availability checks. This requirement does
not disable SSH remote connections.

### Control available permission profiles

Use `allowed_permission_profiles` to control which built-in and custom
[permission profiles](/codex/permissions) users can select. This is the
permission-profile equivalent of `allowed_sandbox_modes`; use the allowlist that
matches how your users select permissions.

Permission-profile allowlists require Codex 0.138.0 or later. Codex 0.137.0 and
earlier ignore `allowed_permission_profiles` and managed
`default_permissions`.

Use the permission-profile examples below only after every managed client runs a
supporting release. Don’t deploy managed custom profiles until the fleet upgrade
is complete.

When the table is present, it’s the complete list of allowed profiles. Profiles
set to `true` are allowed. Profiles that are omitted or set to `false` are
denied, including built-ins added in future Codex versions.

#### Allow the standard profiles

This policy allows read-only and workspace access, but not full access:

```
default_permissions = ":workspace"

[allowed_permission_profiles]
":read-only" = true
":workspace" = true
# ":danger-full-access" is omitted, so it is denied.
```

#### Add a managed least-privilege default

Admins can define a custom profile in the same requirements source. Use
organization-specific profile names that won’t collide with names in users’
loaded config. Custom names can’t start with `:` or use the reserved `filesystem`
name.

Don’t deploy managed custom profiles to clients running Codex 0.137.0 or
earlier. Those clients recognize the profile table but not the managed default
that selects it.

For example:

```
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

```
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

The custom profile can extend `:workspace` even though users can’t select the
built-in `:workspace` profile directly.

#### Turn off a profile allowed by another source

Permission allowlists combine by profile name. Because Codex checks cloud
requirements before system requirements, cloud requirements can use `false` to
turn off a profile allowed by the system file.

Cloud requirements:

```
default_permissions = ":read-only"

[allowed_permission_profiles]
":read-only" = true
":workspace" = false
```

System requirements:

```
[allowed_permission_profiles]
":read-only" = true
":workspace" = true  # Not honored because cloud requirements set this to false.
```

Set `default_permissions` explicitly to an allowed profile. If it’s omitted,
Codex defaults to `:workspace` only when both `:workspace` and `:read-only` are
explicitly allowed. When `allowed_permission_profiles` is absent, managed
requirements don’t restrict which profile names users can select. Every entry
must name a built-in profile or a custom profile defined in a loaded config or
requirements source. Define custom profiles in managed requirements when their
behavior should be controlled centrally.

### Override sandbox requirements by host

Use `[[remote_sandbox_config]]` when one managed policy should apply different
sandbox requirements on different hosts. For example, you can keep a stricter
default for laptops while allowing workspace writes on matching dev boxes or CI
runners. Host-specific entries currently override `allowed_sandbox_modes` only:

```
allowed_sandbox_modes = ["read-only"]

[[remote_sandbox_config]]
hostname_patterns = ["*.devbox.example.com", "runner-??.ci.example.com"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

Codex compares each `hostname_patterns` entry against the best-effort resolved
host name. It prefers the fully qualified domain name when available and falls
back to the local host name. Matching is case-insensitive; `*` matches any
sequence of characters, and `?` matches one character.

The first matching `[[remote_sandbox_config]]` entry wins within the same
requirements source. If no entry matches, Codex keeps the top-level
`allowed_sandbox_modes`. Host name matching is for policy selection only; don’t
treat it as authenticated device proof.

You can also constrain web search mode:

```
allowed_web_search_modes = ["cached"] # "disabled" remains implicitly allowed
```

`allowed_web_search_modes = []` allows only `"disabled"`.
For example, `allowed_web_search_modes = ["cached"]` prevents live web search even in `danger-full-access` sessions.

### Configure network access requirements

Use `[experimental_network]` in `requirements.toml` when administrators should
define network access requirements centrally. These requirements are separate
from the user `features.network_proxy` toggle: they can configure sandboxed
networking without that feature flag, but they don’t grant command network
access when the active sandbox keeps networking off.

```
experimental_network.enabled = true
experimental_network.dangerously_allow_all_unix_sockets = true
experimental_network.allow_local_binding = true
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
exclusive. If it’s `true` without managed allow rules, user-added domain allow
rules don’t remain effective.

The domain syntax, local/private destination rules, deny-over-allow behavior,
and DNS rebinding limitations are the same as the sandboxed networking behavior
described in [Agent approvals & security](/codex/agent-approvals-security#network-isolation).

### Pin feature flags

You can also pin [feature flags](/codex/config-basic/#feature-flags) for users
receiving a managed `requirements.toml`:

```
[features]
personality = true
unified_exec = false

# Disable specific Codex feature surfaces when needed.
browser_use = false
browser_use_full_cdp_access = false
in_app_browser = false
computer_use = false
```

Use the canonical feature keys from `config.toml`’s `[features]` table. Codex normalizes the resulting feature set to meet these pins and rejects conflicting writes to `config.toml` or profile file feature settings.

- `in_app_browser = false` disables the in-app browser pane.
- `browser_use = false` disables Browser Use and Browser Agent availability.
- `browser_use_full_cdp_access = false` prevents users from enabling full CDP
  access in Browser Developer mode.
- `computer_use = false` disables Computer Use availability and related
  install or setup flows.

If omitted, these features are allowed by policy, subject to normal client,
platform, and rollout availability.

### Restrict locked computer use

To prevent [Computer Use](/codex/app/computer-use#locked-use) from operating
after a managed Mac locks, add this requirement:

```
[computer_use]
allow_locked_computer_use = false
```

This requirement doesn’t enable Computer Use. It only prevents locked use on
macOS. If you omit it, locked use remains unconstrained by requirements and is
still subject to normal product availability and the user’s local setting.

### Configure automatic review policy

Use `allowed_approvals_reviewers` to require or allow automatic review. Set it
to `["auto_review"]` to require automatic review, or include `"user"` when users
can choose manual approval.

Set `guardian_policy_config` to replace the tenant-specific section of the
automatic review policy. Codex still uses the built-in reviewer template and
output contract. Managed `guardian_policy_config` takes precedence over local
`[auto_review].policy`.

```
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
`[permissions.filesystem]`. Users can’t weaken these requirements with local
configuration.

```
[permissions.filesystem]
deny_read = [
  # values can be absolute paths...
  "/**/*.env",
  # ...or relative to $HOME/%USERPROFILE% using `~`.
  "~/.ssh",
  # But relative paths starting with `./` are not allowed.
]
```

When deny-read requirements are present, Codex rejects full-access permissions
and keeps local execution in a read-only or workspace sandbox so it can enforce
them. On native Windows, managed `deny_read` applies to direct file tools; shell
subprocess reads don’t use this sandbox rule.

### Enforce managed hooks from requirements

Admins can also define managed lifecycle hooks directly in `requirements.toml`.
Use `[hooks]` for the hook configuration itself, and point `managed_dir` at the
directory where your MDM or endpoint-management tooling installs the referenced
scripts.

To enforce managed hooks even for users who disabled hooks locally, pin
`[features].hooks = true` alongside `[hooks]`. To skip user, project, session,
and plugin hooks while still allowing managed hooks, set
`allow_managed_hooks_only = true`.

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

Notes:

- Codex enforces the hook configuration from `requirements.toml`, but it does
  not distribute the scripts in `managed_dir`.
- Deliver those scripts separately with your MDM or device-management solution.
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

## Managed defaults (`managed_config.toml`)

Managed defaults merge on top of a user’s local `config.toml` and take precedence over any CLI `--config` overrides, setting the starting values when Codex launches. Users can still change those settings during a session; Codex reapplies managed defaults the next time it starts.

Make sure your managed defaults meet your requirements; Codex rejects disallowed values.

### Precedence and layering

Codex assembles the effective configuration in this order (top overrides bottom):

- Managed preferences (macOS MDM; highest precedence)
- `managed_config.toml` (system/managed file)
- `config.toml` (user’s base configuration)

CLI `--config key=value` overrides apply to the base, but managed layers override them. This means each run starts from the managed defaults even if you provide local flags.

Cloud-managed requirements affect the requirements layer (not managed defaults). See the Admin-enforced requirements section above for precedence.

### Locations

- Linux/macOS (Unix): `/etc/codex/managed_config.toml`
- Windows/non-Unix: `~/.codex/managed_config.toml`

If the file is missing, Codex skips the managed layer.

### macOS managed preferences (MDM)

On macOS, admins can push a device profile that provides base64-encoded TOML payloads at:

- Preference domain: `com.openai.codex`
- Keys:
  - `config_toml_base64` (managed defaults)
  - `requirements_toml_base64` (requirements)

Codex parses these “managed preferences” payloads as TOML. For managed defaults (`config_toml_base64`), managed preferences have the highest precedence. For requirements (`requirements_toml_base64`), precedence follows the cloud-managed requirements order described above. The same requirements-side `[features]` table works in `requirements_toml_base64`; use canonical feature keys there as well.

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

