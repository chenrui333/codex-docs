# Codex IDE extension commands

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

