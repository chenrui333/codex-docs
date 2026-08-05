---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/work-admin-faq'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1"]
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

ChatGPT Work launched July 9, 2026. For Enterprise and Edu, web and mobile access is
off by default during a two-week preview. Admins can enable billable usage, and
explicit opt-outs persist when the default changes. Desktop access remains
governed separately through Codex Local permissions and managed configuration.

This FAQ explains how admins manage ChatGPT Work: access and data controls,
compliance and visibility, usage and spend, incident response, and rollout
practices.

## Core administrative controls

Administrators govern ChatGPT Work through several control layers:

- **Access to the enterprise workspace:** Identity and access controls manage
  authentication and access to the workspace. Depending on the plan and
  configuration, administrator-controlled identity features can include SSO,
  domain verification, SCIM provisioning, user lifecycle management, and
  identity-group synchronization. Users can enable account-level OpenAI MFA;
  enforce workspace-wide MFA through your identity provider. Manage SSO and
  related identity settings in the
  [Global Admin Console](https://help.openai.com/en/articles/12289294-admin-portal).
- **Access to ChatGPT Work within the workspace:** On web and mobile, admins use the
  ChatGPT Work access control and role-based access control (RBAC) to decide who can
  use it. Enterprise and Edu access is off during the two-week preview;
  admins can enable it, and explicit opt-outs persist when the default changes.
  Desktop access follows separate Codex Local permissions and
  [managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration). Controls
  vary by plan and surface.
- **Group membership:** Groups can be synchronized through SCIM and an identity
  provider so access updates automatically as employees join the organization,
  change roles, or leave. See
  [Groups and provisioning](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning).
- **Workspace and member roles:** Built-in Owner, Admin, and Member roles
  determine who can administer the workspace. Custom roles and member RBAC
  separately control end-user access to ChatGPT Work, plugins, and other capabilities.
  See
  [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).
- **Plugins and connectors:** Plugin policy governs plugin availability and
  installation. Connector access, action controls, and approval behavior are
  configured separately, and Workspace Agents have additional per-agent
  controls. See [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors),
  [Plugins](https://learn.chatgpt.com/docs/plugins), and the
  [App security white paper](https://cdn.openai.com/business-guides-and-resources/app-security-whitepaper.pdf).
- **Source-system permissions:** A user can access only the content and actions
  allowed by the account or shared connection in the native application. See
  [Admin controls, security, and compliance in apps](https://help.openai.com/en/articles/11509118-admin-controls-security-and-compliance-in-apps-enterprise-edu-and-business).
- **Approval and action restrictions:** For connectors that support Action control,
  admins can allow all actions, read-only actions, or a custom set and decide
  how newly added actions are handled. App permissions separately determine
  when ChatGPT asks before using a connector.
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
[RBAC](https://help.openai.com/en/articles/11750701-rbac), and workspace roles
to determine who can use ChatGPT Work.

Where supported, access can be synchronized with your identity provider through
[SCIM](https://help.openai.com/en/articles/10011769-openai-platform-scim-integration-faq)
and group synchronization. This lets you manage access and permissions centrally
as employees join the organization, change roles, or leave.

Underlying source systems continue to enforce access to enterprise data. ChatGPT Work
respects the permissions defined in connected applications, so users and agents
can access only files, repositories, channels, records, and actions they are
authorized to use. ChatGPT Work doesn't bypass existing access controls or grant new
permissions in connected systems.

<a id="how-does-work-access-data-and-context"></a>
<a id="how-does-work-mode-access-data-and-context"></a>

### How does ChatGPT Work access data and context?

ChatGPT Work can use the current chat, uploaded files, workspace resources, and
connected systems through plugins. Depending on enabled capabilities and
permissions, this can include documents, repositories, tickets, channels,
email, and calendars. Files from earlier chats or memory can be available
when included in the current chat or project, or when applicable
workspace and user memory controls are enabled.

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
- **Scheduled:** Start a task at a future time or on a recurring schedule
  without requiring a user to initiate each run.
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

Coverage for data residency, inference residency, FedRAMP, HIPAA, or a Business
Associate Agreement isn't universal. Confirm current
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
across the information ChatGPT Work accesses. Data stored by ChatGPT follows the
configured workspace retention policies, while connected applications continue
to manage their own data and lifecycle policies. See
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
kinds of visibility. The Global Admin Console shows adoption and credit use by
user, product, and model, including the ability to drill down across Chat, Work,
and Codex usage. The Compliance API covers all user messages and responses
across Chat, Work, and Codex. See
[Workspace analytics](https://learn.chatgpt.com/docs/enterprise/workspace-analytics) and the
[Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api).

### Are prompts, outputs, files, actions, or tool calls logged?

The Compliance Logs Platform provides user prompts and agent responses. It
doesn't track files, actions, or tool calls.

The Compliance Logs Platform retains data for 30 days. Export records
continuously to an approved electronic discovery, data loss prevention, SIEM,
or data-lake system when your organization requires longer retention. See the
[OpenAI Compliance Platform guide](https://help.openai.com/en/articles/9261474-compliance-api-for-chatgpt-enterprise-edu-and-chatgpt-for-teachers).

### Can unusual behavior, failures, or usage spikes be detected quickly?

Workspace analytics, compliance logs, and connected monitoring tools help
admins review usage and investigate supported ChatGPT, Work, and Codex
activity. Signals can include active users, messages, tool activity, agent
activity, authentication and administrative events, and credit consumption.
Exported logs can support electronic discovery, data loss prevention, SIEM,
auditing, and investigations. Detection quality depends on plan, event
coverage, attribution, freshness, and configured rules.

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

## Governance

### How can admins control access, permissions, and policies?

Governance spans three related but separate layers:

- **ChatGPT Work access controls** determine who can use ChatGPT Work on
  each surface.
- **Workspace Agent controls** determine who can build, publish, share,
  schedule, or configure reusable agents and shared connections.
- **Codex managed configuration** governs covered local runtime behavior,
  including permissions, approvals, filesystem and network access, MCP servers,
  hooks, and command rules.

Managed configuration constrains supported runtime behavior. It doesn't grant
workspace access, replace RBAC, or revoke a user's workspace access. These
layers aren't one uniform ChatGPT Work policy surface. Analytics and compliance logs
provide additional visibility within their documented product and event
scopes.

Enterprise administrators can use
[managed requirements](https://learn.chatgpt.com/docs/enterprise/managed-configuration) to enforce
supported settings that users can't override while the requirements are
active. Supported policies cover approval behavior, permission profiles, web
search, hooks, MCP servers, feature flags, command rules, and filesystem
access. Network requirements are experimental and should be tested on the
client versions and operating systems in your deployment before broad use. For
current Codex clients, managed
[permission profiles](https://learn.chatgpt.com/docs/permissions) are the preferred way to define
filesystem, network, and runtime access.

### Can access be scoped by group, role, workspace, or capability?

Yes. ChatGPT Work capabilities can be scoped with workspace roles, identity groups,
and administrator-defined permissions. Assign capabilities to groups based on
business need and organizational policy instead of giving every user identical
access. See the
[RBAC guide](https://help.openai.com/en/articles/11750701-rbac) and this
[RBAC walkthrough](https://vimeo.com/1207482321/d1286e4467?share=copy&fl=sv&fe=ci).

Organizations can use RBAC to determine which users can access ChatGPT Work, manage
workspace settings, configure approved plugins, or build and publish Workspace
Agents. For eligible Enterprise and Edu workspaces, monthly usage limits can
support a phased rollout through a workspace default, group defaults, and user
overrides.

Access to connected systems remains independently governed. Scope plugins, shared
credentials, repositories, and write-capable actions to the minimum required
audience using workspace permissions, plugin settings, and the source system's
controls. For higher-trust environments, use managed policies to restrict
runtime capabilities further.

### How are runtime and network boundaries governed?

The security boundaries for ChatGPT Work depend on the task. A standard Chat conversation, a
connected workflow, a scheduled task, and a Codex chat can run in different
environments with different permissions, tools, and network access.

Govern each execution environment through its applicable controls. ChatGPT Work
permissions on web and mobile govern access to ChatGPT Work and supported browser or
network capabilities. Search, plugins, Workspace Agents, and
source-system permissions remain separate controls. Desktop and Codex chats
follow Codex permissions, managed configuration, MCP policy, sandboxing, and
approval controls. These controls aren't interchangeable.

For Codex activity, local runs in the ChatGPT desktop app, CLI, and IDE execute
on the user's machine with operating-system sandboxing and approval policies.
Codex cloud runs chats in isolated OpenAI-managed environments. Enterprise
administrators can use managed requirements to constrain permission profiles,
approvals, filesystem and network access, MCP servers, hooks, command rules,
and other supported runtime behavior.

## Usage and cost

<a id="how-does-work-usage-translate-into-spend-over-time"></a>
<a id="how-does-work-mode-usage-translate-into-spend-over-time"></a>

### How does ChatGPT Work usage translate into spend over time?

[ChatGPT Work and Codex share pricing, credits, and usage limits](https://learn.chatgpt.com/docs/pricing).
Consumption varies with the model and capability, context size, task duration,
tool use, and output size. Standard Chat usage is separate.

The highest-variance patterns are often workflows that run frequently,
retrieve or process large amounts of information, call multiple tools or connectors,
retry after failures, or produce large artifacts. Cost-sensitive examples
include scheduled or recurring work, high-volume triggers, large files, broad
retrieval across enterprise sources, repeated connector calls, and Codex chats that
process repositories, run commands, or use cloud environments.

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

Admins can need to stop users, plugins, shared credentials, workflows, schedules,
or Codex credentials during user removal or incident review.

Revocation paths include:

- Remove a user's workspace or group access. For SCIM-managed users, remove
  access at the identity provider; otherwise, a later synchronization can
  provision the user again.
- Disable or restrict the relevant plugin or connector.
- Revoke a shared connection, bot, or service account through its owning
  surface. Workspace owners and admins can separately revoke Codex workspace
  access tokens.
- Remove a Workspace Agent from publication or delete it through its agent owner
  or workspace administrator.
- Disable the relevant schedule or trigger.
- For Codex access, separately revoke the relevant access token, repository
  connection, and cloud-environment access. Managed configuration isn't an
  access-revocation mechanism.

## Additional resources for your teams

| Topic                    | Use this when explaining                                                   | Learn ChatGPT page                                               |
| ------------------------ | -------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Workspace setup and RBAC | Who can use and administer Codex                                           | [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)             |
| Authentication           | How ChatGPT sign-in, API key sign-in, and workspace policy differ          | [Authentication](https://learn.chatgpt.com/docs/auth)                                    |
| Approvals and sandboxing | How Codex controls file, command, network, and side-effecting tool actions | [Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)  |
| Managed policy           | How admins enforce Codex settings users can't override                     | [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) |
| Runtime environments     | How Codex cloud setup, secrets, caches, and task phases work               | [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment)      |
| Internet access          | How Codex cloud domain allowlists and HTTP methods work                    | [Agent internet access](https://learn.chatgpt.com/docs/cloud/internet-access)            |
| Permissions              | How filesystem, network, and deny-read controls work                       | [Permissions](https://learn.chatgpt.com/docs/permissions)                                |
| Observability            | How analytics, reporting, and compliance exports work                      | [Governance](https://learn.chatgpt.com/docs/enterprise/governance)                       |
| Automation credentials   | How access tokens are created, limited, revoked, and audited               | [Access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens)                 |

## Recommended admin actions

- **Confirm who should have access first.** Decide whether to restrict access to
  ChatGPT Work, run a pilot, or roll it out broadly. Many organizations start
  with power users, champions, or teams with clear use cases.
- **Review roles and permissions.** In **Permissions & roles**, confirm which
  users or groups can access ChatGPT Work. Match access to business need, readiness,
  and governance expectations.
- **Review plugins and data sources.** ChatGPT Work is most useful with approved
  business context such as files, email, calendars, Slack, or CRM. Review
  enabled plugins, their audiences, and whether connector policies still match how users
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
