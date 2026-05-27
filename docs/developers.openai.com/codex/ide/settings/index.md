---
source_type: 'developers'
source_area: 'codex_ide'
source_url: 'https://developers.openai.com/codex/ide/settings'
source_last_modified: '2026-04-25T06:59:52Z'
source_etag: 'W/"f7967ea037e46d6ebcd3f5fef5f7554c"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0"]
---

# Settings – Codex IDE | OpenAI Developers

Source: https://developers.openai.com/codex/ide/settings

Use these settings to customize the Codex IDE extension.

## Change a setting

To change a setting, follow these steps:

1. Open your editor settings.
2. Search for `Codex` or the setting name.
3. Update the value.

The Codex IDE extension uses the Codex CLI. Configure some behavior, such as the default model, approvals, and sandbox settings, in the shared `~/.codex/config.toml` file instead of in editor settings. See [Config basics](/codex/config-basic).

The extension also honors VS Code’s built-in chat font settings for Codex conversation surfaces.

## Settings reference

| Setting | Description |
| --- | --- |
| `chat.fontSize` | Controls chat text in the Codex sidebar, including conversation content and the composer. |
| `chat.editor.fontSize` | Controls code-rendered content in Codex conversations, including code snippets and diffs. |
| `chatgpt.cliExecutable` | Development only: Path to the Codex CLI executable. You don’t need to set this unless you’re actively developing the Codex CLI. If you set this manually, parts of the extension might not work as expected. |
| `chatgpt.commentCodeLensEnabled` | Show CodeLens above to-do comments so you can complete them with Codex. |
| `chatgpt.localeOverride` | Preferred language for the Codex UI. Leave empty to detect automatically. |
| `chatgpt.openOnStartup` | Focus the Codex sidebar when the extension finishes starting. |
| `chatgpt.runCodexInWindowsSubsystemForLinux` | Windows only: Run Codex in WSL when Windows Subsystem for Linux (WSL) is available. Use this when your repositories and tooling live in WSL2 or when you need Linux-native tooling. Otherwise, Codex can run natively on Windows with the Windows sandbox. Changing this setting reloads VS Code to apply the change. |

