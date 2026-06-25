---
source_type: 'developers'
source_area: 'codex_cli_docs'
source_url: 'https://developers.openai.com/codex/plugins'
source_last_modified: '2026-06-18T22:41:45Z'
source_etag: 'W/"d3ba4376107305afeab42cb408e90589"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1"]
---

# Plugins – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/plugins

## Overview

Plugins bundle skills, app integrations, and MCP servers into reusable
workflows for Codex.

Extend what Codex can do, for example:

- Install the Codex Security plugin to scan authorized code and confirm
  plausible vulnerability findings.
- Install the Gmail plugin to let Codex read and manage Gmail.
- Install the Google Drive plugin to work across Drive, Docs, Sheets, and
  Slides.
- Install the Slack plugin to summarize channels or draft replies.
- Install [Sites](/codex/sites) to create and deploy hosted websites,
  web apps, and games.

A plugin can contain:

- **Skills:** reusable instructions for specific kinds of work. Codex can load
  them when needed so it follows the right steps and uses the right references
  or helper scripts for a task.
- **Apps:** connections to tools like GitHub, Slack, or Google Drive, so
  Codex can read information from those tools and take actions in them.
- **MCP servers:** services that give Codex access to more tools or shared
  information, often from systems outside your local project.

You can share plugins by publishing them through a marketplace source, such as a
repo marketplace for a project or team. See [Build plugins](/codex/plugins/build)
for marketplace setup, packaging, and distribution guidance.

## Use and install plugins

### Plugin Directory in the Codex app

Open **Plugins** in the Codex app to browse and install curated plugins.

![Codex Plugins page](/images/codex/plugins/directory.webp)

The plugin directory groups plugins into categories:

- **Curated by OpenAI:** highlighted plugins available to all Codex users.
- **Shared with you:** plugins shared by other members of your ChatGPT
  workspace.
- **Created by you:** plugins you created or added to your own workspace.

### Plugin directory in the CLI

In Codex CLI, run the following command to open the plugins list:

```
codex
/plugins
```

![Plugins list in Codex CLI](/images/codex/plugins/cli_light.png)

The CLI plugin browser groups plugins by marketplace. Use the marketplace tabs
to switch sources, open a plugin to inspect details, install or uninstall
marketplace entries, and press `Space` on an installed plugin to toggle
its enabled state.

### Install and use a plugin

Once you open the plugin directory:

1. Search or browse for a plugin, then open its details.
2. Select the install button. In the app, select the plus button or
   **Add to Codex**. In the CLI, select `Install plugin`.
3. If the plugin needs an external app, connect it when prompted. Some plugins
   ask you to authenticate during install. Others wait until the first time you
   use them.
4. After installation, start a new thread and ask Codex to use the plugin.

After you install a plugin, you can use it directly in the prompt window:

![Codex Plugins page](/images/codex/plugins/plugin-github-invoke.png)

Describe the task directly

Ask for the outcome you want, such as “Summarize unread Gmail threads
from today” or “Pull the latest launch notes from Google Drive.”

Use this when you want Codex to choose the right installed tools for the
task.

Choose a specific plugin

Type `@` to invoke the plugin or one of its bundled skills
explicitly.

Use this when you want to be specific about which plugin or skill Codex
should use. See [Codex app commands](/codex/app/commands) and
[Skills](/codex/skills).

### How permissions and data sharing work

Installing a plugin makes its workflows available in Codex, but your existing
[approval settings](/codex/agent-approvals-security) still apply. Any
connected external services remain subject to their own authentication,
privacy, and data-sharing policies.

- Bundled skills are available as soon as you install the plugin.
- If a plugin includes apps, Codex may prompt you to install or sign in to
  those apps in ChatGPT during setup or the first time you use them.
- If a plugin includes MCP servers, they may require extra setup or
  authentication before you can use them.
- When Codex sends data through a bundled app, that app’s terms and privacy
  policy apply.

### Remove or turn off a plugin

To remove a plugin, reopen it from the plugin browser and select
**Uninstall plugin**.

Uninstalling a plugin removes the plugin bundle from Codex, but bundled apps
stay installed until you manage them in ChatGPT.

If you want to keep a plugin installed but turn it off, set its entry in
`~/.codex/config.toml` to `enabled = false`, then restart Codex:

```
[plugins."gmail@openai-curated"]
enabled = false
```

## Build your own plugin

If you want to create, test, or distribute your own plugin, see
[Build plugins](/codex/plugins/build). That page covers local scaffolding,
manual marketplace setup, workspace sharing, plugin manifests, and packaging
guidance.

## Plugin guides

- [Record & Replay](/codex/record-and-replay): Show Codex a workflow
  once and turn it into a reusable skill.
- [Codex Security plugin quickstart](/codex/security/plugin): Install the
  plugin, scan authorized code, and review the result.

