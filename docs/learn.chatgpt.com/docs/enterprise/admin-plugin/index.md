---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/admin-plugin'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.151.0", "0.152.0", "0.152.1", "0.153.0"]
codex_cli_versions_raw: ["codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0"]
---

# Using the Admin plugin in ChatGPT Work

Source: https://learn.chatgpt.com/docs/enterprise/admin-plugin

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use this guide to understand how the Admin plugin supports common administration work, prepare for a task, and try prompts for key use cases with the right approvals and context.

[Watch: Admin plugin in ChatGPT Work](https://www.youtube.com/watch?v=29SyCndnMZs)

## 1. Understand what the Admin plugin is for

The Admin plugin is designed to help manage settings, permissions, and controls directly inside ChatGPT Work. You describe the goal in everyday language, and the plugin gathers the right inputs, reads the current state, explains what it finds, and guides the next supported step.

### What the Admin plugin is designed to solve

- Turn an admin request into a clear workflow without requiring you to write an API request.
- Review the current workspace state before making a decision or approving a change.
- Show which authorized sources and fields support the answer, along with anything it could not verify.
- Pause for review before a supported change, then read the record again to confirm the result.

The plugin uses selected admin APIs and approved connected data sources behind the scenes. It does not combine every admin system, expand your permissions, or make every API action available in ChatGPT. The system that owns the data still controls what the plugin can read or change.

### What admin APIs are designed to solve

An admin API gives software a structured way to request data or a supported action. Organizations can use the admin APIs to build internal processes or external tools. Common examples include scheduled reports, repeated work across many records, and connections to approved systems. These workflows usually require engineering, security, and governance review.

You do not need to build an API workflow to use this guide. The rest of the guide is centered on the Admin plugin. ChatGPT workspace administration and OpenAI API Platform administration also remain separate, with their own permissions and authentication requirements.

### Keep credentials private

Use only your organization’s approved connections and secret-storage systems. Never paste a real admin API key into ChatGPT, Codex, a document, or a source file.

## 2. Prepare to use the Admin plugin

Use the Admin plugin for a supported, one-time task when you want to work through the request in everyday language. Describe the goal and provide the stable IDs or approved reporting context. The plugin shows what it found or what it plans to change before you decide whether to continue.

The plugin uses only the sources, credentials, and actions authorized for that task. It does not combine every admin system or give you broader permissions. The original system remains the source of truth.

### Before you begin

1. Find the admin area where the records live.
2. Gather the required inputs and approval.
3. Start with a read-only request.
4. Ask the plugin which sources and fields it used, and what it could not verify.
5. For a supported change, review the plan before you approve it. Then ask the plugin to read the record again and confirm the result.

Confirm that the plugin is available in your workspace and that you have the required permissions. The role and access use cases below reflect the plugin’s current documented scope. The plugin can review roles, feature permissions, and user or group assignments. After you confirm, it can also assign an existing role to an existing group.

The plugin cannot create roles, change a role’s permissions, or confirm access to a specific connector.

The analytics use cases need access to connected, approved data sources. ROI analysis also needs approved business or engineering results; usage records alone are not enough.

## 3. Explore key Admin plugin use cases

Pick a use case, replace each placeholder with a value from your approved request, and follow the steps in order. Start with a read-only request unless the task is a supported change that already has approval.

### List workspace roles

**Prompt to try**

```text
List the roles in workspace {workspace_id}. Separate built-in and custom roles. For each role, explain which features it can use and show the users or groups assigned to it. Don’t make changes.
```

**Steps**

1. **Gather:** Confirm the workspace ID and that you are allowed to view this information.
2. **Run:** Ask for the read-only role list.
3. **Review:** Check the role types, feature access, and assignments.
4. **Verify:** Look into anything unexpected without making changes.

### Review one role

**Prompt to try**

```text
Review role {role_id}. Explain its permissions in plain language, show who has it, and flag anything that looks broader than expected. Don’t edit the role.
```

**Steps**

1. **Gather:** Confirm the role ID and workspace.
2. **Run:** Request the read-only role review.
3. **Review:** Check that the permissions and assignments match what the role is supposed to do.
4. **Verify:** Write down any questions for the role owner. Remember, the plugin cannot create the role or edit its permissions.

### Understand a user’s or group’s access

**Prompt to try**

```text
Help me understand the access for user {user_id} or group {group_id}. Show their assigned roles, explain what access those roles provide, and point out overlaps or gaps. Clearly say what you can’t verify.
```

**Steps**

1. **Gather:** Use the stable ID for the user or group.
2. **Run:** Ask the plugin to explain the access.
3. **Review:** Check which roles are assigned and what access they provide. Note any overlaps or gaps.
4. **Verify:** If the plugin cannot see something, mark it as unknown instead of guessing.

### Assign an existing role to a group

**Prompt to try**

```text
Before making a change, show the current roles for group {group_id} and explain what role {role_id} would add. Confirm the recorded approver and wait for my explicit approval. After the assignment, verify the group’s updated roles.
```

**Steps**

1. **Gather:** Confirm the group and role IDs. Check the approved request and recorded approver.
2. **Run:** Ask the plugin to show the current roles and what would change.
3. **Review:** Approve only if the plan matches the approved request.
4. **Verify:** After the assignment, check the group again to confirm that the existing role was added as approved.

### Check general connector permission

**Prompt to try**

```text
Check whether user {user_id} has general connector access through their assigned roles. Ask the plugin to show which permissions support its answer. If it can’t verify access to a specific connector, have it say so clearly.
```

**Steps**

1. **Gather:** Confirm the user ID and your permission to review the user’s access.
2. **Run:** Request the general permission check.
3. **Review:** Check the assigned role and the permission used for the answer.
4. **Verify:** Use this only as a general check. It does not prove access to a specific connector or connected item.

### Troubleshoot an approved change

**Prompt to try**

```text
Review approved change {change_record_id}. Compare the requested result with the current workspace. If it failed, check the workspace and role first. Then confirm who owns the record, explain the issue, and suggest the safest next step.
```

**Steps**

1. **Gather:** Confirm the approved change record and intended result.
2. **Run:** Ask the plugin to compare the request with the current workspace.
3. **Review:** Check the workspace and role. Next, verify the record owner.
4. **Verify:** Use the current workspace state as the source of truth before choosing the next step.

### Optimize cost and model mix

**Prompt to try**

```text
For {date_range} in workspace {workspace_id}, group verified token use and cost by use case. Compare models and reasoning modes using the speed and quality information available. Flag costly workflows when the data shows little evidence of value. Recommend where spending could be reduced or redirected toward work with stronger productivity or cost results. Include any approved revenue or quality signals. Estimate possible savings, explain tradeoffs, and separate verified observations from assumptions or missing inputs. Keep this read-only.
```

**Steps**

1. **Gather:** Confirm the workspace, date range, and that cost data covers the full period. Check which approved performance or outcome fields are available.
2. **Run:** Ask for the cost and model comparison.
3. **Review:** Separate what the data shows from assumptions, missing inputs, and tradeoffs.
4. **Verify:** Check possible savings with Finance and the workflow owners before acting.

### Discover usage and adoption

**Prompt to try**

```text
Analyze workspace {workspace_id} during {date_range}. Show tasks and token use by team and business function. Group cost by use case. Summarize what teams use ChatGPT and Codex to accomplish. Include examples from Legal, Marketing, and Sales. Compare available use of skills and plugins. Only report tool calls, connected apps, and multi-tool workflows if those fields are available. Show where teams use more advanced workflows and where there may be room to expand. Rank the top {5_or_10} use cases and show whether a small group of highly active users accounts for most usage. Don’t guess about activity that is not in the data.
```

**Steps**

1. **Gather:** Check the workspace, date range, and team mappings. Make sure user-level reporting is approved.
2. **Run:** Ask for the usage and adoption analysis.
3. **Review:** Check which requested fields are available. Leave missing activity out rather than guessing.
4. **Verify:** High usage does not prove advanced use, business value, or individual performance.

### Measure business value and ROI

**Prompt to try**

```text
For workspace {workspace_id} in {date_range}, combine verified usage and cost with approved outcomes. Estimate value by team and use case. Include approved Sales measures for productivity, revenue, and quality. Compare teams and models, as well as workflows and user segments. Rank returns against cost. Show the sources and formula. Clearly state assumptions, limits, and missing inputs. Don’t claim ChatGPT caused the outcomes. Keep this read-only.
```

**Steps**

1. **Gather:** Check the workspace and date range, then confirm the approved outcomes. Review the formula and privacy rules.
2. **Run:** Ask for the ROI analysis.
3. **Review:** Check every source and assumption. Note each limit or missing input.
4. **Verify:** Usage alone cannot prove ROI or causation. Review the result with Finance and business owners.

### Assess Codex ROI

**Prompt to try**

```text
For workspace {workspace_id}, combine verified Codex usage and cost from {date_range} with approved engineering outcomes. Estimate ROI by team, repository, and workflow. Compare productivity and delivery speed with code quality and engineering cost. Identify workflows that show high value or use many resources. Recommend changes to the model, reasoning mode, or workflow. Explain the tradeoffs and uncertainty. Present the findings as patterns in the available data, not proof that Codex caused the outcome. Return findings only; do not make changes.
```

**Steps**

1. **Gather:** Confirm the workspace and reporting period. Review the team and repository mappings and the approved baseline data.
2. **Run:** Ask for the Codex ROI analysis.
3. **Review:** Distinguish observed patterns from assumptions. Protect user and repository data.
4. **Verify:** Review recommendations and outcome baselines with Engineering.

## 4. When an API workflow may make sense

Some organizations build their own admin processes or external tools with the APIs. This approach can support scheduled or continuous work. It can also help when a process spans many records or needs to connect to an approved internal system. This is separate from the guided Admin plugin experience.

Start with a defined admin task: identify the required inputs and permissions, review points, expected result, and how the outcome will be recorded. If your organization automates it, involve the appropriate engineering, security, and governance teams; keep credentials in approved secret storage; and test the workflow before deployment.

### Related resources

- [ChatGPT workspace Admin API reference](https://chatgpt.com/public/admin/api-reference)
- [Administration boundaries](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions#understand-the-control-boundaries)
- [ChatGPT workspace Analytics API](https://learn.chatgpt.com/docs/enterprise/analytics-api)
- [ChatGPT workspace Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api)
