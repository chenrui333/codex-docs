---
source_type: 'developers'
source_area: 'codex_migrate'
source_url: 'https://developers.openai.com/codex/migrate'
source_last_modified: '2026-05-01T23:22:21Z'
source_etag: 'W/"344b0640ed63fc28b79b8ee1e109ed9a"'
codex_cli_versions: ["0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0"]
codex_cli_versions_raw: ["codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0"]
---

# Migrate to Codex | OpenAI Developers

Source: https://developers.openai.com/codex/migrate

Use the import flow to bring your instructions, configuration, skills, MCP
servers, hooks, subagents, and recent sessions from another agent into Codex.
Codex migrates the parts it can handle directly and can open a follow-up thread
to help migrate anything that remains.

![Import from another agent in General settings](/images/codex/migrate/import-flow-light.png)

## Start the migration

1. Open **Settings** in the Codex app.
2. On the **General** page, find **Import other agent setup**.
3. Select **Import** or **Import again**.
4. Review what Codex found, choose what to bring over, then select **Import**.
5. After the import finishes, select **View imported files** if you want to inspect the result.

## How migration works

Codex checks both your user-level setup and the current project. User-level
setup comes from files on your machine; project-level setup comes from files in
the repository you have open.

When you import, Codex:

1. Detects the setup it can find.
2. Imports the selected items it can migrate directly.
3. Checks again after the import finishes.
4. Offers to continue the migration in a new thread if anything still needs
   follow-up work.

## What Codex can import

| Detected setup | Codex destination |
| --- | --- |
| Instruction files | [`AGENTS.md`](/codex/guides/agents-md) |
| `settings.json` | [`config.toml`](/codex/config-basic) |
| Skills | [Codex skills](/codex/skills) |
| Recent sessions from the last 30 days | Codex threads and projects |
| MCP server configuration | [Codex MCP configuration](/codex/mcp) |
| Hooks | [Codex hooks](/codex/hooks) |
| Slash commands | [Codex skills](/codex/skills) |
| Subagents | [Codex agents](/codex/subagents) |

## Finish remaining setup in a new thread

Some detected setup does not have a clean one-to-one mapping into Codex. For
those items, Codex can open a new thread with the
[`migrate-to-codex`](https://github.com/openai/skills/tree/main/skills/.curated/migrate-to-codex)
skill to help finish the migration.

When that happens, Codex shows the remaining setup and offers **Continue in
Codex**.

![Additional setup found after import](/images/codex/migrate/additional-setup-light.png)

If you continue, Codex opens a new thread with the remaining work already filled
in. The thread keeps user-level setup separate from project-level setup so you
can see where each remaining item belongs.

![Follow-up migration task in Codex](/images/codex/migrate/continue-with-codex-light.png)

## What to review after import

Review any migrated setup before you rely on it, especially:

- Tool restrictions or permissions in imported skills and agents.
- MCP server settings that use custom authentication, headers, environment
  variables, or transports.
- Hooks whose behavior may differ in Codex.
- Plugins, marketplaces, or other remaining setup that needs manual follow-up.
- Prompt templates or command-style prompts that depend on arguments, shell
  interpolation, or file-path placeholders.

## After you switch

Once the import finishes, open one of your migrated projects and continue from
there. If you are new to Codex, see the [quickstart](/codex/quickstart) for the
rest of the setup flow.

