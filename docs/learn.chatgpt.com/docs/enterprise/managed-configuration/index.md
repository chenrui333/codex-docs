---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/managed-configuration'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Managed configuration

Source: https://learn.chatgpt.com/docs/enterprise/managed-configuration

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Managed configuration lets enterprise admins set supported requirements and defaults for ChatGPT Work and Codex. Requirements constrain what users and tasks can do. Defaults provide starting values. Support depends on the product, client version, and execution environment.

For Work with local access and dots, supported Global policy governs the shared cloud orchestrator when managed policy is enabled; applicable local execution requirements govern the connected computer. Work cloud containers retain existing Work Cloud policies, and supported device controls still apply to local execution. Codex keeps its existing configuration behavior. Managed configuration does not grant a workspace seat or feature access. Use [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions) for those controls.

Enterprise admins can control supported local client behavior with:

- **Requirements**: admin-enforced constraints that users can't override.

- **Configuration defaults**: system or cloud-managed `config.toml` settings that users can override.

- **Legacy managed defaults**: `managed_config.toml` starting values applied when a supported client launches. Users can still change settings during a run. The client reapplies these defaults the next time it starts.

See [Agent Security](https://learn.chatgpt.com/docs/enterprise/agent-security) for the Global baseline, environment overrides, and orchestrator and executor field lists.

<a id="agent-security-and-work-sync"></a>

<span
  id="agent-security-and-local-computer-access"
  data-localization-body-anchor
/>

## Agent Security and Local computer access with Work Cloud

Use Agent Security in the Admin Console to manage policies and configuration. It replaces Policies & Configuration. Agent Security will be available to everyone, independently of Local computer access with Work Cloud. Existing policies, assignments, and ordering are preserved. Review your existing policies in Agent Security. Local computer access with Work Cloud is a separate opt-in. See [Agent Security](https://learn.chatgpt.com/docs/enterprise/agent-security) for migration guidance.

Before moving policy automation to **Agent Security**:

1. Identify affected integrations. Inventory Terraform configurations and scripts that update policies, and record which policies they manage.

1. Use the policy API to manage Global settings. To manage Local or Codex Cloud settings, use the Agent Security UI. Existing Global API workflows remain available after migration. Test your scripts and Terraform integrations, and confirm that policy assignments and ordering are unchanged.

1. Make any required changes and test the automation. Verify that an intended update reaches the correct Agent Security policy and that the resulting controls are enforced.

Policy migration does not grant local computer access for Work or dots. Reviewing or creating policies is recommended before rollout, but the confirmation flow does not require policy creation to enable access. Before enabling **Allow local computer access**, review the migrated baseline or create a cloud baseline if your policies are currently delivered only through MDM. If `enforce_residency` is enabled in any cloud policy, **Allow local computer access** is disabled for both Work and dots. This safeguard does not configure workspace residency or, by itself, disable Work Cloud or dots.

Environment overrides vary supported settings within a policy. Within a given policy, the order from highest to lowest is OS-specific environment override → all-OS environment override → Global. A higher-priority policy still wins over a lower-priority policy, even when the lower-priority policy is more specific. Some requirements have field-specific merge rules. Confirm which override editors and fields are available for your workspace.

When managed policy and remote hooks are enabled, Work Cloud with local access and dots use admin-managed remote MCP hooks on the cloud orchestrator. Configure `mcp_tool` handlers in Global `requirements.toml`. Work Cloud without local access and personal accounts do not use these enterprise hooks. Command/shell, prompt, and agent handlers; hooks from local configuration, plugins, or local directories; environment-scoped hooks; and `SessionEnd` MCP hooks are not supported with cloud orchestration, even when tools execute locally. When both orchestration and execution are local, existing supported hooks continue to work in local-only Work and Codex threads. Admins can still configure supported managed hooks in Agent Security for those workflows. Before relying on these hooks, test callback connectivity, required events, and failure behavior. An explicit supported denial can block an action, but a `PreToolUse` callback error, timeout, or malformed response can fail the hook without blocking the tool. MCP hooks do not provide a complete Compliance API audit trail. See the [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference).

## Configure plugin marketplaces and defaults

Define local or Git marketplaces and plugin defaults in system `config.toml`
or the supported configuration defaults in **Agent Security**.
These settings are defaults, not enforced policy.

See [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) for configuration keys,
[Configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic#configuration-precedence)
for overrides, and [repo plugin settings](https://developers.openai.com/plugins/build/plugins#enable-or-disable-a-plugin-for-a-repo)
for project-level configuration. [Workspace GitHub import and
sync](https://learn.chatgpt.com/docs/enterprise/plugin-management) is separate.

## Admin-enforced requirements (requirements.toml)

Requirements constrain security-sensitive settings (approval policy, approvals reviewer, automatic review policy, sandbox mode, permission profiles, web search mode, managed hooks, which MCP servers users can enable, and which plugin marketplace sources they can use). When resolving configuration (for example from `config.toml`, [profile files](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles), or CLI config overrides), if a value conflicts with an enforced rule, the local client falls back to a compatible value and notifies the user. If you configure an `mcp_servers` allowlist, the client enables an MCP server only when both its name and identity match an approved entry; otherwise, the client disables it.

Requirements can also constrain [feature flags](https://learn.chatgpt.com/docs/config-file/config-basic#feature-flags) via the `[features]` table in `requirements.toml`. Note that features aren't always security-sensitive, but enterprises can pin values if desired. Omitted keys remain unconstrained.

For Codex 0.138.0 or later, prefer [permission profiles](https://learn.chatgpt.com/docs/permissions)
with `allowed_permission_profiles` and managed `default_permissions`. Use
`allowed_sandbox_modes` only for legacy deployments that still configure
`sandbox_mode`.

For the exact key list, see the [`requirements.toml` section in Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml).

### Migrate the retired `untrusted` approval policy

Codex and ChatGPT Work no longer support `approval_policy = "untrusted"`.
Remove it from managed defaults, legacy `managed_config.toml`, and any user,
project, profile, or startup configuration that sets it.

For interactive, read-only use, select `approval_policy = "on-request"` with a
read-only sandbox or permission profile allowed by your managed requirements.
Commands allowed by that sandbox can run without approval.

To keep stricter command approvals, omit an explicit `approval_policy`, set
`trust_level = "untrusted"` in the project's entry in user-level
`~/.codex/config.toml`, and keep `untrusted` in `allowed_approval_policies`.
This also disables project-local configuration. Setting `on-request` explicitly
overrides that policy. See
[Migrate from the retired `untrusted` approval policy](https://learn.chatgpt.com/docs/agent-approvals-security#migrate-from-the-retired-untrusted-approval-policy)
for examples and security tradeoffs.

### Locations and precedence

For local execution, requirements are applied from lower to higher priority as follows. This ordering also applies to local steps in Local computer access with Work Cloud:

1. System `requirements.toml` (`/etc/codex/requirements.toml` on Unix systems,
   including Linux and macOS, or `%ProgramData%\OpenAI\Codex\requirements.toml`
   on Windows).
2. Agent Security requirements delivered in the cloud config bundle.
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

### Precedence for Local computer access with Work Cloud

For Work with local access and dots, distinguish Global orchestrator policy from execution policy. Applicable local requirements govern the connected computer. Work cloud containers and dots cloud computers use their own execution configuration and requirements, rather than the managed environment bundle used by other executors.

For local execution, MDM and legacy managed-device requirements rank above Agent Security. The device's system requirements file ranks below Agent Security. Within each policy, resolve OS-specific environment overrides before all-OS environment overrides, then Global. Policy priority wins over specificity across policies.

| Control                       | Local Work without sync and local Codex               | Local computer access with Work Cloud                                                                                                                       |
| ----------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Enterprise requirements       | Follow the local requirements order above.            | Apply to local executors. Work cloud containers retain existing Work Cloud policies.                                                                        |
| Device execution restrictions | Enforced by supported local controls.                 | Follow the local requirements order above, including MDM and legacy requirements above Agent Security.                                                      |
| Environment overrides         | Use the configuration model for the relevant product. | Within one policy: OS-specific environment override, then all-OS environment override, then Global. A lower-priority policy cannot win through specificity. |

Requirements impose constraints, while configuration defaults supply starting values. For Work with local access and dots, supported Global policy applies through the shared cloud orchestrator when managed policy is enabled. Applicable local `requirements.toml` requirements govern execution on a connected computer. Work cloud containers and dots cloud computers use their own execution configuration and requirements, rather than the managed environment bundle used by other executor types. Local execution restrictions do not automatically apply to these cloud computers. Review cloud capability permissions and test local and cloud execution separately.

Keep orchestrator controls, including approvals and web search, in Global. Use the dedicated Allowed approval policies and Allowed web search modes controls where available, and TOML for other supported fields. See the [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) for the field list and execution scope.

### Network policy precedence and runtime limits

Within a given policy, the order from highest to lowest is OS-specific environment override → all-OS environment override → Global. A higher-priority policy still wins over a lower-priority policy, even when the lower-priority policy is more specific. Some requirements have field-specific merge rules. The runtime then enforces the resolved requirements. Consider the field-specific network cases below separately from policy priority.

These examples compare environment and Global settings within the same policy, with managed networking already configured and no higher-priority policy changing the values. They describe field-specific merge and runtime behavior.

#### Set different domain access by environment

For the same domain rule within a policy, an admin environment override can allow a domain denied in Global or deny a domain allowed in Global. Without an environment override, the Global rule is inherited. Other effective Deny rules or access controls can still block a request.

**How domain rules combine**

| Global rule   | Environment rule | Domain-policy result                                                  |
| ------------- | ---------------- | --------------------------------------------------------------------- |
| Deny          | Allow            | Allowed by the environment override, subject to the conditions below. |
| Allow         | Deny             | Blocked in that environment.                                          |
| Allow         | Allow            | Allowed by these domain rules.                                        |
| Deny          | Deny             | Blocked by these domain rules.                                        |
| Allow or Deny | No override      | Inherits the Global rule.                                             |

These outcomes compare the same domain key within one policy, with no higher-priority policy changing the result. A higher-priority value replaces the same key. Other inherited keys remain. An Allow does not bypass a different matching Deny, such as an inherited wildcard. An empty environment map does not clear inherited rules.

**Example:** Deny `packages.example.com` in Global and allow it in Development. Development can permit it under the conditions above. Production inherits the Global Deny unless overridden.

Confirm the deployed executor supports these merge rules. Coverage for regular managed executors still needs validation.

Orchestrator limits. Managed HTTP/SOCKS listener ports and non-loopback proxy listeners are unsupported by the cloud runtime; socket-rule support depends on the execution path. A local-execution setting in the table below is not a supported Orchestrator configuration.

#### Other network runtime limits

All field names below are under `experimental_network` in `requirements.toml`. The arrows show a Global value followed by an environment value within the same policy. These local-execution cases do not establish Orchestrator support for the same settings.

| **Setting and attempted override**           | **Runtime behavior**                                                                                                                                                                      | **Admin action**                                                                                                   |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| domains: deny → allow                        | The environment Allow replaces the same Global domain key on supported paths. Other matching Deny rules still apply.                                                                      | Test both allowed and blocked requests on the deployed executor.                                                   |
| `managed_allowed_domains_only`: true → false | Do not infer exclusivity behavior from domain-key composition. With effective `enabled = true` and `managed_allowed_domains_only = true`, ordinary commands need effective Allow entries. | Review effective settings and inherited Allow entries. A deny-only policy does not allow the rest of the internet. |
| `allow_local_binding`: false → true          | On the supported Codex Cloud proxy path, an explicit false can prevent upstream-proxy access. A supported higher-priority Cloud override can change it.                                   | Check the source of the effective value and executor support. Do not apply the Cloud default to Local.             |

Proxy activation, exclusivity, upstream-proxy behavior, and Unix-socket rules have executor-specific behavior. Do not generalize domain-key composition to these settings. Verify the effective values and test the deployed runtime. For Codex Cloud local/private connectivity, see [Configure network access requirements](#configure-network-access-requirements).

#### Verify behavior before rollout

Test the actual destinations, local listeners, proxy behavior, and socket paths your workflows use. Check an action that should succeed and one that should be blocked in each affected environment. Check that the deployed runtime version supports each setting you use.

### Cloud-managed requirements

When a user signs in with ChatGPT on a supported plan, supported local clients
can receive admin-enforced requirements associated with the workspace. This is
a delivery channel for `requirements.toml`-compatible policy. It doesn't grant
workspace access or replace workspace RBAC. Authentication requirements must be
[managed locally](#manage-authentication-locally).

Open **Agent Security** in the Admin Console to review and manage cloud
requirements. Use the migrated global baseline for existing policies. For
example, this policy limits
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

Check that every managed client version supports the keys you select. Assign the policy to the intended users or groups and verify that it takes effect on their supported clients. Use
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

The local loading and cache behavior below describes supported local clients. It does not establish when a changed cloud policy takes effect in an already-running task using Local computer access with Work Cloud. Verify the effective policy before relying on a changed restriction.

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

Test an allowed workflow and a blocked workflow with a user who has the intended permissions. Check the effective settings in the supported client. A workspace role or group alone does not enforce a local runtime restriction.

### Manage authentication locally

Set `allowed_login_methods`, `allowed_chatgpt_workspaces`,
`cli_auth_credentials_store`, and `chatgpt_base_url` in the local system
`requirements.toml` or macOS MDM requirements. Codex ignores these four fields
in cloud-managed requirements. Local authentication requirements apply before
credentials load and before Codex retrieves cloud policy.

To require ChatGPT login to an approved workspace and store credentials in the
OS credential store, use:

```toml
allowed_login_methods = ["chatgpt"]
allowed_chatgpt_workspaces = ["00000000-0000-0000-0000-000000000000"]
cli_auth_credentials_store = "keyring"
```

`allowed_login_methods` accepts `chatgpt`, `api`, or both. If omitted, this setting
doesn't restrict login methods. If set, the list must contain at least one method.
`api` permits API authentication, including Amazon Bedrock.
The workspace restriction also applies to
[Codex access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens).

User-configured `forced_login_method` and `forced_chatgpt_workspace_id` must
follow the requirements. When a user selects a workspace, it must also appear
in the managed workspace allowlist. If no workspaces match, ChatGPT login is
unavailable. API authentication remains available when permitted. If no login method
is available, Codex refuses to start.

See the [requirements reference](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml)
for credential storage modes and service URL configuration.

### Example requirements.toml

This example blocks `--ask-for-approval never` and `--sandbox danger-full-access` (including `--yolo`):

```toml
allowed_approval_policies = ["untrusted", "on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

Here, `untrusted` preserves the stricter approval behavior derived from
`trust_level = "untrusted"`; it does not make `approval_policy = "untrusted"` a
supported explicit setting.

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
`experimental_network.enabled = true` to activate the managed proxy; domain
rules alone do not make the proxy active.

```toml
[experimental_network]
enabled = true
managed_allowed_domains_only = true

[experimental_network.domains]
"api.openai.com" = "allow"
"**.example.com" = "allow"
"blocked.example.com" = "deny"
"**.exfil.example.com" = "deny"
```

Use `experimental_network.managed_allowed_domains_only = true` only when you
also define administrator-owned `"allow"` entries in
`[experimental_network.domains]` and want those rules to be exclusive. If it's
`true` without managed allow rules, user-added domain allow rules don't remain
effective. Do not combine the canonical `domains` map with the legacy
`allowed_domains` or `denied_domains` lists.

`*.example.com` matches subdomains only. `**.example.com` matches the apex
domain and its subdomains. A matching deny rule wins over an allow rule.

The domain syntax, local/private destination rules, deny-over-allow behavior,
and DNS rebinding limitations are the same as the sandbox networking behavior
described in [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security#network-isolation).

The proxy routes local commands that run inside the sandbox. Browser tools
also check managed network denies and exclusive allowlists before accessing
an origin. This is a separate policy check, not routing browser traffic through
the command proxy. It doesn't filter web search, apps and connectors, MCP
servers, native-app traffic, Codex service requests, or other capability-specific traffic.
Use the controls for each surface:

- Use `allowed_web_search_modes` to restrict web search.
- Use `features.apps = false` to disable app and connector integrations, and
  `features.plugins = false` to disable plugins where supported.
- Use the managed `mcp_servers` approved list to restrict MCP servers.
- Use feature requirements such as `browser_use`, `in_app_browser`, and
  `computer_use` to restrict browser and computer-use capabilities.
- For supported managed Codex Cloud commands, configure Agent Security requirements and the Cloud environment internet settings separately.

A command domain allowlist does not replace these capability-specific
controls.

On supported managed Codex Cloud execution paths, Agent Security requirements constrain command networking. Codex Cloud environment internet settings apply separately. An allowed domain in Agent Security does not override a restriction in the Cloud environment's internet settings. These command-network controls do not, by themselves, disable hosted web search, apps, or MCP. ChatGPT Work Cloud has separate capability permissions and does not inherit these Agent Security requirements.

A managed command allowlist applies to commands using the managed proxy. Where policy permits full sandbox escalation and it is approved, that execution can bypass the command proxy. A narrow network grant is different from full sandbox escalation. Configure enforced approval and sandbox requirements for the intended boundary, and test both ordinary and escalated commands.

> **No effective allowed destinations:** When **Manage Networking** and **Only allow domains added by admins** are On, ordinary managed commands need effective allowed destinations. If no Allow entries are configured or inherited, those commands have no allowed destinations. A deny-only policy does not implicitly allow the rest of the internet. Add required Allow entries and check inherited rules before saving. This restriction applies to the managed command proxy, not every tool or approved full sandbox escalation.

> **Codex Cloud local/private connectivity:** An explicit Off value for local/private connectivity can prevent Codex Cloud from reaching its upstream proxy, even when the destination domain is allowed. Check the final `allow_local_binding` value and identify which policy or setting supplies it. On the supported Cloud proxy path, this defaults to true only when no applicable requirement, selected network profile, or proxy feature setting supplies a value. An inherited false still counts as an explicit setting. Where supported, set a higher-priority Cloud override to change this value for Codex Cloud without changing the Global value used by Local. This does not add domain Allow entries. Verify executor support before relying on the override. Do not apply this Cloud default to Local.

Empty environment requirements inherit Global. Manage Networking Off is not the Cloud environment Internet access Off switch. See [Configure networking in the UI](https://learn.chatgpt.com/docs/enterprise/agent-security#configure-networking-in-the-ui).

### Control browser and Computer Use

Use the `[browser_use]` and `[computer_use]` tables in `requirements.toml` to
restrict supported desktop clients. Validate the policy on the client versions
and operating systems in your deployment. A configured allow rule doesn't
install a plugin, grant an operating-system permission, or approve an action
that still requires review.

For browser access, configure an origin policy. An origin includes the scheme,
host, and optional port, such as `https://example.com` or
`https://*.example.com:8443`. Don't include a path, query, or fragment. Unlike
command-network domain rules, browser origin rules distinguish HTTP from HTTPS
and match the port.

This example restricts browser access to an approved site and prevents uploads
and full Chrome DevTools Protocol (CDP) access there:

```toml
[browser_use]
allow_history_access = false
allow_global_persistent_approval = false

[browser_use.default_origin_policy]
access = "deny"

[browser_use.origins."https://example.com"]
access = "allow"
uploads = "deny"
downloads = "allow"
full_cdp_access = "deny"
persistent_approval = false
access_approval_lifetime = "turn"
```

Matching origin rules are resolved per field. A matching deny wins. Otherwise,
the default origin policy supplies fields that matching rules don't specify.
Local configuration can add restrictions but can't relax a managed deny.
Network denies and exclusive managed network allowlists still apply.

Set `browser_use.disable_auto_review = true` to disable automatic approval
review for browser actions, or set `auto_review = "deny"` on an origin policy
to restrict it for that origin. This controls approval handling; it doesn't
disable model safety monitoring.

For native apps, set a default access policy and identify permitted apps. For
example, this macOS policy allows Calculator and prevents saved approvals:

```toml
[computer_use]
default_app_access = "deny"
allow_persistent_approval = false

[computer_use.macos.bundle_ids]
"com.apple.calculator" = "allow"
```

Windows policies can identify packaged apps with
`computer_use.windows.aumids` or executables with
`computer_use.windows.exes`. Executable rules require `publisher_name`,
`product_name`, and `access`; `binary_name` is optional. Use the app's verified
identity rather than its display name alone.

See the [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml)
for the complete fields and [locked-use restrictions](#restrict-locked-computer-use)
for managed macOS devices.

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

To prevent users from enabling [Locked Use](https://learn.chatgpt.com/docs/computer-use#locked-use)
on a managed Mac, add this requirement:

```toml
[computer_use]
allow_locked_computer_use = false
```

This requirement removes the controls for enabling Locked Use. It doesn't
turn off Locked Use if it's already enabled. If you omit it, normal product
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

When managed policy and remote hooks are enabled, Work Cloud with local access and dots use admin-managed remote MCP hooks on the cloud orchestrator. Configure `mcp_tool` handlers in Global `requirements.toml`. Work Cloud without local access and personal accounts do not use these enterprise hooks. Command/shell, prompt, and agent handlers; hooks from local configuration, plugins, or local directories; environment-scoped hooks; and `SessionEnd` MCP hooks are not supported with cloud orchestration, even when tools execute locally. When both orchestration and execution are local, existing supported hooks continue to work in local-only Work and Codex threads. Admins can still configure supported managed hooks in Agent Security for those workflows.

Before relying on these hooks, test callback connectivity, required events, and failure behavior. An explicit supported denial can block an action, but a `PreToolUse` callback error, timeout, or malformed response can fail the hook without blocking the tool. MCP hooks do not provide a complete Compliance API audit trail. The following script and directory examples retain their Codex scope.

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

To restrict plugin marketplace sources, set
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
configured Git marketplace refresh operations. They also filter configured
marketplaces and their plugins at runtime.

The OpenAI-curated Git marketplaces, including the API-key catalog, must also
match the source allowlist. To allow them, include the following Git source
without a `ref` constraint:

```toml
[marketplaces.allowed_sources.openai_curated]
source = "git"
url = "https://github.com/openai/plugins.git"
```

To exclude the curated catalogs, omit that source and ensure no broader host
rule allows it. Bundled plugins and remotely installed workspace plugins are
separate from this curated Git source policy.

These source restrictions apply only where a local client supports plugin
marketplace operations: ChatGPT and Codex in the desktop app, and Codex CLI.
They don't control plugin use in ChatGPT on the web or mobile, and they don't
add plugins to the IDE extension.

## Managed defaults (`managed_config.toml`)

Managed defaults set the configuration a supported local client starts with. At
startup, they override the user's local `config.toml` and any CLI `--config`
overrides. Users can still change those settings during the current run, and the
defaults apply again the next time the client starts.

If a managed default, macOS MDM profile, or saved configuration pins
`gpt-5.5` for Codex users signed in with ChatGPT, replace it with an available
model before October 14, 2026. Choose `gpt-6-sol` once an administrator has
enabled it for the affected users. GPT-5.5 retires from ChatGPT,
ChatGPT Work, and Codex on all plans on that date. The OpenAI API isn't
affected. See [workspace model availability](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability#prepare-for-the-gpt-55-retirement).

For configurations that still pin `gpt-5.4` or `gpt-5.4-mini`, follow the
[GPT-5.4 migration guidance](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability#prepare-for-the-gpt-54-retirement).

Make sure your managed defaults meet your requirements; the local runtime
rejects disallowed values.

### Precedence and layering

The local runtime assembles the effective configuration in this order (top
overrides bottom):

- Managed preferences (macOS MDM; highest precedence)
- `managed_config.toml` (system/managed file)
- `config.toml` (user's base configuration)

CLI `--config key=value` overrides apply to the base, but managed layers override them. This means each run starts from the managed defaults even if you provide local flags.

Cloud `config.toml` uses [normal configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic#configuration-precedence),
not the legacy ordering above. Cloud `requirements.toml` uses
[requirements precedence](#locations-and-precedence).

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
