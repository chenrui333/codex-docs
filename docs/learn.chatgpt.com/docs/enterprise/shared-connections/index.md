---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/shared-connections'
source_kind: 'learn_markdown'
---

# Workspace connections

Source: https://learn.chatgpt.com/docs/enterprise/shared-connections

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

A workspace connection lets an eligible Team Task or @ChatGPT surface use a company-managed app account without each participant connecting a personal account.

For background, see [how plugin permissions and data sharing work](https://learn.chatgpt.com/docs/plugins?surface=web#how-permissions-and-data-sharing-work).

Workspace admins authorize supported app accounts, manage saved connections, and control who can find and use them. The provider controls each account’s data and action permissions.

See [Connecting and managing app accounts](https://help.openai.com/en/articles/20001494-connecting-and-managing-app-accounts-in-chatgpt) for account authorization, and [Creating and managing team tasks in ChatGPT](https://help.openai.com/articles/20001540) for recurring work.

## How it works

Use connections for [@ChatGPT](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams) or [Team Tasks](https://learn.chatgpt.com/docs/enterprise/teams#create-a-team-task) that need company-managed accounts. Admins approve access; team owners select available connections where permitted. Connections can be reused across eligible teams and workflows.

A **connection** authenticates an app to an account.

## Set up a connection

### Before you begin

Confirm the app and authentication method are available in your workspace, then assign these responsibilities:

**Workspace administrator:** With [permission to manage plugins](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors#step-1-enable-plugin-availability) (workspace owner or admin), create and authorize the connection and configure who can find, use, and manage it.

**Provider administrator:** Provision accounts and approve source-service access. For Notion and Linear, involve the provider administrator; this person may differ from the account authenticating the connection.

Provider requirements differ: Gmail may need a separate user account, Drive access must be configured in Google, and GitHub uses user-account sign-in at launch.

**Connection account:** Use an approved account or service identity with only the required resource access. Follow the supported authentication method and avoid reliance on an employee’s personal account. See [Connecting and managing app accounts in ChatGPT](https://help.openai.com/en/articles/20001494-connecting-and-managing-app-accounts-in-chatgpt).

**Connection owner:** Maintain authorization, coordinate permission changes, and restore failed access. Review resource scope, read/write permissions, and revocation before sharing.

**Team or workflow owner:** Agree on required resources and actions with the admin, then select and test the connection in the task or @ChatGPT surface.

### Create a workspace connection

1. In the Admin Console, select the workspace and open Workspace connections &gt; +. Choose the app.

2. Follow the app’s instructions for the offered authentication method. Enable real-time app access if prompted.

3. Authenticate the designated account or complete app installation. Verify the account or installation and requested permissions.

4. Give the saved connection a nickname that describes its access, such as “Project reporting: read access.”

5. Grant access to approved users, teams, or service accounts. Review use and management permissions separately, then hand off to the team or workflow owner for selection and testing.

<span
  id="notion--connect-the-intended-workspace-and-content"
  data-localization-body-anchor
/>

<span
  id="notion-connect-the-intended-workspace-and-content"
  data-localization-body-anchor
/>

### Set up each app

Use the method offered for your app, then configure access and test it in the intended workflow.

### Google Drive

<span
  id="google-drive--authorize-a-google-account"
  data-localization-body-anchor
/>

<span
  id="google-drive-authorize-a-google-account"
  data-localization-body-anchor
/>

#### Authorize an account

Use an approved Google account with access to the required files or shared drives.

1. Choose Google sign-in, select the account you want to connect, and review the requested access before approving.

2. Confirm the Google account, then name the connection in ChatGPT. If the workflow creates files, test the destination and recipients’ access.

<span
  id="google-drive--use-a-google-service-account"
  data-localization-body-anchor
/>

<span
  id="google-drive-use-a-google-service-account"
  data-localization-body-anchor
/>

#### Use a service account

If direct service-account authentication is offered, prepare an approved Google Cloud service account and JSON key. This uses the service account’s resource access, without domain-wide delegation.

1. Give the service-account email access to the required files, folders, or shared drives. Check read and write permissions separately.

2. Enter the complete JSON key in the protected credential field. Keep it out of screenshots and support messages.

3. Save the connection and try reading a file shared with the service account.

**Use a shared drive to create files.** The service account needs write permission there. It cannot own files in a personal My Drive.

For missing files, check sharing with the service-account email and the app’s allowed actions in ChatGPT. Folder sharing does not grant access across the Google Workspace domain.

If Drive offers domain-wide delegation, follow the [delegated-access procedure below](https://learn.chatgpt.com/docs/enterprise/shared-connections#google-workspace-domain-wide-delegation).

### Gmail

#### Authorize a mailbox

If OAuth is offered, authorize the designated Gmail mailbox. Ask IT for a separate user account if the workflow needs its own mailbox.

1. Choose Google sign-in, select the mailbox, and review the requested access before approving.

2. Check the saved connection and read an approved test message. If sending is required, test an approved recipient and verify the sender and delivered message.

Google Groups are not mailboxes. A connected mailbox subscribed to a group can receive its messages but may also expose other mail. Review its contents and allowed actions before sharing.

<span
  id="google-workspace--domain-wide-delegation"
  data-localization-body-anchor
/>

<span
  id="google-workspace-domain-wide-delegation"
  data-localization-body-anchor
/>

#### Set up domain-wide delegation

Delegation requires a verified requesting employee and uses their delegated Google permissions. Before unattended work, confirm the experience can establish that requester. [Direct Drive service-account access](https://learn.chatgpt.com/docs/enterprise/shared-connections#google-drive-use-a-google-service-account) works differently.

Use delegation only where offered. It requires Google Workspace super-admin approval and an approved Google Cloud service account with its numeric OAuth client ID and complete JSON key.

1. Select the apps and actions, obtain their exact required scopes, and have your Google Workspace administrator approve them.

2. In Google Admin, open **Security &gt; Access and data control &gt; API controls &gt; Manage Domain Wide Delegation**. Authorize the numeric client ID and approved scopes; verify the saved grant.

3. Enter the JSON key privately in ChatGPT. Test in the experience that will use the connection, with a verified requester and a resource they can access.

For denied requests, check the requester, approved scopes, and resource access. Do not broaden scopes just to clear an error.

### GitHub

<span
  id="github--select-an-app-installation-and-repositories"
  data-localization-body-anchor
/>

<span
  id="github-select-an-app-installation-and-repositories"
  data-localization-body-anchor
/>

#### Authorize a user account

Use an organization-approved GitHub user account, preferably dedicated to this setup, with access to the required repositories.

**GitHub app sign-in is unavailable for this launch.**

1. Choose GitHub user-account sign-in and authenticate the designated account.

2. Review the account and requested access before approving the connection.

3. Save and test a known repository resource from the intended workflow. Test required write actions separately.

If a repository is missing, check the designated account’s GitHub access and the app’s allowed actions in ChatGPT.

### Notion

#### Prepare a dedicated Notion account

Ask your Notion administrator to provision an approved dedicated account and grant only the required resource access. Confirm workspace membership. The connection uses this account’s permissions.

#### Configure the workspace connection

In Admin Console &gt; Workspace connections, add the Notion plugin. Sign in as the designated account through Notion MCP, select the workspace, and name the connection to identify the workspace and account.

Save and test a known Notion page from the intended task or surface. Test required writes separately and verify the result.

### Linear

#### Prepare a dedicated Linear account

Ask a Linear administrator to invite the designated account as a guest and limit its access to the teams it needs:

- Open Settings → Administration → Members → Invite.

- Enter the designated account’s email address.

- Under Invite as…, choose Guest.

- Select only the Linear teams the account should access.

- Send the invitation and accept it as the designated account.

See [Linear invitation instructions](https://linear.app/docs/invite-members).

If the designated account is already a Member, ask a Linear administrator to update its role:

- Open Settings → Administration → Members.

- Find the account and click ⋯ → Change role… → Guest.

- Limit membership to intended teams. Guests have normal member capabilities within those teams. See [Linear roles](https://linear.app/docs/members-roles).

#### Configure the workspace connection

1. In Admin Console → Workspace connections, add the Linear plugin.

2. Sign in as the designated account, select the workspace, and review permissions.

The connection uses that account’s Linear access. From the task or surface that will use it, confirm that the connection can read an issue in an intended team. Test any required write actions separately.

### Slack

<span
  id="slack--configure-the-chatgpt-in-slack-connection"
  data-localization-body-anchor
/>

<span
  id="slack-configure-the-chatgpt-in-slack-connection"
  data-localization-body-anchor
/>

<span
  id="test-an-existing-workspace-connection"
  data-localization-body-anchor
/>

#### Configure the workspace connection

Confirm the required Slack workspace, channels, app installation, and admin approval. Use the surface’s [shared ChatGPT in Slack connection](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams#configure-company-access). Personal Slack connections and the [dots Add to Slack connection](https://learn.chatgpt.com/docs/dots/channels#slack) are separate.

Test a post in an approved channel and verify its workspace and sender. Test reading and search separately; a successful post does not verify either.

Team and workflow owners

## Select and test

### Configure access and select the connection

**Workspace administrator:** Configure role access and availability; review use and management permissions separately. Give the workflow owner the connection nickname, account, approved resources/actions, and owner’s contact details.

**Team or workflow owner:** Select and save the available connection where permitted, then test it in the intended workflow. If missing, have the workspace admin check access and availability.

<span
  id="configure-access-and-select-the-credential"
  data-localization-body-anchor
/>

### What each setting controls

Enabling @ChatGPT in Slack or Microsoft Teams for a connection also enables that connection’s team and service-account access options. These cannot be disabled independently while @ChatGPT is enabled for that connection.

| **Setting or permission**  | **What to check**                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------- |
| External account           | Can the designated account or installation access the required resources and actions?                   |
| Role access                | Can the approved person or service account use the connection? Check management permissions separately. |
| Availability               | Can the intended users, teams, or service accounts find the connection? Check the configured audience.  |
| Team or workflow selection | Is the connection selected and saved for the team or workflow that will use it?                         |

### Connections for teams and workflows

#### Review a team's connections

Check each plugin’s connection nickname, account, and resource access with the connection owner.

#### Choose a connection for a workflow

For **@ChatGPT**, open the [surface's plugin settings](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams#configure-company-access) and select the connection. Save, then reopen settings to check the selection.

For a [Team Task](https://learn.chatgpt.com/docs/enterprise/teams#create-a-team-task), confirm the selected connection for each app. The team service account runs the task; each app’s authentication method determines its external account. Confirm that method supports the task’s run type, especially if it requires a verified employee.

<span
  id="test-access-through-the-intended-experience"
  data-localization-body-anchor
/>

### Test the connection in your workflow

1. Read a known source from the intended workflow. Verify the identity and resource.

2. Test writes or sends at an approved destination and open the resulting file, record, or message.

3. Verify that an approved user can use the connection and an unauthorized user cannot. Check recipients’ access to generated files.

Connection users

## Use workspace connections

### Understand the connected account's permissions

Actions use the connected account’s permissions, which may exceed your personal access. OAuth uses the authorized account; direct service-account access uses that identity. Some methods require a verified requester; see [Google Workspace delegation](https://learn.chatgpt.com/docs/enterprise/shared-connections#google-workspace-domain-wide-delegation).

### Use an available workspace connection

1. If offered, choose the designated connection. For managed @ChatGPT surfaces or Team Tasks, confirm the selection with the owner.

You do not re-enter the designated account’s credentials for each use. If prompted to sign in, verify the connection and account being authorized.

A workspace connection may read sources you cannot open. Source links do not grant access. Generated files may be private to the connected account, so check recipients’ access before sharing.

Connection owners and users

## Manage and troubleshoot

### Manage changes and remove access

Review the connection’s nickname, availability, and roles.

If authorization or provider permissions change, have the connection owner restore access and the workflow owner retest. Renaming a connection does not change external permissions.

Before disabling a connection, identify affected workflows with their owners. After removal, verify those users and workflows can no longer use it.

Revoke provider authorization separately; disabling the ChatGPT connection does not replace this step.

<span
  id="troubleshoot-by-checking-the-failed-layer"
  data-localization-body-anchor
/>

<span
  id="find-the-right-person-to-resolve-access"
  data-localization-body-anchor
/>

### Troubleshoot access

For a missing connection, verify the workspace and use the [access troubleshooting table](https://learn.chatgpt.com/docs/enterprise/shared-connections#find-the-right-person-to-resolve-access) to find who can check role access and audience.

| **What happens**                            | **Who can help**                                                                                                    |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| The connection is missing                   | Your workspace administrator can check your role and the connection’s audience settings.                            |
| It is available but the job does not use it | The surface or Team owner can check which workspace connection is configured for the workflow’s app.                |
| A source or action fails                    | The connection owner can check which identity the connection uses and whether it can access the resource or action. |
| You can read a summary but not its source   | The source owner can check your access to the original page or file.                                                |
| A recipient cannot open a generated file    | The file owner can review its sharing settings.                                                                     |

Before retrying a failed write or send, check the destination. The action may have completed despite the error; retrying could create duplicates.

## Related guides

- [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors)

- [ChatGPT Work cloud security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security)
