---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1"]
---

# Roles and workspace permissions

Source: https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Administration spans six control boundaries. Granting access at one boundary
doesn't grant access at another. Use this page as the canonical map,
then follow the linked source for current settings and procedures.

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
authority. The workspace plan and a member's seat determine which product
surfaces are available. Built-in workspace roles determine who can administer
the workspace. Role-based access control (RBAC) determines which supported
features members can use.

Administrators can assign custom roles through groups, and a member can receive
access from more than one group. Because available seats, roles, and permissions
change with product and plan updates, use the Help Center for the current
permission list and setup procedure:

- [Manage members, seat types, roles, and access](https://help.openai.com/en/articles/8266401-managing-members-seat-types-roles-and-access-in-chatgpt-enterprise)
- [Configure role-based access control](https://help.openai.com/en/articles/11750701-rbac)
- [Manage groups](https://help.openai.com/en/articles/9083985-group-permissions-in-gpts)

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
