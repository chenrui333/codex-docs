---
source_type: 'learn'
source_area: 'learn_cli_customization'
source_url: 'https://learn.chatgpt.com/docs/cli-customization'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# CLI customization

Source: https://learn.chatgpt.com/docs/cli-customization

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

The Codex CLI provides terminal-specific options for how interactive sessions
look and how you enter commands and prompts.

## Syntax highlighting and themes

The terminal UI (TUI) syntax-highlights fenced Markdown code blocks and file
diffs. Run `/theme` to open the theme picker, preview themes, and save your
selection to `tui.theme` in `$CODEX_HOME/config.toml`.

To add a custom theme, place a `.tmTheme` file in `$CODEX_HOME/themes`, then
select it from the theme picker.

## Shell completions

Generate a completion script for Bash, the Z shell, Fish, or PowerShell:

```bash
codex completion zsh
```

Load the script from your shell configuration. For the Z shell, add:

```bash
eval "$(codex completion zsh)"
```

If the Z shell reports `command not found: compdef`, initialize its completion system
before loading the Codex completions:

```bash
autoload -Uz compinit && compinit
eval "$(codex completion zsh)"
```

Restart the shell, type `codex`, and press <kbd>Tab</kbd> to verify completion.

## Prompt editor

For longer prompts, press <kbd>Ctrl</kbd>+<kbd>G</kbd> in the composer to open
the editor configured by `VISUAL`, or `EDITOR` when `VISUAL` isn't set. Save
and close the editor to return the text to the composer before sending it.

For interactive keyboard controls and the full command and option list, see
[Commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli#cli-interactive-shortcuts).
