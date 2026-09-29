---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/sites'
source_kind: 'learn_markdown'
---

# Sites administration

Source: https://learn.chatgpt.com/docs/enterprise/sites

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Workspace admins can enable Sites, choose which plugins they can use, and manage
published Sites. To build or use a Site, see [Sites](https://learn.chatgpt.com/docs/sites).

    {"For help with workspace access, publishing, and sharing, see "}
    [{"Managing ChatGPT Sites for your workspace"}](https://help.openai.com/articles/20001338)
    {" in the Help Center."}

## Before you begin

Sign in as a workspace owner or admin and select the workspace you want to
manage. If tenant policy blocks access to connected apps, a tenant admin must
enable that access. A tenant is the organization-level admin scope that can
govern multiple workspaces.

Sites is in public beta. Available controls depend on your plan, admin role,
  and feature availability. Review the [Sites
  limits](https://learn.chatgpt.com/docs/sites#understand-limits-and-unsupported-uses), including data
  residency limitations, before choosing what data to use.

These controls apply at different levels:

| Control                     | What it governs                                         | Where to manage it                                                                |
| --------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Sites access                | Who can create and publish Sites                        | Workspace settings, including **Permissions & roles** where available             |
| Site sharing                | Who can visit an individual Site                        | The Site's sharing controls or **Sites** in workspace administration              |
| Plugin permission for Sites | Which plugins can be used in Sites across the workspace | **Admin** > **Plugins** > the plugin > **Allow site visitors to use this plugin** |
| Tenant connector access     | Whether Sites can request access to connected apps      | Tenant administration: **External access** > **ChatGPT Sites** > **Connectors**   |
| Network access              | Which external destinations Sites can contact           | Workspace administration: **Sites** > **Network access**, where available         |

## Enable Sites and choose sharing permissions

<WorkflowSteps>

1. Open your workspace settings and review the Sites permissions. Where
   **Permissions & roles** is available, enable Sites for the roles that need
   to create and publish them.
2. Review public publishing separately. In Enterprise workspaces, public
   publishing is off by default and requires an admin to enable it. You can use
   Sites internally without enabling public publishing.
3. Review external invitations separately from public publishing. Enterprise
   admins manage **Allow members to invite external visitors to sites** under
   **Workspace settings** > **Permissions & roles**. Business workspaces don't
   have a separate external-invitation permission toggle.
4. Ask a member of the intended group to create a Site, keep its audience
   limited, and verify that they can publish it and share it with the intended
   visitors.

</WorkflowSteps>

A new Site is limited to its owner and workspace admins until its access
changes. Visitor access and editor access are separate. See
[Control access and secrets](https://learn.chatgpt.com/docs/sites#control-access-and-secrets) for
sharing options and [Collaborate on a Site](https://learn.chatgpt.com/docs/sites#collaborate-on-a-site)
for editor permissions.

<a id="enable-bring-your-own-plugin"></a>

## Enable plugin use in Sites

Plugins in Sites let a Site use each visitor's own connected
accounts and permissions. Sharing a Site doesn't share the builder's
connections. Visitors sign in with ChatGPT, review the requested access, and
choose which connections to allow. Connected features require membership in
the workspace that owns the Site.

Each plugin has a separate **Allow site visitors to use this plugin** setting. When an admin
hasn't saved a choice for that plugin, the default depends on the workspace
plan:

- **Business and Education:** Available plugins are allowed in Sites by default.
- **Enterprise:** Plugins are off for Sites by default. An admin must allow
  each plugin the workspace needs.

A saved admin choice overrides the default. Allowing a plugin in Sites
doesn't override ordinary plugin permissions or tenant restrictions.

### Allow individual plugins in Sites

1. Open **Admin** > **Plugins** in the intended workspace.
2. Open the plugin you want to allow, such as Notion.
3. In its **Sites** section, review **Allow site visitors to use this plugin**. If it's off and you
   want to allow the plugin, turn it on and select **Save**. If it's already on,
   no change is needed.
4. Review each plugin that the Site needs. Confirm that the plugin, its
   connected app, and the required actions are also available to the intended
   members through your [plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors).

If **Allow site visitors to use this plugin** is disabled because tenant
  connector access is off, follow the **External access** link on the plugin
  page when available. A tenant admin can enable **Connectors** for **ChatGPT
  Sites**. If you don't have tenant admin access, contact an admin of the tenant
  named in the notice.

**Allow site visitors to use this plugin** is one setting per plugin for the whole workspace. It
doesn't assign access by role, connect accounts for members, or replace
visitor consent and the connected service's permissions. It also doesn't
provide separate Sites-specific read and write switches. Review the approved
actions and permissions before enabling a plugin.

<a id="enable-tenant-access-to-connected-apps"></a>

### Check tenant access if plugins are blocked

Use these steps when the plugin page says tenant connector access is off.
If access is already on, no tenant change is needed. Turning it on doesn't
enable individual plugins that a workspace admin has disabled.

1. Follow the plugin page's **External access** link, or open [Admin Console](https://admin.openai.com)
   and select the tenant that governs the workspace.
2. Open **External access**, find **ChatGPT Sites**, and enable **Connectors**
   if it's off.
3. Return to the workspace's plugin settings and review **Allow site visitors to use this plugin**
   for each plugin your team needs.

**External access** belongs to the tenant view. The workspace view has its own
**Sites** settings. If you can't find **External access**, check the selected
admin scope and whether you have tenant admin access. Workspaces without a
tenant don't have this tenant-level control. If the plugin page says connector
access isn't available for the tenant yet, changing the plugin's setting
won't enable it.

### Verify the visitor experience

Ask a builder to create a Site using an approved plugin and share it within
the workspace. Have another member sign in, review access, and connect their
own account. Confirm that the Site shows data that member is allowed to
access. Also test continuing without granting plugin access: features that
require a connection won't work.

For the builder workflow, see
[Bring user data to your Site with plugins](https://learn.chatgpt.com/docs/sites#bring-user-data-to-your-site-with-plugins).

## Configure network access

Where **Network access** is available, use it to control the external
destinations a Site can contact. This setting is separate from plugin
authorization: allowing a hostname doesn't grant access to a connected app.

### Set the workspace policy

1. Open **Sites** in workspace administration.
2. Find **Network access** and open its editor.
3. Choose **Allow all destinations** or **Allow only listed destinations**.
4. For a restricted policy, enter one hostname per line under **Allowed
   destinations**. Use an exact hostname such as `api.example.com`, or
   `*.example.com` to allow its subdomains. The wildcard doesn't include the
   bare `example.com` hostname; add that separately if needed.
5. Select **Save**, reopen the editor, and confirm the saved destinations.
   Test the Site's required network requests.

Don't enter URLs, paths, IP addresses, or ports. The editor supports up to
1,024 destination rules. A `*` rule allows all HTTP destinations. Restricted
policies block raw TCP connections, including when the list contains `*`.

### Allow an additional destination for one Site

To allow a destination for one Site without broadening workspace-wide access:

1. Find the Site in workspace administration and open **More actions** >
   **Network access**.
2. Review the inherited policy.
3. Enter the approved hostnames under **Additional allowed destinations** and
   select **Save**.
4. Reopen the dialog to confirm the saved list, then test the Site.

These exceptions add to the inherited policy; they don't replace it or
restrict destinations it already allows. With an unrestricted inherited
policy, exceptions don't further change access. If the combined destination
limit is exceeded, the saved exceptions aren't applied; shorten the list and
save again.

## Manage workspace Sites

Open **Sites** in workspace administration to find Sites by URL and review
their owners. Use the controls available to your role to:

- **Manage access:** Review or change the Site's audience.
- **Copy source clone command:** Get the command to inspect a Site's source
  code, where available.
- **Transfer ownership:** Assign a new owner when responsibility changes.
- **Suspend:** Stop access to a Site while you investigate an issue. Use
  **Reinstate** when you're ready to make it available again.
- **Delete Site:** Permanently remove a Site when it's no longer needed.

To stop use of a particular plugin in Sites, turn off its **Allow site visitors
to use this plugin** setting and verify the affected Site's behavior. If another allowed
plugin includes the same connector, turning off one plugin doesn't block that
shared connector through the other plugin. Review all relevant plugins when
removing connector access.

## Troubleshoot access

| Symptom                                                      | What to check                                                                                                                                                                                                   |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A member can't create or publish a Site                      | Confirm the selected workspace, Sites availability, and the member's workspace permissions.                                                                                                                     |
| A plugin works in ChatGPT but is unavailable to a Site       | Check **Allow site visitors to use this plugin**, including any saved admin choice, ordinary plugin permissions, and the member's connected account. If tenant policy blocks access, check **External access**. |
| The plugin's Sites toggle is disabled                        | Review the notice beside the toggle. If tenant connector access is off, follow **External access** or contact an admin of the tenant named in the notice.                                                       |
| A visitor can open the Site but can't use connected features | Confirm membership in the Site's workspace, the selected account, visitor consent, and permissions in the connected service. An external invitation doesn't grant workspace membership.                         |
| The Site can't reach an external service                     | Check the hostname against the inherited network policy and any Site-specific exceptions.                                                                                                                       |
| A network policy save conflicts or can't be confirmed        | Select **Refresh and review**, inspect the latest saved policy, then make the intended change. Refresh replaces the unsaved draft.                                                                              |
| An admin setting is missing or read-only                     | Check the selected tenant or workspace, your admin role, and feature availability. The tenant and workspace views expose different controls.                                                                    |

When asking an admin for help, include the Site URL, workspace, plugin or
destination needed, and the exact error. Contact the admin directly to request
access.
