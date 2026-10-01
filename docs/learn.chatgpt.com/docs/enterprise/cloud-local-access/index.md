---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/cloud-local-access'
source_kind: 'learn_markdown'
---

# Local computer access for Work Cloud and dots

Source: https://learn.chatgpt.com/docs/enterprise/cloud-local-access

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Work and dots can use permitted files and tools on a connected computer while OpenAI’s cloud coordinates the task. Enable local computer access separately for each feature.

Start with the shared policy, compatibility, and audit guidance below, then follow the Work or dots setup and end-user guidance for the feature you plan to enable.

This guide helps enterprise workspace owners review policy requirements and enable local computer access for Work and dots. Availability depends on your workspace and rollout.

See [Agent Security](https://learn.chatgpt.com/docs/enterprise/agent-security) for the Global baseline, environment overrides, and orchestrator and executor field lists.

## Benefits of local computer access

Enabling local computer access in these features helps teams continue work across devices. Admins can centrally manage supported requirements in Agent Security for execution on a local computer. These execution requirements do not apply when Work uses a cloud container or a dot uses a cloud computer. Cloud execution uses separate controls for browser access, network access, and computer use.

### Work

- **Continue one Work conversation across devices.** Start on a computer, then review results or give follow-up instructions from the web or mobile app. Tasks using local computer access with Work Cloud use cloud coordination.

- **Use approved resources on your computer.** A task using this feature can use permitted local files and tools through a connected computer while you follow along from another device. Keep that computer online and connected for steps that need it.

- **Manage local execution requirements centrally.** Set supported enterprise requirements in Agent Security for local execution. Review Work Cloud policies separately for cloud execution.

### Dots

- **Do engineering work locally.** Investigate bugs, implement changes, and run builds using permitted local repositories, developer tools, and skills.

- **Coordinate coding work.** Create local Work or Codex threads and control existing local Codex threads.

- **Use desktop apps and the local browser for supported tasks**, including tasks that require a local sign-in when the cloud browser cannot complete them.

## Before and after enabling local computer access with Work Cloud

A task has two parts: coordination and execution. Coordination decides which steps to take and keeps the conversation moving. Execution is the work performed by a tool, such as running a shell command. This feature moves coordination into OpenAI’s cloud. It does not move every tool or file off the computer.

| **Area**                                                           | **Before you enable this feature**                                                     | **After you enable this feature**                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Continuing a local Work conversation                               | Members choose a local or cloud Work thread, where available.                          | When members select Cloud, eligible new conversations use cloud coordination and can continue across devices. When members select Local, both coordination and execution continue to happen locally. For enterprises, the in-app Local/Cloud toggle and its default remain unchanged at launch. |
| Task coordination                                                  | The existing local or cloud workflow applies.                                          | OpenAI’s cloud coordinates the Work task.                                                                                                                                                                                                                                                       |
| Steps that need the user’s computer                                | Local Work can use the computer’s tools and files. Cloud Work cannot use the computer. | The computer still provides those tools and files and must be online and connected.                                                                                                                                                                                                             |
| [Enterprise requirements](https://learn.chatgpt.com/docs/enterprise/managed-configuration) | Existing local requirements and precedence apply to local Work.                        | Local execution requirements govern the connected computer. Supported Global policy applies to cloud orchestration when managed policy is enabled; Work cloud containers use their own execution configuration and requirements.                                                                |
| Local execution controls                                           | Supported device and operating-system controls apply.                                  | For local execution, MDM and legacy managed-device requirements rank above Agent Security. The system requirements file ranks below it.                                                                                                                                                         |
| Codex                                                              | Existing Codex behavior applies.                                                       | Codex behavior and conversation history remain separate.                                                                                                                                                                                                                                        |

## How to set up local computer access

### Review your policy in Agent Security

#### Where to review

Open Admin Console → Agent Security. It replaces Policies & Configuration. Its rollout is independent of local computer access for Work and dots.

- **Policy settings:** Review the Global baseline and any Local overrides. Keep orchestrator controls, including approvals and web search, in Global; environments cannot override them. Use the dedicated UI controls where available, including **Allowed approval policies** and **Allowed web search modes**, and TOML for other supported fields. See [orchestrator and executor controls](https://learn.chatgpt.com/docs/enterprise/agent-security#choose-controls-and-configuration-fields) for where each setting applies.

- **Requirements and Defaults:** Requirements set limits users cannot override. Defaults provide starting values within those limits and cannot override a requirement.

- **Feature access:** Use Workspace settings → Permissions & roles. Local computer access is a separate opt-in for Work and for dots.

#### What carries over

When eligible legacy cloud policies migrate, their settings carry over into Global, preserving policy assignments and ordering. Review the migrated policies in Agent Security and use the table below to check your current setup. If you automate policy updates, also review the final row. See [Agent Security](https://learn.chatgpt.com/docs/enterprise/agent-security) for migration guidance.

| **Your current setup**              | **What to do before enabling this feature**                                                                                                                                                                                                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Existing cloud policies             | Compare the migrated Global baseline with your organization’s required controls. Record the settings, then test that allowed actions succeed and restricted actions are blocked.                                                                                                                |
| Policies delivered only through MDM | MDM delivers policy to devices. Configure supported enterprise requirements for local execution in Agent Security before enabling this feature. For local execution, MDM and legacy managed-device requirements still rank above Agent Security.                                                |
| Terraform or policy-update scripts  | Use the policy API to manage Global settings. To manage Local or Codex Cloud settings, use the Agent Security UI. Existing Global API workflows remain available after migration. Test your scripts and Terraform integrations, and confirm that policy assignments and ordering are unchanged. |

#### Which policy takes precedence

These rules apply at different levels. Each arrow below runs from highest to lowest priority.

- **Across policies:** A higher-priority policy wins over a lower-priority policy, even when the lower-priority policy is more specific.

- **Within one policy:** For supported execution settings, environment override → Global. An environment without an override inherits the applicable Global setting.

- **Local requirements:** macOS MDM requirements → legacy `managed_config.toml` fields interpreted as requirements → Agent Security cloud-managed requirements → system `requirements.toml`. The MDM layer applies on macOS; defaults follow separate configuration rules.

Some requirements have field-specific merge rules. See [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) and the [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) for policy scope, supported fields, and execution scope.

#### How policy applies to Work and dots

Shared behavior for Work and dots with local access spans the following scopes:

- **Task coordination:** When managed policy is enabled, the cloud service coordinating the task enforces supported requirements from Global in Agent Security, such as approval requirements and allowed web-search modes.

- **Local execution:** When a tool runs on a connected computer, it enforces supported local-execution requirements from Agent Security and applicable device policies, including policies delivered through MDM where supported. These can include filesystem and network restrictions. Only fields supported by the local executor apply; configuring a field in MDM or local `requirements.toml` does not guarantee that it is enforced locally.

- **Cloud execution:** Work cloud containers and dots’ cloud computers use separate execution controls. Local filesystem and network restrictions do not automatically apply to these cloud environments.

To configure shared cloud capabilities, go to Admin Console → Permissions & roles → Workspace capabilities → Cloud computer capabilities. These permissions cover both Work Cloud and dots. Review **Cloud browser use** and **Cloud network access** separately; configuring one does not configure the other. Global policies and Codex Cloud overrides do not configure these permissions.

### Check compatibility and data requirements

Review eligibility, data coverage, and the controls your organization relies on before enabling either feature. Shared infrastructure does not mean Work and dots have identical support.

#### Review Work and dots eligibility

- **Work:** Residency applies only to eligible content and supported workloads, regions, and configurations. EKM covers supported stored content in eligible workspaces. Confirm coverage for your workflow rather than assuming every local-access step or connected integration is covered. Work is not supported with UAE inference residency. See [Data residency and inference residency](https://help.openai.com/en/articles/9903489-data-residency-and-inference-residency-for-chatgpt) and [Work cloud security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security#data-handling-and-retention).

- **Dots residency:** During the Enterprise beta, dots do not support data residency or inference residency. Eligible workspaces can opt in after acknowledging those limitations; enabling dots does not make their data or processing residency-compliant.

- **Dots exclusions:** Dots are unavailable for FedRAMP workspaces, workspaces with EKM, and workspaces with inference residency set to AE (UAE). HIPAA workspaces can participate if they meet the other eligibility requirements.

#### Check data handling and the local-access safeguard

- **Cloud processing:** Work with local access and dots still use cloud coordination. Conversations, tool results, and other task context do not stay exclusively on the connected computer.

- **Residency safeguard:** If any cloud policy enables `enforce_residency`, **Allow local computer access** is unavailable for both Work and dots. This safeguard does not set workspace residency or, by itself, disable Work Cloud or dots. Eligible workspaces can still opt in to dots after acknowledging the beta residency limitations; local access remains blocked.

- **Retention and access to data:** Neither experience provides strict zero data retention. API Zero Data Retention is a separate API control. “Eyes-off” commitments and abuse-monitoring controls are also distinct from zero retention. If a workflow requires no retained data, do not enable it for these experiences.

Review retention, deletion, and audit coverage for the actual data and tools involved before rollout. For Work, conversations, hosted execution state, files, and connected-app data can follow different lifecycles; deleting a conversation does not remove every related copy.

#### Check hooks and network compatibility

- **Supported enterprise hooks:** When managed policy and remote hooks are enabled, Work Cloud with local access and dots use admin-managed remote MCP hooks. The cloud orchestrator calls your connected MCP service at supported task and tool events. Configure `mcp_tool` handlers in Global `requirements.toml`. Work Cloud without local access does not use these hooks; these enterprise hooks are not available for personal accounts.

- **Work Cloud and dots with local access:** Command/shell, prompt, and agent handlers; hooks from local configuration, plugins, or local directories; environment-scoped hooks; and `SessionEnd` MCP hooks are not supported with cloud orchestration, even when the task executes tools on your computer. If your workflow depends on one of these hooks, continue using a local-only workflow that supports it until you have reviewed an alternative.

- **Local-only threads in Work and Codex:** When both orchestration and execution are local, existing supported hooks continue to work. Admins can still configure supported managed hooks in Agent Security for this workflow.

- **Failure and audit coverage:** Test callback connectivity, required events, and failure behavior. An explicit supported denial can block an action, but a `PreToolUse` callback error, timeout, or malformed response can fail the hook without blocking the tool. Hooks do not provide a complete [Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api#audit-records-for-local-computer-access-with-work-cloud) audit trail or cover every internal subagent path.

- **Network and app controls:** Verify the field, delivery path, and execution surface in the [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference). App- or device-enforced controls may still apply when the cloud orchestrator does not consume a setting. Managed HTTP/SOCKS listener ports and non-loopback proxy listeners are unsupported by the cloud runtime; socket-rule support depends on the execution path. Review [Network policy precedence and runtime limits](https://learn.chatgpt.com/docs/enterprise/managed-configuration#network-policy-precedence-and-runtime-limits), then test allowed and blocked actions and required connectivity.

For questions about local files, cloud execution, or policy precedence, see the [Work admin FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq), [Work local security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-local-security), and [Work cloud security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security).

### Enable local computer access

Grant local computer access separately for Work and dots. Use workspace defaults and supported custom roles to grant access to the intended users or groups.

Before rollout, review the policies and compatibility requirements above. Reviewing or creating policies in Agent Security is recommended, but the confirmation flow does not require you to create policies before enabling access. Policy migration does not grant local computer access.

#### Work

1. As a workspace owner, open **Workspace settings > Permissions & roles**.

1. Enable **Work Cloud** for the intended users. **Use Codex locally on the ChatGPT desktop app** is not a prerequisite for this feature.

1. Under **Work Cloud**, turn on **Allow local computer access**. Review the confirmation modal, then open **Agent Security** to review or set policies, or confirm to turn on access.

1. Have users update to ChatGPT desktop app version 26.929 or higher. The update is required for local computer access with **Work Cloud** to take effect.

1. Have a member with the intended permissions select **Cloud** in the desktop composer and start a new task. Continue the task from another supported device and verify access to an approved local file or tool while the computer is connected.

#### Dots

1. As a workspace owner, open **Workspace settings > Permissions & roles** and enable dots for the intended users, subject to the eligibility requirements above.

1. Under **Use Dots**, turn on **Allow local computer access**. Review the confirmation modal, then open **Agent Security** to review or set policies, or confirm to turn on access.

1. Have users update to ChatGPT desktop app version 26.929 or higher. The update is required for local computer access to take effect.

1. Have users open their dot’s details in the ChatGPT desktop app and choose **Computers**. Find **Your computer** (or the computer’s name), select **Allow**, then confirm with **Allow access**.

1. Have a member with the intended permissions and a connected computer test a local task with their dot.

### Review OpenTelemetry and audit coverage

For Work with local access and dots, distinguish local execution telemetry from cloud audit records when reviewing OpenTelemetry (OTel) coverage. Your local executor can still export supported execution events. Cloud orchestration events do not reach your existing OpenTelemetry collector.

Use the [Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api#audit-records-for-local-computer-access-with-work-cloud) for supported cloud records. Changing the collector endpoint does not restore cloud orchestration events. Compliance API records do not replace every event in the earlier OpenTelemetry stream.

For dots, use the [Analytics API](https://learn.chatgpt.com/docs/enterprise/analytics-api) for usage and the [Compliance API](https://learn.chatgpt.com/docs/enterprise/compliance-api) for supported audit records. Validate the records your workflow needs alongside local collector delivery; MCP hooks are not a substitute for audit coverage.

See [Work cloud security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security#audit-and-compliance-visibility) for cloud audit coverage.

## End-user experience

For both Work and dots, local steps require the relevant computer to be online and connected, with the ChatGPT desktop app running and signed in to the appropriate account and workspace.

### Work

- **Eligible tasks.** Eligible new tasks started in the ChatGPT desktop app with **Cloud** selected can use that computer’s local executor while it is connected and local access is enabled.

- **Sign-in.** Use Sign in with ChatGPT in the intended workspace. API keys and Codex access tokens do not enable local computer access with Work Cloud.

- **Computer unavailable.** If the computer is unavailable when a new turn begins, an existing eligible task can continue in a cloud container without that computer’s local files or tools. The container does not enforce enterprise requirements from local execution. A task cannot switch from local execution to the cloud during a turn.

- **Access turned off.** Turning off local computer access with Work Cloud interrupts currently running turns. Users can start a new turn in an existing cloud conversation; it uses Work Cloud without access to local files.

- **Existing chats and projects.** Tasks created before this feature is enabled keep their original mode: locally only, or in the cloud without local file access. Start a new task after enabling the feature to use local computer access with Work Cloud.

- **Local/Cloud setting.** For enterprises, the in-app Local/Cloud toggle and its default remain unchanged at launch. Eligible tasks with **Cloud** selected use cloud coordination and the connected computer for local steps.

### Dots

- **Connect a computer.** Open the dot’s details in the ChatGPT desktop app, then choose Computers. Find Your computer (or the computer’s name), select **Allow**, then confirm with Allow access. The computer becomes available for supported local tasks.

- **Computer offline.** The saved access grant remains, but work requiring that computer cannot proceed while it is unavailable. Offline does not mean access has been revoked.

- **Remove access.** Choose Revoke access and confirm to remove the dot’s grant for that computer. Disconnected means access has been removed; it is different from Offline.

- **Admin access changes.** If an admin disables local computer access for dots, an already authorized local task may still be finishing. Do not assume the Work behavior of immediately interrupting running turns applies to dots.

- **Running tasks.** A running local task does not automatically migrate to the cloud. Connection changes may interrupt work or reload the runtime. The dot may continue subsequent work on its cloud computer, but a local child task that no longer has access cannot resume on that computer and is not automatically moved to the cloud.
