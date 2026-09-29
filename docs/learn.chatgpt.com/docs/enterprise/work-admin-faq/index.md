---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/work-admin-faq'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# ChatGPT Work admin FAQ

Source: https://learn.chatgpt.com/docs/enterprise/work-admin-faq

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

ChatGPT Work brings the technology behind Codex into ChatGPT for longer,
multi-step tasks. It can gather context from chats, files, workspace
resources, and connected systems; use approved tools; and create review-ready
outputs. Access, context, actions, network behavior, and credit use vary by
plan, workspace settings, source permissions, and surface.

    {"For general usage and availability, see "}
    [{"ChatGPT Work and Codex"}](https://help.openai.com/articles/20001275)
    {" in the Help Center."}

## Work across devices

<a id="what-does-work-sync-enable"></a>

<span
  id="what-does-local-computer-access-enable"
  data-localization-body-anchor
/>

### What does Local computer access with Work Cloud enable?

Eligible members can continue a Work conversation across desktop, mobile, and web. Tasks using Local computer access with Work Cloud use cloud coordination. For enterprises, the in-app Local/Cloud toggle and its default remain unchanged at launch. Individual steps can still execute in the cloud or use approved resources on a connected computer.

For example, a person can start work with an approved local folder on a laptop, then give follow-up instructions from their phone. Steps that need the laptop still require it to be online and connected.

### How do we enable it?

To enable this feature for the intended users:

1. Enable Work Cloud for the intended users. **Allow local computer access** is nested under Work Cloud. You do not need to enable **Use Codex locally on the ChatGPT desktop app**.

1. Review the cloud policy baseline in **Agent Security**.

1. As a workspace owner, open Workspace settings > Permissions & roles and enable **Allow local computer access**. Complete any policy review and consent steps shown for your workspace. Policy migration can happen before setup. Review policies before rollout; creating policies is not required in the access confirmation flow. See [Local computer access for Work Cloud and dots](https://learn.chatgpt.com/docs/enterprise/cloud-local-access) for separate setup and eligibility requirements.

If `enforce_residency` is enabled in any cloud policy, **Allow local computer access** is disabled for both Work and dots. This safeguard does not configure workspace residency or, by itself, disable Work Cloud or dots.

<span
  id="can-we-enable-sync-if-our-policies-are-delivered-only-through-mdm"
  data-localization-body-anchor
/>

### Can we use this feature if our policies are delivered only through MDM?

Prepare Agent Security policy for supported enterprise requirements during local execution. With Local computer access with Work Cloud enabled, Work cloud containers do not enforce these requirements. MDM delivers requirements to devices.

For local execution, MDM and legacy managed-device requirements rank above Agent Security. The device's system requirements file ranks below Agent Security. This local policy order does not extend enterprise requirement enforcement to Work cloud containers. Work cloud containers continue to use existing Work Cloud policies.

### What if we already use cloud policies?

Use Agent Security in the Admin Console to manage policies and configuration. It replaces Policies & Configuration. Agent Security will be available to everyone, independently of Local computer access with Work Cloud.

Existing policies, assignments, and ordering are preserved. Review your existing policies in Agent Security. Local computer access with Work Cloud is a separate opt-in. See [Agent Security](https://learn.chatgpt.com/docs/enterprise/agent-security) for migration guidance.

Use the policy API to manage Global settings. To manage Local or Codex Cloud settings, use the Agent Security UI. Existing Global API workflows remain available after migration. Test your scripts and Terraform integrations, and confirm that policy assignments and ordering are unchanged.

<span
  id="which-hooks-are-supported-in-synced-work"
  data-localization-body-anchor
/>

### Which hooks are supported in Local computer access with Work Cloud?

When managed policy and remote hooks are enabled, Work Cloud with local access and dots use admin-managed remote MCP hooks on the cloud orchestrator. Configure `mcp_tool` handlers in Global `requirements.toml`. Work Cloud without local access and personal accounts do not use these enterprise hooks. Command/shell, prompt, and agent handlers; hooks from local configuration, plugins, or local directories; environment-scoped hooks; and `SessionEnd` MCP hooks are not supported with cloud orchestration, even when tools execute locally. When both orchestration and execution are local, existing supported hooks continue to work in local-only Work and Codex threads. Admins can still configure supported managed hooks in Agent Security for those workflows.

Before relying on these hooks, test callback connectivity, required events, and failure behavior. An explicit supported denial can block an action, but a `PreToolUse` callback error, timeout, or malformed response can fail the hook without blocking the tool. MCP hooks do not provide a complete Compliance API audit trail.

### Which policy takes priority?

Within a given policy, the order from highest to lowest is OS-specific environment override → all-OS environment override → Global. A higher-priority policy still wins over a lower-priority policy, even when the lower-priority policy is more specific. Some requirements have field-specific merge rules.

For local execution, MDM and legacy managed-device requirements rank above Agent Security. The device's system requirements file ranks below Agent Security.

For Local computer access with Work Cloud, the new enterprise `requirements.toml` configuration applies to local executors. It does not replace existing Work Cloud policies. Managed HTTP/SOCKS listener ports and non-loopback proxy listeners are unsupported by the cloud runtime; socket-rule support depends on the execution path.

### Which Agent Security requirements apply to Work Cloud?

For Work with local access and dots, supported Global policy applies through the shared cloud orchestrator when managed policy is enabled. Applicable local `requirements.toml` requirements govern execution on a connected computer. Work cloud containers and dots cloud computers use their own execution configuration and requirements, rather than the managed environment bundle used by other executor types. Local execution restrictions do not automatically apply to these cloud computers. Review cloud capability permissions and test local and cloud execution separately.

Keep orchestrator controls, including approvals and web search, in Global. Use the dedicated Allowed approval policies and Allowed web search modes controls where available, and TOML for other supported fields. See the [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) for the field list and execution scope.

### What happens if the local computer is unavailable?

Keep the computer online and connected for steps that need its local files or tools. If the computer is unavailable when a new turn starts, an existing eligible task using local computer access with Work Cloud can continue in a cloud container. The cloud container cannot access files or tools on the unavailable computer. It also does not enforce enterprise requirements from local execution. A task cannot switch from local execution to the cloud during a turn.

<a id="what-happens-if-an-admin-turns-work-sync-off"></a>

<span
  id="what-happens-if-an-admin-turns-local-computer-access-off"
  data-localization-body-anchor
/>

### What happens if an admin turns Local computer access with Work Cloud off?

Turning off sync interrupts any currently running turn. Users can send a new message to start a new turn in an existing cloud conversation. That turn automatically uses Work Cloud without access to local files.

Turning off sync does not change data-retention or deletion policies.

### What happens to existing chats and tasks in projects when sync is turned on?

Local computer access with Work Cloud applies only to tasks created after you enable sync. Existing tasks, including tasks in projects, keep their original mode: locally only, or in the cloud without access to local files. Start a new task to use this feature.

### Does this change Codex?

No. Local computer access with Work Cloud does not change Codex's existing configuration behavior, and conversations using this feature do not appear in Codex history.

### Is sync suitable for a ZDR deployment?

No. Local computer access with Work Cloud does not provide strict zero data retention. Data residency and inference residency cover only eligible content and supported workloads, regions, and configurations. Enterprise Key Management (EKM) covers supported stored content in eligible workspaces. Work is not supported with UAE inference residency. Running a step on a connected computer does not make the workflow a ZDR deployment.

## Overview

ChatGPT Work lets users delegate longer, multi-step tasks to ChatGPT. It can gather
information from connected sources, reason across steps, create documents,
presentations, or analyses, and return results for review.

ChatGPT Work is available on supported web, mobile, and desktop surfaces for
eligible plans and workspaces. Where supported, workspace owners or authorized
admins can manage Work Cloud, Work Local, and Codex Local through distinct
permissions. For eligible Enterprise and Edu workspaces, the default workspace
role includes Work unless an authorized administrator turns it off. Browser and
network controls further restrict Work Cloud, and availability depends on role,
plan, workspace, and region. See
[ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex).

For the hosted execution model and security boundaries, see
[ChatGPT Work Overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview).

## Core administrative controls

Administrators govern ChatGPT Work through these control layers:

- **Access to the enterprise workspace:** Identity and access controls manage
  authentication and access to the workspace. Depending on the plan and
  configuration, administrator-controlled identity features can include SSO,
  domain verification, SCIM provisioning, user lifecycle management, and
  identity-group synchronization. SCIM and synchronized identity groups aren't
  included with ChatGPT Business. Users can enable account-level OpenAI MFA.
  ChatGPT doesn't provide workspace-wide MFA enforcement; organizations that
  require it should enforce SSO and MFA through their identity provider. Manage
  SSO and related identity settings in the
  [Global Admin Console](https://help.openai.com/en/articles/12289294-admin-portal).
  See [Multi-factor authentication](https://help.openai.com/en/articles/7967234-enabling-or-disabling-multi-factor-authentication-mfa).
- **Access to ChatGPT Work within the workspace:** Where available, Work Cloud
  governs hosted Work across supported web, mobile, and desktop surfaces. Work
  Local governs local desktop Work, while Codex Local controls supported local
  Codex access in desktop, CLI, and IDE clients. Cloud browser and network
  settings further restrict Work Cloud. Custom role-based access control (RBAC)
  and available permissions depend on the plan and workspace.
- **Group membership:** On plans that support SCIM, synchronize groups through
  an identity provider so access updates as employees join the organization,
  change roles, or leave. See
  [Groups and provisioning](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning).
- **Workspace and member roles:** Built-in Enterprise roles include Owner,
  Admin, Member, and Analytics Viewer. On supported plans, custom roles and
  member RBAC control access to ChatGPT Work, plugins, and other capabilities.
  Where seat types apply, members also need a seat that includes ChatGPT; a
  Codex-only seat doesn't grant access to Work. See
  [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).
- **Plugins and apps:** Plugin policy governs plugin availability and
  installation. App access, action controls, and approval behavior are
  configured separately. Workspace Agents have their own controls where
  available. See [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors),
  [Plugins](https://learn.chatgpt.com/docs/plugins), and the
  [App security white paper](https://cdn.openai.com/business-guides-and-resources/app-security-whitepaper.pdf).
- **Source-system permissions:** A user can access only the content and actions
  allowed by the account or shared connection in the native application. See
  [Admin controls, security, and compliance in apps](https://help.openai.com/en/articles/11509118-admin-controls-security-and-compliance-in-apps-enterprise-edu-and-business).
- **Approval and action restrictions:** For apps that support Action control,
  admins can allow all actions, read-only actions, or a custom set and decide
  how newly added actions are handled. App permissions separately determine
  when ChatGPT asks before using an app.
- **Credits:** ChatGPT Work and Codex share pricing, credits, and usage limits.
  Eligible Enterprise and Edu admins can set monthly per-user limits through a
  workspace default, group defaults, and individual overrides. Users can
  request increases when the workspace allows it. Business follows a separate
  credit and spend-control model. See
  [ChatGPT usage limits and spend controls](https://learn.chatgpt.com/docs/enterprise/usage-limits).
- **Analytics and reporting:** The Global Admin Console and workspace analytics
  support adoption and credit-usage analysis. Use the Compliance API and Codex
  reporting surfaces for their documented event and product scopes; review the
  current schemas before promising coverage of particular prompts, files,
  approvals, actions, errors, or tool calls. See
  [Governance](https://learn.chatgpt.com/docs/enterprise/governance).

## Access, data, systems, and user actions

### How are access to data, systems, and user actions protected?

ChatGPT Work is governed by the identity, access, and permission controls already
established in your ChatGPT workspace. Administrators use identity management,
workspace roles, and, on eligible plans,
[RBAC](https://help.openai.com/en/articles/11750701-rbac) to determine who can
use ChatGPT Work.

Where supported, access can be synchronized with your identity provider through
[SCIM](https://help.openai.com/en/articles/10011769-openai-platform-scim-integration-faq)
and group synchronization. This lets you manage access and permissions centrally
as employees join the organization, change roles, or leave.

Underlying source systems enforce the permissions of the account or approved
shared connection used for the operation. An individual connection uses that
person's source-system access. An agent-owned or shared connection can give
authorized agent users access through the connected account, including data or
actions their own account couldn't access. Restrict the connection's scopes,
available actions, and agent audience to the intended business need. See
[Workspace Agent connections and permissions](https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business).

<a id="how-does-work-access-data-and-context"></a>
<a id="how-does-work-mode-access-data-and-context"></a>

### How does ChatGPT Work access data and context?

ChatGPT Work can use the current chat, uploaded files, workspace resources, and
connected systems through approved apps and, when applicable, plugins.
Depending on enabled capabilities and permissions, this can include documents,
repositories, tickets, channels, email, and calendars. Earlier files can be
available through the current chat, supported projects, authorized Library
access, or enabled automatic Library references. Saved memories follow their
own workspace and user controls.

Each context source keeps its own controls: users supply chat context,
admins manage workspace resources, and connected systems enforce authentication
and permissions. ChatGPT Work can access only information authorized for the user or an
approved shared connection.

ChatGPT Work inherits applicable ChatGPT workspace protections. Residency, retention,
logging, and feature availability vary by plan, region, surface, and connected
system, so confirm coverage for your configuration.

### What high-impact actions are restricted or require review?

Action risk varies. Reading or drafting is generally lower impact than changing
data, sharing information, or acting in external systems. Combine roles, narrow
permissions and credentials, and supported approvals to limit higher-impact
actions to trusted, reviewed use.

Common action categories include:

- **Read:** Access, search, or summarize information from approved sources
  without changing the underlying data.
- **Draft:** Prepare documents, email, reports, code, or other content for a
  person to review before use.
- **Write:** Create, update, or delete records in connected systems, such as
  documents, tickets, repositories, or project-management tools.
- **Share:** Send, publish, or otherwise make information available to more
  people, systems, or external destinations.
- **Schedule:** Start a task at a future time or on a recurring schedule
  without requiring a user to start each run.
- **Execute:** Run code, shell commands, browser automation, or other
  tool-driven tasks that interact directly with external environments.

For higher-impact actions, use human review, restricted credentials, narrow
scopes, and supported approvals. Plugin actions still follow each integration's
permissions and security controls.

## Compliance

<a id="how-does-work-support-enterprise-privacy-and-data-commitments"></a>
<a id="how-does-work-mode-support-enterprise-privacy-and-data-commitments"></a>

### How does ChatGPT Work support enterprise privacy and data commitments?

ChatGPT Work uses the privacy, security, and data commitments applicable to the customer's ChatGPT workspace, subject to plan, configuration, surface, feature, and region. For ChatGPT Enterprise, this includes [no training on business data by default](https://help.openai.com/en/articles/8983130-what-if-i-want-to-keep-my-history-on-but-disable-model-training), encryption in transit and at rest, workspace-level access controls, and supported audit logging.

For Work with local access, residency applies only to eligible content and supported workloads, regions, and configurations; EKM covers supported stored content in eligible workspaces. Work is not supported with UAE inference residency. This experience does not provide strict zero data retention. Dots have separate beta exclusions and do not support data or inference residency. See [compatibility and data requirements](https://learn.chatgpt.com/docs/enterprise/cloud-local-access#check-compatibility-and-data-requirements). HIPAA and Business Associate Agreement coverage depend on the features and agreement in use.

Connected services have their own retention, logging, access, residency, and compliance requirements. When ChatGPT Work uses plugins, repositories, or third-party systems, evaluate both the ChatGPT workspace controls and the connected system's controls.

For Codex activity, enterprise controls can extend to development environments, repositories, configured tools, and related activity. Review [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup) and [Governance](https://learn.chatgpt.com/docs/enterprise/governance) alongside the workspace controls.

### What data is stored, retained, or deleted?

Data retention and deletion for ChatGPT Work are governed by the ChatGPT workspace
plan, administrative settings, and the capabilities in use. Retention can vary
across the information ChatGPT Work accesses. Conversations and eligible Library
files follow their applicable workspace settings. Project files, transient
uploads, saved memories, compliance events, synchronized app data, and
third-party records can have separate retention and deletion rules. See
[Chat and file retention policies](https://help.openai.com/en/articles/8983778-chat-and-file-retention-policies-in-chatgpt).

ChatGPT Work can create chat content, uploaded or generated files, artifacts,
and execution metadata. Codex chats can also create repository or environment
metadata, command output, diffs, and logs. Check the current product and
[Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api) documentation for exact data
classes, retention periods, and deletion paths.

Review retention requirements across both the ChatGPT workspace and connected
enterprise systems so your organization's data governance, compliance, and
record-retention policies apply to each system.

## Observability

### What usage data is available to admins or owners?

Admins and owners can use product analytics and compliance logs for different
kinds of visibility. The Global Admin Console provides supported ChatGPT and
Codex adoption and credit-usage views; available user, product, agent, and model
breakdowns depend on the analytics surface and workspace. For eligible
workspaces, the Compliance API provides covered ChatGPT conversation records,
including supported cloud Work activity. Coverage depends on the product,
surface, permissions, available endpoint, and documented event schema. See
[Workspace analytics](https://learn.chatgpt.com/docs/enterprise/workspace-analytics) and the
[Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api).

### Are prompts, outputs, files, actions, or tool calls logged?

For eligible Enterprise and Edu workspaces, the Compliance Logs Platform
provides Work user prompts and agent responses.
[Connected app calls are separately logged](https://help.openai.com/en/articles/11509118-admin-controls-security-and-compliance-in-apps-enterprise-edu-and-business),
and eligible workspaces can access active Library files through supported
[Library-specific Compliance API endpoints](https://help.openai.com/en/articles/20001052-library-for-chatgpt).
These records don't establish a complete audit trail for every hosted file
operation, shell command, browser interaction, tool invocation, or approval.
Confirm the current event and product coverage in the authenticated Compliance
API documentation.

The Compliance Logs Platform retains data for 30 days. Export records
continuously to an approved electronic discovery, data loss prevention, SIEM,
or data-lake system when your organization requires longer retention. See the
[OpenAI Compliance Platform guide](https://help.openai.com/en/articles/9261474-compliance-api-for-chatgpt-enterprise-edu-and-chatgpt-for-teachers).

Enabling Local computer access with Work Cloud changes what your existing OpenTelemetry (OTel) collector receives. Your local executor can still export supported execution events. Cloud orchestration events do not reach your existing OpenTelemetry collector.

Use the Compliance API for supported cloud records. Changing the collector endpoint does not restore cloud orchestration events. Compliance API records do not replace every event in the earlier OpenTelemetry stream. See [Review OpenTelemetry and audit coverage](https://learn.chatgpt.com/docs/enterprise/cloud-local-access#review-opentelemetry-and-audit-coverage).

### Can unusual behavior, failures, or usage spikes be detected quickly?

Workspace analytics, compliance logs, and connected monitoring tools help
admins review usage and investigate supported ChatGPT, Work, and Codex
activity. Depending on the selected reporting surface, signals can include
active users, supported messages, app activity, agent usage, authentication or
administrative events, and credit consumption. Exported logs can support
electronic discovery, data loss prevention, SIEM, auditing, and investigations.
Detection quality depends on plan, event coverage, attribution, freshness, and
configured rules.

Signals that can warrant review include unexpected increases in usage or credit
consumption, unusual user or agent activity, recurring operational errors, and
relevant authentication or administrative events. Confirm the exact signals
against the applicable analytics, compliance, and audit-log schemas.

For Codex activity, Codex analytics and the Analytics API provide supported
adoption and activity metrics. Organizations using local Codex clients can opt
in to OpenTelemetry exports for events such as API requests, errors, prompt
metadata, tool-approval decisions, and tool results. Prompt contents are
redacted unless `otel.log_user_prompt = true` is enabled as a separate explicit
opt-in. See
[Monitoring and telemetry](https://learn.chatgpt.com/docs/agent-approvals-security#monitoring-and-telemetry).
This local Codex telemetry doesn't provide an OpenTelemetry export for ChatGPT
Work on the web.

## Governance

### How can admins control access, permissions, and policies?

Governance spans three related but separate layers:

- **ChatGPT Work access controls** determine who can use Work and whether local-thread sync is available.

- **Workspace Agent controls** determine who can build, publish, share, schedule, or configure reusable agents and shared connections, where available.

- **Agent Security** holds the global cloud policy baseline for supported Work and Codex controls. For Work with local access and dots, supported Global policy applies to cloud orchestration when managed policy is enabled. Local execution requirements govern the connected computer; cloud computers use their own execution configuration and requirements. Codex retains its existing configuration behavior.

[Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) constrains supported runtime behavior. It doesn't grant workspace access, replace RBAC, or revoke a user's workspace access. These layers aren't one uniform ChatGPT Work policy surface. Analytics and compliance logs provide more visibility within their documented product and event scopes.

For supported local Codex clients, enterprise administrators can apply
[managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) and
[permission profiles](https://learn.chatgpt.com/docs/permissions). Those local-client controls don't
grant access to, or replace the workspace permissions for, hosted ChatGPT Work.

### Can access be scoped by group, role, workspace, or capability?

Yes. On eligible Enterprise and Edu plans that support custom member RBAC,
ChatGPT Work capabilities can be scoped with workspace roles, identity groups,
and administrator-defined permissions. ChatGPT Business uses applicable
workspace-level controls but doesn't include custom member RBAC or SCIM group
synchronization. Assign supported capabilities based on business need and
organizational policy. See the
[RBAC guide](https://help.openai.com/en/articles/11750701-rbac) and this
[RBAC walkthrough](https://vimeo.com/1207482321/d1286e4467?share=copy&fl=sv&fe=ci).

Where custom RBAC is available, organizations can use it to determine which
users can access ChatGPT Work, manage workspace settings, configure approved
plugins, or use supported Workspace Agent features. For eligible Enterprise and
Edu workspaces, monthly usage limits can support a phased rollout through a
workspace default, group defaults, and user overrides.

Access to connected systems remains independently governed. Scope plugins, shared
credentials, repositories, and write-capable actions to the minimum required
audience using workspace permissions, plugin settings, and the source system's
controls. For supported local Codex clients, managed configuration can further
restrict local runtime capabilities. Hosted Work follows its own workspace and
product-specific controls.

### How are runtime and network boundaries governed?

The security boundaries for ChatGPT Work depend on the task. A standard Chat conversation, a
connected workflow, a scheduled task, and a Codex chat can run in different
environments with different permissions, tools, and network access.

Govern each execution environment through its applicable controls. Work Cloud
governs hosted Work across supported web, mobile, and desktop surfaces. Work
Local governs local desktop Work, and Codex Local controls supported local
Codex access in desktop, CLI, and IDE clients. Browser and shell network
permissions further restrict Work Cloud. Search, apps, plugins, available
Workspace Agents, and source-system permissions remain separate controls.
Applicable managed configuration and local runtime policies govern only their
supported local experiences. These controls aren't interchangeable.

For Codex activity, local runs in the ChatGPT desktop app, CLI, and IDE execute
on the user's machine with operating-system sandboxing and approval policies.
Codex cloud runs chats in isolated OpenAI-managed environments. For supported
local clients, enterprise administrators can use managed requirements to
constrain permission profiles, approvals, filesystem and network access, MCP
servers, hooks, command rules, and other supported runtime behavior.

## Usage and cost

<a id="how-does-work-usage-translate-into-spend-over-time"></a>
<a id="how-does-work-mode-usage-translate-into-spend-over-time"></a>

### How does ChatGPT Work usage translate into spend over time?

[ChatGPT Work and Codex share pricing, credits, and usage limits](https://learn.chatgpt.com/docs/pricing).
For eligible credit-based agreements, review employees' combined Chat and Work
usage against the shared workspace credit allocation. Consumption varies with
the model, applicable reasoning or speed settings, processed input and output,
and eligible tools or features.

Using committed credits doesn't automatically increase your invoice. Actual
charges depend on the remaining credit balance, contracted rates, account
overage eligibility, and configured workspace overage limit. For planning
examples, effective user limits, reporting boundaries, and billing details,
see [ChatGPT Work: usage and cost](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-usage-and-cost).

The highest-variance patterns are often workflows that run frequently,
retrieve or process large amounts of information, call multiple tools or apps,
retry after failures, or produce large artifacts. Cost-sensitive examples
include scheduled or recurring work, large files, broad
retrieval across enterprise sources, repeated app calls, and Codex chats that
process repositories, run commands, or use cloud environments. Workspace Agent
API triggers can also add usage where available.

Use spend controls, usage analytics, and reporting to monitor these patterns
over time. Review usage by the dimensions supported in the current analytics
surface and adjust limits or rollout scope based on business value. Don't treat
aggregated analytics as exact per-workflow cost attribution.

Workspace analytics, compliance logs, and connected monitoring tools can help
administrators review usage and investigate supported activity. The ability to
detect risky or unusual behavior depends on plan, log coverage, attribution,
data freshness, and the rules configured in your monitoring systems.

### What usage limits, alerts, or caps are available?

Eligible Enterprise and Edu workspaces can use monthly per-user limits and
workspace-wide spend controls for credit-based usage:

- **Monitor credit consumption:** Review supported credit-usage reports in the
  Global Admin Console and workspace settings.
- **Set a default monthly limit:** Establish a default per-user credit limit
  for the workspace.
- **Apply group-specific limits:** Give groups monthly per-user defaults that
  reflect their workflows, responsibilities, or rollout stage.
- **Create user overrides:** Give a specific user a different limit without
  changing the default for the entire group.
- **Review increase requests:** If requests are enabled, users can request a
  higher monthly limit. Approval creates a user override.
- **Control overall workspace exposure:** Configure workspace credit alerts and
  the overage limit separately in the Global Admin Console. Alerts notify
  recipients; the overage limit controls eligible usage after the committed
  credit pool is exhausted.
- **Export usage data:** Eligible Enterprise administrators can access
  credit-usage data through the unified Cost API for internal reporting or
  monitoring.

Users can view their own usage and, if enabled, request more credits, but they
can't change assigned limits. See
[Manage usage limits and overages](https://help.openai.com/en/articles/20001001-manage-usage-limits-and-overages-in-chatgpt-enterprise-and-edu)
and the
[spend-controls walkthrough](https://vimeo.com/1207484127/0f2029dd01?share=copy&fl=sv&fe=ci).

## Incident and revocation controls

### How can admins stop access or activity?

During user removal or incident review, admins might need to stop access,
disable apps, revoke shared credentials, pause scheduled tasks, or revoke Codex
credentials.

Revocation paths include:

- Remove a user's workspace or group access. For SCIM-managed users, remove
  access at the identity provider; otherwise, a later synchronization can
  provision the user again.
- Disable or restrict the relevant plugin or app.
- Revoke a shared connection, bot, or service account through its owning
  surface. Workspace owners and admins can separately revoke Codex workspace
  access tokens.
- Remove a Workspace Agent from publication or delete it through its agent owner
  or workspace administrator.
- Disable the relevant scheduled task or, where available, Workspace Agent API
  trigger.
- For Codex access, separately revoke the relevant access token, repository
  connection, and cloud-environment access. Managed configuration isn't an
  access-revocation mechanism.

## Additional resources for your teams

| Topic                    | Use this when explaining                                                      | Learn ChatGPT page                                               |
| ------------------------ | ----------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Work overview            | How cloud execution, browser access, network policy, and data boundaries work | [ChatGPT Work Overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) |
| Workspace setup and RBAC | Who can use and administer Codex                                              | [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)             |
| Authentication           | How ChatGPT sign-in, API key sign-in, and workspace policy differ             | [Authentication](https://learn.chatgpt.com/docs/auth)                                    |
| Approvals and sandboxing | How Codex controls file, command, network, and side-effecting tool actions    | [Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)  |
| Managed policy           | How admins enforce Codex settings users can't override                        | [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) |
| Runtime environments     | How Codex cloud setup, secrets, caches, and task phases work                  | [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment)      |
| Internet access          | How Codex cloud domain allowlists and HTTP methods work                       | [Agent internet access](https://learn.chatgpt.com/docs/cloud/internet-access)            |
| Permissions              | How filesystem, network, and deny-read controls work                          | [Permissions](https://learn.chatgpt.com/docs/permissions)                                |
| Observability            | How analytics, reporting, and compliance exports work                         | [Governance](https://learn.chatgpt.com/docs/enterprise/governance)                       |
| Automation credentials   | How access tokens are created, limited, revoked, and audited                  | [Access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens)                 |

## Recommended admin actions

- **Choose who needs ChatGPT Work.** Identify the users or groups and the tasks they need to complete, then grant access through the supported workspace and role settings.
- **Set roles and permissions.** In **Permissions & roles**, grant ChatGPT Work access to the intended users or groups. Check all assigned roles to confirm their effective access.
- **Review plugins and data sources.** ChatGPT Work is most useful with approved
  business context such as files, email, calendars, Slack, or CRM. Review
  enabled plugins, their audiences, and whether app policies still match how users
  should delegate work.
- **Set expectations for appropriate use cases.** Position ChatGPT Work for multi-step,
  higher-value tasks such as research, synthesis, analysis, file creation,
  workflow updates, and reusable outputs. Use Chat for quick questions,
  light rewrites, or brainstorming.
- **Set credit and usage controls.** ChatGPT Work can use more credits than a standard Chat conversation because tasks can run longer. Configure workspace defaults, group defaults, and user overrides. Give users guidance on choosing the right model and effort for each task.
- **Identify your first high-value workflows.** Start with clear, reviewable
  outcomes such as customer briefings, recurring reports, research synthesis,
  tracker updates, or polished documents and slides.
- **Prepare champions and support teams.** Give champions, training leads,
  and support teams rollout resources first so they can answer questions,
  collect feedback, and model effective delegation.
- **Explain review and approval expectations.** Tell users to check outputs and important claims before using or sharing them, and to approve consequential actions before they run.
- **Monitor adoption and adjust.** Review usage, feedback, credit consumption,
  and delegated work after rollout. Use the findings to adjust access,
  guidance, training, and expansion.
