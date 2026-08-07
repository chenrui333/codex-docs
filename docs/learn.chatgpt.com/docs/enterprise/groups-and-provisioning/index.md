---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0"]
---

# Groups and provisioning

Source: https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Groups organize ChatGPT workspace access for a set of members and can carry
custom roles. Group membership is separate from local runtime policy and
permissions in connected systems.

For the complete control model, see
[Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions).

## Compare membership sources

Each group has one authoritative membership source:

| Group type                | Membership source                   | When it applies                                                                  |
| ------------------------- | ----------------------------------- | -------------------------------------------------------------------------------- |
| Manually managed          | ChatGPT workspace administration    | The group is small, temporary, or not managed through directory sync             |
| Identity-provider managed | Your identity provider through SCIM | Membership should follow the organization's directory and member-removal process |

Manual and identity-provider-managed groups can coexist. For synchronized
groups, the identity provider is the membership source; later provisioning
updates can overwrite workspace-side changes. The Help Center owns current SCIM
behavior, supported attributes, and setup steps.

## Understand the access boundary

SCIM provisions workspace membership and group assignments. It doesn't grant
permissions in GitHub, Google Drive, Slack, or another connected system. It also
doesn't replace local runtime requirements or Platform API organization access.

Workspace RBAC and local runtime requirements are separate control systems. A
group can be relevant to both, but don't infer a managed-requirements matching
or precedence rule from workspace group order. Use
[Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) for the
documented delivery and local precedence rules.

## Use current setup procedures

Workspace administration details can change. Use these sources for current UI
steps, availability, and limits:

- [Manage members, seat types, roles, and access](https://help.openai.com/en/articles/8266401-managing-members-seat-types-roles-and-access-in-chatgpt-enterprise)
- [Manage groups](https://help.openai.com/en/articles/9083985-group-permissions-in-gpts)
- [SCIM integration FAQ](https://help.openai.com/en/articles/10011769-openai-platform-scim-integration-faq)
- [Manage workspace settings](https://help.openai.com/en/articles/8411955)

## Related docs

- [Authentication](https://learn.chatgpt.com/docs/auth)
- [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions)
- [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration)
- [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup)
