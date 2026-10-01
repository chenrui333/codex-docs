---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/apps-and-connectors'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Plugin controls

Source: https://learn.chatgpt.com/docs/enterprise/apps-and-connectors

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Plugins package reusable workflows and can include skills and MCP servers that connect
to other tools. ChatGPT and Codex use the same public plugin directory on
supported surfaces, while admins decide which plugins are available in their workspace.
Learn more about [plugins](https://learn.chatgpt.com/docs/plugins),
[skills](https://learn.chatgpt.com/docs/skills-and-plugins), and
[connected services](https://help.openai.com/en/articles/11487775).

    {"For workspace controls and data-handling guidance, see "}
    [{"Admin controls, security, and compliance for plugins and apps"}](https://help.openai.com/articles/11509118)
    {" in the Help Center."}

In this guide, **app** and **MCP server** refer to the same connected
integration and are interchangeable terms. We use **MCP server** in the prose,
but preserve **app** in UI labels such as **Workspace apps** and
**App permissions**, and in CSV column names.

A member can use an MCP server's capabilities only when the plugin and MCP server
are available to their role and the authenticated account has access to the
connected service. For a shared credential, the member also needs permission
to use that credential; the external account can differ from their personal account.

Plugins work in Chat and Work across ChatGPT on the web, desktop, and mobile,
in Codex in the ChatGPT desktop app, and through the Codex CLI plugin browser.
They aren't available in the IDE extension.

To see how these controls fit with workspace roles and permissions, see
[Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).

To configure plugin authentication for supported workspace
experiences, see [Workspace connections](https://learn.chatgpt.com/docs/enterprise/shared-connections).
Installing a plugin for everyone doesn't, by itself, provide a shared account.

Plugins in Sites let each visitor use their own connected accounts. Each
  plugin has a separate Sites permission, with defaults that depend on the
  workspace plan. See [Enable plugin use in
  Sites](https://learn.chatgpt.com/docs/enterprise/sites#enable-plugin-use-in-sites) to review plugin
  defaults, change access, and troubleshoot tenant restrictions.

## Understand the capability chain

A plugin can span these control layers:

| Layer                   | What it determines                                                       | Where to manage it                                                                                                              |
| ----------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Availability            | Whether the plugin bundle is available to the user                       | [Workspace settings](https://chatgpt.com/admin/settings) for supported web and desktop surfaces; the CLI plugin browser for CLI |
| Included skills         | Which reusable instructions the installed plugin contributes             | The plugin package and [Skill controls](https://learn.chatgpt.com/docs/enterprise/skills)                                                               |
| MCP server access       | Whether users can use an MCP server's capabilities                       | [Workspace apps](https://chatgpt.com/admin/ca) and [Permissions & roles](https://chatgpt.com/admin/settings)                    |
| Actions and permissions | Which actions users can run and when ChatGPT asks before using its tools | The connection's **Action control** and **App permissions** in [Workspace apps](https://chatgpt.com/admin/ca)                   |
| Service authorization   | Which external data and actions the authenticated identity can access    | The connected service and its identity provider                                                                                 |
| Runtime permissions     | What an agent can do after it receives data or a tool                    | The runtime, sandbox, and approval controls for the active surface                                                              |

Use these layers as a two-step rollout: first make the right plugins available,
then configure the capabilities and permissions each workflow needs.

## Step 1: Enable plugin availability

For supported web and desktop surfaces, workspace plugin controls determine
which roles can use or install a plugin. The Codex CLI uses its own plugin
browser for installation. See
[Build plugins](https://developers.openai.com/plugins/build/plugins) for
packaging and distribution.

To import workspace plugins from GitHub and keep them up to date, see
[Plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management).

### Export the public catalog for review

Eligible ChatGPT Enterprise workspace owners and admins can download a CSV of
the public plugins available to their workspace. Use the export to review
plugin, MCP server, and skill metadata before changing plugin availability.

1. Open [Admin > Plugins](https://chatgpt.com/admin/plugins).
2. Select **Public**.
3. Select the download icon (**Export CSV**) in the page header.

The download uses the filename `public-plugins-security-review.csv` and includes:

- Plugin metadata: `Plugin Name`, `Plugin Description`, `Date Added (UTC)`,
  `OpenAI Verified`, `Developer Name`, and `Version`.
- MCP server metadata: `App Name(s)` and `App Description(s)`.
- Chat skill metadata: `Skill Name(s)` and `Skill Description(s)`.

When a plugin includes more than one MCP server or skill, semicolons separate the
corresponding values. The export uses a public-catalog snapshot that can be up
to 48 hours old,
includes only public plugins visible to the current workspace, and does not
include plugins created for that workspace. It isn't available in FedRAMP
workspaces.

## Step 2: Manage capabilities

Conversation sync does not grant additional plugin, MCP server, or connected-service access. For Local computer access with Work Cloud, Agent Security's enterprise `apps` and `plugins` requirements apply to local executors. Work cloud containers retain existing Work Cloud policies. Configure these requirements through TOML and review them alongside workspace permissions and the connected account's permissions.

Review hook support separately from plugin availability:

- **Enterprise hooks.** Where enabled for your workspace, Local computer access with Work Cloud supports admin-defined MCP hooks that run on the cloud coordinator (orchestrator) for supported lifecycle and tool events. Command hooks and hooks from local configuration or plugins are not supported with cloud orchestration, even when tools execute locally.
- **Cloud orchestration:** Command hooks and hooks from local configuration or plugins do not run, even when tools execute locally and the plugin itself is allowed. Consumers do not have hooks support in this feature. When both orchestration and execution are local, existing supported hooks continue to work in local-only Work and Codex threads. Admins can still configure supported managed hooks in Agent Security for those workflows.
- **Auditing.** Before relying on these hooks, test the callback connection, confirm the events it receives, and check how failures affect the task. MCP hooks do not provide a complete Compliance API audit trail.

See [Hooks](https://learn.chatgpt.com/docs/hooks) and the [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) for supported requirements.

<WarningTip>
  Making an MCP server or plugin available in ChatGPT doesn't grant access to
  files, records, or actions in the connected service. When troubleshooting
  access, check the member's workspace role and approved action settings. Then
  confirm the authenticated account or shared connection has the expected
  permissions in the connected service.
</WarningTip>

Plugins in ChatGPT and Codex can include MCP server connections that search, retrieve, sync,
or act on external systems. Plugin availability and the access and actions
granted to each connection are separate controls.

Manage MCP server capabilities from
[Workspace apps](https://chatgpt.com/admin/ca) and
[Permissions & roles](https://chatgpt.com/admin/settings). Available controls
let admins:

- Enable MCP server connections and assign access by workspace role.
- For connections that support **Action control**, allow read-only actions or an
  approved custom set, including how the workspace handles newly added actions.
- Set **App permissions** that determine when ChatGPT asks before using a connection.
- Keep access within the scopes and permissions granted by each connected
  service and authenticated account.

For current availability and procedures, see
[Admin controls, security, and compliance in apps](https://help.openai.com/en/articles/11509118).

## Restrict company app accounts to authorized workspaces

When activated, verified-domain restrictions prevent users from creating new connections to supported apps with company-domain accounts in personal ChatGPT workspaces or other unauthorized workspaces. Employees must use an authorized workspace to connect those company accounts.

Verifying a domain does not activate this restriction. Existing app connections are not automatically disconnected.

For supported apps, availability, and setup guidance, see [Admin controls, security, and compliance for plugins and apps](https://help.openai.com/en/articles/11509118).

<a id="choose-a-starting-set-of-apps"></a>

## Choose a focused initial set

Enable plugins that support an approved business need. Set each plugin’s audience to the users or roles that need it, and complete any required review before enabling it.

For each connected service, record the business owner, permitted data, approved
read or write actions, authentication method, and a support or removal contact.

Before enabling write actions or publishing a new connected capability, verify
its role scope and test with an account that has only the intended permissions
in the connected service.

For a broad rollout, begin with categories teams use every day, such as email,
calendar, and file or document systems. Use the
[Plugins Directory](https://chatgpt.com/apps) to confirm current availability
and capabilities across supported ChatGPT and Codex surfaces.

Whatever the initial set, start with read actions. Before enabling write
actions, identify the plugin owner, review MCP server scopes and service
permissions, confirm data access, and document external effects and a recovery
path.

## Understand data flow and security

When ChatGPT uses an MCP server included with a plugin, it sends a request
to the connected service and returns data or action results allowed by the
authenticated account's permissions in that service.

ChatGPT handles data from connected services in two ways:

- **Non-synced:** ChatGPT processes data from Chat and deep research transiently
  and doesn't index it.
- **Synced:** ChatGPT indexes selected connected content in advance. You can see
  whether a connection supports sync on its plugin page.

The mode changes how ChatGPT indexes connected content; it doesn't replace
normal chat-retention controls. ChatGPT conversations that use these connections remain
available through the Compliance API.

OpenAI's connected-service guidance documents encryption in transit and at rest, per-user
authorization, role and action controls, restricted network access for
conversations that use these connections, and no model training on information accessed
through these connections for Business, Enterprise, and Edu customers. When a request reaches
a connected service, that service's scopes, retention, data residency, and other
policies also apply.

See [security and compliance for connected services](https://help.openai.com/en/articles/11509118)
and [connections with sync](https://help.openai.com/en/articles/10847137) for current
data-handling details. For locally configured MCP servers in the ChatGPT desktop
app, Codex CLI, or IDE extension, see
[Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp).

## Use current procedures and references

- [Admin controls, security, and compliance in apps](https://help.openai.com/en/articles/11509118)
- [Apps in ChatGPT](https://help.openai.com/en/articles/11487775)
- [Apps with sync](https://help.openai.com/en/articles/10847137)
- [Manage workspace settings](https://help.openai.com/en/articles/8411955)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [Skills and plugins](https://learn.chatgpt.com/docs/skills-and-plugins)
- [Build plugins](https://developers.openai.com/plugins/build/plugins)
- [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)
