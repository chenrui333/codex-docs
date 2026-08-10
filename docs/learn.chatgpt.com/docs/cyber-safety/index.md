---
source_type: 'learn'
source_area: 'learn_cyber_safety'
source_url: 'https://learn.chatgpt.com/docs/cyber-safety'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0"]
---

# Cyber Safety

Source: https://learn.chatgpt.com/docs/cyber-safety

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Daybreak Blue and Daybreak Red help approved users move from findings to validated fixes during authorized defensive cybersecurity work. Combine the right model with a controlled environment, a written engagement scope, least-privilege permissions, and automatic review before sensitive actions run.

## Choose the right access tier

Start with **Daybreak Blue**, which provides access to frontier models such as GPT-5.6 Sol, for most authorized defensive work, including:

- Vulnerability discovery and triage.
- Secure code review and threat modeling.
- Detection engineering and incident response.
- Malware analysis in a controlled environment.
- Remediation and patch validation.

**Daybreak Red** provides separately approved access to purpose-trained cybersecurity models such as GPT-5.6 Cyber for explicitly authorized specialist workflows, including controlled vulnerability reproduction, proof-of-concept or exploit validation, penetration testing, red teaming, and complex system analysis. It isn't the default choice for routine security work, and access isn't available automatically or on every surface.

These advanced workflows can resemble malicious activity without the authorized engagement context. Use the approved model and surface only for systems you own or are explicitly authorized to assess, and keep appropriate human oversight in place.

For example:

- **Daybreak Blue:** Review the approved lab repository for authentication weaknesses, rank findings by evidence and impact, and propose patches without accessing external systems.
- **Daybreak Red:** Within the approved lab and engagement window, reproduce the documented authentication flaw, validate a minimal proof of concept, and stop before credential access, persistence, or production changes.

## Trusted Access for Cyber

