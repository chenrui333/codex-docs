---
source_type: 'learn'
source_area: 'learn_integrated_terminal'
source_url: 'https://learn.chatgpt.com/docs/integrated-terminal'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0"]
---

# Integrated terminal

Source: https://learn.chatgpt.com/docs/integrated-terminal

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Each chat in the ChatGPT desktop app includes a terminal scoped to its current project or
worktree. Open it from the terminal icon in the top-right corner of the app, or
press <kbd>Ctrl</kbd>+<kbd>`</kbd>.

> Illustration: Integrated terminal drawer open beneath a ChatGPT chat

## Run and validate your project

Use the terminal to validate changes, run scripts, and perform Git operations
without switching apps. ChatGPT can read the current terminal output, so it can
check a running development server or refer to a failed build while it works
with you.

Common commands include:

- `git status`
- `git pull --rebase`
- `pnpm test` or `npm test`
- `pnpm run lint` or another project-specific check

## Create reusable actions

If you run a command regularly, define an action in your [local environment](https://learn.chatgpt.com/docs/environments/local-environment#actions).
Actions appear as shortcuts in the ChatGPT desktop app and run in the integrated
terminal.

<kbd>Cmd</kbd>+<kbd>K</kbd> opens the app command palette; it doesn't clear the
terminal. To clear the terminal, press <kbd>Ctrl</kbd>+<kbd>L</kbd>.
