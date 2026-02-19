# Codex IDE extension slash commands

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

