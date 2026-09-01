---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/chatgpt-work-local-security'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.151.0", "0.152.0"]
codex_cli_versions_raw: ["codex-cli 0.151.0", "codex-cli 0.152.0"]
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

## Computer Use and application approvals

[Computer Use](https://learn.chatgpt.com/docs/computer-use) can interact with supported desktop applications only when the capability is available, the required operating-system permissions are granted, and the user authorizes the application. Depending on the available options, approval can apply to the current session or future tasks.

On macOS, Screen Recording allows Computer Use to see application content, and Accessibility allows it to click, type, and navigate. Supported macOS tasks can run in the background. On Windows, Computer Use operates on the active, visible desktop and cannot run in the background while the user continues using that same session.

Users can stop a task at any time. Computer Use cannot approve operating-system security prompts, authenticate as an administrator, or automate terminal applications or ChatGPT itself.

### Locked devices

Supported macOS configurations can optionally allow an approved Computer Use task to continue while the Mac is locked. Availability depends on the app version, feature rollout, applicable requirements, and remote-control eligibility.

Administrators can disable locked-device operation through supported managed configuration. Windows Computer Use requires an active, unlocked desktop; macOS locked-use behavior does not establish equivalent Windows support.

## Browser sessions and existing sign-ins

Work Local does not automatically gain access to every browser or company account. Access depends on the browser used, the signed-in account, and the approvals required for that browser experience.

| Browser path                                | Session and security boundary                                                                                                                                                                                                 |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Desktop in-app browser](https://learn.chatgpt.com/docs/browser)    | Uses a browser profile separate from the user's regular browser. The user can sign in within that profile, and supported website access may require approval. The built-in browser cannot automate file uploads.              |
| [Chrome extension](https://learn.chatgpt.com/docs/chrome-extension) | Can interact with existing browser tabs and accounts when the extension and website access are approved. Users can approve a site once or allow future access; browser-history and local-file access require separate review. |
| Computer Use operating a browser            | Uses a browser approved as a desktop application, including accounts already signed in to that browser. Operating-system permissions, application approval, and the existing account's permissions still apply.               |

Website approval options and sensitive-action confirmations vary by browser experience. Allowing all sites reduces future approval prompts, so users should review that choice before enabling it.

A hosted cloud browser is separate from the user's local browsers and does not automatically inherit their existing sign-ins. Supported cloud workflows can request a separate, user-authorized sign-in.

## Apps, plugins, and connected accounts

A connected app can provide access to information or actions in another system. A plugin can use an app as an underlying tool. Making a plugin available does not automatically enable the required app, authorize an account, or permit every action.

Plugin and app availability depend on the workspace plan and configuration. The [ChatGPT Work overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) describes plugins and their underlying apps as off by default for Enterprise and Edu workspaces and on by default for Business workspaces. Verify the actual settings for the relevant workspace and product experience.

Before a task uses a connected system, confirm that the workspace allows the app and any required plugin, the connection is authorized, and the connected account can access the requested information or action. Read-only settings, allowed actions, and confirmation requirements vary by integration.

Desktop-only plugins, local tools, and other locally provided capabilities can follow different installation or approval paths. Do not assume that every local tool uses the same administrative approval process.

### Personal and shared connections

A personal connection uses the connected user's permissions in the source system. A shared or agent-owned connection uses the connected account's permissions, which can be broader than the user's own access.

Limit shared accounts to the necessary data and actions, restrict who can use them, and apply supported action or confirmation controls. Records in the connected system remain subject to that system's permissions and retention policies.

## Administrator access and managed-device policies

Review the Work controls available in **Workspace settings** > **Permissions & roles**. Whether local and hosted Work appear as distinct permissions depends on the workspace configuration and rollout. For additional guidance, see the [Work administrator FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq).

Enable only the execution environments approved for each user or group, and verify effective access after making changes.

Workspace permissions determine who can use Work. Administrators can also restrict supported desktop capabilities through enforced requirements defined in `requirements.toml`. Depending on the deployment, these requirements can be delivered through workspace-managed configuration, a system-level configuration file, or supported macOS mobile device management tools.

Enforced requirements cannot be overridden by individual users. Managed defaults, by contrast, establish initial settings that users may be able to change. Neither replaces workspace roles or operating-system permissions.

| Managed setting                                       | Security purpose                                                             |
| ----------------------------------------------------- | ---------------------------------------------------------------------------- |
| `features.computer_use = false`                       | Disable supported Computer Use capabilities.                                 |
| `allow_appshots = false`                              | Prevent supported Appshot capture.                                           |
| `features.in_app_browser = false`                     | Disable the desktop app's built-in browser.                                  |
| `features.browser_use = false`                        | Disable supported browser automation; review other browser paths separately. |
| `features.apps = false` or `features.plugins = false` | Restrict supported connected applications or plugins.                        |
| `computer_use.allow_locked_computer_use = false`      | Prevent supported Computer Use while a Mac is locked.                        |

Available settings and delivery methods depend on the client, operating system, workspace, and deployment configuration. Validate restrictions on a representative managed device. For supported policy settings, configuration examples, and MDM setup instructions, see [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration).

## Local networking and private resources

A task can reach company information through paths such as a device browser, an approved desktop application, or a connected app. Existing device, proxy, VPN, source-system, and endpoint controls may apply differently to each path.

Access to a corporate VPN does not automatically authorize every tool to use every internal resource. Likewise, a cloud Work browser or cloud-network control is not a universal restriction on local device networking. Review the actual connection, identity, destination, and action required by the workflow.

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

Determine whether the relevant systems record the task identity, supported prompts and responses, connected-app calls, browser approvals, application actions, local file activity, or endpoint events. Source-system and device records can provide different visibility from ChatGPT workspace records.

OpenAI does not store a separate complete record of Chrome actions performed through the extension. Do not assume that every local file operation, screenshot, browser action, approval, or external update appears in the Compliance API.

## Start with one approved task

Start with a small group on managed devices and choose one approved task, such as comparing selected finance workbooks. Confirm each user's Work access and provide only the files, applications, browser sessions, or connected accounts the task requires.

Check that approved actions work, restricted actions are blocked, and available records meet your monitoring needs. Have a user review the results and any external changes before expanding access.
