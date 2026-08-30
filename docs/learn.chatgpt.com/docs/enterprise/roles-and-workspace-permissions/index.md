---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0"]
---

# Roles and workspace permissions

Source: https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Different settings cover different parts of your organization's ChatGPT
experience. Giving someone access in one area doesn't automatically give them
access in another. Use this page to see how the six control boundaries work
together, then follow the linked guidance for current setup steps.

In workspace settings, **Codex Local** is a grouping label for certain local
access and access-token controls, not a separate product or client. Individual
controls in the group can have different scopes. The current **Allow members to
use Codex Local** workspace permission covers local use in the ChatGPT desktop
app, Codex CLI, and IDE extension. Managed configuration is a separate layer
that constrains supported runtime behavior for covered capabilities in those clients. Features
and effective requirements can differ by client and version.

## Understand the control boundaries

| Boundary          | What it controls                                                                                                                                                                                      | What it doesn't control                                                                          | Current source                                                                                                                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ChatGPT workspace | Membership, seats, built-in administration roles, and role-based access to supported workspace features                                                                                               | Local agent permissions, Platform API organization access, or permissions in a connected service | [ChatGPT workspace access](https://help.openai.com/en/articles/8266401-managing-members-seat-types-roles-and-access-in-chatgpt-enterprise) and [RBAC](https://help.openai.com/en/articles/11750701-rbac) |
| Local clients     | Runtime behavior for covered capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension, including approvals, filesystem and network access, permission profiles, and allowed integrations | A ChatGPT seat, feature or model entitlement, or access to external data                         | [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) and [Permissions](https://learn.chatgpt.com/docs/permissions)                                                                                                   |
| Codex cloud       | Eligibility to use hosted Codex workflows and the cloud environments made available to the user                                                                                                       | Local runtime policy or the repository permissions granted by a source system                    | [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment)                                                                                                                                              |
| Platform API      | Organization and project membership, API keys, model access, usage, and billing for API-authenticated work                                                                                            | ChatGPT workspace membership, local-client access, or Codex cloud access                         | [OpenAI API Platform](https://platform.openai.com/docs/overview)                                                                                                                                         |
| Plugins           | Plugin availability and installation, bundled skills, connector access, and supported connector actions                                                                                               | Authorization in the connected service or broader local and cloud runtime permissions            | [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors)                                                                                                                                                 |
| Connected systems | Which repositories, files, messages, and actions the authenticated account can access in the source system                                                                                            | ChatGPT workspace, plugin, Codex cloud, or Platform API entitlement                              | The connected service's administration and access controls                                                                                                                                               |

A request must pass every boundary that applies to it. For example, workspace
access can make a plugin available, but the connected service still decides which
data the signed-in account can read. A local permission profile can restrict a
run in a supported local client, but it can't grant a workspace feature or
model.

## Assign workspace access

ChatGPT workspace administration separates product access from administrative
authority.

### Understand the difference between a seat, an admin role, and a custom role

A seat determines which product surfaces a member can access. Depending on the
workspace plan, available seat types can include ChatGPT and Codex seats.

Built-in workspace roles determine administrative authority. The **Owner** role
manages workspace-wide settings, the **Admin** role manages supported operations
and groups, the **Member** role doesn't have administrative rights, and the
**Analytics Viewer** role can access workspace analytics.

Custom roles define which supported features a member can use. They don't
replace seat or plan eligibility, grant permissions in a connected system, or
change local runtime requirements.

  <iframe
    src="https://player.vimeo.com/video/1215495812"
    title="Role-based access control walkthrough"
    loading="lazy"
    allow="autoplay; fullscreen; picture-in-picture"
    allowFullScreen
    referrerPolicy="strict-origin-when-cross-origin"
    class="h-full w-full border-0"
  ></iframe>

### Set the workspace default, then create targeted custom roles

Only workspace owners can configure role-based access control (RBAC) and create
custom roles. Workspace settings establish the baseline for eligible
permissions. Owners can assign custom roles through manually managed or
SCIM-synced groups, or directly to individual members where supported. A member
can receive more than one custom role.

For eligible permissions, **Default** inherits the workspace setting, **On**
grants access, and **Off** explicitly denies access. An explicit **Off** in any
applicable role blocks access even when another role grants it. Available
permission states can vary by feature.

### Review Work Local and Work Cloud permissions

When your workspace offers **Work Local** and **Work Cloud**, check both the
workspace default and each applicable custom role. Work is available only to
eligible workspaces, and available controls can differ by plan, workspace
configuration, and rollout. A role can't expand the access allowed by a
member's seat.

**Work Cloud** governs supported ChatGPT Work tasks in the cloud. **Work
Local** without **Work Cloud** allows local work in the ChatGPT desktop app but
doesn't allow members to start cloud tasks. Codex Local access instead uses the
separate **Allow members to use Codex Local** permission. Changing a Work
permission doesn't change Codex Local access or replace local runtime
requirements.

For current eligibility and settings, see
[ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex).

Because available seats, roles, and permissions change with product and plan
updates, use the Help Center for the current permission list and setup
procedure:

- [Manage members, seat types, roles, and access](https://help.openai.com/en/articles/8266401-managing-members-seat-types-roles-and-access-in-chatgpt-enterprise)
- [Configure role-based access control](https://help.openai.com/en/articles/11750701-rbac)
- [Manage groups](https://help.openai.com/en/articles/9083985-group-permissions-in-gpts)

### Control Computer History access

[Computer History](https://learn.chatgpt.com/docs/customization/computer-history) is off by default for
Business and Enterprise workspaces. Members cannot turn it on until an
administrator explicitly grants access. Enterprise administrators can grant
access by role:

1. Open [**Workspace Settings > Permissions & roles**](https://chatgpt.com/admin/settings).
2. Find **Computer History** and choose the workspace role that should have
   access.
3. Turn on **Enable Computer History** for that role.

This permission only allows assigned members to turn on Computer History; it
does not turn on the feature for them. Each member must opt in from the ChatGPT
desktop app on macOS and can choose which apps and websites contribute. Members
without the required workspace permission cannot enable the feature through
local settings.

## Apply local runtime policy

Local runtime policy constrains covered capabilities in the ChatGPT desktop
app, Codex CLI, and IDE extension. Cloud-managed requirements additionally
depend on supported ChatGPT sign-in and plan eligibility. Permission profiles
and managed requirements can constrain commands, filesystem access, network
access, approvals, and other local runtime behavior. They don't change the
user's seat, workspace role, model entitlement, or permissions in an external
system.

Users can select a built-in or custom permission profile when local policy
allows it. Administrators can distribute defaults and requirements through the
supported managed-configuration channels. See [Permissions](https://learn.chatgpt.com/docs/permissions)
for profile behavior and [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)
for requirements, delivery, and precedence.

## Related docs

- [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)
- [Groups and provisioning](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning)
- [Workspace model availability](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability)
- [Access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens)
- [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)
- [Authentication](https://learn.chatgpt.com/docs/auth)
