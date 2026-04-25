---
source_type: 'developers'
source_url: 'https://developers.openai.com/codex/app/commands'
source_last_modified: '2026-04-25T06:34:54Z'
source_etag: 'W/"88a1b7116add206986a2dde19944c5fa"'
codex_cli_versions: ["0.125.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0"]
---

# Commands – Codex app | OpenAI Developers

Source: https://developers.openai.com/codex/app/commands

Use these commands and keyboard shortcuts to navigate the Codex app.

## Keyboard shortcuts

|  | Action | macOS shortcut |
| --- | --- | --- |
| **General** |  |  |
|  | Command menu | `Cmd` + `Shift` + `P` or `Cmd` + `K` |
|  | Settings | `Cmd` + `,` |
|  | Open folder | `Cmd` + `O` |
|  | Navigate back | `Cmd` + `[` |
|  | Navigate forward | `Cmd` + `]` |
|  | Increase font size | `Cmd` + `+` or `Cmd` + `=` |
|  | Decrease font size | `Cmd` + `-` or `Cmd` + `_` |
|  | Toggle sidebar | `Cmd` + `B` |
|  | Toggle diff panel | `Cmd` + `Option` + `B` |
|  | Toggle terminal | `Cmd` + `J` |
|  | Clear the terminal | `Ctrl` + `L` |
| **Thread** |  |  |
|  | New thread | `Cmd` + `N` or `Cmd` + `Shift` + `O` |
|  | Find in thread | `Cmd` + `F` |
|  | Previous thread | `Cmd` + `Shift` + `[` |
|  | Next thread | `Cmd` + `Shift` + `]` |
|  | Dictation | `Ctrl` + `M` |

## Slash commands

Slash commands let you control Codex without leaving the thread composer. Available commands vary based on your environment and access.

### Use a slash command

1. In the thread composer, type `/`.
2. Select a command from the list, or keep typing to filter (for example, `/status`).

You can also explicitly invoke skills by typing `$` in the thread composer. See [Skills](/codex/skills).

Enabled skills also appear in the slash command list.

### Available slash commands

| Slash command | Description |
| --- | --- |
| `/feedback` | Open the feedback dialog to submit feedback and optionally include logs. |
| `/mcp` | Open MCP status to view connected servers. |
| `/plan-mode` | Toggle plan mode for multi-step planning. |
| `/review` | Start code review mode to review uncommitted changes or compare against a base branch. |
| `/status` | Show the thread ID, context usage, and rate limits. |

## Deeplinks

The Codex app registers the `codex://` URL scheme so links can open specific parts of the app directly.

| Deeplink | Opens | Supported query parameters |
| --- | --- | --- |
| `codex://settings` | Settings. | None. |
| `codex://skills` | Skills. | None. |
| `codex://automations` | Inbox in automation create mode. | None. |
| `codex://threads/<thread-id>` | A local thread. `<thread-id>` must be a UUID. | None. |
| `codex://new` | A new thread. | Optional: `prompt`, `originUrl`, `path`. |

For new-thread deeplinks:

- `prompt` sets the initial composer text.
- `path` must be an absolute path to a local directory and, when valid, makes that directory the active workspace for the new thread.
- `originUrl` tries to match one of your current workspace roots by Git remote URL. If both `path` and `originUrl` are present, Codex resolves `path` first.

## See also

- [Features](/codex/app/features)
- [Settings](/codex/app/settings)

