# Codex app settings

Source: https://developers.openai.com/codex/app/settings

Use the settings panel to tune how the Codex app behaves, how it opens files,
and how it connects to tools. Open [**Settings**](codex://settings) from the app menu or
press `Cmd`+`,`.

## General

Choose where files open and how much command output appears in threads. You can also
require `Cmd`+`Enter` for multiline prompts or prevent sleep while a
thread runs.

## Appearance

Pick a theme, decide whether the window is solid, and adjust UI or code fonts. Font
choices apply across the app, including the diff review panel and terminal.

## Notifications

Choose when turn completion notifications appear, and whether the app should prompt for
notification permissions.

## Agent configuration

Codex agents in the app inherit the same configuration as the IDE and CLI extension.
Use the in-app controls for common settings, or edit `config.toml` for advanced
options. See [Codex security](/codex/agent-approvals-security) and
[config basics](/codex/config-basic) for more detail.

## Git

Use Git settings to standardize branch naming and choose whether Codex uses force
pushes.
You can also set prompts that Codex uses to generate commit messages and pull request descriptions.

## Integrations & MCP

Connect external tools via MCP (Model Context Protocol). Enable recommended servers or
add your own. If a server requires OAuth, the app starts the auth flow. These settings
also apply to the Codex CLI and IDE extension because the MCP configuration lives in
`config.toml`. See the [Model Context Protocol docs](/codex/mcp) for details.

## Personalization

Choose **Friendly**, **Pragmatic**, or **None** as your default personality. Use
**None** to disable personality instructions. You can update this at any time.

You can also add your own custom instructions. Editing custom instructions updates your
[personal instructions in `AGENTS.md`](/codex/guides/agents-md).

## Archived threads

The **Archived threads** section lists archived chats with dates and project
context. Use **Unarchive** to restore a thread.