[Trusted Access for Cyber](https://openai.com/index/trusted-access-for-cyber/) is the reviewed access program; Daybreak Blue and Daybreak Red are access tiers for approved models. Access depends on approval and provisioning for your specific identity or service, ChatGPT workspace or API organization and project, authorized model, and allowed product surface.

- Individuals can request access through the [individual Trusted Access application](https://chatgpt.com/cyber).
- Organizations can submit the [enterprise Trusted Access request form](https://openai.com/form/enterprise-trusted-access-for-cyber/) and coordinate with their OpenAI representative.

Submitting an application or completing identity verification doesn't guarantee approval.

Applying, verifying your identity, or receiving approval for Daybreak Blue
  doesn't grant access to Daybreak Red. Specialist access requires separate
  approval and provisioning.

For enterprise access, use the approved workspace, API organization, or project only for your organization's authorized internal work. Don't extend it to external users, third-party customers, externally offered services, downstream product features, or systems outside the approved engagement. If the approved identity, workspace, API organization, project, model, or surface is unclear, stop and confirm it with your OpenAI representative.

Trusted Access doesn't automatically grant [Zero Data Retention](https://developers.openai.com/api/docs/guides/your-data#data-retention-controls-for-abuse-monitoring). Confirm any separately approved retention controls for the exact API organization and applicable endpoint before you begin.

## Configure a controlled cybersecurity engagement

Trusted Access governs approved model access, but it doesn't configure your environment or enforce your engagement scope. Your team must set up the following isolation, permission, review, and human-oversight controls.

### Isolate the environment

Run the engagement in a controlled lab or sandbox. Start without unrestricted internet access, access to sensitive production systems, or access to unrelated infrastructure. Keep secrets, credentials, persistent access, and durable system changes out of reach unless the written engagement explicitly requires and authorizes them.

Test filesystem and network boundaries before beginning higher-risk work. Keep the host environment isolated even when the model or reviewer approves an individual action.

### Define and enforce the engagement scope

Document the rules of engagement before the model starts. Include:

- Approved target systems, hosts, and environments.
- Excluded systems, including production and unrelated infrastructure.
- Approved and prohibited actions.
- The engagement window and data-handling requirements.
- Vulnerability disclosure, patch approval, and maintainer coordination.
- Stop conditions and actions that require explicit human approval.

Give the agent the relevant scope as task context. This written scope doesn't enforce itself: apply independent filesystem, network, identity, and tool controls to make unauthorized actions impossible whenever practical.

Use Codex [permission profiles](https://learn.chatgpt.com/docs/permissions) to create a least-privilege boundary. Choose `:read-only` when the task doesn't require changes, or extend `:workspace` when the engagement needs workspace edits. For example:

```toml
approval_policy = "on-request"
approvals_reviewer = "auto_review"
default_permissions = "cyber-lab"

[permissions.cyber-lab]
description = "Limit security testing to the approved lab and workspace."
extends = ":workspace"

[permissions.cyber-lab.filesystem]
glob_scan_max_depth = 3

[permissions.cyber-lab.filesystem.":workspace_roots"]
"**/.env*" = "deny"
"**/*.pem" = "deny"

[permissions.cyber-lab.network]
enabled = true
# Uncomment only for an approved host that resolves to a private address.
# allow_local_binding = true

[permissions.cyber-lab.network.domains]
"lab.example.com" = "allow"
```

Replace `lab.example.com` with an approved target. The bounded filesystem scan avoids searching the entire workspace on Linux, WSL, and Windows; increase the depth or use exact deny paths if sensitive files appear deeper. Don't combine permission profiles with legacy `sandbox_mode` settings; follow the [permission-profile configuration guidance](https://learn.chatgpt.com/docs/permissions#define-and-select-a-profile).

If the approved lab host resolves to a private address, Codex blocks it by default even when the host is on the allowlist. Set `allow_local_binding = true` only for an explicitly approved private-network engagement, keep the destination allowlist narrow, and review the [local and private network guidance](https://learn.chatgpt.com/docs/permissions#local-and-private-networks). You can also allowlist the exact approved private IP address.

Avoid `:danger-full-access` and `--yolo` for cybersecurity engagements. Full Access removes the enforceable sandbox boundary that automatic review depends on. Managed organizations can exclude `:danger-full-access`, limit allowed approval policies, and require automatic review through [enterprise-managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration#configure-automatic-review-policy).

Before enabling **Full Access** for an approved security model, the
ChatGPT desktop app shows a model-specific warning about dangerous actions. The
warning recommends **Approve for me** instead and links to
[reviewer-policy configuration](https://learn.chatgpt.com/docs/sandboxing/auto-review#configuration).
The warning doesn't restore the sandbox boundary or override organization
policy.

### Review sensitive actions before execution

[Auto-review](https://learn.chatgpt.com/docs/sandboxing/auto-review) routes eligible sandbox-boundary approval requests to a separate reviewer before the proposed action runs. The reviewer considers the proposed action, bounded task context, and applicable policy, then allows or denies the request. Organizations can customize that policy for their approved targets, prohibited actions, and required human-review conditions.

In the ChatGPT desktop app, selecting an approved Daybreak model
automatically switches the permissions control to **Approve for me** when that
mode is available for your account and allowed by organization policy. This
also applies when you use the desktop app's `/model` command. If that mode
isn't available, the current permission mode stays unchanged. Model selection
never overrides managed organization requirements.

For automatic review to run, keep all three controls in place:

1. Use an interactive approval policy such as `approval_policy = "on-request"`.
2. Set `approvals_reviewer = "auto_review"`.
3. Keep an enforceable sandbox or permission-profile boundary.

Requests to a target on the network allowlist stay inside the network boundary and don't automatically trigger Auto-review. To review a sensitive command even when its destination is on the allowlist, create an explicit [command rule](https://learn.chatgpt.com/docs/agent-configuration/rules) under `~/.codex/rules/`:

```python
prefix_rule(
    pattern = ["curl"],
    decision = "prompt",
    justification = "Review requests to the approved cybersecurity target.",
)
```

Restart Codex after adding the rule. With `approvals_reviewer = "auto_review"`, matching commands go to the reviewer before execution. Add corresponding prompt rules for every sensitive command, or use `approval_mode = "prompt"` for individual [MCP tools](https://learn.chatgpt.com/docs/extend/mcp). Actions that require a person's decision still need explicit human approval.

Auto-review doesn't inspect routine actions that are already permitted inside the sandbox. With `approval_policy = "never"` or Full Access, a sensitive action might not create a reviewable approval request. Automatic review can make mistakes and doesn't replace isolation, written scope, monitoring, or explicit human oversight.

For a scoped policy and organization-wide enforcement, see [Configure an authorized cybersecurity engagement](https://learn.chatgpt.com/docs/sandboxing/auto-review#configure-an-authorized-cybersecurity-engagement).

## Apply the same controls in custom agent workflows

If you build with the Responses API, the Agents SDK, or another harness, add review at the tool-execution boundary. Check sensitive proposed actions against the approved engagement scope before execution, route ambiguous or high-risk actions to a person, enforce independent filesystem and network restrictions, keep audit logs, and fail closed if the reviewer or policy is unavailable.

Codex Auto-review doesn't automatically protect custom tools or external harnesses. Use [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals#review-cybersecurity-actions-before-execution) for the Agents SDK pattern and the [open-source reviewer policy](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md) as a reference.

Codex product-side sandboxing and review are separate from [API cybersecurity checks](https://developers.openai.com/api/docs/guides/safety-checks/cybersecurity). API safeguards can return `cyber_policy` errors, and per-user `safety_identifier` values can help limit the impact of a safeguard action.

## False positives

Legitimate cybersecurity or unrelated activity can still trigger a safeguard. If a safeguard blocks, reroutes, or limits a request, inspect the available client notice and request logs. Report suspected Codex false positives through `/feedback` when available. For API access restrictions and appeals, follow the [API cybersecurity checks guidance](https://developers.openai.com/api/docs/guides/safety-checks/cybersecurity#appeals).

All users remain subject to the [Usage Policies](https://openai.com/policies/usage-policies/) and [Terms of Use](https://openai.com/policies/row-terms-of-use/).
