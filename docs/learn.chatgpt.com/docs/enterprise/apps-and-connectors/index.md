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

Plugins package reusable workflows and can include skills and apps that connect
to other tools. ChatGPT and Codex use the same public plugin directory on
supported surfaces, while admins decide which plugins are available in their workspace.
Learn more about [plugins](https://learn.chatgpt.com/docs/plugins),
[skills](https://learn.chatgpt.com/docs/skills-and-plugins), and
[apps and connectors](https://help.openai.com/en/articles/11487775).

A member can use a connector-backed capability only when the plugin and app are
available to their role and they have access to the connected service.

Plugins work in Chat and Work across ChatGPT on the web, desktop, and mobile,
in Codex in the ChatGPT desktop app, and through the Codex CLI plugin browser.
They aren't available in the IDE extension.

To see how these controls fit with workspace roles and permissions, see
[Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).

## Understand the capability chain

A plugin can span these control layers:

| Layer                   | What it determines                                                           | Where to manage it                                                                                                              |
| ----------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Availability            | Whether the plugin bundle is available to the user                           | [Workspace settings](https://chatgpt.com/admin/settings) for supported web and desktop surfaces; the CLI plugin browser for CLI |
| Included skills         | Which reusable instructions the installed plugin contributes                 | The plugin package and [Skill controls](https://learn.chatgpt.com/docs/enterprise/skills)                                                               |
| App access              | Whether users can use a connector-backed capability                          | [Workspace apps](https://chatgpt.com/admin/ca) and [Permissions & roles](https://chatgpt.com/admin/settings)                    |
| Actions and permissions | Which actions users can run and when ChatGPT asks before using the connector | The connector's Action control and App permissions in [Workspace apps](https://chatgpt.com/admin/ca)                            |
| Service authorization   | Which external data and actions the authenticated identity can access        | The connected service and its identity provider                                                                                 |
| Runtime permissions     | What an agent can do after it receives data or a tool                        | The runtime, sandbox, and approval controls for the active surface                                                              |

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
plugin, app, and skill metadata before changing plugin availability.

1. Open [Admin > Plugins](https://chatgpt.com/admin/plugins).
2. Select **Public**.
3. Select the download icon (**Export CSV**) in the page header.

The download uses the filename `public-plugins-security-review.csv` and includes:

- Plugin metadata: `Plugin Name`, `Plugin Description`, `Date Added (UTC)`,
  `OpenAI Verified`, `Developer Name`, and `Version`.
- App metadata: `App Name(s)` and `App Description(s)`.
- Chat skill metadata: `Skill Name(s)` and `Skill Description(s)`.

When a plugin includes more than one app or skill, semicolons separate the
corresponding values. The export uses a public-catalog snapshot that can be up
to 48 hours old,
includes only public plugins visible to the current workspace, and does not
include plugins created for that workspace. It isn't available in FedRAMP
workspaces.

## Step 2: Manage capabilities

<WarningTip>
  Making an app or plugin available in ChatGPT doesn't grant access to files,
  records, or actions in the connected service. Before troubleshooting or
  expanding access, check the member's workspace role and approved action
  settings. Then confirm the authenticated account or shared connection has the
  expected permissions in the connected service.
</WarningTip>

Plugins in ChatGPT and Codex can include connectors that search, retrieve, sync,
or act on external systems. Plugin availability and the access and actions
granted to each connector are separate controls.

Manage connector-backed capabilities from
[Workspace apps](https://chatgpt.com/admin/ca) and
[Permissions & roles](https://chatgpt.com/admin/settings). Available controls
let admins:

- Enable apps or connectors and assign access by workspace role.
- For connectors that support Action control, allow read-only actions or an
  approved custom set, including how the workspace handles newly added actions.
- Set App permissions that determine when ChatGPT asks before using an app.
- Keep access within the scopes and permissions granted by each connected
  service and authenticated user.

For current availability and procedures, see
[Admin controls, security, and compliance in apps](https://help.openai.com/en/articles/11509118).

<a id="choose-a-starting-set-of-apps"></a>

## Choose a focused initial set

Start with plugins that support a clear business need. Decide whether to make
each plugin available to everyone, limit it to a role or pilot group, or require
further review.

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
actions, identify the plugin owner, review connector scopes and service
permissions, confirm data access, and document external effects and a recovery
path.

## Understand data flow and security

When ChatGPT uses an app or connector included with a plugin, it sends a request
to the connected service and returns data or action results allowed by the
authenticated user's permissions in that service.

ChatGPT handles connected app data in two ways:

- **Non-synced:** ChatGPT processes data from Chat and deep research transiently
  and doesn't index it.
- **Synced:** ChatGPT indexes selected connected content in advance. You can see
  whether an app supports sync on its plugin page.

The mode changes how ChatGPT indexes connected content; it doesn't replace
normal chat-retention controls. ChatGPT conversations that use apps remain
available through the Compliance API.

OpenAI's app guidance documents encryption in transit and at rest, per-user
authorization, role and action controls, restricted network access for
conversations that use apps, and no model training on information accessed
through apps for Business, Enterprise, and Edu customers. When a request reaches
a connected service, that service's scopes, retention, data residency, and other
policies also apply.

See [app security and compliance](https://help.openai.com/en/articles/11509118)
and [apps with sync](https://help.openai.com/en/articles/10847137) for current
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
