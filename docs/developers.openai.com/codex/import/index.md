---
source_type: 'developers'
source_area: 'codex_import'
source_url: 'https://developers.openai.com/codex/import'
source_last_modified: '2026-06-14T16:18:01Z'
source_etag: 'W/"f13938be3c3210d02f9599502af34b34"'
codex_cli_versions: ["0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3"]
codex_cli_versions_raw: ["codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3"]
---

# Import to Codex | OpenAI Developers

Source: https://developers.openai.com/codex/import

Use the import flow to bring your instructions, settings, skills, plugins,
projects, and recent chat sessions from other agents into Codex. Codex imports
the supported items directly and lets you finish setup for any imported plugins
or connections that need authorization.

Importing does not change or delete your existing agent setup.

![Choose the other AI apps to import from](/images/codex/import/import-source.png)

## Start an import

1. In the Codex app, open **Settings**.
2. Under **General**, find **Import other agent setup**.
3. Select **Import**.
4. Choose the agents you want to import from, then select **Continue**.
5. On **Select items to import**, select **Continue** to import everything or **Customize** to choose specific items.
6. If you customize the import, select the items to bring over, then select **Confirm**.
7. After the import finishes, open an imported project or thread to continue working.

![Select the setup and recent work to import into Codex](/images/codex/import/import-overview.png)

## How importing works

Codex checks both your user-level setup and your existing projects. User-level
setup comes from files on your machine. Project-level setup comes from files in
the repositories and folders you select.

When you import, Codex:

1. Detects supported setup and recent work.
2. Imports the items you select.
3. Leaves your existing agent setup unchanged.
4. Checks whether imported plugins or connections still need setup.
5. Shows a status card when follow-up is required.

## What Codex can import

| Imported item | Codex destination |
| --- | --- |
| Instruction files | [`AGENTS.md`](/codex/guides/agents-md) |
| `settings.json` | [`config.toml`](/codex/config-basic) |
| Skills | [Codex skills](/codex/skills) |
| Plugins | Codex plugins |
| Existing project folders | Codex projects using the same folders |
| Chat sessions from the last 30 days | Codex threads |
| MCP server configuration | [Codex MCP configuration](/codex/mcp) |
| Hooks | [Codex hooks](/codex/hooks) |
| Slash commands | [Codex skills](/codex/skills) |
| Subagents | [Codex agents](/codex/subagents) |

![Choose the instructions, settings, skills, plugins, projects, and chats to import](/images/codex/import/import-instructions.png)

## Finish setup after importing

When the import completes, Codex shows a status card in the lower-left corner.
If an imported plugin or connection still needs setup, the card calls it out.

When Codex flags an item that needs attention, select **Finish** and follow the
prompts to complete setup.

## What to review after importing

Review imported setup before you rely on it, especially:

- Tool restrictions or permissions in imported skills and agents.
- MCP server settings that use custom authentication, headers, environment
  variables, or transports. You may need to sign in again.
- Hooks whose behavior may differ in Codex.
- Plugins, marketplaces, or other setup that needs manual follow-up.
- Prompt templates or command-style prompts that depend on arguments, shell
  interpolation, or file-path placeholders.

## After you import

Once the import finishes, open one of your imported projects and continue from
there. If you are new to Codex, see the [quickstart](/codex/quickstart) for the
rest of the setup flow.

