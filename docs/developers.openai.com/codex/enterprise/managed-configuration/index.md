# Managed configuration

Source: https://developers.openai.com/codex/enterprise/managed-configuration

Enterprise admins can control local Codex behavior in two ways:

- **Requirements**: admin-enforced constraints that users can’t override.
- **Managed defaults**: starting values applied when Codex launches. Users can still change settings during a session; Codex reapplies managed defaults the next time it starts.

## Admin-enforced requirements (requirements.toml)

Requirements constrain security-sensitive settings (approval policy, sandbox mode, web search mode, and optionally which MCP servers can be enabled). When resolving configuration (for example from `config.toml`, profiles, or CLI config overrides), if a value conflicts with an enforced requirement, Codex falls back to a requirements-compatible value and notifies the user. If an `mcp_servers` allowlist is configured, Codex enables an MCP server only when both its name and identity match an approved entry; otherwise, Codex disables it.

Requirements can also be used to constrain [feature flags](/codex/config-basic/#feature-flags) via the `[features]` table in `requirements.toml`. Note features are generally not security-sensitive, but enterprises have the option of pinning values, if desired. Omitted keys remain unconstrained.

For the exact key list, see the [`requirements.toml` section in Configuration Reference](/codex/config-reference#requirementstoml).

### Locations and precedence

Requirements layers are applied in this order (earlier wins per field):

1. Cloud-managed requirements (ChatGPT Business or Enterprise)
2. macOS managed preferences (MDM) via `com.openai.codex:requirements_toml_base64`
3. System `requirements.toml` (`/etc/codex/requirements.toml` on Unix systems, including Linux/macOS)

Across layers, requirements are merged per field: if an earlier layer sets a field (including an empty list), later layers do not override that field, but lower layers can still fill fields that remain unset.

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

If a user matches multiple group-specific rules, the first matching rule applies. Codex does not fill unset requirement fields from later matching group rules.

For example, if the first matching group rule sets only `allowed_sandbox_modes = ["read-only"]` and a later matching group rule sets `allowed_approval_policies = ["on-request"]`, Codex applies only the first matching group rule and does not fill `allowed_approval_policies` from the later rule.

#### How Codex applies cloud-managed requirements locally

When a user starts Codex and signs in with ChatGPT on a Business or Enterprise plan, Codex applies managed requirements on a best-effort basis. Codex first checks for a valid, unexpired local managed requirements cache entry and uses it if available. If the cache is missing, expired, invalid, or does not match the current auth identity, Codex attempts to fetch managed requirements from the service (with retries) and writes a new signed cache entry on success. If no valid cached entry is available and the fetch fails or times out, Codex continues without the managed requirements layer.

After cache resolution, managed requirements are enforced as part of the normal requirements layering described above.

### Example requirements.toml

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

You can also pin [feature flags](/codex/config-basic/#feature-flags):

```
[features]
personality = true
unified_exec = false
```

Use the canonical feature keys from `config.toml`’s `[features]` table. Codex normalizes the effective feature set to satisfy these pins and rejects conflicting writes to `config.toml` or profile-scoped feature settings.

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

