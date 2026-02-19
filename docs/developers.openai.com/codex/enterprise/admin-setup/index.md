# Admin Setup

Source: https://developers.openai.com/codex/enterprise/admin-setup

Set up Codex for your ChatGPT Enterprise workspace

This guide is for ChatGPT Enterprise admins who want to set up Codex for their workspace.

## Enterprise-grade security and privacy

Codex supports ChatGPT Enterprise security features, including:

- No training on enterprise data
- Zero data retention for the CLI and IDE
- Residency and retention follow ChatGPT Enterprise policies
- Granular user access controls
- Data encryption at rest (AES 256) and in transit (TLS 1.2+)

For more, see [Security](/codex/security).

## Local vs. cloud setup

Codex operates in two environments: local and cloud.

1. Local use includes the Codex app, CLI, and IDE extension. The agent runs on the developer’s computer in a sandbox.
2. Use in the cloud includes Codex cloud, iOS, Code Review, and tasks created by the [Slack integration](/codex/integrations/slack). The agent runs remotely in a hosted container with your codebase.

Use separate permissions and role-based access control (RBAC) to control access to local and cloud features. You can enable local, cloud, or both for all users or for specific groups.

## Codex local setup

### Enable Codex app, CLI, and IDE extension in workspace settings

To enable Codex locally for workspace members, go to [Workspace Settings > Settings and Permissions](https://chatgpt.com/admin/settings). Turn on **Allow members to use Codex Local**. This setting doesn’t require the GitHub connector.

After you turn this on, users can sign in to use the Codex app, CLI, and IDE extension with their ChatGPT account. If you turn off this setting, users who attempt to use the Codex app, CLI, or IDE will see the following error: “403 - Unauthorized. Contact your ChatGPT administrator for access.”

## Team Config

Teams who want to standardize Codex across an organization can use Team Config to share defaults, rules, and skills without duplicating setup on every local configuration.

| Type | Path | Use it to |
| --- | --- | --- |
| [Config basics](/codex/config-basic) | `config.toml` | Set defaults for sandbox mode, approvals, model, reasoning effort, and more. |
| [Rules](/codex/rules) | `rules/` | Control which commands Codex can run outside the sandbox. |
| [Skills](/codex/skills) | `skills/` | Make shared skills available to your team. |

For locations and precedence, see [Config basics](/codex/config-basic#configuration-precedence).

## Codex cloud setup

### Prerequisites

Codex cloud requires **GitHub (cloud-hosted) repositories**. If your codebase is on-premises or not on GitHub, you can use the Codex SDK to build similar workflows on your own infrastructure.

To set up Codex as an admin, you must have GitHub access to the repositories
commonly used across your organization. If you don’t have the necessary
access, work with someone on your engineering team who does.

### Enable Codex cloud in workspace settings

Start by turning on the ChatGPT GitHub Connector in the Codex section of [Workspace Settings > Settings and Permissions](https://chatgpt.com/admin/settings).

To enable Codex cloud for your workspace, turn on **Allow members to use Codex cloud**.

Once enabled, users can access Codex directly from the left-hand navigation panel in ChatGPT.

![Codex cloud toggle](/images/codex/enterprise/cloud-toggle-config.png)

After you turn on Codex in your Enterprise workspace settings, it may take up
to 10 minutes for Codex to appear in ChatGPT.

### Configure the GitHub Connector IP allow list

To control which IP addresses can connect to your ChatGPT GitHub connector, configure these IP ranges:

- [ChatGPT egress IP ranges](https://openai.com/chatgpt-actions.json)
- [Codex container egress IP ranges](https://openai.com/chatgpt-agents.json)

These IP ranges can change. Consider checking them automatically and updating your allow list based on the latest values.

### Allow members to administer Codex

This toggle allows users to view Codex workspace analytics and manage environments (edit and delete).

Codex supports role-based access (see [Role-based access (RBAC)](#role-based-access-rbac)), so you can turn on this toggle for a specific subset of users.

### Enable Codex Slack app to post answers on task completion

Codex integrates with Slack. When a user mentions `@Codex` in Slack, Codex starts a cloud task, gets context from the Slack thread, and responds with a link to a PR to review in the thread.

To allow the Slack app to post answers on task completion, turn on **Allow Codex Slack app to post answers on task completion**. When enabled, Codex posts its full answer back to Slack when the task completes. Otherwise, Codex posts only a link to the task.

To learn more, see [Codex in Slack](/codex/integrations/slack).

### Enable Codex agent to access the internet

By default, Codex cloud agents have no internet access during runtime to help protect against security and safety risks like prompt injection.

As an admin, you can allow users to enable agent internet access in their environments. To enable it, turn on **Allow Codex agent to access the internet**.

When this setting is on, users can use an allow list for common software dependency domains, add more domains and trusted sites, and specify allowed HTTP methods.

### Enable code review with Codex cloud

To allow Codex to do code reviews, go to [Settings → Code review](https://chatgpt.com/codex/settings/code-review).

Users can specify whether they want Codex to review their pull requests. Users can also configure whether code review runs for all contributors to a repository.

Codex supports two types of code reviews:

1. Automatically triggered code reviews when a user opens a PR for review.
2. Reactive code reviews when a user mentions @Codex to look at issues. For example, “@Codex fix this CI error” or “@Codex address that feedback.”

## Role-based access (RBAC)

Codex supports role-based access. RBAC is a security and permissions model used to control access to systems or resources based on a user’s role assignments.

To enable RBAC for Codex, navigate to Settings & Permissions → Custom Roles in [ChatGPT’s admin page](https://chatgpt.com/admin/settings) and assign roles to groups created in the Groups tab.

This simplifies permission management for Codex and improves security in your ChatGPT workspace. To learn more, see the [Help Center article](https://help.openai.com/en/articles/11750701-rbac).

## Set up your first Codex cloud environment

1. Go to Codex cloud and select **Get started**.
2. Select **Connect to GitHub** to install the ChatGPT GitHub Connector if you haven’t already connected GitHub to ChatGPT.
   - Allow the ChatGPT Connector for your account.
   - Choose an installation target for the ChatGPT Connector (typically your main organization).
   - Allow the repositories you want to connect to Codex (a GitHub admin may need to approve this).
3. Create your first environment by selecting the repository most relevant to your developers, then select **Create environment**.
   - Add the email addresses of any environment collaborators to give them edit access.
4. Start a few starter tasks (for example, writing tests, fixing bugs, or exploring code).

You have now created your first environment. Users who connect to GitHub can create tasks using this environment. Users who have access to the repository can also push pull requests generated from their tasks.

### Environment management

As a ChatGPT workspace administrator, you can edit and delete Codex environments in your workspace.

### Connect more GitHub repositories with Codex cloud

1. Select **Environments**, or open the environment selector and select **Manage Environments**.
2. Select **Create Environment**.
3. Select the repository you want to connect.
4. Enter a name and description.
5. Select the environment visibility.
6. Select **Create Environment**.

Codex automatically optimizes your environment setup by reviewing your codebase. Avoid advanced environment configuration until you observe specific performance issues. For more, see [Codex cloud](/codex/cloud).

### Share setup instructions with users

You can share these steps with end users:

1. Go to [Codex](https://chatgpt.com/codex) in the left-hand panel of ChatGPT.
2. Select **Connect to GitHub** in the prompt composer if you’re not already connected.
   - Sign in to GitHub.
3. You can now use shared environments with your workspace or create your own environment.
4. Try a task in both Ask and Code mode. For example:
   - Ask: Find bugs in this codebase.
   - Write code: Improve test coverage following the existing test patterns.

## Track Codex usage

- For workspaces with rate limits, use [Settings → Usage](https://chatgpt.com/codex/settings/usage) to view workspace metrics for Codex.
- For more detail on enterprise governance, refer to the [Governance](/codex/enterprise/governance) page.
- For enterprise workspaces with flexible pricing, you can see credit usage in the ChatGPT workspace billing console.

## Zero data retention (ZDR)

Codex supports OpenAI organizations with [Zero Data Retention (ZDR)](https://platform.openai.com/docs/guides/your-data#zero-data-retention) enabled.

