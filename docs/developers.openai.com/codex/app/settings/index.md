# Settings – Codex app | OpenAI Developers

Source: https://developers.openai.com/codex/app/settings

Use the settings panel to tune how the Codex app behaves, how it opens files,
and how it connects to tools. Open [**Settings**](codex://settings) from the app menu or
press `Cmd`+`,`.

## General

Choose where files open and how much command output appears in threads. You can also
require `Cmd`+`Enter` for multiline prompts or prevent sleep while a
thread runs.

## Notifications

Choose when turn completion notifications appear, and whether the app should prompt for
notification permissions.

## Agent configuration

Codex agents in the app inherit the same configuration as the IDE and CLI extension.
Use the in-app controls for common settings, or edit `config.toml` for advanced
options. See [Codex security](/codex/agent-approvals-security) and
[config basics](/codex/config-basic) for more detail.

## Appearance

In **Settings**, you can change the Codex app appearance by choosing a base theme,
adjusting accent, background, and foreground colors, and changing the UI and code
fonts. You can also share your custom theme with friends.

![Codex app Appearance settings showing theme selection, color controls, and font options](/images/codex/app/theme-selection-light.webp)

## Git

Use Git settings to standardize branch naming and choose whether Codex uses force
pushes.
You can also set prompts that Codex uses to generate commit messages and pull request descriptions.

## Integrations & MCP

Connect external tools via MCP (Model Context Protocol). Enable recommended servers or
add your own. If a server requires OAuth, the app starts the auth flow. These settings
also apply to the Codex CLI and IDE extension because the MCP configuration lives in
`config.toml`. See the [Model Context Protocol docs](/codex/mcp) for details.

## Browser use

Use these settings to install or enable the bundled Browser plugin and manage
allowlisted and blocklisted websites. Codex asks before using a website
unless you’ve allowlisted it. Removing a site from the blocklist lets Codex ask
again before using it in the browser.

See [In-app browser](/codex/app/browser) for browser preview, comment, and
browser use workflows.

## Computer Use

On macOS, check your Computer Use settings to review desktop-app access and related
preferences after setup. To revoke system-level access, update Screen Recording
or Accessibility permissions in macOS Privacy & Security settings. The feature
isn’t available in the European Economic Area, the United Kingdom, or Switzerland
at launch.

## Personalization

Choose **Friendly**, **Pragmatic**, or **None** as your default personality. Use
**None** to disable personality instructions. You can update this at any time.

You can also add your own custom instructions. Editing custom instructions updates your
[personal instructions in `AGENTS.md`](/codex/guides/agents-md).

## Context-aware suggestions

Use context-aware suggestions to surface follow-ups and tasks you may want to resume when you
start or return to Codex.

## Memories

Enable Memories, where available, to let Codex carry useful context from past
threads into future work. See [Memories](/codex/memories) for setup, storage,
and per-thread controls.

## Archived threads

The **Archived threads** section lists archived chats with dates and project
context. Use **Unarchive** to restore a thread.

