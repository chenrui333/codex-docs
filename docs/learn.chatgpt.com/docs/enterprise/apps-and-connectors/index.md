---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/apps-and-connectors'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0"]
---

# Plugin controls

Source: https://learn.chatgpt.com/docs/enterprise/apps-and-connectors

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

A plugin extends ChatGPT and Codex by packaging skills and optional connectors
so teams can distribute workflows and knowledge. The products share one
universal plugin directory, while admins control availability and installation
for their workspace. Learn more about [plugins](https://learn.chatgpt.com/docs/plugins),
[skills](https://learn.chatgpt.com/docs/skills-and-plugins), and
[apps and connectors](https://help.openai.com/en/articles/11487775).

When a plugin includes a connector, workspace admins must make the plugin
available through plugin controls and configure connector access before members
can use the connector-backed capability.

Plugins work in Chat and Work across ChatGPT on the web, desktop, and mobile,
in Codex in the ChatGPT desktop app, and through the Codex CLI plugin browser.
They aren't available in the IDE extension.

For the complete administration model, see
[Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).

## Understand the capability chain

Each layer has a separate scope and control surface:

| Layer                                | What it determines                                                           | Where to manage it                                                                                                              |
| ------------------------------------ | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Plugin availability and installation | Whether the plugin bundle is available to the user                           | [Workspace settings](https://chatgpt.com/admin/settings) for supported web and desktop surfaces; the CLI plugin browser for CLI |
| Bundled skills                       | Which reusable instructions the installed plugin contributes                 | The plugin package and [Skill controls](https://learn.chatgpt.com/docs/enterprise/skills)                                                               |
| Connector access                     | Whether users can use a connector-backed capability                          | [Workspace apps](https://chatgpt.com/admin/ca) and [Permissions & roles](https://chatgpt.com/admin/settings)                    |
| Connector actions and permissions    | Which actions users can run and when ChatGPT asks before using the connector | The connector's Action control and App permissions in [Workspace apps](https://chatgpt.com/admin/ca)                            |
| Source-system authorization          | Which external data and actions the authenticated identity can access        | The connected service and its identity provider                                                                                 |
| Runtime permissions                  | What an agent can do after it receives data or a tool                        | The runtime, sandbox, and approval controls for the active surface                                                              |

Depending on the workflow, admins can govern plugin availability, connector
access, connector actions and permissions, provider authorization, and runtime
policy independently.

## Plugin availability controls

Workspace plugin controls determine whether a plugin is available or installed
for supported workspace roles. The Codex CLI plugin browser controls CLI
installation through its own path. See [Build plugins](https://developers.openai.com/plugins/build/plugins) for
packaging and distribution.

## Connector-backed capability controls

Plugins in ChatGPT and Codex can include connectors that search, retrieve, sync,
or act on external systems. Workspace admins configure plugin availability
separately from the access and actions granted to each connector.

Manage connector-backed capabilities from
[Workspace apps](https://chatgpt.com/admin/ca) and
[Permissions & roles](https://chatgpt.com/admin/settings). Available controls
let admins:

- Enable reviewed connectors and assign access by workspace role.
- For connectors that support Action control, allow read-only actions or an
  approved custom set, including how the workspace handles newly added actions.
- Set App permissions that determine when ChatGPT asks before using a connector.
- Keep access within the scopes and permissions granted by each connected
  service and authenticated user.

For current availability and procedures, see
[Admin controls, security, and compliance in apps](https://help.openai.com/en/articles/11509118).

<a id="choose-a-starting-set-of-apps"></a>

## Choose a starting set of plugins

For a broad initial rollout, consider plugin categories teams use every day:
email, calendar, and file or document systems such as Google Drive or Notion.
Use the [Plugins Directory](https://chatgpt.com/apps) to confirm current
availability and capabilities across supported ChatGPT and Codex surfaces.

Start with read actions. Enable write actions only after reviewing the plugin's
owner, each connector's requested scopes, data access, external effects, and
recovery path.

## Understand data flow and security

When ChatGPT uses a connector-backed plugin, the connector sends a request to
the connected service and returns data or action results allowed by the
authenticated user's provider permissions. Custom MCP servers expose these
operations as tools through Model Context Protocol (MCP).

For non-synced connector use, ChatGPT processes data from Chat and deep
research transiently and doesn't index it. Connectors with sync index selected
connected content in advance. This indexing distinction doesn't replace normal
chat-retention controls; chats that use plugins remain available through the
Compliance API.

OpenAI's current connector guidance also documents encryption in transit and at
rest, per-user authorization, role and action controls, restricted network
access for chats that use plugins, and no model training on information accessed
through plugins for Business, Enterprise, and Edu customers. Review the
connected service's scopes, retention, and data-residency policies because those
policies apply when a request reaches that service.

See [app security and compliance](https://help.openai.com/en/articles/11509118)
and [apps with sync](https://help.openai.com/en/articles/10847137) for the
current data-handling details. For locally configured MCP servers in the
ChatGPT desktop app, Codex CLI, or IDE extension, see
[Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp).

## Use current procedures

- [Admin controls, security, and compliance in apps](https://help.openai.com/en/articles/11509118)
- [Apps in ChatGPT](https://help.openai.com/en/articles/11487775)
- [Apps with sync](https://help.openai.com/en/articles/10847137)
- [Manage workspace settings](https://help.openai.com/en/articles/8411955)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [Skills and plugins](https://learn.chatgpt.com/docs/skills-and-plugins)
- [Build plugins](https://developers.openai.com/plugins/build/plugins)
- [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)
