---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams'
source_kind: 'learn_markdown'
---

# Set up and manage @ChatGPT in Slack and Microsoft Teams

Source: https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

In supported Slack and Microsoft Teams conversations, people can ask @ChatGPT to summarize information, draft responses, or use approved tools.

For everyday use, see the [Help Center user guide](https://help.openai.com/articles/20001537).

ChatGPT admins connect platforms and configure surfaces, [plugins](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors#step-2-manage-capabilities), and [workspace connections](https://learn.chatgpt.com/docs/enterprise/shared-connections). Slack and Teams admins manage the messaging-platform setup.

For detailed setup, see the [Help Center setup guide](https://help.openai.com/articles/20001538).

## How access works

Choose which plugins and workspace connections @ChatGPT’s service account can use. People who can use the surface can access those tools and data, which may differ from their personal access.

@ChatGPT uses configured connections and conversation context. It does not inherit a person’s file, app, or private-channel access. [Personal plugin access](https://learn.chatgpt.com/docs/plugins?surface=web#how-permissions-and-data-sharing-work) requires separate authorization where supported. Shared replies are visible to conversation participants.

## Before you begin

Before setup, identify the ChatGPT workspace and Slack workspaces or Microsoft Teams tenant you intend to connect. Confirm that @ChatGPT is available for your organization and agree on the pilot audience.

Assign the following responsibilities before setup:

- ChatGPT workspace admin or owner: Connect the platform, create the surface, and choose its plugins and workspace connections.

- Slack or Teams admin: Approve permissions and install the app. Teams admins also manage audience assignment and coordinate required consent with an authorized Microsoft administrator.

- **Connection owner:** Prepare approved company accounts and verify their resource and action permissions. Follow the [Workspace connections guide](https://learn.chatgpt.com/docs/enterprise/shared-connections#create-a-workspace-connection) for authorization.

- **Pilot owner:** Define the audience and supported conversations to test, including people who should not have access.

## Set up Slack

<span
  id="1-confirm-the-slack-workspace-and-permissions"
  data-localization-body-anchor
/>

### 1. Plan your surface configuration

A surface defines where @ChatGPT is available and which tools it can use.

Configure one surface per Slack workspace, including each connected workspace in Enterprise Grid.

### 2. Connect Slack in ChatGPT

In the [OpenAI admin console](https://admin.openai.com/), select the intended workspace and open Agents to connect Slack. Review the requested permissions.

Have the Slack owner or authorized app manager complete any required approval, then confirm the connection in ChatGPT.

If your organization already uses ChatGPT in Slack, a Slack admin must approve the additional app permissions to use the new @ChatGPT experience. See the [guidance for existing Slack installations](https://help.openai.com/articles/20001536). Existing installations won’t stop working immediately at launch.

<span
  id="3-create-the-deployment-and-choose-its-scope"
  data-localization-body-anchor
/>

<span
  id="set-destination-controls-and-instructions"
  data-localization-body-anchor
/>

### 3. Create the surface and choose its scope

Create a surface for the connected Slack workspace and give it a recognizable name.

For a channel pilot, choose **Selected channels only** and add the approved channels. This does not block direct messages.

### 4. Test the experience

Before adding company connections, test a request in an approved Slack channel and in a direct message.

If @ChatGPT does not respond or show that it is working within a minute, follow the [setup troubleshooting checks](#h.no5mkx5zlseo) below.

## Set up Microsoft Teams

Microsoft Teams admins manage app installation, user access, and any required Microsoft consent. ChatGPT workspace admins manage the Teams connection, surface settings, and [workspace connections](https://learn.chatgpt.com/docs/enterprise/shared-connections).

For step-by-step setup instructions, see the [Help Center setup guide](https://help.openai.com/articles/20001538).

## Check your surface scope

Confirm the surface matches its Slack workspace or Teams tenant. Enterprise Grid needs one surface per connected workspace.

<span
  id="enable-the-credential-for-the-deployment"
  data-localization-body-anchor
/>

## Configure company access

Keep company-managed access separate from personal authorization:

1. **Personal access:** Where supported, using plugins connected in [ChatGPT.com](https://chatgpt.com/) or the desktop app requires separate authorization. This is separate from shared company access.

2. **Shared company access:** Surface plugins use the configured company account’s permissions, which may differ from participants’ personal access. Members do not each authenticate the shared account.

{/*  */}

1. Check the surface’s connected Slack workspace or Teams tenant.

2. Have the connection owner verify the approved company account’s permissions. Use the [Workspace connections guide](https://learn.chatgpt.com/docs/enterprise/shared-connections#create-a-workspace-connection) for setup and authorization.

3. Add the approved plugin and select the intended workspace connection.

4. Save, then have the pilot owner test the connection in its Slack or Teams conversation.

## Enable Codex Cloud for Slack

Codex Cloud delegation from Slack requires separate setup where available.

1. Enable **Codex Cloud** for your workspace.

2. Where [Codex Cloud role-based access control](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions#review-codex-cloud-access-and-environment-administration) applies, grant access to the Slack surface’s service account and requesting users.

3. [Publish a cloud environment and share it with your workspace](https://learn.chatgpt.com/docs/environments/cloud-environments#share-within-an-enterprise-workspace).

4. Verify each requesting user’s access to the environment and any repositories requiring authentication.

5. Have a pilot user request a repository investigation in Slack and confirm the coding task starts.

The service account finds environments; the coding task runs as the requesting user. The service account does not need GitHub access.

<span
  id="verify-a-pilot-before-expanding-access"
  data-localization-body-anchor
/>

## Validate setup

Before expanding access, use approved test data to check successful requests and access boundaries for each supported conversation type.

- **Slack:** Test an approved channel, an excluded channel, and direct messages. Channel restrictions do not block direct messages.

- Teams: Test assigned and unassigned users. Test personal chat only where your surface supports it.

- **Connections and actions:** Verify the acting account, source access, and results of enabled write or send actions in approved destinations.

- **Reply visibility:** Confirm who can see responses and open linked sources or files.

## Maintain the surface

Assign an owner to maintain platform connections, app assignment, and approved plugins. Involve platform admins for installation or consent changes and connection owners for reauthorization.

After a permission or connection change, repeat the relevant [validation checks](#h.ts4i3qduozr) before expanding access. Use the [Workspace connections guide](https://learn.chatgpt.com/docs/enterprise/shared-connections) to review company-account access and troubleshoot authorization.

Before offboarding or removing access, identify affected surfaces and connections and coordinate with their administrators.

<span
  id="why-cant-a-teammate-open-a-generated-file"
  data-localization-body-anchor
/>

<span
  id="why-did-a-working-connection-stop-working"
  data-localization-body-anchor
/>

<span
  id="what-should-i-include-in-a-support-request"
  data-localization-body-anchor
/>

<span
  id="what-else-should-we-confirm-before-enabling-chatgpt"
  data-localization-body-anchor
/>

## Setup FAQ

<ToggleSection title="Why can’t people find @ChatGPT or get a response?">

For Slack surfaces:

- Confirm that @**ChatGPT** is installed in the Slack workspace you are testing.

- Check that the channel belongs to the surface’s connected Slack workspace.

- Have a Slack admin check required scopes on the [app details page](https://slack.com/marketplace/A097V82EGG2-chatgpt).

For Teams surfaces:

- Confirm that a Microsoft Teams admin has enabled @ChatGPT for your tenant.

- Confirm that the app is assigned to the intended users and added to the team where you are testing through the approved installation route. See the [Help Center setup guide](https://help.openai.com/articles/20001538) for detailed instructions.

- Confirm a ChatGPT surface exists for the Teams tenant you are testing.

</ToggleSection>

<ToggleSection title="Why is company information missing?">

Check the surface’s plugins and the [connected account’s access](https://learn.chatgpt.com/docs/enterprise/shared-connections#troubleshoot-access) in the source system.

</ToggleSection>

<ToggleSection title="Do Slack and Teams support the same features?">

Conversation types and features can differ between platforms. Check the [Help Center user guide](https://help.openai.com/articles/20001537) and test each planned workflow.

</ToggleSection>

<ToggleSection title="How does @ChatGPT interact with memory?">

At launch, @ChatGPT does not include memory or use a person’s ChatGPT memories.

</ToggleSection>
