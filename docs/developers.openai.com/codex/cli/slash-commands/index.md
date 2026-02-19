# Slash commands in Codex CLI

Source: https://developers.openai.com/codex/cli/slash-commands

Slash commands give you fast, keyboard-first control over Codex. Type `/` in the composer to open the slash popup, choose a command, and Codex will perform actions such as switching models, adjusting permissions, or summarizing long conversations without leaving the terminal.

This guide shows you how to:

- Find the right built-in slash command for a task
- Steer an active session with commands like `/model`, `/personality`, `/permissions`, `/experimental`, `/agent`, and `/status`

## Built-in slash commands

Codex ships with the following commands. Open the slash popup and start typing the command name to filter the list.

| Command | Purpose | When to use it |
| --- | --- | --- |
| [`/permissions`](#update-permissions-with-permissions) | Set what Codex can do without asking first. | Relax or tighten approval requirements mid-session, such as switching between Auto and Read Only. |
| [`/sandbox-add-read-dir`](#grant-sandbox-read-access-with-sandbox-add-read-dir) | Grant sandbox read access to an extra directory (Windows only). | Unblock commands that need to read an absolute directory path outside the current readable roots. |
| [`/agent`](#switch-agent-threads-with-agent) | Switch the active agent thread. | Inspect or continue work in a spawned sub-agent thread. |
| [`/apps`](#browse-apps-with-apps) | Browse apps (connectors) and insert them into your prompt. | Attach an app as `$app-slug` before asking Codex to use it. |
| [`/compact`](#keep-transcripts-lean-with-compact) | Summarize the visible conversation to free tokens. | Use after long runs so Codex retains key points without blowing the context window. |
| [`/diff`](#review-changes-with-diff) | Show the Git diff, including files Git isn’t tracking yet. | Review Codex’s edits before you commit or run tests. |
| [`/exit`](#exit-the-cli-with-quit-or-exit) | Exit the CLI (same as `/quit`). | Alternative spelling; both commands exit the session. |
| [`/experimental`](#toggle-experimental-features-with-experimental) | Toggle experimental features. | Enable optional features such as sub-agents from the CLI. |
| [`/feedback`](#send-feedback-with-feedback) | Send logs to the Codex maintainers. | Report issues or share diagnostics with support. |
| [`/init`](#generate-agentsmd-with-init) | Generate an `AGENTS.md` scaffold in the current directory. | Capture persistent instructions for the repository or subdirectory you’re working in. |
| [`/logout`](#sign-out-with-logout) | Sign out of Codex. | Clear local credentials when using a shared machine. |
| [`/mcp`](#list-mcp-tools-with-mcp) | List configured Model Context Protocol (MCP) tools. | Check which external tools Codex can call during the session. |
| [`/mention`](#highlight-files-with-mention) | Attach a file to the conversation. | Point Codex at specific files or folders you want it to inspect next. |
| [`/model`](#set-the-active-model-with-model) | Choose the active model (and reasoning effort, when available). | Switch between general-purpose models (`gpt-4.1-mini`) and deeper reasoning models before running a task. |
| [`/plan`](#switch-to-plan-mode-with-plan) | Switch to plan mode and optionally send a prompt. | Ask Codex to propose an execution plan before implementation work starts. |
| [`/personality`](#set-a-communication-style-with-personality) | Choose a communication style for responses. | Make Codex more concise, more explanatory, or more collaborative without changing your instructions. |
| [`/ps`](#check-background-terminals-with-ps) | Show experimental background terminals and their recent output. | Check long-running commands without leaving the main transcript. |
| [`/fork`](#fork-the-current-conversation-with-fork) | Fork the current conversation into a new thread. | Branch the active session to explore a new approach without losing the current transcript. |
| [`/resume`](#resume-a-saved-conversation-with-resume) | Resume a saved conversation from your session list. | Continue work from a previous CLI session without starting over. |
| [`/new`](#start-a-new-conversation-with-new) | Start a new conversation inside the same CLI session. | Reset the chat context without leaving the CLI when you want a fresh prompt in the same repo. |
| [`/quit`](#exit-the-cli-with-quit-or-exit) | Exit the CLI. | Leave the session immediately. |
| [`/review`](#ask-for-a-working-tree-review-with-review) | Ask Codex to review your working tree. | Run after Codex completes work or when you want a second set of eyes on local changes. |
| [`/status`](#inspect-the-session-with-status) | Display session configuration and token usage. | Confirm the active model, approval policy, writable roots, and remaining context capacity. |
| [`/debug-config`](#inspect-config-layers-with-debug-config) | Print config layer and requirements diagnostics. | Debug precedence and policy requirements, including experimental network constraints. |
| [`/statusline`](#configure-footer-items-with-statusline) | Configure TUI status-line fields interactively. | Pick and reorder footer items (model/context/limits/git/tokens/session) and persist in config.toml. |

`/quit` and `/exit` both exit the CLI. Use them only after you have saved or committed any important work.

The `/approvals` command still works as an alias, but it no longer appears in the slash popup list.

## Control your session with slash commands

The following workflows keep your session on track without restarting Codex.

### Set the active model with `/model`

1. Start Codex and open the composer.
2. Type `/model` and press Enter.
3. Choose a model such as `gpt-4.1-mini` or `gpt-4.1` from the popup.

Expected: Codex confirms the new model in the transcript. Run `/status` to verify the change.

### Set a communication style with `/personality`

Use `/personality` to change how Codex communicates without rewriting your prompt.

1. In an active conversation, type `/personality` and press Enter.
2. Choose a style from the popup.

Expected: Codex confirms the new style in the transcript and uses it for later responses in the thread.

Codex supports `friendly`, `pragmatic`, and `none` personalities. Use `none` to disable personality instructions.

If the active model doesn’t support personality-specific instructions, Codex hides this command.

### Switch to plan mode with `/plan`

1. Type `/plan` and press Enter to switch the active conversation into plan mode.
2. Optional: provide inline prompt text (for example, `/plan Propose a migration plan for this service`).
3. You can paste content or attach images while using inline `/plan` arguments.

Expected: Codex enters plan mode and uses your optional inline prompt as the first planning request.

While a task is already running, `/plan` is temporarily unavailable.

### Toggle experimental features with `/experimental`

1. Type `/experimental` and press Enter.
2. Toggle the features you want (for example, **Multi-agents**), then restart Codex.

Expected: Codex saves your feature choices to config and applies them on restart.

### Update permissions with `/permissions`

1. Type `/permissions` and press Enter.
2. Select the approval preset that matches your comfort level, for example `Auto` for hands-off runs or `Read Only` to review edits.

Expected: Codex announces the updated policy. Future actions respect the new approval mode until you change it again.

### Grant sandbox read access with `/sandbox-add-read-dir`

This command is available only when running the CLI natively on Windows.

1. Type `/sandbox-add-read-dir C:\absolute\directory\path` and press Enter.
2. Confirm the path is an existing absolute directory.

Expected: Codex refreshes the Windows sandbox policy and grants read access to that directory for later commands that run in the sandbox.

### Inspect the session with `/status`

1. In any conversation, type `/status`.
2. Review the output for the active model, approval policy, writable roots, and current token usage.

Expected: You see a summary like what `codex status` prints in the shell, confirming Codex is operating where you expect.

### Inspect config layers with `/debug-config`

1. Type `/debug-config`.
2. Review the output for config layer order (lowest precedence first), on/off state, and policy sources.

Expected: Codex prints layer diagnostics plus policy details such as `allowed_approval_policies`, `allowed_sandbox_modes`, `mcp_servers`, `rules`, `enforce_residency`, and `experimental_network` when configured.

Use this output to debug why an effective setting differs from `config.toml`.

### Configure footer items with `/statusline`

1. Type `/statusline`.
2. Use the picker to toggle and reorder items, then confirm.

Expected: The footer status line updates immediately and persists to `tui.status_line` in `config.toml`.

Available status-line items include model, model+reasoning, context stats, rate limits, git branch, token counters, session id, current directory/project root, and Codex version.

### Check background terminals with `/ps`

1. Type `/ps`.
2. Review the list of background terminals and their status.

Expected: Codex shows each background terminal’s command plus up to three recent, non-empty output lines so you can gauge progress at a glance.

Background terminals appear when `unified_exec` is in use; otherwise, the list may be empty.

### Keep transcripts lean with `/compact`

1. After a long exchange, type `/compact`.
2. Confirm when Codex offers to summarize the conversation so far.

Expected: Codex replaces earlier turns with a concise summary, freeing context while keeping critical details.

### Review changes with `/diff`

1. Type `/diff` to inspect the Git diff.
2. Scroll through the output inside the CLI to review edits and added files.

Expected: Codex shows changes you’ve staged, changes you haven’t staged yet, and files Git hasn’t started tracking, so you can decide what to keep.

### Highlight files with `/mention`

1. Type `/mention` followed by a path, for example `/mention src/lib/api.ts`.
2. Select the matching result from the popup.

Expected: Codex adds the file to the conversation, ensuring follow-up turns reference it directly.

### Start a new conversation with `/new`

1. Type `/new` and press Enter.

Expected: Codex starts a fresh conversation in the same CLI session, so you can switch tasks without leaving your terminal.

### Resume a saved conversation with `/resume`

1. Type `/resume` and press Enter.
2. Choose the session you want from the saved-session picker.

Expected: Codex reloads the selected conversation’s transcript so you can pick up where you left off, keeping the original history intact.

### Fork the current conversation with `/fork`

1. Type `/fork` and press Enter.

Expected: Codex clones the current conversation into a new thread with a fresh ID, leaving the original transcript untouched so you can explore an alternative approach in parallel.

If you need to fork a saved session instead of the current one, run `codex fork` in your terminal to open the session picker.

### Generate `AGENTS.md` with `/init`

1. Run `/init` in the directory where you want Codex to look for persistent instructions.
2. Review the generated `AGENTS.md`, then edit it to match your repository conventions.

Expected: Codex creates an `AGENTS.md` scaffold you can refine and commit for future sessions.

### Ask for a working tree review with `/review`

1. Type `/review`.
2. Follow up with `/diff` if you want to inspect the exact file changes.

Expected: Codex summarizes issues it finds in your working tree, focusing on behavior changes and missing tests. It uses the current session model unless you set `review_model` in `config.toml`.

### List MCP tools with `/mcp`

1. Type `/mcp`.
2. Review the list to confirm which MCP servers and tools are available.

Expected: You see the configured Model Context Protocol (MCP) tools Codex can call in this session.

### Browse apps with `/apps`

1. Type `/apps`.
2. Pick an app from the list.

Expected: Codex inserts the app mention into the composer as `$app-slug`, so you can immediately ask Codex to use it.

### Switch agent threads with `/agent`

1. Type `/agent` and press Enter.
2. Select the thread you want from the picker.

Expected: Codex switches the active thread so you can inspect or continue that agent’s work.

### Send feedback with `/feedback`

1. Type `/feedback` and press Enter.
2. Follow the prompts to include logs or diagnostics.

Expected: Codex collects the requested diagnostics and submits them to the maintainers.

### Sign out with `/logout`

1. Type `/logout` and press Enter.

Expected: Codex clears local credentials for the current user session.

### Exit the CLI with `/quit` or `/exit`

1. Type `/quit` (or `/exit`) and press Enter.

Expected: Codex exits immediately. Save or commit any important work first.

