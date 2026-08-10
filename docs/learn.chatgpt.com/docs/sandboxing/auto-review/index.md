---
source_type: 'learn'
source_area: 'learn_sandboxing'
source_url: 'https://learn.chatgpt.com/docs/sandboxing/auto-review'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0"]
---

# Auto-review

Source: https://learn.chatgpt.com/docs/sandboxing/auto-review

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Auto-review replaces manual approval at the sandbox boundary with a separate
reviewer agent. The main Codex agent still runs inside the same sandbox, with
the same approval policy and the same network and filesystem limits. The
difference is who reviews eligible escalation requests.

Auto-review only applies when approvals are interactive. In practice, that
  means `approval_policy = "on-request"` or a granular approval policy that
  still surfaces the relevant prompt category. With `approval_policy = "never"`,
  there is nothing to review.

In the ChatGPT desktop app, selecting an approved Daybreak model
automatically switches the permissions control to **Approve for me** when that
mode is available for your account and allowed by organization policy. This
also applies when you use the desktop app's `/model` command. If that mode
isn't available, the current permission mode stays unchanged. Model selection
never overrides managed organization requirements.

Before enabling **Full Access** for an approved security model, the
ChatGPT desktop app shows a model-specific warning about dangerous actions. The
warning recommends **Approve for me** instead and links to
[reviewer-policy configuration](#configuration). The warning doesn't restore
the sandbox boundary or override organization policy.

## How auto-review works

At a high level, the flow is:

1. The main agent works inside `read-only` or `workspace-write`.
2. When it needs to cross the sandbox boundary, it requests approval.
3. If `approvals_reviewer = "auto_review"`, Codex routes that approval request
   to a separate reviewer agent instead of stopping for a person.
4. The reviewer decides whether the action should run and returns a rationale.
5. If the action is approved, execution continues. If it is denied, the main
   agent is instructed to find a materially safer path or stop and ask the
   user.

Auto-review is a reviewer swap, not a permission grant. It does not expand
`writable_roots`, enable network access, or weaken protected paths. It only
changes how Codex handles actions that already need approval.

## When it triggers

Auto-review evaluates approval requests that would otherwise pause for a human.
These include:

- Shell or exec tool calls that request escalated sandbox permissions.
- Network requests blocked by the current sandbox or policy.
- File edits outside the allowed writable roots.
- MCP or app tool calls that require approval based on their tool annotations
  or configured approval mode.
- Computer Use access to a new website or domain.

Auto-review does not run for routine actions already allowed inside the
sandbox. If a command can run under the active `sandbox_mode`, or a tool call
stays within the allowed policy, the main agent continues without review.

Computer Use is a separate case. App approvals for Computer Use still surface
directly to the user, so Auto-review does not replace those app-level prompts.

## What auto-review blocks

At a high level, Auto-review is designed to block actions such as:

- sending private data, secrets, or credentials to untrusted destinations
- probing for credentials, tokens, cookies, or session material
- broad or persistent security weakening
- destructive actions with significant risk of irreversible damage

The exact policy lives in the open-source Codex repository:
[policy_template.md](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy_template.md)
and
[policy.md](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md).
That policy can be customized per enterprise with `guardian_policy_config` or
per user with local [`[auto_review].policy`](/codex/config-file/config-advanced#approval-policies-and-sandbox-modes).

## What the reviewer sees

The reviewer is itself a Codex agent with a narrower job than the main agent:
decide whether a specific boundary-crossing action should run.

The reviewer sees a compact transcript plus the exact approval request. That
typically includes user messages, surfaced assistant updates, relevant tool
calls and tool outputs, and the action now being proposed for approval. It can
also perform read-only checks to gather missing context, but it does so rarely.

Hidden assistant reasoning is not included. Auto-review sees retained
chat items and tool evidence, not private chain-of-thought.

## Denials and failure behavior

An explicit denial is not treated like an ordinary sandbox error. Codex returns
the review rationale to the main agent and adds a stronger instruction:

- Do not pursue the same outcome via workaround, indirect execution, or policy
  circumvention.
- Continue only with a materially safer alternative.
- Otherwise, stop and ask the user.

Codex also applies a rejection circuit breaker per turn. In the current
open-source implementation, Auto-review interrupts the turn after `3`
consecutive denials or `10` denials within a rolling window of the last `50`
reviews in the same turn.

Any non-denial resets the consecutive-denial counter. When the breaker trips,
Codex emits a warning and aborts the current turn with an interrupt rather than
letting the agent loop on more escalation attempts.

Timeouts are surfaced separately from explicit denials, and the main agent is
informed that a timeout alone is not proof that the action is unsafe.

There is also an explicit override path for denied actions. In the current
open-source TUI, run `/approve` to open the **Auto-review Denials** picker, then
select one recent denied action to approve for one retry. Codex records up to 10
recent denials per task. That approval is narrow: it applies to the exact
denied action, not similar future actions; it is recorded for one retry in the
same context; and the retry still goes through Auto-review. Under the hood,
Codex injects a developer-scoped approval marker for that exact action. The
reviewer then sees that explicit user override as context, but it still follows
policy and can deny again if policy says the user cannot overwrite that class of
denial.

## Configuration

For setup details, see
[Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration#configure-automatic-review-policy).

The default reviewer policy is in the open-source Codex repository:
[core/src/guardian/policy.md](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md).
Enterprises can replace its tenant-specific section with
`guardian_policy_config` in managed requirements. Individual users can also set
a local
[`[auto_review].policy`](/codex/config-file/config-advanced#approval-policies-and-sandbox-modes)
in their `config.toml`, but managed requirements take precedence:

```toml
[auto_review]
policy = """
YOUR POLICY GOES HERE
"""
```

To customize the policy, copy the whole default policy wording first, then
iterate based on your individual risk profile.

## Configure an authorized cybersecurity engagement

For authorized security work, combine automatic review with a written
engagement scope and a least-privilege [permission profile](https://learn.chatgpt.com/docs/permissions).
Use an approved lab target, document the actions and engagement window, and
keep production systems, unrelated hosts, credentials, and persistent changes
out of scope unless explicitly authorized.

Both `[auto_review].policy` and `guardian_policy_config` replace your current
reviewer policy. They don't merge with policies bundled with your model or
managed by your organization. The built-in review instructions and response
format still apply. Before using either example, copy the complete current
policy, keep every existing rule, and add the rules for your approved work.
Replace the uppercase placeholder with that complete policy. If you can't
access the current policy, don't override it.

The following local `config.toml` template enables review and adds scoped
conditions after the existing reviewer policy:

```toml
approval_policy = "on-request"
approvals_reviewer = "auto_review"
default_permissions = ":workspace"

[auto_review]
policy = """
PASTE THE COMPLETE ACTIVE REVIEWER POLICY HERE BEFORE USING THIS EXAMPLE.

## Environment Profile
- Authorized target: lab.example.com.
- Approved actions: inspect the target, reproduce authorized vulnerabilities,
  and validate fixes within the documented engagement window.

## Tenant Risk Taxonomy and Allow/Deny Rules
- Allow only actions against the approved target that match the documented
  engagement scope and approved actions.
- Deny out-of-scope or unknown hosts, production access, credential theft,
  persistence, data exfiltration, destructive operations, and policy bypass.
- Deny ambiguous actions and high-impact changes until a human explicitly
  approves the exact target, action, and side effects.
"""
```

Replace the example target and allowed actions with the actual approved scope.
Enforce target restrictions with independent filesystem and network rules;
reviewer instructions don't replace those boundaries.

Organizations can enforce the same conditions in managed `requirements.toml`:

```toml
allowed_approval_policies = ["on-request"]
allowed_approvals_reviewers = ["auto_review"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
default_permissions = ":workspace"

guardian_policy_config = """
PASTE THE COMPLETE ACTIVE REVIEWER POLICY HERE BEFORE USING THIS EXAMPLE.

## Environment Profile
- Authorized target: lab.example.com.

## Tenant Risk Taxonomy and Allow/Deny Rules
- Allow only approved actions against the documented engagement target.
- Deny out-of-scope hosts, production access, credential theft, persistence,
  data exfiltration, destructive operations, and attempts to bypass policy.
- Deny ambiguous or high-impact actions until a human explicitly approves the
  exact target, action, and side effects.
"""

[allowed_permission_profiles]
":read-only" = true
":workspace" = true
# ":danger-full-access" is omitted, so it is denied.
```

`allowed_permission_profiles` controls current permission profiles.
`allowed_sandbox_modes` also prevents full access in deployments that still use
legacy `sandbox_mode`.

Managed `guardian_policy_config` takes precedence over a user's local
`[auto_review].policy`. Keep `approval_policy = "on-request"` or another
eligible interactive approval policy and keep an enforceable sandbox boundary.
With `approval_policy = "never"`, `:danger-full-access`, or `--yolo`, an action
can avoid creating the boundary-crossing approval request that review requires.

A network destination on the allowlist doesn't trigger review by itself. Add
explicit [command rules](https://learn.chatgpt.com/docs/agent-configuration/rules) with
`decision = "prompt"`, or configure sensitive MCP tools to require approval,
when actions inside the sandbox must still reach the reviewer.

See [Cyber Safety](https://learn.chatgpt.com/docs/cyber-safety) for model access, engagement setup, and
custom agent workflows, and [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration#configure-automatic-review-policy)
for enterprise precedence and supported client versions. For custom API or
Agents SDK harnesses, use [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals#review-cybersecurity-actions-before-execution).

## Reduce review volume without weakening security

Auto-review works best when the sandbox already covers your common safe
workflows. If too many mundane actions need review, fix the boundary first
instead of teaching the reviewer to approve noisy escalations forever.

In practice, the highest-leverage changes are:

- Add narrow
  [`writable_roots`](https://learn.chatgpt.com/docs/config-file/config-advanced#approval-policies-and-sandbox-modes)
  for scratch directories or neighboring repos you intentionally use.
- Add narrowly scoped [prefix rules](https://learn.chatgpt.com/docs/agent-configuration/rules). Prefer precise command
  prefixes such as `["cargo", "test"]` or `["pnpm", "run", "lint"]` over broad
  patterns such as `["python"]` or `["curl"]`. Broad rules often erase the very
  boundary Auto-review is meant to guard.

Auto-review session transcripts are retained under `~/.codex/sessions` by
default, so you can ask Codex to analyze past traffic there before changing
policy or permissions.

## Limits

Auto-review improves the default operating point for long-running agentic work,
but it is not a deterministic security guarantee.

- It only evaluates actions that ask to cross a boundary.
- It can still make mistakes, especially in adversarial or unusual contexts.
- It should complement, not replace, good sandbox design, monitoring, and
  organization-specific policy.

For the research rationale and published evaluation results, see the
[Alignment Research post on Auto-review](https://alignment.openai.com/auto-review/).
