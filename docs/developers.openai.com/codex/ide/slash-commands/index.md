---
source_type: 'developers'
source_area: 'codex_ide'
source_url: 'https://developers.openai.com/codex/ide/slash-commands'
source_last_modified: '2026-04-25T06:40:05Z'
source_etag: 'W/"cd0bd1e7c43713a6ded2fa693993c5ef"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0"]
---

# Slash commands – Codex IDE | OpenAI Developers

Source: https://developers.openai.com/codex/ide/slash-commands

Slash commands let you control Codex without leaving the chat input. Use them to check status, switch between local and cloud mode, or send feedback.

## Use a slash command

1. In the Codex chat input, type `/`.
2. Select a command from the list, or keep typing to filter (for example, `/status`).
3. Press **Enter**.

## Available slash commands

| Slash command | Description |
| --- | --- |
| `/auto-context` | Turn Auto Context on or off to include recent files and IDE context automatically. |
| `/cloud` | Switch to cloud mode to run the task remotely (requires cloud access). |
| `/cloud-environment` | Choose the cloud environment to use (available only in cloud mode). |
| `/feedback` | Open the feedback dialog to submit feedback and optionally include logs. |
| `/local` | Switch to local mode to run the task in your workspace. |
| `/review` | Start code review mode to review uncommitted changes or compare against a base branch. |
| `/status` | Show the thread ID, context usage, and rate limits. |

