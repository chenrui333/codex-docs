---
source_type: 'learn'
source_area: 'learn_enterprise'
source_url: 'https://learn.chatgpt.com/docs/enterprise/gpts-and-sharing'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1"]
codex_cli_versions_raw: ["codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1"]
---

# GPTs and Sharing

Source: https://learn.chatgpt.com/docs/enterprise/gpts-and-sharing

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

## Sharing

Control who can create GPTs and whether they can be shared with specific people, groups, or the entire workspace.

GPT builders can use either connected apps or custom actions, but not both in
  the same GPT.

## Connected apps and actions

Allow GPT builders to use approved workspace apps or configure actions that interact with permitted third-party APIs. Access remains subject to workspace policies, user permissions, and approved domains.

## Domains

Restrict GPT actions to approved external domains to control which third-party APIs GPTs created in your workspace can access. If no domains are allowed, custom GPT actions cannot execute.

<WarningTip>
  Domain approval does not replace API authentication or user authorization.
</WarningTip>

## Managing GPTs

Review GPTs created in your workspace, manage sharing and ownership,
and delete GPTs when appropriate. The management view organizes GPTs
by assigned and unassigned ownership and includes the following
information:

- Name
- Builder
- Custom actions
- Who can access
- Chats
- Created
- Updated
