---
source_type: 'learn'
source_area: 'learn_cloud'
source_url: 'https://learn.chatgpt.com/docs/cloud'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Codex Cloud

Source: https://learn.chatgpt.com/docs/cloud

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

## Run coding tasks in the cloud

Give Codex coding tasks to work through in the cloud, from investigating bugs to building features. Review changes and continue from the web, mobile, or desktop app.

> Illustration: A published cloud environment beside a new task composer with the same environment selected

### Start here

- [Get started](#getting-started)

### Why use Codex Cloud

- **Start with or without a repository:** If the default environment is available, you can start without choosing a repository. You can also ask Codex to check out any repository available to Codex through your connected GitHub or GitLab account.
- **Keep work moving:** Each task has its own workspace and can keep working while your computer is asleep.
- **Review the work:** Inspect changed files and check results, request follow-up changes, and commit or open a pull request when you're ready.

## Getting started

**Get started with Codex Cloud.**

Choose where to run your first task. If you want the same repositories and tools for future tasks, you can create and publish a reusable environment.

### 1. Choose Cloud

Sign in to ChatGPT. On the web or in the desktop app, start a chat and choose Work in > Cloud. On mobile, open Codex.

### 2. Choose an environment

If you see the default environment, select it to start without choosing a repository. To use a setup someone has already prepared, select a published environment. In Enterprise workspaces, select a published environment you can access.

### 3. Send your first task

Try a task that needs no repository, such as “Write a Python script that finds duplicate files by content. Test it on sample files.” Review the script and test results, then ask for any changes in the same chat.

### Next steps

- [Create and publish a reusable environment](https://learn.chatgpt.com/docs/environments/cloud-environments#create-and-publish-an-environment)
- [Configure internet access](https://learn.chatgpt.com/docs/environments/cloud-environments#connect-to-services)
- [Set up environment variables and network secrets](https://learn.chatgpt.com/docs/environments/cloud-environments#configure-environment-variables-and-network-secrets)
- [Understand saved state](https://learn.chatgpt.com/docs/environments/cloud-environments#reuse-and-update-saved-state)
- [Use ChatGPT in Slack](https://learn.chatgpt.com/docs/third-party/slack)

## See what Codex Cloud can do

Run coding tasks with your project tools and service access, then review the results.

- [Prepare your development workflow](https://learn.chatgpt.com/docs/environments/cloud-environments#create-and-publish-an-environment): Let Codex inspect your repositories and prepare their dependencies and tools. Review the checks before publishing.
- [Reuse your project setup](https://learn.chatgpt.com/docs/environments/cloud-environments#reuse-and-update-saved-state): Reuse your repositories, dependencies, and tools across tasks. Each task has its own workspace. Update the setup as your project changes.
- [Connect your tools and services](https://learn.chatgpt.com/docs/environments/cloud-environments#connect-to-services): Give Codex access to the package registries, APIs, and private services your project needs. Configure network access and supply credentials in the environment settings.

## Use Codex Cloud when…

- [Work should run remotely](https://learn.chatgpt.com/docs/environments/cloud-environments): Give Codex a cloud environment with the repositories and tools it needs.
- [Several tasks need the same setup](https://learn.chatgpt.com/docs/environments/cloud-environments): Start tasks from a published environment while keeping each task's working state separate.
- [Your workflow needs service credentials](https://learn.chatgpt.com/docs/environments/cloud-environments#connect-to-services): Use network secrets for allowed HTTPS services and limit the environment's network destinations.
- [Start cloud work from the CLI](https://learn.chatgpt.com/docs/developer-commands?surface=cli#cli-codex-cloud): Start a task from your terminal, or list recent cloud chats and check their status.
