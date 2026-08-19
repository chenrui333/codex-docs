---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/admin-setup'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0"]
---

# Admin rollout guide

Source: https://learn.chatgpt.com/docs/enterprise/admin-setup

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use this guide to plan a ChatGPT Enterprise rollout across these administration
boundaries:

- Workspace access.
- Local runtime policy for covered capabilities in the ChatGPT desktop app,
  Codex CLI, and IDE extension.
- Codex cloud.
- Platform API access.
- Plugins and connector access.
- Permissions in connected systems.

Complete the steps in order for a new rollout, or use the linked pages to change
one boundary.

In workspace settings, **Codex Local** is a grouping label for certain local
access and access-token controls, not a separate product or client. The current
**Allow members to use Codex Local** control covers local use in the ChatGPT
desktop app, Codex CLI, and IDE extension. Managed configuration is a separate
policy layer that can constrain supported runtime behavior for covered
capabilities in those clients. This guide names the individual surface when
behavior or availability differs.

Start with the canonical map in
[Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).
Use Help Center guidance for current ChatGPT workspace procedures and the
linked developer documentation for local and hosted runtime behavior.

<a id="enterprise-grade-security-and-privacy"></a>

For enterprise security, privacy, and runtime protections, see
[Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security) and the
[Codex security white paper](https://trust.openai.com/?itemUid=382f924d-54f3-43a8-a9df-c39e6c959958&source=click).

<a id="pre-requisites-determine-owners-and-rollout-strategy"></a>

## Step 1: Assign owners and choose a rollout

Assign an owner for each part of the rollout:

- **Workspace access:** Membership, seats, roles, and supported workspace
  features.
- **Local runtime policy:** Approvals, permission profiles, filesystem and
  network access, and other requirements for supported local clients.
- **Codex cloud:** Hosted environments, repository connections, and cloud
  runtime policy.
- **Connected systems:** Provider-side application installation, accounts, and
  permissions.
- **Reporting and compliance:** Analytics access, audit exports, and downstream
  data handling.

Decide whether each audience needs covered local capabilities in the ChatGPT
desktop app, Codex CLI, IDE extension, Codex cloud, or a combination. Treat
Platform API access as a separate organization and project boundary when a
workflow uses API-key authentication.

## Step 2: Configure workspace access and identity

Use ChatGPT workspace membership, seats, groups, and supported RBAC permissions
to grant the intended audiences supported workspace features. Verify local
client and Codex cloud access against the current workspace guidance rather
than assuming that the same role controls every surface. Keep built-in
administration roles limited to the people who administer the workspace.

Workspace controls and labels change over time. Use these sources for current
procedures:

- [Manage members, seat types, roles, and access](https://help.openai.com/en/articles/8266401-managing-members-seat-types-roles-and-access-in-chatgpt-enterprise)
- [Configure role-based access control](https://help.openai.com/en/articles/11750701-rbac)
- [Manage workspace settings](https://help.openai.com/en/articles/8411955)
- [Groups and provisioning](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning)
- [Authentication](https://learn.chatgpt.com/docs/auth)

Test sign-in and feature access with a representative member before expanding
the rollout. Workspace access doesn't grant repository, file, or action access
in a connected service.

## Step 3: Configure local runtime requirements

Local requirements constrain runtime behavior when a user starts a supported
local run in the ChatGPT desktop app, Codex CLI, or IDE extension. Deliver
`requirements.toml` through a supported cloud, device, or system channel. Keep
this policy separate from ChatGPT workspace roles and groups.

Use permission profiles for supported local clients instead of building new
deployments around legacy sandbox-mode restrictions. For example:

```toml
default_permissions = ":workspace"

[allowed_permission_profiles]
":read-only" = true
":workspace" = true
```

To disable Computer Use across the supported browser and desktop feature
surfaces, constrain each public feature key that participates in the experience:

```toml
[features]
browser_use = false
browser_use_full_cdp_access = false
browser_use_external = false
in_app_browser = false
computer_use = false
```

For the authoritative key list, delivery behavior, precedence, and more
examples, see
[Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) and the
[`requirements.toml` reference](https://learn.chatgpt.com/docs/config-file/config-reference#requirementstoml).

<a id="team-config"></a>
<a id="step-4-standardize-local-configuration-with-team-config"></a>

## Step 4: Standardize repository configuration

Use repository-scoped configuration to share project defaults, rules, and
skills without duplicating setup for every user. Check configuration into
`.codex` or `.agents` according to the feature's documented location:

| Type          | Source                                           | Use it to                                                  |
| ------------- | ------------------------------------------------ | ---------------------------------------------------------- |
| Configuration | [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic) | Set repository defaults for supported local clients        |
| Rules         | [Rules](https://learn.chatgpt.com/docs/agent-configuration/rules)        | Control commands that require approval outside the sandbox |
| Skills        | [Build skills](https://learn.chatgpt.com/docs/build-skills)              | Make repository workflows available to supported clients   |

Repository configuration can supply defaults and reusable workflows. It can't
grant workspace, model, Platform API, or connected-system access.

## Step 5: Configure Codex cloud

Codex cloud uses hosted environments and connected source repositories. Plan
each boundary:

1. Grant the intended audience Codex cloud access through supported workspace
   controls.
2. Install and configure the supported source-system integration.
3. Limit repository access in the source system to the repositories each
   audience needs.
4. Configure cloud environments, secrets, and internet access for those
   repositories.
5. Configure optional hosted workflows such as code review.
6. Test with a representative user who has the intended workspace and
   repository permissions.

Codex cloud respects the repository permissions and protections exposed by the
connected source system. Workspace access doesn't bypass those controls. See
[Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment),
[GitHub integration](https://learn.chatgpt.com/docs/third-party/github), and
[Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security) for Codex cloud
setup and runtime guidance.

## Step 6: Configure plugins and connected capabilities

Review plugin installation, bundled skills, connector-backed capabilities,
connector actions, and source-system authorization as separate decisions.
Disabling a connector-backed capability doesn't necessarily uninstall the
plugin or its bundled skills.

Before including a plugin or skill in the rollout:

1. Confirm its source, accountable owner, intended audience, and review date.
2. Review bundled skills, connectors, MCP servers, hooks, and the data and
   actions each capability requires.
3. Test it with non-sensitive data and the least access it needs.
4. Record who owns re-review and retirement.

Plugins work in Chat and Work across ChatGPT on the web, desktop, and mobile,
in Codex in the ChatGPT desktop app, and through the Codex CLI plugin browser.
They aren't available in the IDE extension.
ChatGPT and Codex share one universal public plugin directory; workspace
controls determine which of those plugins members can access.

See [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors) and
[Skill controls](https://learn.chatgpt.com/docs/enterprise/skills) for the complete model.

## Step 7: Set up governance and observability

Choose the reporting surface that matches the question:

<a id="analytics-api-setup-steps"></a>
<a id="compliance-api-setup-steps"></a>

- Use [Workspace analytics](https://learn.chatgpt.com/docs/enterprise/workspace-analytics) for
  interactive ChatGPT workspace analytics and Codex analytics.
- Use the [Analytics API](https://learn.chatgpt.com/docs/enterprise/analytics-api) for programmatic,
  aggregated reporting through the Codex Analytics API.
- Use the [Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api) for audit and
  investigation records.
- Use [ChatGPT usage limits and spend controls](https://learn.chatgpt.com/docs/enterprise/usage-limits)
  when plan-dependent Codex activity consumes eligible ChatGPT workspace
  credits.

Use the authenticated API references for current access requirements, schemas,
fields, retention, and request behavior. Don't build an integration from a
copied contract in this guide.

Protect the integration boundary:

- Store API keys and other integration credentials in the organization's
  secret-management system.
- Limit access to downstream systems and retained data to the approved
  audience.
- Protect exported Compliance API records according to their sensitivity and
  the organization's retention policy, and test collection and deletion
  workflows against the current contract.

## Step 8: Verify and maintain the rollout

Verify every applicable boundary with representative identities:

- ChatGPT workspace membership, seat, and supported role permissions.
- Covered local capabilities in the ChatGPT desktop app, Codex CLI, and IDE
  extension, including sign-in and effective runtime requirements.
- Codex cloud access, environment configuration, and repository permissions.
- Platform API organization and project access for API-key workflows.
- Plugin installation, bundled skills, connector access, and supported actions.
- Connected-system authorization and data access.
- Analytics and compliance access for the responsible administrators.

Record the owner and current procedural source for each control. This record
lets administrators update procedures when UI or policy changes without
changing the administration model.

After the initial rollout, review access, connected capabilities, credit use,
support feedback, and the workflows teams actually use. Adjust the rollout
scope and administrator guidance when those signals change.
