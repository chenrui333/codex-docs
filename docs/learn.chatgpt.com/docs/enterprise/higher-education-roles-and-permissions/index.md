---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/higher-education-roles-and-permissions'
source_kind: 'learn_markdown'
---

# Best practices for ChatGPT Edu workspace configuration in higher education

Source: https://learn.chatgpt.com/docs/enterprise/higher-education-roles-and-permissions

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Configure campus access with five recommended custom roles: **Core, Plus, Advanced, Power, and TEST**. Use the matrices below to choose each role's permissions, then set model access and usage limits separately.

The permission labels and section order follow Edu Admin Console views reviewed on October 19 and 21, 2026. The values are recommended settings, not a copy of that workspace's configuration. Feature availability can differ by workspace and rollout.

## Choose the recommended roles

| Custom role  | Recommended members                                                            | Purpose                                                                                                                                     |
| ------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Core**     | Undergraduate students and faculty with everyday needs                         | Study, teaching, writing, research, working with documents, and introductory coding. Use Core as the campus baseline.                       |
| **Plus**     | Graduate students, professional staff, and faculty who use ChatGPT frequently  | Recurring academic and administrative work with additional approved workflows.                                                              |
| **Advanced** | Research faculty, analysts, and program leads                                  | Complex research, analysis, and approved advanced reasoning.                                                                                |
| **Power**    | Developers, data and IT teams, computer science labs, and advanced researchers | Coding, automation, and complex projects. Grant administrative authority separately.                                                        |
| **TEST**     | A small implementation team with named test owners                             | Validate a planned configuration with sample data and explicit test cases before changing a campus role. Remove temporary grants afterward. |

These are suggested names for custom roles your institution can create. **Plus** here is not the ChatGPT Plus subscription, and none of these names refers to an Edu plan or built-in admin role. Choose a role based on the work a person needs to do; a professor, student, or staff member can qualify for any appropriate level.

Keep most people in the built-in **Member** role. Assign built-in administrative authority separately:

| Built-in role        | Recommended assignment                                                                                          |
| -------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Owner**            | The platform owner and a documented backup responsible for workspace configuration and custom-role assignments. |
| **Admin**            | IT or academic technology staff responsible for supported member, group, app, and usage operations.             |
| **Analytics viewer** | Program leads who need reporting without general administration.                                                |
| **Member**           | Students, faculty, staff, researchers, and builders using the service.                                          |

