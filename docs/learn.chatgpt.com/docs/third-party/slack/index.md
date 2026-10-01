---
source_type: 'learn'
source_area: 'learn_third_party'
source_url: 'https://learn.chatgpt.com/docs/third-party/slack'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Use ChatGPT in Slack

Source: https://learn.chatgpt.com/docs/third-party/slack

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Mention `@ChatGPT` in a Slack channel to start a request. If your workspace has
Cloud delegation enabled, ChatGPT can send repository work to a separate
[Codex Cloud](https://learn.chatgpt.com/docs/cloud) task and return the result to the thread.

**For workspace admins:** See [Set up and manage @ChatGPT in Slack and Microsoft Teams](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams) for app setup, workspace connections, and access controls.

## Set up the Slack app

A ChatGPT workspace owner or admin sets up the workspace's Slack deployment.
The available controls depend on your workspace's enabled features.

If you don't see these controls, ask your ChatGPT workspace admin whether Slack
deployments are available. Your Slack workspace's app policies also apply.

Cloud delegation must be available in your workspace and requires a published
environment shared with the workspace. Ask your admin to
[enable Codex Cloud for Slack](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams#enable-codex-cloud-for-slack).
Where Codex Cloud role-based access control is enabled, both the deployment's
service account and your account need Codex Cloud access.

### Connect your account when prompted

Workspace setup and your personal account connection are separate. If ChatGPT
asks you to connect your account before continuing:

1. Select the connection link in the Slack message and sign in if prompted.
2. Connect Slack for the same workspace where you made the request.
3. Return to the original Slack thread and mention `@ChatGPT` to retry.

<a id="start-a-task"></a>
<a id="start-a-chat"></a>

## Start a request

1. In a channel where the app is enabled, mention `@ChatGPT` and describe the
   result you want. For coding work, include the repository and relevant context
   from the thread.
2. Complete any account-connection or approval prompts. Review the requested work
   and access before you approve.
3. Continue related requests in the same thread, mentioning `@ChatGPT` again.

For example:

```text
@ChatGPT investigate the failing checkout tests in acme/storefront and propose a fix.
```

Then follow up in that thread:

```text
@ChatGPT add a regression test for the fix and summarize the checks you ran.
```

Use an enabled public or private channel in your workspace. Slack Connect
channels shared with another organization aren't supported by this flow.

<a id="how-codex-chooses-an-environment-and-repo"></a>

## Run repository work in Codex Cloud

Cloud delegation requires an eligible workspace-shared environment with a
published version. For an Enterprise workspace, prepare and publish a tested
setup using the [cloud environment guide](https://learn.chatgpt.com/docs/environments/cloud-environments)
and follow the guidance to [share it within your Enterprise
workspace](https://learn.chatgpt.com/docs/environments/cloud-environments#share-within-an-enterprise-workspace).
Confirm that the environment is available for the requested repository.

- **Environment selection**: ChatGPT selects from accessible workspace-shared Cloud
  environments. When using your account, it checks that you can access the
  environment before starting. Personal Cloud environments aren't included. Name
  the repository or shared environment in your request to help ChatGPT choose.
- **Separate coding task**: Repository work runs in a separate task using your
  account. You need access to the selected environment and to any repositories
  that require authentication.
- **Follow-up work**: Related requests in the same Slack thread can continue the
  coding task and environment when they use the same account to run it. A
  request using another account may start a separate coding task. Start a new
  conversation when you need a different environment.

Sharing an environment doesn't grant repository access or share your personal
credential values. Review its [environment-owned values and prepared
files](https://learn.chatgpt.com/docs/environments/cloud-environments#share-within-an-enterprise-workspace)
before sharing, because those can be available to people who use the environment.

If no eligible shared environment is available, resolve the environment or
access issue before retrying. For service access, see
[Connect to services](https://learn.chatgpt.com/docs/environments/cloud-environments#connect-to-services)
and [Environment variables and network secrets](https://learn.chatgpt.com/docs/environments/cloud-environments#configure-environment-variables-and-network-secrets).

<a id="enterprise-data-controls"></a>

## Review approvals and results

When a request needs your authorization, ChatGPT can show a private approval
card with **Allow** and **Deny** controls. Review the assignment and any
available environment choice before deciding.

ChatGPT can post a message in the original thread when the task starts. When the
**Follow along** and **Cancel** controls are available, they appear for the
requester. Use **Follow along** to open the task and inspect its work; the
channel reply doesn't give every channel member access to the underlying task.

ChatGPT returns the result to the thread. Review the answer, changes, and
reported checks before using or merging it.
Mention `@ChatGPT` in the thread to request a correction or follow-up.

## Data usage, privacy, and security

A response posted to a Slack channel can be read by people with access to that
channel. Ask ChatGPT to share only information appropriate for that audience. A
private approval card doesn't make the resulting channel reply private.

Keep secrets out of Slack prompts and use the environment's credential controls
for repository work. Review [Agent Security](https://learn.chatgpt.com/docs/environments/cloud-environments#agent-security)
and the [deployment access
boundaries](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams#security-faq), and follow your
workspace's data and app policies.

## Move to the ChatGPT app

If you previously used `@Codex`, start new requests with `@ChatGPT` after your
admin enables the ChatGPT app. Follow any connection and approval prompts.

## Tips and troubleshooting

- **No response**: Confirm that ChatGPT is enabled for the channel and mention
  `@ChatGPT` explicitly. Use a channel within your organization rather than a
  Slack Connect channel.
- **Account connection requested again**: Check that you connected ChatGPT to
  the Slack workspace where you're making the request, then retry in the same
  thread.
- **No eligible Cloud environment**: Check that the environment is published and
  shared with the workspace, and that the account running the task has the
  required access. A personal Cloud environment won't appear in this flow.
- **A coding task won't start**: Ask your admin to confirm that Cloud delegation
  is available and Codex Cloud is enabled for your workspace. Where Codex Cloud
  role-based access control is enabled, check that both the deployment's
  service account and your account have Codex Cloud access. Also check your
  access to the selected environment and its repositories.
- **Different environment needed**: Start a new conversation and name the
  repository or shared environment you want to use.
- **Task controls unavailable**: The **Follow along** and **Cancel** controls
  depend on the deployment's configuration and are intended for the requester.
- **Long threads**: Summarize the relevant issue, expected outcome, and repository
  in your latest request so the task has enough context.
