---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/chatgpt-work-local-security'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# ChatGPT Work local security

Source: https://learn.chatgpt.com/docs/enterprise/chatgpt-work-local-security

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

ChatGPT Work can use approved files, applications, and browser sessions on a user's computer to complete local tasks. Access depends on workspace permissions, the user's existing account access, operating-system permissions, application approvals, and supported device policies.

Local capabilities depend on the supported desktop app, operating system, workspace entitlement, role permissions, device policy, and product rollout.

## Security at a glance

- Local tasks run through the ChatGPT desktop app. Opening a hosted cloud task in the same app does not make that task local.

- Available local and hosted Work controls depend on workspace configuration and rollout.

- File access, Computer Use, browsers, and connected apps use different permissions and approvals.

- A browser or application already signed in to a company system can expose the permissions of that existing account.

- Supported managed-device policies can restrict local features without replacing workspace access controls.

- Business, Enterprise, and Edu workspace data processed by covered OpenAI services is encrypted in transit and at rest and is not used to train OpenAI models by default.

- Local files, task context, browser data, connected-system records, and audit events can follow different storage and retention rules.

## Where local tasks run

Work Local accesses approved resources through the desktop app on the user's computer. Work Cloud runs on OpenAI-managed infrastructure, even when opened from the same desktop app.

Local files can remain on the device, but relevant file excerpts, prompts, screenshots, browser content, or tool results may be sent to OpenAI services to complete a task. Local execution does not mean offline or device-only model inference.

## Files and device access

A local task can work with information the user provides or makes available, including supported files, application content, browser sessions, and authorized connected systems. Access depends on the user's existing privileges and the controls governing that specific capability.

Granting local Work access does not automatically approve every application, grant administrator rights, or bypass the permissions of the account used to reach another system. An approved shared connection can have different privileges from the user's personal account.

Direct file reads, file edits, and shell commands follow the task's sandbox and approval settings. Computer Use accesses content through an approved native application under that application's permissions. A restriction on direct file access does not by itself establish the same restriction on files the application can open.

## Computer Use and application approvals

