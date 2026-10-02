---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# ChatGPT Work cloud security

Source: https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

ChatGPT Work is part of your existing ChatGPT workspace and follows its
applicable privacy, security, and data-handling policies. For Business,
Enterprise, and Edu workspaces, existing protections include encryption in
transit and at rest, and OpenAI doesn't use business data to train its models by
default.

For an overview of the security controls, see the [ChatGPT Work enterprise security whitepaper](https://cdn.openai.com/pdf/chatgpt-work-enterprise-security.pdf).

Work Cloud also introduces hosted task execution and optional tools that can
access connected systems or take authorized actions. Review the permissions,
retention settings, and available audit records for the capabilities your
organization enables.

Capabilities and controls depend on the workspace plan, rollout, configuration,
and connected integration. For the broader execution model, see the
[ChatGPT Work Overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview).

## Security at a glance

- Cloud execution runs on OpenAI-managed infrastructure. A task using Local computer access with Work Cloud can also use approved local tools through a connected computer.

- The cloud environment does not automatically inherit local files, applications, browser sessions, or private-network access.

- Connected apps use the permissions of the authorized account, which can be an individual, shared, or agent-owned account.

- Workspace and feature-specific controls govern Work access, local execution, cloud browsing, connected apps, and code or shell networking.

- Business, Enterprise, and Edu workspace data is encrypted in transit and at rest and is not used to train OpenAI models by default.

- Retention and audit visibility depend on the data category, storage location, event, and product configuration.

## Where cloud tasks run

For new tasks created after you enable Local computer access with Work Cloud, OpenAI's cloud coordinates the task while individual steps can execute in the cloud or on an approved, connected computer. This feature applies only to tasks created after you enable sync. Existing tasks, including tasks in projects, keep their original mode: locally only, or in the cloud without access to local files. Start a new task to use this feature.

If the computer is unavailable when a new turn starts, an existing eligible task using local computer access with Work Cloud can continue in a cloud container. The cloud container cannot access files or tools on the unavailable computer. It also does not enforce enterprise requirements from local execution. A task cannot switch from local execution to the cloud during a turn.

A step that needs a computer's local files or tools requires that computer to be online and connected. Workspace permissions, supported policy, and the user's existing access continue to apply.

The user's device sits within the organization's own IT-managed trust boundary, outside OpenAI-operated systems. Cloud execution remains in the OpenAI-managed environment. A synced task can separately use approved local tools through a connected computer, subject to its permissions.

Work Cloud uses the Codex task-execution harness. Work and Codex share core execution and isolation mechanisms, but their available tools, permissions, and administrative controls aren't identical. The customer controls workspace access, approved connections, and information intentionally supplied to a task. OpenAI manages the hosted execution environment.

Work Cloud runs on shared, OpenAI-managed infrastructure. In the current supported execution path, tasks run in VM-backed sandboxes, with execution state associated with the authenticated account user in the workspace. Work can reuse an environment across tasks or replace it while preserving eligible state. This doesn't mean every task receives a new container or that each customer has a dedicated physical host. Customers don't provide, host, or manage Work Cloud containers.

## What a cloud task can access

A cloud task can use information made available through an authorized path:

- Information a person enters into a conversation.

- Files intentionally uploaded, attached from Library, or made available through a project.

- Content retrieved through an enabled app and an authorized account connection.

- Website content accessed through an enabled cloud browser or another permitted web capability, subject to applicable access controls.

The cloud execution environment does not directly inherit a computer's files, installed applications, browser session, or corporate-network access. A task using Local computer access with Work Cloud can separately call approved local tools on a connected computer. Those local calls remain subject to the controls and permissions of that computer and the systems it accesses.

An authorized connection can make information from an internal system available
through its own access path. That connection doesn't give the cloud task
unrestricted access to the employee's device or network.

## Apps, plugins, and connected accounts

An app can give Work access to information or actions in another system. A
plugin can use an app as one of its underlying tools. Making a plugin available
doesn't automatically enable the underlying app, authorize an account, or
approve every action the integration can perform.

A task that uses a connected app, directly or through a plugin, can proceed
only when:

- The workspace enables the app and any plugin that requires it.
- The person has the necessary workspace or role access.
- The connection uses an authorized individual, shared, or agent-owned
  account.
- The connected account, approved scopes, and available app action settings
  permit the requested information or operation.

For apps that support **Action control**, administrators can allow read-only
actions, all actions, or a custom set. **App permissions** control when
ChatGPT asks for confirmation to work with an app. Depending on the app and
workspace, options can include **Always ask**, **Any changes**, **Important
actions**, and **Never ask**. With **Any changes**, supported reads can proceed
without a prompt while changes require confirmation.

An authorized write can run without a prompt when the configured policy allows
it. This doesn't expand the app's allowed actions, workspace access, or the
connected account's permissions. ChatGPT can still block some high-risk
actions.

Confirm the plugin and each underlying app are available in the workspace.
Review role access, connected-account authorization, and action permissions as
distinct decisions. See
[Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors).

### Personal and shared connections

A personal connection uses the connected employee's permissions in the source
system. A shared or agent-owned connection uses the permissions of its
connected account instead. That account might access information or perform
actions that the requesting person couldn't access with a personal account.

Before enabling a shared connection, limit the account's permissions and
scopes, choose who can use it, and review the actions it can perform. See
[Workspace Agent connections and permissions](https://help.openai.com/en/articles/20001143-chatgpt-workspace-agents-for-enterprise-and-business).

Content retrieved from a connected app isn't automatically saved as a Library
file. If the content is later saved to a conversation, project, Library, or
synced index, that copy follows the rules for its saved location.

## Cloud browser and network access

The cloud browser, web search, connected apps, and code or shell networking are
separate capabilities. Restricting one doesn't automatically disable the
others.

### Cloud browser

The cloud browser is a hosted tool a Work task can use to interact with
websites. Opening ChatGPT in a web browser or desktop app doesn't enable cloud
browsing; a cloud task can run without it.

The hosted browser doesn't inherit the user's local browser profile, open tabs,
existing sign-ins, saved passwords, password manager, or browsing history.
Where supported, users can sign in separately through a secure hosted sign-in
flow. This doesn't grant access to their local browser session.

Supported website interactions can include public forms and can combine
information from an authorized app with a website task. Where available,
website permissions include **Always ask**, **Auto approve**, and **Always
allow**. **Auto approve** applies automated risk checks; **Always allow**
removes the interactive website-access review. Neither grants new app
permissions or approves every action on a website. Consequential actions can
still require separate confirmation.

Configure **Cloud browser use** and **Cloud network access** under **Admin Console > Permissions & roles > Workspace capabilities > Cloud computer capabilities**. These shared capabilities are available to Work Cloud and dots and can be configured independently of Work Cloud access. A Work task still needs Work access and permission to use each capability it requires. Review browser access and code or shell network access separately. Disabling one does not automatically disable the other.

For a Work task to use the cloud browser in an Enterprise workspace,
administrators must enable both Work access and cloud browser access. See
[Using cloud browser in ChatGPT](https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt).

Also review **Cloud computer use** under **Workspace capabilities > Cloud computer capabilities**. This control also applies to ChatGPT Work. **Use password manager** is a separate permission directly under **Workspace capabilities**, outside the **Cloud computer capabilities** group. It governs password-manager access in the local in-app browser and cloud browser.

### Code and shell networking

Public internet access for code or shell execution follows its own network
policy. When public internet access is off, network destinations required for
ChatGPT Work can remain reachable through a managed destination allowlist.

The allowlist governs network destinations, not shell commands. Disabling
public internet access for code or shell execution doesn't, by itself, disable
the cloud browser, web search, or connected apps. Changes to the network
setting apply after the current code run or shell command finishes and the
execution environment refreshes.

See [Code and shell sandboxing](https://learn.chatgpt.com/docs/sandboxing?surface=web).

## Data handling and retention

A conversation using Local computer access with Work Cloud uses cloud coordination even when a tool runs on a connected computer. Review the data sent to the orchestrating service separately from files remaining on the device. Confirm the applicable storage, retention, residency, and audit coverage for the workflow before rollout.

Local computer access with Work Cloud does not provide strict zero data retention. Data residency and inference residency cover only eligible content and supported workloads, regions, and configurations. Enterprise Key Management (EKM) covers supported stored content in eligible workspaces. Work is not supported with UAE inference residency. If your organization requires ZDR, do not enable this feature.

Work Cloud follows the applicable ChatGPT workspace privacy and security protections. See [Enterprise privacy](https://openai.com/enterprise-privacy/).

Information associated with a cloud task doesn't follow one universal retention schedule:

| **Data category**                    | **Retention and deletion behavior**                                                                                                                                                                                                                                                       |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Work conversations                   | Follow the workspace conversation-retention settings. Deleted chats are generally scheduled for permanent deletion within 30 days, subject to published security, legal, and de-identification exceptions.                                                                                |
| Hosted execution state and snapshots | Follow a separate lifecycle from conversations and files. Access to execution state is scoped to the account user, and the workspace conversation-retention setting informs eligible stored snapshots. Ending a task or deleting a chat doesn't immediately purge every related artifact. |
| Files saved to Library               | Uploaded or generated files follow applicable Library and workspace retention rules. Deleting a conversation doesn't delete a file saved to Library.                                                                                                                                      |
| Project files                        | Remain associated with their project until removed or the project is deleted, subject to applicable deletion rules.                                                                                                                                                                       |
| Saved memories, when enabled         | Follow separate memory controls. Deleting a conversation doesn't necessarily delete an existing saved memory.                                                                                                                                                                             |
| Transient uploads                    | Eligible temporary Enterprise uploads outside Library can expire after 48 hours unless another applicable retention setting applies.                                                                                                                                                      |
| Connected-app content                | Source-system records follow that system's policies. Copies saved to a conversation, project, Library, or synced index follow the rules for their saved location.                                                                                                                         |
| Cloud browser data                   | Hosted browser data is separate from local browser data. Users can remove saved cloud browser cookies through the applicable settings.                                                                                                                                                    |
| Compliance records                   | Compliance Logs Platform records are available for 30 days. Exported copies follow the receiving system's retention policy.                                                                                                                                                               |

Deleting a conversation, removing a Library file or saved memory, disconnecting an app, and clearing hosted browser data are separate actions. Review the relevant storage location instead of assuming one action removes every copy. See [Chat and file retention policies](https://help.openai.com/en/articles/8983778-chat-and-file-retention-policies-in-chatgpt).

Retained conversation and execution context can help Work resume interrupted tasks and refer to earlier work. Consider that continuity alongside your security requirements when setting retention.

Eligible Enterprise and Edu workspaces can use Enterprise Key Management for supported stored content, including supported hosted execution snapshots when customer-managed encryption is required. Coverage varies by data category and deployment. Rotating a key doesn't delete existing data or, by itself, deny access to earlier encrypted content. Revoking or disabling key access is a separate action that can disrupt supported workflows. Neither replaces a retention or deletion policy.

Data residency and inference residency apply only to eligible content and supported workloads, subject to the organization's agreement, region, and configuration. Connected apps, external providers, and some processing or synced indexes can follow separate location rules. Verify support for the product, integration, and region. See [Data residency and inference residency](https://help.openai.com/en/articles/9903489-data-residency-and-inference-residency-for-chatgpt).

OpenAI API [Zero Data Retention](https://developers.openai.com/api/docs/guides/your-data#zero-data-retention) is an API-specific control and doesn't define retention for ChatGPT Work.

## Administrator access controls

Enable **Allow local computer access** under Work Cloud. **Use Codex locally on the ChatGPT desktop app** is not a prerequisite. If `enforce_residency` is enabled in any cloud policy, **Allow local computer access** is disabled for both Work and dots. This safeguard does not configure workspace residency or, by itself, disable Work Cloud or dots. Before enabling it, review or create the global cloud baseline in **Agent Security**.

Use the policy API to manage Global settings. To manage Local or Codex Cloud settings, use the Agent Security UI. Existing Global API workflows remain available after migration. Test your scripts and Terraform integrations, and confirm that policy assignments and ordering are unchanged.

Review each control in the context where it applies:

- **Enterprise requirements.** For Work with local access and dots, supported Global policy applies through the shared cloud orchestrator when managed policy is enabled. Applicable local `requirements.toml` requirements govern execution on a connected computer. Work cloud containers and dots cloud computers use their own execution configuration and requirements, rather than the managed environment bundle used by other executor types. Local execution restrictions do not automatically apply to these cloud computers. Review cloud capability permissions and test local and cloud execution separately.

- **Local execution.** Supported device controls still apply to steps that run on the connected computer.

- **Cloud execution policy.** Work Cloud manages its own execution environment under existing Work Cloud policies. The local environment's managed execution policy does not carry over. Desktop browser site rules do not become cloud-browser restrictions.

Keep orchestrator controls, including approvals and web search, in Global. Use the dedicated Allowed approval policies and Allowed web search modes controls where available, and TOML for other supported fields. See the [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) for the field list and execution scope.

Turning off Local computer access with Work Cloud interrupts currently running turns. Users can start a new turn in an existing cloud conversation. That turn automatically uses Work Cloud without access to local files.

Review the controls that apply to each part of a cloud task:

- **Work Cloud and Work Local:** Where independent controls are available, manage cloud and local Work as distinct controls in **Workspace settings** > **Permissions & roles**. In other workspaces, local Work can share a control with Codex Local.

- **Apps and plugins:** Choose which integrations are available and which people or roles can use them.

- **Connected-account actions:** Review account permissions, application scopes, and available action or confirmation controls.

- **Browser and networking:** Assess cloud browser access and code or shell public-network access independently.

Enable **Work Cloud** only for approved users or groups. For cloud-only Work without cross-device sync, enable Work Cloud and disable Work Local for the intended role, where separate controls are available. Cross-device sync requires both permissions. Turning either permission off and saving the change also turns off Sync. Where local Work and Codex share a control, review the effect on both before disabling local execution. These controls don't prevent an authorized person from intentionally uploading a file to a cloud task.

For supported role permissions with **Default**, **On**, and **Off** states, **Default** inherits the workspace setting, **On** grants access through that role, and **Off** does not grant access through that role. Ordinary role permissions combine additively, so another assigned role can still grant access. Lockdown Mode and product eligibility apply separately. Some Work and plugin settings use different, two-state controls. Verify effective access across all assigned roles. See [Role-based access control](https://help.openai.com/en/articles/11750701-rbac).

Where available, the **Work Cloud** permission applies across supported web, mobile, and desktop experiences. It doesn't independently select which of those surfaces can run cloud tasks. Consider device-management or other access controls if a deployment must exclude a particular surface.

## Audit and compliance visibility

For eligible Enterprise and Edu workspaces, the Compliance Logs Platform can
include supported Work prompts and responses. Connected-app calls have separate
logs, and available source-system audit records vary by integration.
Supported compliance endpoints can provide access to eligible Library files.

Coverage depends on the event and the system where it occurs. Don't assume
every shell command, browser interaction, app invocation, file operation, or
approval appears in a customer-visible compliance export.

Endpoint monitoring can observe the ChatGPT client or network traffic on managed
devices, but can't inspect actions inside the hosted execution environment. Use
supported Work, compliance, and connected-system records instead.

Review current compliance event coverage alongside workspace reporting,
connected-system audit logs, and the retention policies of systems receiving
exported records. See the
[OpenAI Compliance Platform](https://help.openai.com/en/articles/9261474-compliance-api-for-chatgpt-enterprise-edu-and-chatgpt-for-teachers).

## Verify cloud access and controls

Test cloud access with a task that reflects your team’s work. For example, a security team could
compare an approved vendor advisory with an authorized inventory and review a
draft exposure assessment before deciding what to do. If cloud browsing or
connected apps are unavailable, provide the advisory and an approved inventory
extract directly.

Enable only the access the task requires. Check connected-account permissions, retention settings, and available audit records. Tell users which results and actions require human review. For rollout planning, see the
[Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup).
