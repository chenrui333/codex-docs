---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/user-lifecycle'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.152.0", "0.152.1"]
codex_cli_versions_raw: ["codex-cli 0.152.0", "codex-cli 0.152.1"]
---

# User lifecycle management

Source: https://learn.chatgpt.com/docs/enterprise/user-lifecycle

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use this guide to give employees the right ChatGPT workspace access when they
join, update that access when their responsibilities change, and remove access
when they leave. The process also covers workspace seats, group-based roles,
Codex access tokens, and connected systems with their own access controls.

Single sign-on (SSO) verifies an employee's identity. Provisioning adds the
employee to a workspace. Neither action alone determines the employee's seat,
feature permissions, local runtime policy, or access to an external system.

Manage employee access across three lifecycle milestones:

- **Join:** Provision workspace access, groups, roles, and the correct seat.
- **Move:** Update the employee's groups and remove only obsolete direct roles.
- **Leave:** Remove workspace access, revoke tokens, and review connected systems.

## Verify prerequisites and assign owners

Before onboarding employees, identify who controls each part of the lifecycle:

| Owner                     | Responsibility                                                                                        |
| ------------------------- | ----------------------------------------------------------------------------------------------------- |
| Workspace owner           | Enable directory synchronization, assign workspace roles, approve seat types, and review audit access |
| Identity administrator    | Configure the identity provider, application assignments, provisioning groups, and sync status        |
| Workspace administrator   | Review workspace members, group membership, and supported administration settings                     |
| Security or service owner | Review Codex tokens, connected systems, shared automation, and required audit evidence                |

Confirm the target workspace, verify the organization's email domain when
required, and identify a workspace owner who can enable directory
synchronization. Then check which controls the workspace plan supports:

| Capability                                 | Supported workspace plans                                                                                    |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Directory synchronization through SCIM     | ChatGPT Enterprise, Edu, and Healthcare                                                                      |
| Custom roles and role-based access control | ChatGPT Enterprise, Edu, Healthcare, and Teachers                                                            |
| Codex access tokens                        | ChatGPT Business and Enterprise                                                                              |
| Codex-only seats                           | Eligible Enterprise and qualifying existing Business workspaces; unavailable to Edu, Teachers, or Healthcare |

SCIM stands for System for Cross-domain Identity Management. A Business
workspace can support Codex access tokens without SCIM, while an Edu workspace
can support SCIM without Codex access tokens or Codex-only seats. Apply only
the controls available to your workspace.