Workspace permissions determine who can use Work Local. Administrator policies can further restrict which native applications [Computer Use](https://learn.chatgpt.com/docs/computer-use) may operate and whether application approvals can be saved for future sessions. Required operating-system permissions and application approvals still apply. When a task uses an application or signed-in account, that account's permissions determine which information and actions are available.

Allowing an application through administrator policy does not install the required plugin, grant operating-system permissions, or approve an action that still requires review. For supported controls and configuration examples, see [Managed browser and Computer Use controls](https://learn.chatgpt.com/docs/enterprise/managed-configuration#control-browser-and-computer-use).

On macOS, Screen Recording allows Computer Use to see application content, and Accessibility allows it to click, type, and navigate. Supported macOS tasks can run in the background. On Windows, Computer Use operates on the active, visible desktop and cannot run in the background while the user continues using that same session.

Users can stop a task at any time. Computer Use cannot approve operating-system security prompts, authenticate as an administrator, or automate terminal applications or ChatGPT itself.

### Locked devices

Supported macOS configurations can optionally allow an approved Computer Use task to continue after the Mac locks. Availability depends on the app version, feature rollout, applicable requirements, and remote-control eligibility.

Enabling Locked Use installs a macOS authorization plugin that can temporarily unlock the Mac for an active, trusted Computer Use turn. ChatGPT covers every display during the temporary unlock. If it detects local keyboard or pointer input, it relocks the Mac and pauses automatic unlock until the user unlocks it manually. See [How Locked Use works](https://learn.chatgpt.com/docs/computer-use#locked-use).

Administrators can prevent users from enabling Locked Use on managed Macs. This requirement does not turn off Locked Use if it is already enabled. Windows Computer Use requires an active, unlocked desktop. See [Locked Use restrictions](https://learn.chatgpt.com/docs/enterprise/managed-configuration#restrict-locked-computer-use).

## Browser sessions and existing sign-ins

Work Local does not automatically gain access to every browser or company account. Access depends on the browser used, the signed-in account, and the approvals required for that browser experience.

| Browser path                                | Session and security boundary                                                                                                                                                                                                                                                                           |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Desktop in-app browser](https://learn.chatgpt.com/docs/browser)    | Uses a profile separate from the user's regular browser. Users can sign in within that profile. On supported clients, managed Browser Use policies restrict agent access to sites and available browser capabilities. The built-in browser cannot automate file uploads.                                |
| [Chrome extension](https://learn.chatgpt.com/docs/chrome-extension) | Can interact with existing tabs and signed-in accounts when the extension and website access are approved. On supported clients, the same managed Browser Use policies apply to agent actions through the extension.                                                                                    |
| Computer Use operating a browser            | Operates the browser as an approved native application and can use accounts already signed in. **Browser Use's site and capability policies do not apply to this path.** Native-app policies, operating-system permissions, application approvals, and the signed-in account's permissions still apply. |

Supported Browser Use policies can restrict site access, uploads, downloads, browser-history access, and full Chrome DevTools Protocol (CDP) access for browser debugging. Administrators can also restrict automatic approval review, saved approvals, and how long site-access approvals last. A user approval cannot override an administrator's denial. See [Managed browser controls](https://learn.chatgpt.com/docs/enterprise/managed-configuration#control-browser-and-computer-use).

A hosted cloud browser is separate from the user's local browsers and does not automatically inherit their existing sign-ins. Website sign-in through the cloud browser is not available in Enterprise or Edu workspaces.

## Apps, plugins, and connected accounts

A connected app can provide access to information or actions in another system. A plugin can use an app as an underlying tool. Making a plugin available does not automatically enable the required app, authorize an account, or permit every action.

Plugin and app defaults depend on the plan and whether the workspace is new or existing. New Enterprise and Edu workspaces start with a selected set of apps enabled; those defaults do not change existing workspace settings and do not apply to Healthcare workspaces. In general, new plugins and apps are disabled by default in Enterprise and Edu. Business apps are enabled by default. Administrators can change availability. See the [current plugin and app defaults](https://help.openai.com/en/articles/11509118) and the [ChatGPT Work overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview).

Before a task uses a connected system, confirm that the workspace allows the app and any required plugin, the connection is authorized, and the connected account can access the requested information or action. Read-only settings, allowed actions, and confirmation requirements vary by integration.

Plugins that provide browser or Computer Use capabilities require their own availability and installation review. Making a plugin available does not override managed browser or native-app policies, operating-system permissions, or required approvals. Desktop-only plugins and locally provided tools may follow different installation paths. See [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors).

### Personal and shared connections

A personal connection uses the connected user's permissions in the source system. A shared or agent-owned connection uses the connected account's permissions, which can be broader than the user's own access.

Limit shared accounts to the necessary data and actions, restrict who can use them, and apply supported action or confirmation controls. Records in the connected system remain subject to that system's permissions and retention policies.

## Administrator access and managed-device policies

Review the Work controls available in **Workspace settings** > **Permissions & roles**. Whether local and hosted Work appear as distinct permissions depends on the workspace configuration and rollout. For additional guidance, see the [Work administrator FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq).

Enable only the execution environments approved for each user or group, and verify effective access after making changes.

Workspace permissions determine who can use Work. Administrators can also restrict supported desktop capabilities through enforced requirements defined in `requirements.toml`. Depending on the deployment, these requirements can be delivered through workspace-managed configuration, a system-level configuration file, or supported macOS mobile device management tools.

Enforced requirements cannot be overridden by individual users. Managed defaults, by contrast, establish initial settings that users may be able to change. Neither replaces workspace roles or operating-system permissions.

Supported local clients load managed requirements during configuration loading. A background refresh can make newer cloud-managed requirements available for a later configuration load; it does not by itself demonstrate that an existing task is using the new policy. macOS MDM requirement changes are read at the next client launch. After changing managed requirements, restart the applicable local client and verify its effective settings before relying on the restriction. Workspace permission changes can follow a different activation path. See [How local clients apply cloud-managed requirements](https://learn.chatgpt.com/docs/enterprise/managed-configuration#how-local-clients-apply-cloud-managed-requirements).

| Managed setting                                       | Security purpose                                                                              |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `features.computer_use = false`                       | Disable native Computer Use capabilities.                                                     |
| `allow_appshots = false`                              | Prevent supported Appshot capture.                                                            |
| `features.in_app_browser = false`                     | Disable the desktop app's built-in browser.                                                   |
| `features.browser_use = false`                        | Disable supported Browser Use capabilities; external Browser Use has a separate flag.         |
| `features.browser_use_external = false`               | Disable agent-driven Browser Use through supported browser extensions.                        |
| `features.apps = false` or `features.plugins = false` | Restrict supported connected applications or plugins.                                         |
| `computer_use.allow_locked_computer_use = false`      | Prevent users from enabling Locked Use on managed Macs; does not disable existing Locked Use. |

These are restriction examples, not a list of enabled defaults. Omitting a feature requirement leaves normal client, platform, rollout, and user settings in effect. Browser Use feature flags, the built-in browser pane, and native Computer Use are separate controls; validate each browser path independently.

Available settings and delivery methods depend on the client, operating system, workspace, and deployment configuration. Validate restrictions on a representative managed device. For supported policy settings, configuration examples, and MDM setup instructions, see [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration).

## Local networking and private resources

Work Local can reach company information through a browser, a native application, a connected app, or another supported tool. Network controls apply differently to each path, and access to a corporate VPN does not itself authorize a task to use an internal resource.

Managed network requirements and Browser Use origin policies are separate checks. Validate both on the app versions and operating systems in your deployment before relying on a network restriction to limit Browser Use. Browser policy checks do not mean browser traffic is routed through the command-network proxy, and Browser Use policies do not govern traffic from native applications.

Managed network requirements under `[experimental_network]` are experimental and may change. Windows support is limited; test the exact client and environment before applying them to Windows users. Domain rules alone do not activate the managed proxy; `experimental_network.enabled = true` is required and does not override a sandbox that keeps networking off.

Review the connection, signed-in account, destination, and action required by the workflow. For configuration details and platform limitations, see [Network access requirements](https://learn.chatgpt.com/docs/enterprise/managed-configuration#configure-network-access-requirements).

## Data handling and retention

Apply your organization's endpoint, file-access, proxy, and data-loss-prevention controls to the specific device and workflow. Confirm whether those controls can prevent sensitive information from entering the task before processing. Audit logs and compliance exports help with monitoring and investigation but do not block processing on their own.

Storage and retention depend on the information category and where it is saved.

| Information category                            | What to review                                                                                                                                                     |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Local conversation records                      | How the desktop experience stores, deletes, backs up, or shares local records. Do not assume hosted-conversation retention settings apply to every local artifact. |
| Local files and generated outputs               | Device storage, endpoint policy, user-authorized uploads, external sharing, and any separately saved copies.                                                       |
| Prompts, file excerpts, and application context | Content supplied to a model or service, applicable workspace terms, and the workflow's actual data flow.                                                           |
| Voice and Appshots                              | Microphone input, frontmost-window screenshots, accessible application text, local session storage, and any content sent as task context.                          |
| Browser data                                    | The browser profile involved, existing sign-ins, browsing history, downloads, website approvals, and any separately stored task content.                           |
| Connected-system records                        | Source-system permissions and retention, connected-account identity, and any information separately saved to the conversation or another destination.              |
| Compliance and activity records                 | Which Work Local events are available for the workspace, the supported integration, and the receiving system's retention policy.                                   |

For supported Business, Enterprise, and Edu workspaces, business data processed by covered OpenAI services is encrypted in transit and at rest and is not used to train or improve OpenAI models by default. These protections do not mean OpenAI governs every device file, third-party application, browser profile, or source-system record.

Do not apply a hosted-conversation, temporary-upload, or compliance-log retention period to local records without confirming that it applies to the specific data category.

## Audit and compliance visibility

Available reporting depends on the workspace plan, product experience, event, connected application, and deployed configuration. Verify Work Local coverage before relying on a workspace export for incident response or regulatory review.

In supported versions, Browser Use can emit OpenTelemetry events for capability checks, including site access, uploads, and downloads. These events record the decision and decision source, with policy details where available. The decision source can be unknown. When export is configured, they are sent to the customer's OpenTelemetry endpoint alongside other local-runtime telemetry.

OpenTelemetry export is separate from Compliance API records and must be configured independently. These events do not establish a complete record of every browser or native-app action. See [OpenTelemetry configuration](https://learn.chatgpt.com/docs/config-file/config-advanced#observability-and-telemetry).

Determine whether the relevant systems record the task identity, supported prompts and responses, connected-app calls, browser approvals, application actions, local file activity, or endpoint events. Source-system and device records can provide different visibility from ChatGPT workspace records.

OpenAI does not store a separate complete record of Chrome actions performed through the extension. Do not assume that every local file operation, screenshot, browser action, approval, or external update appears in the Compliance API.

## Start with one approved task

Start with a small group on managed devices and choose one approved task, such as comparing selected finance workbooks. Confirm each user's Work access and provide only the files, applications, browser sessions, or connected accounts the task requires.

Check that approved actions work, restricted actions are blocked, and available records meet your monitoring needs. Have a user review the results and any external changes before expanding access.