Have a workspace Owner create and assign custom roles. A custom role does not confer Owner or Admin authority. See [workspace roles](https://help.openai.com/en/articles/8266401-managing-members-workspace-roles-and-seats-in-chatgpt-enterprise-and-edu).

## Apply the matrix

Open [Admin Console](https://admin.openai.com), select the intended Edu workspace, then go to **Policy & security → Permissions**. Use **Workspace default** for the campus baseline and **Roles** for overrides.

| Matrix value | Action in the console                                                                                                                       |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **On**       | Enable for the role, subject to the workspace's entitlement and approved institutional uses.                                                |
| **Off**      | Leave disabled for this role. For approved exceptions, use a role tied to a specific responsibility.                                        |
| **Review**   | Start with Off. Complete the decision described below the table, then explicitly choose On or Off. Review is guidance, not a console state. |

Set **Workspace default** to match the Core column, with Review items Off until resolved. For each custom role, use **Default** only where the workspace value is the intended value; otherwise set an explicit On or Off. Some controls offer only On and Off.

Ordinary roles combine grants: Off in one role does not cancel On in another. Check both direct assignments and group roles. A separate Lockdown Mode restriction can still apply. Parent permissions may hide their child controls when disabled; enable an approved parent before configuring its children. [How RBAC works](https://help.openai.com/en/articles/11750701-rbac).

## Permissions by role

Choose a role to show its recommendations in every permission and model table. Select **All roles** to compare the full matrix. The sections follow the order in **Permissions → Workspace default**. The two **Allow local computer access** rows are distinguished by their parent section.

### Chat

<RoleMatrix id="edu-role-matrix-1" label="Recommended role" allRolesLabel="All roles" showSelector={true}>

| Permission                                          | Core   | Plus   | Advanced | Power  | TEST   |
| --------------------------------------------------- | ------ | ------ | -------- | ------ | ------ |
| Search the web                                      | On     | On     | On       | On     | On     |
| Run deep research                                   | On     | On     | On       | On     | On     |
| Create and manage projects                          | On     | On     | On       | On     | On     |
| Share projects                                      | On     | On     | On       | On     | On     |
| Share projects via workspace links                  | Review | Review | Review   | Review | Review |
| Browse and run workspace agents                     | Review | Review | On       | On     | On     |
| Build workspace agents                              | Off    | Review | Review   | Review | On     |
| Share workspace agents                              | Off    | Review | Review   | Review | On     |
| Publish workspace agents                            | Off    | Review | Review   | Review | Review |
| Share workspace agents with agent-owned connections | Off    | Review | Review   | Review | Review |
| Create and manage GPTs                              | Off    | Off    | Off      | Off    | Review |
| Publish GPTs to workspace                           | Off    | Review | Review   | Review | Review |
| Publish GPTs externally                             | Off    | Off    | Off      | Off    | Off    |
| Allow OpenAI GPTs                                   | On     | On     | On       | On     | On     |
| Allow all third party GPTs                          | Off    | Off    | Off      | Off    | Off    |
| Allow owner-approved GPTs only                      | On     | On     | On       | On     | On     |
| Use image generation models                         | On     | On     | On       | On     | On     |
| Use Voice                                           | On     | On     | On       | On     | On     |
| Share screen and video in Voice                     | On     | On     | On       | On     | On     |
| Reference Space files automatically                 | On     | On     | On       | On     | On     |
| Use ChatGPT Record                                  | Review | Review | Review   | Review | On     |
| Reference past notes and transcripts                | Review | Review | Review   | Review | On     |
| Run code in Canvas and code blocks                  | On     | On     | On       | On     | On     |
| Allow internet access in Canvas and code blocks     | On     | On     | On       | On     | On     |
| Share chats and scheduled tasks in the workspace    | On     | On     | On       | On     | On     |
| Use ChatGPT for PowerPoint                          | Review | Review | Review   | On     | On     |
| Use ChatGPT for Excel and Sheets                    | On     | On     | On       | On     | On     |
| Use ChatGPT for Word                                | Review | Review | Review   | On     | On     |

</RoleMatrix>

Keep everyday learning, research, and collaboration available across roles. Apply institutional rules for recordings, screen sharing, stored files, and network-connected code. For **Review** items, identify the approved course, team, workflow, and sharing audience before enabling those permissions.

Give agent-building access to people maintaining an approved workflow. Reserve workspace-wide publication for designated publishers. An agent-owned connection requires a separate review of the shared account, source data, permitted actions, and recipients; prefer users' own connections where supported. For details, see [Workspace agent administration](https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business).

Use plugins for new reusable workflows. Keep GPT creation off; grant temporary migration access only where still supported. Custom GPTs are scheduled to retire on December 11, 2026; follow the owning workspace's notice. Migration does not transfer custom actions or sharing settings. For details, see [GPT migration guidance](https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq).

### Work

<RoleMatrix id="edu-role-matrix-2" label="Recommended role" allRolesLabel="All roles" showSelector={false}>

| Permission                                       | Core   | Plus   | Advanced | Power  | TEST |
| ------------------------------------------------ | ------ | ------ | -------- | ------ | ---- |
| Use Work                                         | On     | On     | On       | On     | On   |
| Locally on the ChatGPT desktop app               | On     | On     | On       | On     | On   |
| In the cloud on ChatGPT web, mobile, and desktop | On     | On     | On       | On     | On   |
| Allow event-triggered scheduled tasks            | Off    | Review | Review   | Review | On   |
| Allow local computer access                      | Review | Review | Review   | Review | On   |

</RoleMatrix>

This follows the recommended setup's broad Work access for eligible members. Local work, cloud work, and a cloud task's access to a connected computer remain separate decisions. Enable **Allow local computer access** only for approved files, applications, and devices, with the applicable Agent security configuration.

For event-triggered tasks, approve the trigger, connected app, allowed actions, owner, and monitoring. Members also need Work and app access. Sharing scheduled tasks is controlled separately in Chat. [Work and Codex availability](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex) · [Scheduled-task controls](https://help.openai.com/en/articles/8411955-managing-workspace-settings-in-chatgpt-enterprise).

### Codex

<RoleMatrix id="edu-role-matrix-3" label="Recommended role" allRolesLabel="All roles" showSelector={false}>

| Permission                                                        | Core   | Plus   | Advanced | Power  | TEST   |
| ----------------------------------------------------------------- | ------ | ------ | -------- | ------ | ------ |
| Use Codex locally on the ChatGPT desktop app                      | On     | On     | On       | On     | On     |
| Enable Computer History                                           | Off    | Off    | Review   | Review | Review |
| Discover and control devices remotely                             | Review | Review | Review   | Review | On     |
| Use Windows computer-use                                          | Off    | Off    | Review   | Review | On     |
| Enable device code sign-in for Codex, Excel, PowerPoint, and Word | Review | Review | Review   | Review | On     |
| Use Codex in the cloud                                            | On     | On     | On       | On     | On     |
| Manage workspace environments                                     | Off    | Off    | Off      | Off    | Off    |
| Use Codex Security                                                | Off    | Off    | Review   | Review | On     |
| Administer Codex                                                  | Off    | Off    | Off      | Off    | Off    |
| Administer Codex Security                                         | Off    | Off    | Off      | Off    | Off    |

</RoleMatrix>

Provide coding access across eligible roles, including students in coding courses. Review repository access, local runtime policy, and cloud environments separately. Device-code sign-in affects all four products named in the control.

Review Computer History capture and user opt-in before granting access to Computer History. Grant **Manage workspace environments**, **Administer Codex**, and **Administer Codex Security** through the specific responsibility roles below. A Power or TEST assignment should not automatically grant service administration. For details, see [Codex permission boundaries](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).

### Workspace capabilities—Let agents use cloud computers

<RoleMatrix id="edu-role-matrix-4" label="Recommended role" allRolesLabel="All roles" showSelector={false}>

| Permission           | Core   | Plus   | Advanced | Power  | TEST   |
| -------------------- | ------ | ------ | -------- | ------ | ------ |
| Use a browser        | On     | On     | On       | On     | On     |
| Allow network access | Review | Review | Review   | Review | Review |
| Allow computer use   | Off    | Review | Review   | Review | On     |

</RoleMatrix>

Before enabling a control, review how it affects Work Cloud, dots, and team automations. Browser access, network access, and computer use are separate controls. Approve required network destinations and applications for each workflow.

### Workspace capabilities—dots

<RoleMatrix id="edu-role-matrix-5" label="Recommended role" allRolesLabel="All roles" showSelector={false}>

| Permission                            | Core | Plus   | Advanced | Power  | TEST   |
| ------------------------------------- | ---- | ------ | -------- | ------ | ------ |
| Use dots                              | Off  | Review | Review   | Review | On     |
| Add dots to Slack and Microsoft Teams | Off  | Review | Review   | Review | Review |
| Allow local computer access           | Off  | Review | Review   | Review | Review |
| Use custom rules for dots             | Off  | Review | Review   | Review | Review |

</RoleMatrix>

Dots is labeled **Beta** in the inspected console. Approve the ongoing responsibilities, messaging destinations, and rules before enabling it. The **Allow local computer access** row here is the dots permission; it is separate from the identically named Work control. [Read the dots guidance](https://help.openai.com/en/articles/20001530-getting-started-with-your-dot).

### Workspace capabilities—plugins and skills

<RoleMatrix id="edu-role-matrix-6" label="Recommended role" allRolesLabel="All roles" showSelector={false}>

| Permission                             | Core   | Plus   | Advanced | Power  | TEST   |
| -------------------------------------- | ------ | ------ | -------- | ------ | ------ |
| Use plugins                            | On     | On     | On       | On     | On     |
| Upload plugins                         | Review | Review | Review   | Review | On     |
| Upload plugins with custom MCP servers | Off    | Review | Review   | Review | Review |
| Share plugins                          | Review | Review | Review   | Review | On     |
| Publish plugins to workspace           | Review | Review | Review   | Review | Review |
| Create plugins with MCPs               | Off    | Review | Review   | Review | Review |
| Use skills                             | On     | On     | On       | On     | On     |
| Upload skills                          | Review | Review | Review   | Review | On     |
| Share skills                           | Review | Review | Review   | Review | On     |
| Publish skills to workspace            | Review | Review | Review   | Review | Review |
| Install skills for others              | Off    | Off    | Off      | Off    | Off    |

</RoleMatrix>

Use **Plugins → Plugins** and **Plugins → Skills** to approve individual items and their audiences. MCP-backed plugins require an integration owner, reviewed authentication, and approved data access and actions. Use the additional roles below to assign responsibility for publishing items to the workspace and installing them for other people.

Plugin access does not authorize included apps or broaden permissions in the connected service. Review required apps and account authorization separately. For details, see [Plugin and app controls](https://help.openai.com/en/articles/11509118-admin-controls-security-and-compliance-for-plugins-and-apps).

### Workspace capabilities—Sites

<RoleMatrix id="edu-role-matrix-7" label="Recommended role" allRolesLabel="All roles" showSelector={false}>

| Permission                           | Core   | Plus   | Advanced | Power  | TEST   |
| ------------------------------------ | ------ | ------ | -------- | ------ | ------ |
| Use Sites                            | Review | Review | Review   | Review | On     |
| Publish sites to the public internet | Off    | Off    | Off      | Off    | Off    |
| Publish Sites with private tunnels   | Off    | Off    | Off      | Off    | Off    |
| Invite external visitors to sites    | Off    | Review | Review   | Review | Review |
| Attach private tunnels to Sites      | Off    | Off    | Off      | Off    | Off    |

</RoleMatrix>

Review site ownership, permitted content, and the displayed Sites terms before enabling those permissions. Grant permission to publish sites to the public internet through the institution's publishing process. Treat the two private-tunnel controls as separate grants for approved technical integrations; keep them off in the general campus roles. Their presence in a demo workspace does not establish availability in every Edu workspace.

Check the supported Sites scope for your workspace and region before enabling Sites. New Sites in US or EU data residency workspaces use that region for supported storage and hosting; existing Sites are not automatically migrated. Sites hosting is separate from inference residency. See [Sites administration](https://help.openai.com/en/articles/20001338-managing-chatgpt-sites-for-your-workspace).

### Workspace capabilities—teams, memory, and credentials

<RoleMatrix id="edu-role-matrix-8" label="Recommended role" allRolesLabel="All roles" showSelector={false}>

| Permission                        | Core   | Plus   | Advanced | Power  | TEST   |
| --------------------------------- | ------ | ------ | -------- | ------ | ------ |
| Create teams                      | Review | On     | On       | On     | On     |
| Create and update team tasks      | Review | On     | On       | On     | On     |
| Use password manager              | Review | Review | Review   | Review | Review |
| Use shared memory                 | On     | On     | On       | On     | On     |
| Use improved memory               | On     | On     | On       | On     | On     |
| Create personal access tokens     | Review | Review | Review   | On     | Review |
| View workspace members and groups | On     | On     | On       | On     | On     |

</RoleMatrix>

Assign an accountable owner to each team and team task. Define which institutional information may be retained in memory and whether the directory should be visible to the intended population. If institutional policy requires either feature to be off, change the corresponding row for every affected role.

Review password-manager use with IT. Allow personal access tokens only for approved integrations with an owner, the minimum necessary scope, and an expiration or revocation process. A token permission does not grant workspace Admin keys.

### Data export

<RoleMatrix id="edu-role-matrix-9" label="Recommended role" allRolesLabel="All roles" showSelector={false}>

| Permission                             | Core | Plus   | Advanced | Power  | TEST   |
| -------------------------------------- | ---- | ------ | -------- | ------ | ------ |
| Allow members to export their own data | Off  | Review | Review   | Review | Review |

</RoleMatrix>

Decide how students, faculty, and staff take permitted work with them when leaving. This permission covers members' own data. Edu workspaces with a data residency configuration are not eligible for member export. For details, see [Edu export requirements](https://help.openai.com/en/articles/20001279-exporting-data-from-a-chatgpt-edu-workspace).

### Teen experiences

<RoleMatrix id="edu-role-matrix-10" label="Recommended role" allRolesLabel="All roles" showSelector={false}>

| Permission                 | Core   | Plus   | Advanced | Power  | TEST   |
| -------------------------- | ------ | ------ | -------- | ------ | ------ |
| Apply teen content filters | Review | Review | Review   | Review | Review |

</RoleMatrix>

Choose the setting based on the actual population, including under-18 students. A role name, credit allowance, or filter setting does not determine eligibility to use ChatGPT.

### Space sharing

<RoleMatrix id="edu-role-matrix-11" label="Recommended role" allRolesLabel="All roles" showSelector={false}>

| Permission                                    | Core   | Plus   | Advanced | Power  | TEST   |
| --------------------------------------------- | ------ | ------ | -------- | ------ | ------ |
| Share Space files, pages, folders, and spaces | On     | On     | On       | On     | On     |
| Workspace links                               | Review | Review | Review   | Review | Review |

</RoleMatrix>

Allow collaboration with approved recipients. Review whether workspace links fit the audience for course materials, research, and departmental files. The sharing permission controls creating shares and changing access; turning it off does not remove access to content already shared with a member.

## Assign publishing and administration responsibilities

Assign narrowly scoped roles to the appropriate people instead of granting these capabilities to everyone in Power or TEST. Keep unrelated permissions Off in each additional role so it does not inherit broader workspace grants.

| Suggested additional role        | Permissions to enable                                                                                                                                     | Who should receive it                                                            |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Workspace publisher**          | Only the relevant permission (Publish workspace agents, Publish plugins to workspace, or Publish skills to workspace) and its required parent permissions | Owners of reviewed content and workflows approved for campus-wide distribution.  |
| **Site publisher**               | Use Sites and Publish sites to the public internet; enable external invitations only if needed                                                            | Institutional web publishers responsible for content, audience, and maintenance. |
| **Codex environment manager**    | Use Codex in the cloud and Manage workspace environments                                                                                                  | Maintainers of shared coding environments.                                       |
| **Codex administrator**          | Administer Codex, with required product access                                                                                                            | Staff operating the Codex service.                                               |
| **Codex Security administrator** | Use Codex Security and Administer Codex Security                                                                                                          | Security staff responsible for the service and approved repositories.            |
| **Skill distributor**            | Use skills and Install skills for others, with the authoring permissions needed for the workflow                                                          | Staff responsible for managed skill distribution.                                |
| **Integration maintainer**       | Only the required MCP, personal-token, or Sites private-tunnel permissions, plus their required parent permissions                                        | Named technical owners of reviewed integrations.                                 |

For example, a faculty member may receive Plus and Workspace publisher, while a student in a programming course receives Core with Codex access. Increasing a researcher's credit allowance does not require giving them publishing or administration permissions.

## Model access by role

Open **Policy & security → Models**. Configure **Workspace default**, then use **Roles** for role-specific settings. The table uses the model names and preference labels shown in the console we inspected. Enable only models available to your workspace.

<RoleMatrix id="edu-role-matrix-12" label="Recommended role" allRolesLabel="All roles" showSelector={true}>

| Permission                          | Core | Plus | Advanced | Power  | TEST   |
| ----------------------------------- | ---- | ---- | -------- | ------ | ------ |
| 6.1 Sol                             | Off  | Off  | Review   | On     | On     |
| 6 Astra                             | Off  | Off  | Review   | On     | On     |
| 6 Sol                               | Off  | Off  | Review   | On     | On     |
| 6 Luna                              | On   | On   | On       | On     | On     |
| 5.6 Sol                             | On   | On   | On       | On     | On     |
| 5.6 Terra                           | Off  | Off  | Review   | Review | Review |
| 5.6 Luna                            | On   | On   | On       | On     | On     |
| Daybreak Blue                       | Off  | Off  | Off      | Off    | Off    |
| Allow medium/high/extra high effort | On   | On   | On       | On     | On     |
| Allow Pro models                    | Off  | Off  | Review   | On     | On     |
| Allow fast mode                     | Off  | Off  | Review   | Review | Review |
| Allow Ultra Fast mode               | Off  | Off  | Off      | Review | Review |

</RoleMatrix>

**Model recommendations:** Keep 5.6 Sol available for ordinary Chat and 6 Luna for routine Work and Codex. Keep 5.6 Luna as a fallback where needed. Enable 6.1 Sol and 6 Sol for Power workflows, and review them for Advanced users. Approve Astra/Pro access and faster modes based on the expected work and budget. Keep Daybreak Blue outside general campus roles; consider a separately approved security role only where eligible.

A model being listed or enabled in the demo does not establish access for every Edu workspace or every product. In particular, 6.1 Sol and 6 Luna are Work and Codex options, not regular Chat defaults. Use **Models → Test** to check model access for the intended member. See [current model availability](https://help.openai.com/en/articles/11165333-chatgpt-enterprise-and-edu-models-and-limits).

### Defaults by product

| Console control          | Core and Plus                               | Advanced                                                 | Power                                                        | TEST                        |
| ------------------------ | ------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------ | --------------------------- |
| Chat → Model             | 5.6 Sol, or the current approved Chat model | Approved Chat model                                      | Approved Chat model                                          | Match the role being tested |
| Chat → Effort            | Instant                                     | Medium for reasoning-heavy work                          | Medium                                                       | Match the role being tested |
| Chat → New chats         | Admin default                               | Admin default                                            | Admin default                                                | Match the role being tested |
| Work & Codex → Model     | 6 Luna; 5.6 Luna if needed                  | 6 Luna, with an approved Sol override for demanding work | 6.1 Sol when enabled; otherwise, an available approved model | Match the role being tested |
| Work & Codex → Effort    | Medium                                      | Medium                                                   | Medium                                                       | Match the role being tested |
| Work & Codex → Speed     | Standard                                    | Standard                                                 | Standard                                                     | Match the role being tested |
| Work & Codex → New chats | Admin default                               | Admin default                                            | Admin default                                                | Match the role being tested |

A starting default does not grant model access. **Allow medium/high/extra high effort** and **Allow Pro models** apply to Chat; **Allow fast mode** and **Allow Ultra Fast mode** apply to Work & Codex. Members can select other permitted options. Review role overrides for each product separately.

## Set usage limits independently

Use **Billing → Usage limits** to configure member limits through workspace defaults, group defaults, and user overrides. Review the shared credit pool and workspace overage limit separately in **Billing**. The amounts below illustrate credit-based limits; approve them based on your institution's agreement, purchased credits, expected activity, and the displayed limit period.

| Usage group | Illustrative monthly limit per member | Budget owner          |
| ----------- | ------------------------------------- | --------------------- |
| Core        | 1,000 credits                         | Teaching and learning |
| Plus        | 2,500 credits                         | Academic technology   |
| Advanced    | 5,000 credits                         | Research office       |
| Power       | 10,000 credits                        | IT or engineering     |
| TEST        | 5,000 credits                         | Implementation lead   |

A group's usage limit does not create a permission role or grant features. Use corresponding groups when membership matches, and separate groups when access and budget needs differ. Set the fallback for unassigned users to the intended campus baseline.

For credit-based agreements, keep workspace overages at **0** unless additional spending is approved. User overrides take precedence over group limits; otherwise, the highest applicable group limit takes precedence over the workspace default. Alerts notify recipients but do not stop usage. Running work can settle after a limit is reached. See [Usage limits and overages](https://help.openai.com/en/articles/20001001-manage-usage-limits-and-overages-in-chatgpt-enterprise-and-edu).

Use the [current rate card](https://help.openai.com/en/articles/11481834-chatgpt-rate-card-business-enterpriseedu-credit-based-pricing) for included allowances and chargeable usage.

## Use the Admin plugin to prepare and check changes

The Admin plugin can review roles and permissions and, after confirmation, assign an existing role to an existing group. It cannot create roles or edit their permissions. Configure the roles and permissions in Admin Console first. See [Admin plugin scope](https://learn.chatgpt.com/docs/enterprise/admin-plugin).

Attach your institution's approved matrix, resolve every Review item, and replace the placeholders below.

### Compare the workspace with the matrix

**Prompt:**

```text
Use the Admin plugin to compare workspace {workspace_id} with the attached Core, Plus, Advanced, Power, and TEST matrix. Show role IDs and a table of current versus recommended permissions. Flag missing roles, unresolved decisions, and anything you cannot inspect. Prepare a manual Admin Console change checklist. Do not make changes.
```

### Assign a configured role to a group

**Prompt:**

```text
In workspace {workspace_id}, prepare to assign existing role {role_id} to existing group {group_id}. Show current assignments, the access this adds, and the recorded approver. Wait for my explicit approval. Then make only that assignment and re-read the group to verify it.
```

### Verify assignments and overlaps

**Prompt:**

```text
Review user {user_id} in workspace {workspace_id} against the attached approved matrix. Show direct and group-based roles, overlapping grants, and unexpected access. Mark unsupported checks as unknown. Do not claim that role access verifies a specific connected app. Do not make changes.
```

## Configure and verify

1. In **Identity & access → Groups & roles → Roles**, select **Add role**. Enter a role name and description, then select **Create role**. Create only the roles your institution needs.
2. In **Policy & security → Permissions → Workspace default**, apply the Core baseline. In **Roles**, open each role and apply the approved matrix values. Select **Save changes**.
3. In **Groups & roles → Roles**, open the role. Use **Role groups → Add group** to assign the intended groups. Manage SCIM-synchronized membership in the identity provider.
4. Configure **Models → Workspace default** and **Models → Roles**, then set usage limits. Approve individual plugins, apps, skills, and source-system access separately.
5. Use **Permissions → Permissions by roles** to compare assignments and **Test** to inspect effective access. Allow up to five minutes for permission updates. Use **Models → Test** to check model access.
6. Verify actual workflows with representative members, including someone with overlapping roles. Use the **TEST** custom role to exercise allowed actions and attempt intentionally blocked actions, then remove temporary grants.

The comparison view can retain older labels that differ from the editable permission page. Configure shared cloud-computer access in **Workspace capabilities → Let agents use cloud computers** using **Use a browser**, **Allow network access**, and **Allow computer use**.

| Check                                                                                                       | Expected result                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Core member uses Chat, deep research, images, Work, and Codex                                               | Approved, entitled tools are available; the expected limits apply.                                                                   |
| Plus, Advanced, or Power member uses an approved exception                                                  | Only the intended additional capabilities and models are available.                                                                  |
| Member without publishing or administration responsibilities attempts a publishing or administration action | The action remains unavailable after considering every assigned role.                                                                |
| Member has both Core and an additional responsibility role                                                  | Access reflects the combined grants and the intended exception.                                                                      |
| Work or dots task uses a cloud computer or connected device                                                 | Only the approved browser, network, computer-use, and local-access capabilities work.                                                |
| A plugin or agent connects to a source system                                                               | The plugin or agent uses the intended account and approved data, performs approved actions, and cannot access unrelated source data. |
| A member starts Chat and Work/Codex                                                                         | Starting model, effort, speed, and available alternatives match the intended product settings.                                       |
| A course, project, or temporary test ends                                                                   | Group membership and direct grants are removed; access and budget match the new responsibilities.                                    |

Review roles each term and whenever a new permission appears. Where **Admin preview** is offered, decide preview access and launch access separately. General workspace settings, identity policies, Agent security, app actions, and retention remain separate from these role matrices.
