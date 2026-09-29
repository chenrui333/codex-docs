---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/teams'
source_kind: 'learn_markdown'
---

# Set up and manage teams and Team Tasks

Source: https://learn.chatgpt.com/docs/enterprise/teams

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Teams give people in ChatGPT a shared place to organize work and collaborate. With Team Tasks, members can set up work to run on a schedule or when a specific event occurs, such as preparing a weekly report or summarizing new project updates.

To get started, learn how to [set up a team](https://learn.chatgpt.com/docs/enterprise/teams#set-up-a-team) and [create a Team Task](https://learn.chatgpt.com/docs/enterprise/teams#create-a-team-task).

Enterprise admins control who can create teams and manage Team Tasks through two permissions: [Create teams and Create and manage team automations](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions#set-the-workspace-default-then-create-targeted-custom-roles). Admins can also make [workspace connections](https://learn.chatgpt.com/docs/enterprise/shared-connections#create-a-workspace-connection) available to teams. Each team’s service account and configured connections determine which external accounts its tasks use.

For more on team membership and tasks, see [Teams in ChatGPT](https://help.openai.com/articles/20001541) and [Creating and managing team tasks in ChatGPT](https://help.openai.com/articles/20001540) in the Help Center.

<span
  id="plan-the-teams-access-and-responsibilities"
  data-localization-body-anchor
/>

## How teams and Team Tasks work

[Workspace connections](https://learn.chatgpt.com/docs/enterprise/shared-connections) let Team Tasks use company-managed app accounts so each team member doesn't need to connect their own account.

Teams can include people within a department or across functions who share a goal. A team in ChatGPT is separate from a [workspace group created manually or synced through SCIM](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning#compare-membership-sources).

Here are examples of scheduled and event-triggered Team Tasks:

| **Team**         | **Who works together**                                                                        | **Example Team Task**                                                                                           |
| ---------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Product launch   | Product, marketing, and support teams preparing a release.                                    | When a message arrives in the launch Slack channel, summarize launch progress, milestone changes, and blockers. |
| Customer success | Account managers and customer success teams supporting customers.                             | Each Monday, summarize the previous week's customer updates, follow-ups and open questions.                     |
| Sales            | Sales, solutions engineers, and customer success teams closing deals and onboarding customers | When a deal closes, prepare an onboarding brief with customer goals, commitments, and open questions.           |
| Marketing        | Project leads and contributors responsible for a shared project.                              | Each morning, summarize project progress, blockers, and upcoming deadlines.                                     |

Team Tasks run in the cloud with the team's service account and configured app connections.

### Before you begin

Before setting up a team or its tasks, a workspace owner should enable the following permissions for the intended users through workspace settings or custom roles:

- [Create teams](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions#set-the-workspace-default-then-create-targeted-custom-roles): Required to create a team

- [Create and manage team tasks](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions#set-the-workspace-default-then-create-targeted-custom-roles): Required to create or edit team tasks

See [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions#set-the-workspace-default-then-create-targeted-custom-roles).

- **Workspace admin:** Set up and authorize approved workspace connections, and choose who can find and use them. Check the external account’s data and action permissions. See [Workspace connections](https://learn.chatgpt.com/docs/enterprise/shared-connections#create-a-workspace-connection).

- **Team owner:** After creating the team, select the available connections it needs where your permissions allow. Before scheduling a Team Task, confirm which external account each connection uses.

<span
  id="2-configure-membership-and-assign-maintainers"
  data-localization-body-anchor
/>

### Set up a team

1. **Create the team**. In the intended workspace, open Settings &gt; Teams and select Create team. Enter a Name and optional Description, then select Create.

2. **Review access and invite colleagues**. Before inviting colleagues, review access to earlier runs and generated files; individual tasks and runs cannot have separate access restrictions. Select Invite, search by Name or email, and select Add member or Add members. Members can invite coworkers and remove non-owner members. Same-workspace join links do not require owner approval.

3. **Add the team’s connections.** Workspace connections use centrally managed accounts; team connections share an individually connected account with the team. As team owner, choose a connection you’re allowed to use. Review its data and action permissions, and complete any required sign-in before unattended work. Team ownership doesn’t grant workspace admin permissions. See [Workspace connections](https://learn.chatgpt.com/docs/enterprise/shared-connections#create-a-workspace-connection) for admin setup.

<span
  id="create-and-validate-the-first-team-task"
  data-localization-body-anchor
/>

<span
  id="2-review-the-schedule-actions-and-audience"
  data-localization-body-anchor
/>

<span
  id="3-validate-access-and-the-first-result"
  data-localization-body-anchor
/>

### Create a Team Task

1. Open **Scheduled** &gt; **+ New Task**. Select the **Team toggle** and the team that will own the task.

2. Choose a **Trigger**. For **Schedule**, check the timing and time zone. For a supported event trigger, check its conditions and required connection.

3. In **Instructions**, describe the goal and expected output. Include success criteria and guardrails. Link task-specific sources, and review shared instructions if the team has a designated [Space](https://learn.chatgpt.com/docs/space). Tasks do not inherit the creator’s personal memories, custom instructions, or chat history.

4. Review **Plugins** and **Advanced** settings, including **Model**. Choose a model available to the team; this may differ from your personal account. Select **Create**.

5. Select **Run now** and inspect the result in **Previous runs**. Use **Edit** to change instructions or settings.

<span
  id="review-membership-connections-and-destinations"
  data-localization-body-anchor
/>

<span
  id="handle-departures-and-stop-work-when-needed"
  data-localization-body-anchor
/>

## Teams and Team Tasks FAQ

<ToggleSection title="Can team membership be imported or kept in sync with workspace groups or Slack/Microsoft Teams channels?">

No. ChatGPT team membership is separate from workspace groups and Slack or Microsoft Teams channels. It cannot be imported or synced; add and remove members in ChatGPT.

</ToggleSection>

<ToggleSection title="Who can create a team, change its membership, and manage its tasks?">

[Workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions#set-the-workspace-default-then-create-targeted-custom-roles) control team creation and task creation or updates. The creator becomes team owner without gaining workspace admin rights. Members can invite coworkers and remove non-owner members; same-workspace join links need no owner approval.

Only the team owner can delete the team. Workspace admins manage approved connections and who can use them.

</ToggleSection>

<ToggleSection title="Are these workspace controls enforced across every supported team and task creation or editing entry point?">

Yes. Create teams governs team creation; Create and manage team automations governs task creation and updates across supported entry points. Team membership and connection permissions still apply.

</ToggleSection>

<ToggleSection title="What access does someone gain when they join a team?">

New members can see all earlier runs and generated files; individual tasks and runs cannot have separate access restrictions. [Pages and Spaces retain their own sharing permissions](https://learn.chatgpt.com/docs/space/collaboration#share-a-page-or-space). Joining a team, you’ll inherit any pages and spaces that are shared with the team. Joining does not share personal chats or connections. Workspace members opening a join link can see the team’s name and member list before joining.

</ToggleSection>

<ToggleSection title="How can workspace admins review activity without joining a team?">

Admins can review activity through the [Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api#get-started) and restrict access by role.

</ToggleSection>

<ToggleSection title="Whose account does a Team Task use?">

Team Tasks use the team’s service account and [configured app connections](https://learn.chatgpt.com/docs/enterprise/shared-connections#understand-the-connected-accounts-permissions). A connection’s account determines its data and actions, which may differ from the creator’s or editor’s personal access. See [Connecting and managing app accounts](https://help.openai.com/en/articles/20001494-connecting-and-managing-app-accounts-in-chatgpt).

</ToggleSection>

<ToggleSection title="How do plugins and connections work together?">

[Team plugins and connections](https://learn.chatgpt.com/docs/enterprise/shared-connections#connections-for-teams-and-workflows) serve different purposes: plugins provide tools or skills; connections supply app access. Members need not connect the same account individually.

</ToggleSection>

<ToggleSection title="Can workspace connections expose information beyond a member&#x27;s personal access?">

Yes. Connected accounts may access information a member’s own account cannot. Review team membership alongside each connection’s resource access.

</ToggleSection>

<ToggleSection title="Can Team Tasks write to connected systems?">

Yes, if the tool and connection allow it—for example, posting to Slack. Unattended runs cannot complete a new app sign-in and remain subject to action-approval requirements.

</ToggleSection>

<ToggleSection title="What happens when a task creator or team owner leaves?">

Authorized teammates can edit, pause, or resume shared tasks. Before [offboarding a creator or owner](https://learn.chatgpt.com/docs/enterprise/user-lifecycle#remove-a-departing-employee), review team ownership and required connections.

Team-owned tasks are designed to persist after the creator leaves, but required connections may lose access.

Owners must transfer ownership before leaving. Connections the new owner cannot access become disabled for the entire team.

</ToggleSection>

<ToggleSection title="What happens to active and queued runs when a task is paused or deleted?">

Pausing prevents future scheduled and event-triggered runs. Neither pausing nor deleting a task should be relied on to interrupt an active run.

</ToggleSection>

<ToggleSection title="What team and task activity can admins audit?">

The team’s Activity view keeps track of changes. Authorized members can inspect individual runs and results.

Use supported [Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api#confirm-the-administration-boundaries) records to investigate team activity. Confirm which team, task, and connection records are available before relying on them for an audit.

Use the current [Admin API reference](https://chatgpt.com/public/admin/api-reference) for each event’s exact fields and supported coverage.

</ToggleSection>

<ToggleSection title="How are Team Tasks billed?">

Team Tasks use workspace credits. Team spending limits are separate from user limits.

</ToggleSection>
