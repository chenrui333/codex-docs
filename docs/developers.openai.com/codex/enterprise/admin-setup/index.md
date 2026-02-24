# Admin Setup

Source: https://developers.openai.com/codex/enterprise/admin-setup

This guide is for ChatGPT Enterprise admins who want to set up Codex for their workspace.

Use this page as the step-by-step rollout guide. It focuses on setup order and decision points. For detailed policy, configuration, and monitoring details, use the linked pages: [Authentication](/codex/auth), [Security](/codex/security), [Managed configuration](/codex/enterprise/managed-configuration), and [Governance](/codex/enterprise/governance).

## Enterprise-grade security and privacy

Codex supports ChatGPT Enterprise security features, including:

- No training on enterprise data
- Zero data retention for the App, CLI, and IDE (code remains in developer environment)
- Residency and retention that follow ChatGPT Enterprise policies
- Granular user access controls
- Data encryption at rest (AES-256) and in transit (TLS 1.2+)

For security controls and runtime protections, see [Security](/codex/security). Refer to [Zero Data Retention (ZDR)](https://platform.openai.com/docs/guides/your-data#zero-data-retention) for more details.

## Local vs. cloud setup

Codex operates in two environments: local and cloud.

1. **Codex local** includes the Codex app, CLI, and IDE extension. The agent runs on the developer’s computer in a sandbox.
2. **Codex cloud** includes hosted Codex features (including Codex cloud, iOS, Code Review, and tasks created by the [Slack integration](/codex/integrations/slack) or [Linear integration](/codex/integrations/linear)). The agent runs remotely in a hosted container with your codebase.

You can enable local, cloud, or both, and control access with workspace settings and role-based access control (RBAC).

## Step 0: Owners and rollout decision

Ensure you have the following owners:

- Workspace owner with access to ChatGPT Enterprise
- IT management owner for managed configuration
- Governance owner for analytics / compliance review

A rollout decision:

- Codex local only (Codex app, CLI, and IDE extension)
- Codex cloud only (Codex web, GitHub code review)
- Both local + cloud

Review [authentication](https://developers.openai.com/codex/auth) before rollout:

- Codex local supports ChatGPT sign-in or API keys. Confirm MFA/SSO requirements and any managed login restrictions in authentication
- Codex cloud requires ChatGPT sign-in

## Step 1: Enable workspace toggles

Turn on only the Codex features you plan to roll out in this phase.

Go to [Workspace Settings > Settings and Permissions](https://chatgpt.com/admin/settings).

### Codex local

Turn on **Allow members to use Codex Local**.

This enables use of the Codex app, CLI, and IDE extension for allowed users.

If this toggle is off, users who attempt to use the Codex app, CLI, or IDE will see the following error: “403 - Unauthorized. Contact your ChatGPT administrator for access.”

#### Enable device code authentication for Codex CLI

Allow developers to sign in with device codes when using Codex CLI in a non-interactive environment. More details in [authentication](https://developers.openai.com/codex/auth/).

![Codex local toggle](/images/codex/enterprise/local-toggle-config.png)

### Codex cloud

### Prerequisites

Codex cloud requires **GitHub (cloud-hosted) repositories**. If your codebase is on-premises or not on GitHub, you can use the Codex SDK to build similar workflows on your own infrastructure.

To set up Codex as an admin, you must have GitHub access to the repositories
commonly used across your organization. If you don’t have the necessary
access, work with someone on your engineering team who does.

### Enable Codex cloud in workspace settings

Start by turning on the ChatGPT GitHub Connector in the Codex section of [Workspace Settings > Settings and Permissions](https://chatgpt.com/admin/settings).

To enable Codex cloud for your workspace, turn on **Allow members to use Codex cloud**. Once enabled, users can access Codex directly from the left-hand navigation panel in ChatGPT.

Note that it may take up to 10 minutes for Codex to appear in ChatGPT.

#### Allow members to administer Codex

Allows users to view overall Codex [workspace analytics](https://chatgpt.com/codex/settings/analytics), access [cloud-managed requirements](https://chatgpt.com/codex/settings/managed-configs), and manage Cloud environments (edit and delete).

Codex cloud not required.

#### Enable Codex Slack app to post answers on task completion

Codex posts its full answer back to Slack when the task completes. Otherwise, Codex posts only a link to the task.

To learn more, see [Codex in Slack](/codex/integrations/slack).

#### Enable Codex agent to access the internet

By default, Codex cloud agents have no internet access during runtime to help protect against security and safety risks like prompt injection.

This setting enables users to use an allowlist for common software dependency domains, add more domains and trusted sites, and specify allowed HTTP methods.

For security implications of internet access and runtime controls, see [Security](/codex/security).

![Codex cloud toggle](/images/codex/enterprise/cloud-toggle-config.png)

## Step 2: Set up custom roles (RBAC)

Use RBAC to control which users or groups can access Codex local and Codex cloud.

### What RBAC lets you do

Workspace Owners can use RBAC in ChatGPT admin settings to:

- Set a default role for users who are not assigned any custom role
- Create custom roles with granular permissions
- Assign one or more custom roles to Groups (including SCIM-synced groups)
- Manage roles centrally from the Custom Roles tab

Users can inherit multiple roles, and permissions resolve to the maximum allowed across those roles.

### Important behavior to plan for

Users in any custom role group do not use the workspace default permissions.

If you are gradually rolling out Codex, one suggestion is to have a “Codex Users” group and a second “Codex Admin” group that has the “Allow members to administer Codex” toggle enabled.

For RBAC setup details and the full permission model, see the [OpenAI RBAC Help Center article](https://help.openai.com/en/articles/11750701-rbac).

## Step 3: Configure Codex local managed settings

For Codex local, set an admin-approved baseline for local behavior before broader rollout.

### Use managed configuration for two different goals

- **Requirements** (`requirements.toml`): Admin-enforced constraints users cannot override
- **Managed defaults** (`managed_config.toml`): Starting values applied when Codex launches

### Team Config

Teams who want to standardize Codex across an organization can use Team Config to share defaults, rules, and skills without duplicating setup on every local configuration.

| Type | Path | Use it to |
| --- | --- | --- |
| [Config basics](/codex/config-basic) | `config.toml` | Set defaults for sandbox mode, approvals, model, reasoning effort, and more. |
| [Rules](/codex/rules) | `rules/` | Control which commands Codex can run outside the sandbox. |
| [Skills](/codex/skills) | `skills/` | Make shared skills available to your team. |

For locations and precedence, see [Config basics](/codex/config-basic#configuration-precedence).

### Recommended first decisions for local rollout

Define a baseline for your pilot:

- Approval policy posture
- Sandbox mode posture
- Web search posture
- MCP / connectors policy
- Local logging and telemetry posture

For exact keys, precedence, MDM deployment, and examples, see [Managed configuration](/codex/enterprise/managed-configuration) and [Security](/codex/security).

If you plan to restrict login method or workspace for local clients, see the admin-managed authentication restrictions in [Authentication](https://developers.openai.com/codex/auth).

## Step 4: Configure Codex cloud usage (if enabled)

This step covers repository and environment setup after the Codex cloud workspace toggle is enabled.

### Connect Codex cloud to repositories

1. Navigate to [Codex](https://chatgpt.com/codex) and select **Get started**
2. Select **Connect to GitHub** to install the ChatGPT GitHub Connector if you haven’t already connected GitHub to ChatGPT
3. Install or authorize the ChatGPT GitHub Connector
4. Choose an installation target for the ChatGPT Connector (typically your main organization)
5. Allow the repositories you want to connect to Codex

For more, see [Cloud environments](https://developers.openai.com/codex/cloud/environments).

Codex uses short-lived, least-privilege GitHub App installation tokens for each operation and respects the user’s existing GitHub repository permissions and branch protection rules.

### Configure IP addresses (as needed)

Configure connector / IP allow lists if required by your network policy with these [egress IP ranges](https://openai.com/chatgpt-agents.json).

These IP ranges can change. Consider checking them automatically and updating your allow list based on the latest values.

### Enable code review with Codex cloud

To allow Codex to perform code reviews on GitHub, go to [Settings → Code review](https://chatgpt.com/codex/settings/code-review).

Code review can be configured at the repository level. Users can also enable auto review for their PRs and choose when Codex automatically triggers a review. More details on [GitHub](https://developers.openai.com/codex/integrations/github) integration page.

Additional integration docs for [Slack](/codex/integrations/slack), [GitHub](/codex/integrations/github), and [Linear](/codex/integrations/linear).

## Step 5: Set up governance and observability

Codex gives enterprise teams several options for visibility into adoption and impact. Set up governance early so your team can monitor adoption, investigate issues, and support compliance workflows.

### Codex governance typically uses

- Analytics Dashboard for quick, self-serve visibility
- Analytics API for programmatic reporting and BI integration
- Compliance API for audit and investigation workflows

### Recommended minimum setup

- Assign an owner for adoption reporting
- Assign an owner for audit and compliance review
- Define a review cadence
- Decide what success looks like

For details and examples, see [Governance](/codex/enterprise/governance).

## Step 6: Confirm and validate setup

### What to verify

- Users can sign in to Codex local (ChatGPT or API key)
- (If enabled) Users can sign in to Codex cloud (ChatGPT sign-in required)
- MFA and SSO requirements match your enterprise security policy
- RBAC and workspace toggles produce the expected access behavior
- Managed configuration is applied for users
- Governance data is visible for admins

For authentication options and enterprise login restrictions, see [Authentication](/codex/auth).

Once your team is confident with setup, you can confidently roll Codex out to additional teams and organizations.

