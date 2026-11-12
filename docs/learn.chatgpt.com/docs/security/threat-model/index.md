---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/threat-model'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Improve the repository threat model

Source: https://learn.chatgpt.com/docs/security/threat-model

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Update a monitored repository's threat model when the generated version misses
security assumptions or deployment context. This guide applies to Daybreak Defense Factory. For local plugin policy, see [Configure the
scan](https://learn.chatgpt.com/docs/security/plugin/scans#configure-the-scan).

## What a threat model is

A threat model is a short security summary of how your repository works. Daybreak creates the first draft from the code and uses it to guide future commit scans and prioritize findings.

A threat model describes:

- Entry points and who can supply input to them
- Trust boundaries and authentication or authorization assumptions
- Sensitive data and privileged actions
- Areas that need particular attention

For example:

> The public account API accepts authenticated users' JSON requests and file
> uploads. Users may change only accounts in their own tenant. The identity
> service authenticates the caller, but each handler must check tenant access.
> Billing changes go through a privileged internal service. Prioritize missing
> tenant checks and upload paths that can reach that service.

Identify uncertain assumptions. For example, don't describe an endpoint
as internal-only unless that is true of the deployment you want assessed.

## Edit the threat model

1. Open **Repositories** in Daybreak and select the monitored repository.
2. Open its **Threat model** and choose the edit control.
3. Add the deployment details or security assumptions the scan should use, then save your changes.

Changes apply to future scans.

Revisit the model after changes to authentication, tenant boundaries, or exposed
services. Keep facts about the deployment separate from priorities for the scan.

## Add context for validation

Select **Manage** under **Validation context** on the repository overview.
If the repository has a `SECURITY.md` file, you can read it here. Make any changes to
the file in the repository.

Use **Additional context** for details Daybreak should consider when it checks
future findings. For example, identify which gateway enforces tenant
membership and which routes can bypass it. Select **Save**.
