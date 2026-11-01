---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/dynamic-groups'
source_kind: 'learn_markdown'
---

# Dynamic groups

Source: https://learn.chatgpt.com/docs/enterprise/dynamic-groups

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Dynamic groups organize workspace members using user attributes sent by your identity provider through SCIM. You define membership rules using supported attributes, such as department or location. As those attributes change, group membership updates to include people who match the rules and remove people who no longer match.

For example, a dynamic group can include members whose department is Engineering and whose location is London. You manage the rules in ChatGPT Admin, while your identity provider supplies the user attributes.

## Before you begin

- Sign in as a workspace owner or admin in a workspace where dynamic groups are available.
- Configure SCIM provisioning for your workspace and make sure your identity provider sends the attributes you want to use.
- Choose attribute values that match the values your identity provider sends. See the supported attributes and payload paths in this guide.

Group membership and feature permissions are separate. A member’s applicable roles, seat type, and product eligibility still determine access. See [Groups and provisioning](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning) for the access model.

## Create a dynamic group

1. Open [ChatGPT Admin](https://admin.openai.com/) and select your workspace.
2. Under **Identity & access**, select **Groups & roles**.
3. Select **Create group** using the **+** button.
4. Enter a group name, such as **Demo**, turn on **Dynamic group**, and select **Next**.

![Create the Demo group with Dynamic group enabled](<https://developers.openai.com/images/codex/dynamic-groups/create-dynamic-group.webp>)

5. Under **Add membership rules**, choose an **Attribute**, an **Operator**, and a **Value**. In this example, select **department**, **Equals**, and enter **Engineering**.
6. Select **Add condition** to add another rule. For this example, select **location**, **Equals**, and enter **London**.

Members must match **all conditions**. The example below matches members whose department is Engineering **and** whose location is London.

![Membership rules requiring department to equal Engineering and location to equal London](<https://developers.openai.com/images/codex/dynamic-groups/membership-rules.webp>)

7. Select **Create**. Open the group’s **Settings** tab to review its name and membership rules.

![Demo settings with the saved dynamic membership rules and Re-sync button](<https://developers.openai.com/images/codex/dynamic-groups/group-settings.webp>)

Creating the group saves its membership rules. Select **Re-sync** to apply those rules to existing workspace members.

## Edit membership rules

To change which members qualify for a dynamic group:

1. Open the group and select **Settings**.
2. Edit its membership rules and select **Save changes**.
3. Select **Re-sync** to apply the saved rules to existing workspace members.

**Save changes** stores the rules without starting a re-sync. **Re-sync** uses the saved rules and is unavailable while you have unsaved changes.

## Re-sync membership

Use **Re-sync** to re-evaluate the group’s membership against its current rules and the SCIM attributes already available in the workspace.

1. Open the dynamic group and select **Settings**.
2. In **Membership rules**, select **Re-sync**.
3. Follow the **Syncing group membership** status panel. A queued sync can show **Starts in** with a countdown before processing begins. You can collapse the panel or use **Cancel sync** while that option is available.
4. After processing finishes, open **Group members** to review the result.

![The Syncing group membership panel shows a countdown and Cancel sync control](<https://developers.openai.com/images/codex/dynamic-groups/resync-status.webp>)

Membership rule controls are unavailable while the sync is active. Canceling a sync can leave membership partially updated. After making any rule changes, save them and run **Re-sync** again to apply the saved rules. If an expected member is missing, check that their SCIM attributes have reached the workspace and that their values match every condition.

## View a member’s SCIM attributes

Use a member’s profile card to check the SCIM attribute values available in your workspace and compare them with your dynamic group’s membership rules.

1. Under **Identity & access**, select **Members**.
2. Search for the member by name or email, then select their name to open their profile card.
3. Review the **SCIM attributes** table, which lists each available attribute and its value.

The example below shows a test member’s SCIM values, including `department`, `title`, and `costCenter`.

![Member profile card with name, email, and group names masked, showing SCIM attribute names and values](<https://developers.openai.com/images/codex/dynamic-groups/member-scim-attributes.webp>)

## Supported SCIM attributes

The following table lists the supported attribute names and the user-payload fields recognized for each one. All attributes in this catalog use the string type, including `isAdmin`.

A plain field name refers to a top-level field. A path beginning with `/` identifies a field inside the named SCIM extension object. For example, `/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User/department` refers to `department` inside the `urn:ietf:params:scim:schemas:extension:enterprise:2.0:User` object.

| Attribute name | Recognized fields in the SCIM payload                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `department`   | `department`<br />`/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User/department`<br />`/urn:scim:schemas:extension:enterprise:1.0/department`<br />`/urn:scim:schemas:extension:enterprise:2.0/department`                                                                                                                                                                                                                                          |
| `title`        | `title`                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `manager`      | `manager`<br />`/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User/manager/value`<br />`/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User/manager/displayName`<br />`/urn:scim:schemas:extension:enterprise:1.0/manager/value`<br />`/urn:scim:schemas:extension:enterprise:1.0/manager/displayName`<br />`/urn:scim:schemas:extension:enterprise:2.0/manager/value`<br />`/urn:scim:schemas:extension:enterprise:2.0/manager/displayName` |
| `costCenter`   | `costCenter`<br />`/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User/costCenter`<br />`/urn:scim:schemas:extension:enterprise:1.0/costCenter`                                                                                                                                                                                                                                                                                                       |
| `division`     | `division`<br />`/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User/division`<br />`/urn:scim:schemas:extension:enterprise:1.0/division`                                                                                                                                                                                                                                                                                                             |
| `organization` | `organization`<br />`/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User/organization`<br />`/urn:scim:schemas:extension:enterprise:1.0/organization`                                                                                                                                                                                                                                                                                                 |
| `userType`     | `userType`                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `country`      | `country`                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `isAdmin`      | `isAdmin`                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `location`     | `location`                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

For `manager`, the catalog recognizes the top-level field and the nested extension `value` or `displayName` fields. For `country`, send the top-level field shown in the table.

## Related documentation

- [Groups and provisioning](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning)