A Business workspace can keep and add Codex-only seats only if it had a Codex
seat before June 24, 2026, or a qualifying pending Codex-seat invitation as of
that date. New Business workspaces and workspaces without a qualifying seat or
invitation can't add their first Codex-only seat. See
[Manage workspace lifecycle and migration in ChatGPT Business](https://help.openai.com/en/articles/8801890-managing-workspace-lifecycle-and-migration-in-chatgpt-business).

Where the workspace supports more than one seat type, review the default in
**Workspace settings > Identity & access** before enabling automated
provisioning. SCIM-provisioned users inherit that default, and a seat controls
which product surfaces are available. A custom role can't grant access that
the seat doesn't include.

Use **Permissions & roles** to inspect local-access, access-token,
credential-lifetime, and remote-device controls. Some workspaces combine local
access in **Codex and Work Local**, with the **Allow members to use Codex and
Work Locally** control. Others separate **Codex Local**, with **Allow members
to use Codex locally**, from **Work Local**, with **Use Work locally**.
Separate Codex and Work controls don't grant access to each other. Token
controls appear either in the local-access section or in a separate **Access
tokens** section. These settings are separate from group membership and
assigned seat types.

The following example shows combined **Codex and Work Local** controls and a
separate **Access tokens** section:

> Illustration: ChatGPT Permissions & roles showing Codex and Work Local access, personal access tokens, and the access token expiration limit.

For current prerequisites and supported identity patterns, see
[Identity and provisioning](https://help.openai.com/en/articles/9672121)
and [Manage members, seat types, roles, and access](https://help.openai.com/en/articles/8266401-managing-members-seat-types-roles-and-access-in-chatgpt-enterprise).

## Choose how employees join the workspace

Choose one primary provisioning method for each audience:

| Method                     | How access begins                                                       | Where to remove access                                  |
| -------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------- |
| Manual invitation          | A workspace owner or admin invites an employee                          | Workspace member administration                         |
| Automatic Account Creation | An employee with an eligible email domain signs in                      | Workspace administration and the relevant identity flow |
| Directory Sync with SCIM   | An identity administrator assigns the employee in the identity provider | The identity-provider application or provisioning group |

Use manual invitations for a small pilot or a group that isn't managed through
directory synchronization. Use SCIM when workspace membership should follow
the identity provider as employees join, change teams, or leave.

Don't enable Automatic Account Creation and SCIM together. Users added through
Automatic Account Creation might lack SCIM management, so removing them from
an identity-provider group might not remove their workspace access. See the
[SCIM integration FAQ](https://help.openai.com/en/articles/10011769-openai-platform-scim-integration-faq)
for current guidance.

SCIM can connect a single ChatGPT workspace or an organization's tenant,
depending on the approved identity setup. Keep each workspace and product
assignment explicit. A shared directory connection doesn't automatically grant
or remove access across every workspace or Platform API organization.

## Connect a provisioning group to the correct workspace

Configure the connection before adding the first pilot employee. A workspace
owner and an identity administrator have separate responsibilities:

1. Have the workspace owner select the intended ChatGPT workspace and inspect
   **Workspace settings > Groups**. Record existing group names, members,
   custom-role assignments, and relevant project or GPT sharing.
2. Have the identity administrator identify the exact identity-provider group
   intended for synchronization. Compare its name and membership against every
   existing workspace group.
3. If a synchronized group shares a name with an existing workspace group,
   reconcile or rename the conflicting group before enabling synchronization.
   Have the workspace owner approve the resulting members, inherited roles, and
   sharing. A matching existing group becomes SCIM-managed, and its membership
   switches to identity-provider control.
4. Select a narrowly scoped pilot group and record the approved workspace,
   expected employees, and group-role assignments.
5. Have the workspace owner open **Workspace settings > Identity & access**
   and select **Enable Directory Sync**. If prompted, choose **Use SCIM only
   for this workspace** for workspace-level provisioning, or **Keep the option
   to expand across products** for approved tenant-level provisioning. If
   tenant-level SCIM is already active, manage that existing connection
   instead of creating a second workspace connection.
6. Have the identity administrator complete the identity-provider connection,
   select the ChatGPT application, and assign the approved group to provision
   members into the intended workspace.
7. In **Workspace settings > Groups**, confirm that the selected group displays
   its SCIM badge. Verify the group name, synchronized members, and target
   workspace before using it for access.
8. Have the workspace owner open **Permissions & roles > Custom roles**,
   create or select the approved role, and assign it to the synchronized group.
   Role configuration is available on the web and requires workspace owner
   access.
9. Review the group's effective permissions and the default workspace seat
   type before adding a representative pilot employee.

The identity-provider administrator controls application and group membership;
the workspace owner controls directory synchronization and workspace role
assignment. See the [SCIM integration FAQ](https://help.openai.com/en/articles/10011769-openai-platform-scim-integration-faq)
and [Configure role-based access control](https://help.openai.com/en/articles/11750701-rbac)
for current provider-specific steps and availability.

## Provision a new employee

For an employee managed through SCIM:

1. Confirm the intended workspace, verified email address, default seat type,
   and identity-provider group.
2. Assign the employee to the ChatGPT application or access-granting group in
   the identity provider.
3. Allow the directory synchronization to complete. Check the current
   identity-provider status if the employee doesn't appear.
4. In **Workspace settings > Members**, verify the employee's email,
   membership or pending invitation, seat type, and SCIM badge.
5. In **Workspace settings > Groups**, confirm the employee belongs to the
   intended synchronized group. Have the workspace owner verify the custom
   role assigned to that group.
6. Have a representative employee sign in to the correct workspace and verify
   the specific product surfaces, features, and connected systems they need.
7. Record the access owner and the successful verification using your
   organization's approved process.

If you add an employee manually, send the invitation from workspace member
administration, then perform the same seat, group, role, and sign-in checks.

A group organizes members but doesn't grant access to every feature by itself.
For the current role-assignment procedure, see
[Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions)
and [Configure role-based access control](https://help.openai.com/en/articles/11750701-rbac).

## Update access when an employee changes teams

An employee who changes teams can keep access from previous group or role
assignments. Update the source that owns the membership before verifying the
new access level:

1. Identify the employee's new team, required workspace, seat, approved
   feature permissions, and destination group.
2. Add the employee to the approved destination group before removing them
   from their previous group if they must remain in the workspace throughout
   the change. Update SCIM-managed membership in the identity provider; update
   manually managed membership through workspace administration.
3. Confirm that the approved role is already assigned to the destination group.
   Preserve existing role assignments on shared groups so the other members
   keep their approved access.
4. Have a workspace owner change a group-to-role assignment only after
   approving a separate group-wide policy change and reviewing its effect on
   every member.
5. Have a workspace owner open the employee's profile, review **Direct roles**,
   and remove outdated roles assigned directly to that person. Custom roles use **Default**,
   **On**, and **Off**. An explicit **Off** in any assigned role overrides
   **On** in another role.
6. Review the employee's effective permissions across all direct and
   group-assigned roles before approving the team change.
7. If the workspace supports more than one seat type, have a workspace owner open
   **Workspace settings > Members > Change seat type** and review the
   employee's intended product access.
8. Before converting a ChatGPT seat to a Codex-only seat, confirm that the
   employee should lose access to chats, memories, projects, and other
   ChatGPT features. The underlying data isn't deleted and becomes available
   again if the employee returns to a ChatGPT seat.
9. After synchronization and permission updates complete, verify both the
   newly allowed actions and the actions that should no longer be available.

If the employee owns an automation workflow, review whether its Codex token,
secret-manager entry, or connected-service authorization should move to another
approved owner. Removing the employee's local Codex permission suspends that
employee's Codex tokens but doesn't revoke them. Restoring the permission
reactivates those tokens, so revoke credentials that must lose access permanently.

## Remove a departing employee

Start with the system that owns the employee's workspace membership:

1. Determine whether SCIM manages the employee or an administrator added the
   employee manually.
2. For a SCIM-managed employee, remove that employee's ChatGPT application
   assignment and remove the employee from every access-granting provisioning
   group in the identity provider. Don't remove the shared groups themselves.
3. For an employee who isn't managed through SCIM, have a workspace owner or
   admin remove the member from **Workspace settings > Members**.
4. Confirm that the member is no longer present in the intended workspace.
   For SCIM-managed access, verify that synchronization completed and that no
   other identity-provider assignment can restore the membership.
5. Record the completed removal and assign an owner to review tokens,
   connected systems, and retained data.

Don't rely on a workspace-side removal when the identity provider still assigns
the employee to a SCIM-managed group. A later synchronization can add the
employee back to the workspace.

### Revoke Codex access tokens and transfer automation

Removing a person from the workspace doesn't replace an explicit review of
credentials used by trusted automation. Apply this procedure only when the
workspace supports and enables Codex access tokens.

Removing local Codex permission suspends existing tokens but doesn't revoke
them. Those tokens can work again if a workspace owner restores the permission,
so explicitly revoke credentials that must lose access permanently.

The **Access tokens** page identifies each token's creator and status. Use
**Revoke** to remove access from active tokens:

> Illustration: ChatGPT Access tokens showing token names, their creators and status, and the Revoke action.

1. Have a workspace owner or admin open
   [Access tokens](https://chatgpt.com/admin/access-tokens).
2. Identify tokens created by the departing employee and the workflows using
   those tokens.
3. Choose the replacement identity. For a durable non-human workflow on an
   eligible pay-as-you-go plan, use an approved dedicated [service
   account](https://learn.chatgpt.com/docs/enterprise/service-accounts). Otherwise, identify an
   approved active workflow owner. Have a workspace owner grant that person
   access-token creation permission if needed and confirm that the person has
   local Codex permission.
4. Create the replacement token. A permitted service-account operator can
   create a token from the service account's detail page. For a personal
   replacement, have the new workflow owner create a token for their own
   ChatGPT workspace identity. If the dialog shows **Scopes**, select
   **Codex**. Select other scopes only when the workflow requires them. A
   dialog without **Scopes** creates a Codex-only token. An administrator can't
   create a personal token on another user's behalf.
5. Update the workflow's stored secret, then verify that it runs successfully
   with the replacement token.
6. Have the workspace owner or admin revoke the departing employee's tokens
   and any replaced credentials.
7. Confirm that the revoked tokens can no longer start new authenticated runs.

When an approved replacement owner creates a token, use a descriptive workflow
name and choose the shortest credential lifetime allowed by your organization's
policy. If **Scopes** appears, select **Codex** and avoid permissions the
workflow doesn't require. The following example shows the scoped interface:

> Illustration: ChatGPT Create access token dialog showing Name, Scopes with Codex selected, Expiration, and the Create action.

Workspace owners and admins can revoke any token in their workspace. A member
with access-token permission can revoke only tokens they created. For current
token permissions and rotation steps, see
[Access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens#rotate-or-revoke-a-token).

### Review connected systems and retained data

Workspace provisioning doesn't manage every authorization boundary. Ask the
relevant service owner to review access to:

- Source repositories and connected GitHub accounts.
- Google Drive, Slack, and other connected applications.
- Installed plugins, bundled skills, and connector-backed capabilities.
- Hosted Codex environments, shared automation, and stored secrets.
- Managed devices, locally stored credentials, and supported remote sessions.
- Separate Platform API organizations, projects, and API keys.

Apply the controls owned by each system instead of assuming that a workspace
group or SCIM change updates permissions everywhere. See
[Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions)
for the complete boundary model and [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors)
for plugin availability, bundled skills, and connected-app permissions.

Removing workspace access isn't the same as deleting content. When a member
leaves, the workspace automatically reassigns their projects and custom
GPT ownership to a workspace owner. Those items aren't flagged for deletion.
If the member rejoins, ownership returns to that member.

For Enterprise and Edu workspaces, chats, files, and canvas documents follow
the configured workspace retention policy. Business workspaces keep chats,
files, and canvas documents indefinitely. Healthcare workspaces also provide
data retention controls; review the applicable workspace configuration and
[ChatGPT for Healthcare guidance](https://help.openai.com/en/articles/20001046-chatgpt-for-healthcare).

Reassigning a project or GPT doesn't transfer the former member's private
conversations or files, and the workspace owner can't view that private content
through the ownership change. See
[Workspace member removal and data retention](https://help.openai.com/en/articles/8266418)
for current plan-specific behavior.

If security or compliance requires evidence of the change, record the
affected workspace, employee, identity-provider assignment, completion time,
approval owner, and token-revocation verification in the approved system.
Confirm available records, administrator permissions, and retention in the
authenticated [Admin API reference](https://chatgpt.com/admin/api-reference).
Sensitive compliance scopes can require a workspace owner. For the product
overview, see [Compliance API and audit events](https://learn.chatgpt.com/docs/enterprise/compliance-api).
Don't infer event coverage, fields, or retention periods from this guide.

## Troubleshoot missing or unexpected access

| Symptom                                               | What to check                                                                             | Corrective action                                                                                                       |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| An employee can sign in but can't find the workspace  | The target workspace, invitation, identity-provider assignment, and email address         | Correct the assignment or email mapping, then verify workspace membership                                               |
| A synchronized employee receives the wrong seat       | The default seat type for the workspace and the current member record                     | Have a workspace owner review the default and the employee's supported seat options                                     |
| A team change doesn't remove a feature                | Other group memberships, **Direct roles**, and the employee's combined permissions        | Remove the employee from obsolete groups, then have a workspace owner revoke only that employee's obsolete direct roles |
| A manual group becomes SCIM-managed without approval  | Matching group names, identity-provider members, inherited roles, and existing sharing    | Reconcile approved group membership in the identity provider and review affected access                                 |
| Other employees lose access after a team change       | Recent changes to shared group-role assignments and the former team's approved access     | Have a workspace owner restore the approved shared group role, then update only the moving employee's membership        |
| An automation token stops working after a team change | The workflow owner's local Codex permission and current token status                      | Have a workspace owner restore approved local Codex access, or rotate and revoke the affected token                     |
| An access change doesn't appear immediately           | Identity-provider sync status, the expected sync window, and recent role updates          | Have the identity administrator verify the sync before contacting OpenAI Support                                        |
| A removed employee returns to the workspace           | The identity-provider application assignment and every access-granting provisioning group | Remove the employee in the identity provider instead of only in workspace settings                                      |
| A departing employee still has a listed token         | The token creator, workflow owner, and workspace administrator's token permissions        | Rotate any required automation credential, then revoke the departing employee's token                                   |
| A connected application still allows access           | The source system's account, plugin availability, and application grant                   | Ask the relevant service owner to remove access using that system's supported controls                                  |

Most identity providers synchronize every 30 to 40 minutes, although some
apply updates immediately. Custom-role changes can take about five minutes to
appear. You can't force a SCIM synchronization, so don't remove and recreate
a workspace member to work around a delayed update.

If an access removal or group update still hasn't completed after the expected
provider-specific window, have the identity administrator collect:

- The affected workspace and employee email address.
- The identity provider, application assignment, and provisioning group.
- The attempted change, its timestamp, and the latest synchronization status.
- The direct roles, group roles, or tokens that still need review.

Contact [OpenAI Support](https://help.openai.com/) with those details through
the Help Center. Treat a departed employee who retains access as a security
exception and follow your organization's incident-escalation process.

For provider-specific setup and synchronization behavior, use the current
[SCIM integration FAQ](https://help.openai.com/en/articles/10011769-openai-platform-scim-integration-faq).
For sign-in and identity errors, see
[Troubleshooting authentication](https://help.openai.com/en/articles/10489721-login-and-authentication-faq-s-and-troubleshooting-sso-scim-and-domain-verification).

## Verify the complete employee lifecycle

Use a representative test employee to verify all three transitions before a
broader rollout:

| Lifecycle stage | Primary owner                 | Successful outcome                                                                                                            |
| --------------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Joiner          | Identity administrator        | The employee joins the correct workspace with the intended seat, group, and feature access                                    |
| Mover           | Identity and workspace owners | Administrators update group membership, and workspace owners remove obsolete direct roles while preserving shared group roles |
| Leaver          | Identity and security owners  | Administrators remove workspace access, review supported tokens, and revoke or reassign external access                       |

Record who approved each change, what you verified, and which owner is
responsible for resolving any remaining access exceptions. Schedule recurring
access reviews according to your organization's identity and security policies.

## Related docs

- [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)
- [Groups and provisioning](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning)
- [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions)
- [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors)
- [Access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens)
- [Service accounts](https://learn.chatgpt.com/docs/enterprise/service-accounts)
- [Authentication](https://learn.chatgpt.com/docs/auth)
- [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)
- [Compliance API and audit events](https://learn.chatgpt.com/docs/enterprise/compliance-api)
