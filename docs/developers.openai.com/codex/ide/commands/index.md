---
source_type: 'developers'
source_area: 'codex_ide'
source_url: 'https://developers.openai.com/codex/ide/commands'
source_last_modified: '2026-04-25T06:50:32Z'
source_etag: 'W/"5be07632ccd60e5563d207a6c860f829"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0"]
---

# Commands – Codex IDE | OpenAI Developers

Source: https://developers.openai.com/codex/ide/commands

Use these commands to control Codex from the VS Code Command Palette. You can also bind them to keyboard shortcuts.

## Assign a key binding

To assign or change a key binding for a Codex command:

1. Open the Command Palette (**Cmd+Shift+P** on macOS or **Ctrl+Shift+P** on Windows/Linux).
2. Run **Preferences: Open Keyboard Shortcuts**.
3. Search for `Codex` or the command ID (for example, `chatgpt.newChat`).
4. Select the pencil icon, then enter the shortcut you want.

## Extension commands

| Command | Default key binding | Description |
| --- | --- | --- |
| `chatgpt.addToThread` | - | Add selected text range as context for the current thread |
| `chatgpt.addFileToThread` | - | Add the entire file as context for the current thread |
| `chatgpt.newChat` | macOS: `Cmd+N` Windows/Linux: `Ctrl+N` | Create a new thread |
| `chatgpt.implementTodo` | - | Ask Codex to address the selected TODO comment |
| `chatgpt.newCodexPanel` | - | Create a new Codex panel |
| `chatgpt.openSidebar` | - | Opens the Codex sidebar panel |

