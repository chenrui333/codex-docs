---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# ChatGPT Work Overview

Source: https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

ChatGPT Work and Codex share core execution, isolation, and permission
mechanisms, and fall within the same security boundaries that are part of your
ChatGPT Business or Enterprise agreement. The capabilities and controls
available to each experience depend on whether a task runs locally or in the
cloud, its available tools, and applicable workspace policies.

ChatGPT Work can complete multi-step tasks using the files, applications, and tools available to an authorized workspace member. With sync enabled, members can continue eligible conversations across desktop, mobile, and web. For enterprises, the in-app Local/Cloud toggle and its default remain unchanged at launch. OpenAI's cloud coordinates the task, while individual steps can run in a cloud environment or on an approved, connected computer.

> **Update the desktop app.** Users must update to the latest version of the ChatGPT desktop app for Local computer access with Work Cloud to take effect after it is enabled for their workspace.

Availability and controls depend on your plan, workspace configuration, and rollout.

    {"For general usage and availability, see "}
    [{"ChatGPT Work and Codex"}](https://help.openai.com/articles/20001275)
    {" in the Help Center."}

For a focused review of hosted execution, connected-account permissions,
browser and network settings, retention, and audit visibility, see
[ChatGPT Work cloud security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security).

For device access, local browser sessions, managed policies, and local data
handling, see
[ChatGPT Work local security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-local-security).

## Execution isolation, files, and device access

The files and tools available to ChatGPT Work depend on where Work is running,
user permissions and admin configuration.

### Local Work

Local execution lets a Work task use approved resources on the computer, subject to user permissions, workspace controls, and supported device policy. When sync is enabled, cloud coordination calls on the connected computer for steps that need it. That computer must be online and connected.

Local execution does not mean that the conversation or task context stays only on the device. See [Work local security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-local-security) for data and device boundaries.

### Cloud Work

Cloud execution runs supported steps on OpenAI-managed infrastructure. If the computer is unavailable when a new turn starts, an existing eligible task using local computer access with Work Cloud can continue in a cloud container. The cloud container cannot access files or tools on the unavailable computer. It also does not enforce enterprise requirements from local execution. A task cannot switch from local execution to the cloud during a turn.

A cloud execution environment does not automatically inherit a computer's files, applications, browser sessions, or network access. A task using Local computer access with Work Cloud can separately use approved local tools through an online, connected computer. Uploads, project sources, and authorized connected apps remain distinct ways to supply information.

When [Library](https://help.openai.com/en/articles/20001052-file-storage-and-library-in-chatgpt) is available, eligible uploaded or generated files can be saved there. Review the controls available in your workspace. Users can explicitly access or attach files they are authorized to use.

See [Code and shell sandboxing](https://learn.chatgpt.com/docs/sandboxing?surface=web), [Creating and editing documents, spreadsheets, and presentations](https://help.openai.com/en/articles/20001278-creating-and-editing-documents-spreadsheets-and-presentations-with-chatgpt-work), and [File storage and Library in ChatGPT](https://help.openai.com/en/articles/20001052-library-for-chatgpt).

Local computer access with Work Cloud applies only to tasks created after you enable sync. Existing tasks, including tasks in projects, keep their original mode: locally only, or in the cloud without access to local files. Start a new task to use this feature.

<span
  id="enable-and-govern-local-computer-access"
  data-localization-body-anchor
/>

## Enable and govern Local computer access with Work Cloud

A workspace owner enables **Allow local computer access** after reviewing the required Work permissions and the cloud policy in **Agent Security**. Enable Work Cloud for the intended users. **Allow local computer access** is nested under Work Cloud. You do not need to enable **Use Codex locally on the ChatGPT desktop app**.

Review these policy boundaries before enabling sync:

- **Enterprise requirements.** For Work with local access and dots, supported Global policy applies through the shared cloud orchestrator when managed policy is enabled. Applicable local `requirements.toml` requirements govern execution on a connected computer. Work cloud containers and dots cloud computers use their own execution configuration and requirements, rather than the managed environment bundle used by other executor types. Local execution restrictions do not automatically apply to these cloud computers. Review cloud capability permissions and test local and cloud execution separately.

- **Local execution.** MDM and legacy managed-device requirements rank above Agent Security. The device's system requirements file ranks below Agent Security.

- **Enterprise hooks.** Where enabled for your workspace, Local computer access with Work Cloud supports admin-defined MCP hooks that run on the cloud coordinator (orchestrator) for supported lifecycle and tool events. Command hooks and hooks from local configuration or plugins are not supported with cloud orchestration, even when tools execute locally. When both orchestration and execution are local, existing supported hooks continue to work in local-only Work and Codex threads. Admins can still configure supported managed hooks in Agent Security for those workflows.

- **Logging and auditing.** Before relying on these hooks, test the callback connection, confirm the events it receives, and check how failures affect the task. MCP hooks do not provide a complete Compliance API audit trail.

Keep orchestrator controls, including approvals and web search, in Global. Use the dedicated Allowed approval policies and Allowed web search modes controls where available, and TOML for other supported fields. See the [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) for the field list and execution scope.

Turning off Local computer access with Work Cloud interrupts currently running turns. Users can start a new turn in an existing cloud conversation. That turn automatically uses Work Cloud without access to local files.

Local computer access with Work Cloud does not change Codex configuration behavior or combine Work history with Codex history. See [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) and the [Work admin FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq).

## Network access and external destinations

Work uses tools like code/shell execution and the cloud browser to complete
tasks. Each of these tools has configurable permissions.

- **Code and shell commands**: Public internet access depends on the applicable
  workspace policy and individual Work network setting. When public internet
  access isn't allowed, commands can still reach OpenAI-approved destinations
  required for Work to function. This controls network destinations, not which
  commands can run.
- **Web search**: Search has controls separate from the Work code and shell
  network setting.

When available, the individual code and shell setting appears under
**Settings** > **Data controls** > **Work network access**. Turning on **Allow
public internet access** doesn't override an applicable administrator
restriction. Turning it off limits code and shell commands to required
destinations on the managed allowlist; it doesn't disable connected apps, web
search, or the cloud browser.

Changes to the code and shell network setting take effect after the current run
finishes and Work refreshes its execution environment. See
[Code and shell sandboxing](https://learn.chatgpt.com/docs/sandboxing?surface=web) and
[Work access controls](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex).

Outgoing interaction controls are separate from
[workspace IP access restrictions](https://help.openai.com/en/articles/12111596-ip-allowlisting-for-chatgpt),
which limit incoming access to the ChatGPT workspace or Compliance API.

## Cloud browser and website access

The
[Cloud Browser](https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt)
is one of the tools ChatGPT Work can use and is distinct from the
[In-app Browser](https://help.openai.com/en/articles/20001277-using-the-built-in-browser-in-the-chatgpt-desktop-app).
It operates remotely and uses a browser session separate from the user's local
browser. It can't access local tabs, extensions, browsing history, saved
passwords, or authenticated local sessions.

The cloud browser can navigate public websites, enter information into supported
public forms, and combine relevant information from an approved app with a
website task. Website sign-in through the cloud browser isn't available in
Enterprise or Edu workspaces. Browser availability depends on your plan,
region, rollout, and workspace permissions.
For Enterprise workspaces, an administrator must enable cloud browser access in
addition to Work access.

Website access and actions have separate controls:

- By default, ChatGPT asks before visiting a new website. Where available, users
  can select **Always ask**, **Auto approve**, or **Always allow**, and allow or
  block individual websites. **Auto approve** applies automated risk checks.
  **Always allow** removes the interactive website-access review. Administrators
  have the same ability to limit approval settings for users (for example,
  disable **Always allow** workspace-wide).
- Allowing a website doesn't approve every action on that site. ChatGPT can
  request a separate confirmation before actions that could create a financial,
  legal, account, or other consequential commitment.

Users can inspect available page screenshots and browser replay in a Work
conversation. These user-visible records don't establish Compliance API export
or a complete administrator-visible execution history.

See
[Using cloud browser in ChatGPT](https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt)
and [Browser](https://learn.chatgpt.com/docs/browser?surface=web).

## Connected applications, credentials, and permissions

A connected app or Plugin gives Work access only through the integration your
workspace allows and the permissions granted for that connection. Admins can
control Plugin and app availability, workspace role access, external
authorization, action settings, and source-system permissions within the admin
dashboard.

For Enterprise and Edu workspaces, plugins and their underlying apps are off by
default. For Business workspaces, plugins and apps are on by default. Making a
plugin available doesn't automatically enable its required app or grant access
to an account. The required connection must be authorized for an individual,
shared, or agent-owned account before ChatGPT Work can access it. A shared or
agent-owned connection uses the connected account's source-system permissions,
which can differ from the requesting user's permissions.

Where supported, administrators can restrict an app to read-only actions or an
approved set of actions. App permission settings can also determine whether
ChatGPT asks before using an app, making changes, or performing important
actions. Not every app supports the same action controls, and not every action
requires an individual human confirmation.

For synced apps, changes to source content or permissions can take time to
appear. Disconnecting an app doesn't automatically remove information already
saved in a conversation, generated file, or record with its own retention
policy.

See
[Admin controls, security, and compliance for plugins and apps](https://help.openai.com/en/articles/11509118-admin-controls-security-and-compliance-in-apps-enterprise-edu-and-business),
[Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors),
[Google Workspace administrator-managed setup](https://help.openai.com/en/articles/10929079-google-workspace-admin-managed-setup),
[ChatGPT apps with sync](https://help.openai.com/en/articles/10847137-chatgpt-apps-with-sync).

## Privacy and data handling

ChatGPT Work follows the privacy, security, and data-handling policies applicable to your ChatGPT workspace. Local computer access with Work Cloud does not provide strict zero data retention. Data residency and inference residency cover only eligible content and supported workloads, regions, and configurations. Enterprise Key Management (EKM) covers supported stored content in eligible workspaces. Work is not supported with UAE inference residency. Conversations, uploaded files, generated files, connected applications, and browser data can have different retention and deletion rules. If `enforce_residency` is enabled in any cloud policy, **Allow local computer access** is disabled for both Work and dots. This safeguard does not configure workspace residency or, by itself, disable Work Cloud or dots.

For details, see [Enterprise privacy](https://openai.com/enterprise-privacy/),
[Chat and file retention policies](https://help.openai.com/en/articles/8983778-chat-and-file-retention-policies-in-chatgpt),
[Data residency and inference residency](https://help.openai.com/en/articles/9903489-data-residency-and-inference-residency-for-chatgpt),
and the [ChatGPT Work Admin FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq).

### Retention depends on the data type

- **Work conversations:** Follow the applicable ChatGPT workspace conversation
  retention and deletion settings.
- **Files saved to Library:** Follow the applicable file and workspace
  retention rules. Deleting a conversation doesn't delete files stored in
  Library.
- **Project files:** Remain with the project until its deletion, subject to the
  applicable deletion rules and exceptions.
- **Transient uploads outside Library:** For Enterprise, transient uploads can
  expire after 48 hours unless a different retention setting applies.
- **Saved memories, when enabled:** Follow separate memory controls.
- **Cloud browser cookies:** Remain separate from local browser data. Users can
  clear them from the Cloud browser settings.
- **Compliance Logs Platform records:** Remain available in the platform for 30
  days. Exported copies follow the receiving system's retention policy.
- **Connected application data:** Source records follow the connected
  application's policies. Copies saved in a chat, file, or synced index also
  follow the applicable OpenAI storage and retention rules.

Deleting a conversation, ending a Work task, clearing browser cookies, and
retaining compliance records are different operations. Deleting a chat removes
it from view and schedules permanent deletion within 30 days, subject to the
published security, legal, and de-identification exceptions.

See
[Chat and file retention policies](https://help.openai.com/en/articles/8983778-chat-and-file-retention-policies-in-chatgpt),
[Memory in ChatGPT](https://help.openai.com/en/articles/8590148-memory-in-chatgpt-faq),
and the
[OpenAI Compliance Platform](https://help.openai.com/en/articles/9261474-compliance-api-for-chatgpt-enterprise-edu-and-chatgpt-for-teachers).
