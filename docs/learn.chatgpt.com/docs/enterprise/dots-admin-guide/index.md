---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/dots-admin-guide'
source_kind: 'learn_markdown'
---

# Manage dots permissions and capabilities

Source: https://learn.chatgpt.com/docs/enterprise/dots-admin-guide

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

A dot is a personal agent in ChatGPT that can take on ongoing work, use connected apps, and delegate tasks to Work or Codex. You choose who can use dots, configure their capabilities, and manage personal dots across your workspace. Members connect their accounts and tell their dots what to work on.

**[dots security guide](https://learn.chatgpt.com/docs/enterprise/dots-security)**

Use the dots security guide for a detailed review with your security team. This admin guide covers workspace setup, access, and day-to-day management.

For current availability, supported plans, and workspace settings, see [Manage dots in ChatGPT workspaces](https://help.openai.com/en/articles/20001554-manage-dots-in-chatgpt-workspaces).

## Find what you need

| If you need to…                                    | Start here                                                                                                                        |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Give a group access                                | [Set up dots for work](#set-up-dots-for-work)                                                                                     |
| Choose which data and tools a dot can use          | [App access](#2-configure-app-access) and [computer capabilities](#available-admin-controls)                                      |
| Set up Slack                                       | [Slack connections and dot identities](#3-configure-communication-channels)                                                       |
| Find, pause, resume, or delete a personal dot      | [Manage dots in your workspace](#manage-dots-in-your-workspace)                                                                   |
| Track adoption or investigate an action            | [Monitor usage](#monitor-usage) and [Review admin activity and compliance records](#review-admin-activity-and-compliance-records) |
| Remove access when someone changes roles or leaves | [Manage access changes](#manage-access-changes)                                                                                   |

## Set up dots for work

### 1. Configure role-based access

Workspace owners manage access through workspace defaults and custom roles. To give selected groups access, keep the workspace default off and assign a custom role to those groups. Check every role assigned to a member: if one role grants access, turning it off in another role won't remove it.

Review these permissions in **Permissions**:

- **Use dots**: Allow members to use dots.

- **Add dots to Slack and Microsoft Teams**: Allow members to connect their dots to supported messaging channels where available.

- **Allow local computer access**: Allow dots to use a member’s local computer.

- **Use custom rules for dots**: Allow members to add or edit rules for their dots.

For role creation, assignment, and access checks, see the [role-based access control guide](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions#set-the-workspace-default-then-create-targeted-custom-roles).

1. Open **Admin Console** > **Permissions**.

2. Under Permissions &gt; Workspace default &gt; Workspace capabilities, enable **Use dots** if it should be available by default; otherwise grant access through a custom role.

3. Set Slack participation and custom dot rules. Local computer access requires a separate admin opt-in; review [local computer access setup](https://learn.chatgpt.com/docs/enterprise/cloud-local-access#enable-local-computer-access) before enabling it.

4. Under **Let agents use cloud computers**, review **Use a browser**, **Allow network access**, and **Allow computer use** where your policies allow browsing websites, accessing online services, and interacting with apps. Review both workspace defaults and custom roles.

5. Under Workspace capabilities, set Use password manager according to your workspace policy.

6. Save, then check access for an intended member.

When you enable dots, you may be asked to turn on cloud computer capabilities that are still off. Dots, Work Cloud, and team automations share these permissions. Choose the capabilities your organization's policies allow.

To review them later, go to **Admin Console** > **Permissions** > **Workspace default** > **Workspace capabilities** > **Let agents use cloud computers**. Local computer access is a separate opt-in.

Members still need to complete [Slack](https://learn.chatgpt.com/docs/dots/channels#slack) and [local-computer setup](https://learn.chatgpt.com/docs/dots/computers-and-apps#connect-your-computer) after you enable access. Supported app connections they've already set up may be available to their dot.

### 2. Configure app access

A personal dot can use its owner's existing ChatGPT app connections. Through each connection, it can read or change only what the connected account permits and the workspace allows. When setting up access, check:

1. **Which apps members can use.** Set available apps and allowed actions in [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors).
2. **What the connected account can access.** Check the account's permissions in the source app. Enabling dots doesn't give it access to every shared drive, channel, or document.
3. **When approval is required.** Check the connected app's approval setting for the specific action, such as sending a message. Enabling the app alone does not authorize a send. See [app permissions](https://help.openai.com/en/articles/20001495-managing-app-permissions-in-chatgpt) for the options.

For example, permission to read a document may not include editing or sharing it. To restrict access to a particular source, check the connected account and app permissions.

For Auto-review and the difference between authorizing a draft and authorizing a send, see [approvals and unattended work](https://learn.chatgpt.com/docs/enterprise/dots-security#set-rules-for-approvals-and-unattended-work).

### 3. Configure communication channels

Members can connect Slack to their dot in two ways:

| Setup                                              | Member experience                                                                                              | What to configure                                                           |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Connect the member’s Slack account through Plugins | Members talk to their dot in ChatGPT. It can use their Slack connection without having its own Slack identity. | Slack plugin access, the connected account, allowed actions, and approvals. |
| Give the dot its own Slack identity                | The owner can message or mention the dot in Slack, and its posts are visible to people in that conversation.   | Dots messaging permission, Slack app approval, and each member’s dot setup. |

Turning off a dot's Slack identity doesn't remove its access through the member's connected Slack account. Check both when removing Slack access. For member setup, see [Messaging](https://learn.chatgpt.com/docs/dots/channels#slack).

**Before members connect their dots to Slack**

- **ChatGPT workspace owner:** Enable Use dots and Add dots to Slack and Microsoft Teams for the intended members through workspace defaults or custom roles.

- **Slack workspace owner or app manager:** Ensure the ChatGPT app is installed in Slack. Approve app requests if required by your workspace. See [Slack’s app approval guidance](https://slack.com/help/articles/360024269514-Manage-app-requests-for-your-workspace).

- **Each member:** Connect your dot to Slack from its profile. See [Message your dot in Slack](https://learn.chatgpt.com/docs/dots/channels#slack).

Enabling the ChatGPT permission does not install an app in Slack or connect a member’s dot.

### Verify an approved workflow

After configuring access, test the workflow with the member, connected accounts, and computer environment intended for the work. Use disposable documents and test recipients.

1. **Check effective permissions.** Review workspace defaults and every assigned role. Confirm which apps, cloud capabilities, and local connections the workflow needs.
2. **Prepare a draft from an allowed source.** Check the source, connected identity, and output. If the workflow uses both a signed-in website and an app connection, check both accounts.
3. **Test approval behavior.** Use a harmless action and test recipient. Record the instruction, any approval request, and the final state in the receiving service. A written policy alone does not create a product-enforced restriction.
4. **Review available records.** Check activity and compliance records to confirm which parts of the test you can reconstruct. Document any missing records.

Compare the result with the requirements approved by your security team. Resolve any gaps in required restrictions or records before using the workflow with affected data.

## Available admin controls

| **Area**                            | **Admin capability**                                                                                                   |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Access to dots                      | Grant or revoke dots access through workspace permissions.                                                             |
| Cloud and connected local computers | Control Use a browser, Allow network access, Allow computer use, Use password manager, and local-computer access.      |
| Messaging and participation         | Enable or disable Slack participation.                                                                                 |
| Connected apps                      | Set available apps and allowed actions through [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors).               |
| Custom dot rules                    | When disabled, members cannot add or edit custom rules, and saved rules do not apply.                                  |
| Models                              | Enterprise model controls and defaults do not apply to the main dot. Review delegated Work and Codex tasks separately. |

For cloud-browser site rules and controls still in development, see [browser, network, and device access](https://learn.chatgpt.com/docs/enterprise/dots-security#review-browser-network-and-device-access). For connected computers and delegated tasks, see [controls by work environment](https://learn.chatgpt.com/docs/enterprise/dots-security#controls-by-work-environment).

## Review availability and data requirements

Before enabling dots, review current availability in [Getting started with your dot](https://help.openai.com/en/articles/20001530-getting-started-with-your-dot) and the workspace notices shown during setup. Review the security guide's [eligibility and data requirements](https://learn.chatgpt.com/docs/enterprise/dots-security#confirm-eligibility-and-data-requirements) for regional, residency, Enterprise Key Management, and HIPAA coverage. Confirm that your workspace configuration, any applicable business associate agreement (BAA), and the intended workflow meet your organization's requirements before enabling access.

Check requirements for the dot itself, tasks it delegates to Work or Codex, and any connected computer. For cloud browser, network, and computer use, see [cloud security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security). For work on employee devices, see [local computer access](https://learn.chatgpt.com/docs/enterprise/cloud-local-access).

## Manage dots in your workspace

Open **Admin Console** > **Dots** to see the personal dots created in your workspace. Use the inventory to find a dot and review its owner and status, then open its details to manage it.

### Review a dot's details

The details include the member who created the dot, its active or paused status, its identity, and its Slack or Microsoft Teams connection status. The identity is the dot's service account, or its dot ID when a service account isn't available. Connection status shows whether a messaging service is connected; the [messaging permission](#3-configure-communication-channels) controls who can set up that connection.

### Pause and resume a dot

Pause a dot from Admin Console when you need to stop it temporarily. An admin pause prevents the member from resuming the dot. Check the inventory to confirm that its status is paused.

Resuming a dot restores its previous user state. A dot that was active becomes active again; a dot that the member had already paused stays paused. Billing stops during the admin pause and resumes if the dot returns to an active state.

### Delete a dot

Delete a dot from Admin Console when it should be removed from the workspace. After deletion completes, it no longer appears in the inventory and billing is paused. Deletion removes the dot's context; it does not preserve the dot for later resumption.

Files, Codex threads, and ChatGPT conversations the dot created are stored separately and aren't deleted with it. Review and delete those items in their respective locations when needed. Use pause when you want to preserve the dot and resume it later.

### Revoke and restore access

To remove a member's permission to use dots, review the workspace default and every role assigned directly or through groups. Remove every applicable **Use dots** grant. Turning off one role's permission does not remove access if another role still grants it.

| Change                               | What happens to the dot                                                                                                                              | What to check                                                                       |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Revoke the member's dots permission  | The dot is hidden from the member, paused, and shown as disabled in the inventory. Billing stops. The dot cannot resume while permission is revoked. | Check the member's effective permissions and the dot's inventory status.            |
| Restore the member's dots permission | The dot returns to its previous user state. If it was active, it becomes active again and billing resumes.                                           | Check the restored permission and whether the dot is active or remains user-paused. |

For offboarding, also review the connections and delegated work in [Manage access changes](#manage-access-changes).

## Monitor usage

Workspace analytics includes enabled-dot counts and total active users of dots. Enabled dots are dots that are not paused. Use these measures together to understand how many dots are enabled and how many people are using them.

For daily reporting by member or workspace, use the [Analytics API](https://learn.chatgpt.com/docs/enterprise/analytics-api). The daily usage endpoint `/v1/analytics/workspaces/{workspace_id}/usage` identifies dots with `client_id = DOTS`.

Tasks a dot starts or manages in Work or Codex count toward those products' usage limits and appear in their reporting. Include those tasks when reviewing usage. See [Work usage and cost](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-usage-and-cost) for the available controls, and check the current terms for your plan when setting budgets.

## Review admin activity and compliance records

Audit logs capture admin actions on dots, including pause, resume, delete, manage, and saved-tier changes. Use these records to review changes made by administrators.

To investigate work a dot has done, use the [Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api#confirm-the-administration-boundaries). Supported dots records include user prompts and responses, supported tool-call events, and connected-app MCP calls and results. Dots-attributed records use `client_id = DOTS`; the agent object includes the dot ID, name, and type when available.

Workspace owners or admins can select their workspace in Admin Console, then open **Credentials** > **Admin keys** and create a key with the appropriate available permissions: `enterprise.analytics.usage.read` for unified usage reporting, or `CODEX_LOG` access for dots compliance records. Only workspace owners can grant broad compliance or **Conversation messages** access where supported. Use the [Admin API reference](https://chatgpt.com/public/admin/api-reference) to list and download compliance JSONL files and select records with `client_id = DOTS`.

### Check records for an investigation

Compare a harmless test action with the available export records. Check whether they identify the user, dot, initiating request, tool, applicable approval, and result. Record missing fields and events. A requested tool call does not establish that an action completed; use the receiving service's records to confirm the outcome.

Protect downloaded records according to the sensitivity of the messages and connected data they contain.

## Manage access changes

When someone changes roles or leaves, check their dot's permissions, connections, and ongoing work:

1. **Remove dots access.** Check the workspace default and every role assigned directly or through groups. Remove each permission that grants access; any remaining grant can keep it enabled.
2. **Check connected accounts and devices.** Review plugin authorizations, website sessions, local computer access, and the dot's Slack identity. Each has its own settings.
3. **Decide what happens to ongoing work.** Review the [pause and deletion controls](#manage-dots-in-your-workspace), then check active tasks, recurring schedules, and tasks delegated to Work or Codex separately. Decide what should stop and who should take over any remaining responsibilities.
4. **Delete data where needed.** Access changes and deletion are separate steps. Follow the deletion process for the dot's context and any files or tasks stored elsewhere.

For adding and removing workspace members, see [User lifecycle management](https://learn.chatgpt.com/docs/enterprise/user-lifecycle). For dots access removal, see [Manage dots in ChatGPT workspaces](https://help.openai.com/en/articles/20001554-manage-dots-in-chatgpt-workspaces).

### Record access-removal results

After completing the access-change checklist, record which permissions, app authorizations, website sessions, computer connections, and messaging identities were removed. Check active work and schedules separately, including work delegated to Work or Codex. Record any work that remains active and its responsible owner.

Removing access does not reverse actions already completed in another service. Check the receiving service when an action needs to be undone.

### Respond to an unexpected action

Pause the dot from Admin Console, confirm its paused status in the inventory, and ask the member to review the affected task. Save the task link and available activity records, check the app or computer permissions involved, and follow your organization's incident process. Whether you can undo an action depends on the action and the service.

## Help members work well with dots

Help members choose work to delegate and connect the accounts and tools they'll need. Encourage them to tell their dot what to do, when to do it, and who should see the result.

For example, “Prepare a weekly project update for me to review” asks for a draft. “Post the approved update in our team channel every Friday” also gives permission to post. Members should check important results and know how to review activity, change a schedule, and pause their dot. Share [Getting started](https://learn.chatgpt.com/docs/dots/getting-started), [Tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory), and [Controls](https://learn.chatgpt.com/docs/dots/controls) to help them get started.
