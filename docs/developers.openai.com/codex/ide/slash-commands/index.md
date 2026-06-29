---
source_type: 'developers'
source_area: 'codex_ide'
source_url: 'https://developers.openai.com/codex/ide/slash-commands'
source_last_modified: '2026-05-21T23:47:09Z'
source_etag: 'W/"b69ecfd9ec34d6f49977b3f8aa5a4a12"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4"]
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
| `/goal` | Set a persistent goal for Codex to work toward. |
| `/local` | Switch to local mode to run the task in your workspace. |
| `/review` | Start code review mode to review uncommitted changes or compare against a base branch. |
| `/status` | Show the thread ID, context usage, and rate limits. |

If `/goal` doesn’t appear in the slash command list, enable `features.goals`
in `config.toml`:

```
[features]
goals = true
```

You can also run `codex features enable goals` from the CLI or ask Codex to run it.

