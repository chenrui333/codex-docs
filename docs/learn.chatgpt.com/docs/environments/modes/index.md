---
source_type: 'learn'
source_area: 'learn_environments'
source_url: 'https://learn.chatgpt.com/docs/environments/modes'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Codex environments

Source: https://learn.chatgpt.com/docs/environments/modes

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

In the ChatGPT desktop app, open the ChatGPT dropdown and select **Codex**.
When starting a Codex chat, choose where it runs:

- **Local**: work directly in your current project directory.
- **Worktree**: isolate changes in a Git worktree. [Learn more](https://learn.chatgpt.com/docs/environments/git-worktrees).
- **Cloud**: run a remote task in its own workspace. See [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)
  for help choosing an environment.

Both **Local** and **Worktree** chats run on your computer.
Use **Work in** to choose **This computer** or **Cloud**. For a local Git project,
the separate **Worktree** control lets you isolate changes from your current checkout.

If the default environment is available, select it to start without choosing a
repository. You can also select a published environment. In Enterprise
workspaces, choose a published environment or ask an admin for access to a
shared one. Shared access lets you use the environment; it doesn't grant
permission to edit it.

You can also start and continue cloud tasks on the web or on mobile. On mobile,
open **Codex** and choose an available environment.

To create an environment, start a new task on the web or in the desktop app.
Choose **Work in** > **Cloud**, open **Select environment**, then select
**Create environment**. Codex inspects your selected repositories and helps
prepare and test their setup before you publish it.

In the desktop app, the default environment can automatically use a project's
repositories when they are hosted on GitHub.com and you have connected your
GitHub account. This automatic project setup doesn't include GitLab repositories.
Adding a repository to a running task, including on mobile, is separate from
this automatic project setup. See [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments#start-a-task-in-codex-cloud).

Each Cloud task has its own working files. In the desktop app, when you add a repository
to a task running in the default environment, that change applies to the current
task. To reuse a setup across tasks, create a reusable environment. File changes
in a task don't update a published environment. To change its starting point for
future tasks, update and republish the environment's setup if you have permission
to edit it.

A cloud task uses the files and services available in its cloud environment.
Your computer's local files, running processes, browser sign-ins, and VPN access
aren't automatically transferred to it.

For more terms, see [Codex concepts](https://learn.chatgpt.com/docs/prompting).

> Illustration: Desktop composer with the Work in menu open to This computer and Cloud, and a separate Worktree option
