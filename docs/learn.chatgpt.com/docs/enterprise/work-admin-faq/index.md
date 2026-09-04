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

This FAQ explains how admins manage ChatGPT Work: access and data controls,
compliance and visibility, usage and spend, incident response, and rollout
practices. For the hosted execution model and security boundaries, see
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

ChatGPT Work uses the privacy, security, and data commitments applicable to the
customer's ChatGPT workspace, subject to plan, configuration, surface, feature,
and region. For ChatGPT Enterprise, this includes
[no training on business data by default](https://help.openai.com/en/articles/8983130-what-if-i-want-to-keep-my-history-on-but-disable-model-training),
encryption in transit and at rest, workspace-level access controls, and
supported audit logging.

Coverage for data residency, inference residency, HIPAA, or a Business Associate
Agreement isn't universal. Confirm current
[data and inference residency guidance](https://help.openai.com/en/articles/9903489-data-residency-and-inference-residency-for-chatgpt)
and the customer's agreement for the features and regions in use.

Connected services have their own retention, logging, access, residency, and
compliance requirements. When ChatGPT Work uses plugins, repositories, or third-party
systems, evaluate both the ChatGPT workspace controls and the connected
system's controls.

For Codex activity, enterprise controls can extend to development environments,
repositories, configured tools, and related activity. Review
[Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup) and
[Governance](https://learn.chatgpt.com/docs/enterprise/governance) alongside the workspace controls.

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

- **ChatGPT Work access controls** determine who can use ChatGPT Work on
  each surface.
- **Workspace Agent controls** determine who can build, publish, share,
  schedule, or configure reusable agents and shared connections, where
  Workspace Agents are available.
- **Codex managed configuration** governs covered local Codex runtime behavior
  and doesn't configure hosted ChatGPT Work.

Managed configuration constrains supported runtime behavior. It doesn't grant
workspace access, replace RBAC, or revoke a user's workspace access. These
layers aren't one uniform ChatGPT Work policy surface. Analytics and compliance logs
provide additional visibility within their documented product and event
scopes.

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

- **Confirm who should have access first.** Decide whether to restrict access to
  ChatGPT Work, run a pilot, or roll it out broadly. Many organizations start
  with power users, champions, or teams with clear use cases.
- **Review roles and permissions.** In **Permissions & roles**, confirm which
  users or groups can access ChatGPT Work. Match access to business need, readiness,
  and governance expectations.
- **Review plugins and data sources.** ChatGPT Work is most useful with approved
  business context such as files, email, calendars, Slack, or CRM. Review
  enabled plugins, their audiences, and whether app policies still match how users
  should delegate work.
- **Set expectations for appropriate use cases.** Position ChatGPT Work for multi-step,
  higher-value tasks such as research, synthesis, analysis, file creation,
  workflow updates, and reusable outputs. Use Chat for quick questions,
  light rewrites, or brainstorming.
- **Review credit and usage controls.** Because ChatGPT Work can perform longer-running
  tasks, it can use more credits than a standard Chat conversation. Review
  defaults, group defaults, user overrides, and internal guidance about
  matching effort to business value.
- **Identify your first high-value workflows.** Start with clear, reviewable
  outcomes such as customer briefings, recurring reports, research synthesis,
  tracker updates, or polished documents and slides.
- **Prepare champions and support teams.** Give champions, training leads,
  and support teams rollout resources first so they can answer questions,
  collect feedback, and model effective delegation.
- **Communicate review and approval expectations.** Remind users that people
  remain responsible for reviewing outputs, validating important claims, and
  approving consequential actions before they are shared or used.
- **Monitor adoption and adjust.** Review usage, feedback, credit consumption,
  and delegated work after rollout. Use the findings to adjust access,
  guidance, training, and expansion.
