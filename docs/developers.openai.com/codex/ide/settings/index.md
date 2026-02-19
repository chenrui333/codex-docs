# Codex IDE extension settings

Source: https://developers.openai.com/codex/ide/settings

Use these settings to customize the Codex IDE extension.

## Change a setting

To change a setting, follow these steps:

1. Open your editor settings.
2. Search for `Codex` or the setting name.
3. Update the value.

The Codex IDE extension uses the Codex CLI. Configure some behavior, such as the default model, approvals, and sandbox settings, in the shared `~/.codex/config.toml` file instead of in editor settings. See [Config basics](/codex/config-basic).

## Settings reference

| Setting | Description |
| --- | --- |
| `chatgpt.cliExecutable` | Development only: Path to the Codex CLI executable. You don’t need to set this unless you’re actively developing the Codex CLI. If you set this manually, parts of the extension might not work as expected. |
| `chatgpt.commentCodeLensEnabled` | Show CodeLens above to-do comments so you can complete them with Codex. |
| `chatgpt.localeOverride` | Preferred language for the Codex UI. Leave empty to detect automatically. |
| `chatgpt.openOnStartup` | Focus the Codex sidebar when the extension finishes starting. |
| `chatgpt.runCodexInWindowsSubsystemForLinux` | Windows only: Run Codex in WSL when Windows Subsystem for Linux (WSL) is available. Recommended for improved sandbox security and better performance. Codex agent mode on Windows currently requires WSL. Changing this setting reloads VS Code to apply the change. |

