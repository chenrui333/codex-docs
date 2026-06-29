---
source_type: 'developers'
source_area: 'codex_cli_docs'
source_url: 'https://developers.openai.com/codex/cli'
source_last_modified: '2026-06-13T00:21:16Z'
source_etag: 'W/"1dd0c944cec611464483b1ee1cf5fae6"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4"]
---

# CLI – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/cli

Codex CLI is OpenAI’s coding agent that you can run locally from your terminal. It can read, change, and run code on your machine in the selected directory.
It’s [open source](https://github.com/openai/codex) and built in Rust for speed and efficiency.

ChatGPT Plus, Pro, Business, Edu, and Enterprise plans include Codex. Learn more about [what’s included](/codex/pricing).

## CLI setup

Choose your install option

macOS/LinuxWindowsnpmHomebrew

1. 1

   ### Install

   Install the Codex CLI with the standalone installer for macOS and Linux.

   macOS/Linux install command

   curl -fsSL https://chatgpt.com/codex/install.sh | shCopy

   For unattended installs, set `CODEX_NON_INTERACTIVE=1` on the shell that runs the downloaded installer. See [Environment variables](/codex/environment-variables#installer-variables) for details.

   macOS/Linux unattended install command

   curl -fsSL https://chatgpt.com/codex/install.sh | CODEX\_NON\_INTERACTIVE=1 shCopy
2. 2

   ### Run

   Run Codex in a terminal. It can inspect your repository, edit files, and run commands.

   Run Codex command

   codexCopy

   The first time you run Codex, you'll be prompted to sign in. Authenticate with your ChatGPT account or an API key.

   See the [pricing page](/codex/pricing) if you're not sure which plans include Codex access.
3. 3

   ### Upgrade

   New versions of the Codex CLI are released regularly. See the [changelog](/codex/changelog) for release notes. To upgrade a standalone install, rerun the installer:

   macOS/Linux upgrade command

   curl -fsSL https://chatgpt.com/codex/install.sh | shCopy

The Codex CLI is available on macOS, Windows, and Linux. On Windows, run Codex
natively in PowerShell with the Windows sandbox, or use WSL2 when you need a
Linux-native environment. For setup details, see the
[Windows setup guide](/codex/windows).

If you’re new to Codex, read the [best practices guide](/codex/learn/best-practices).

---

## Work with the Codex CLI

[### Run Codex interactively

Run `codex` to start an interactive terminal UI (TUI) session.](/codex/cli/features#running-in-interactive-mode)[### Control model and reasoning

Use `/model` to switch between available models or adjust reasoning levels.](/codex/cli/features#models-and-reasoning)[### Image inputs

Attach screenshots or design specs so Codex reads them alongside your prompt.](/codex/cli/features#image-inputs)[### Image generation

Generate or edit images directly in the CLI, and attach references when you want Codex to iterate on an existing asset.](/codex/cli/features#image-generation)[### Run local code review

Get your code reviewed by a separate Codex agent before you commit or push your changes.](/codex/cli/features#running-local-code-review)[### Use subagents

Use subagents to parallelize complex tasks.](/codex/subagents)[### Web search

Use Codex to search the web and get up-to-date information for your task.](/codex/cli/features#web-search)[### Codex Cloud tasks

Launch a Codex Cloud task, choose environments, and apply the resulting diffs without leaving your terminal.](/codex/cli/features#working-with-codex-cloud)[### Scripting Codex

Automate repeatable workflows by scripting Codex with the `exec` command.](/codex/noninteractive)[### Model Context Protocol

Give Codex access to additional third-party tools and context with Model Context Protocol (MCP).](/codex/mcp)[### Approval modes

Choose the approval mode that matches your comfort level before Codex edits or runs commands.](/codex/cli/features#approval-modes)

