---
source_type: 'developers'
source_area: 'codex_concept'
source_url: 'https://developers.openai.com/codex/concepts/sandboxing/auto-review'
source_last_modified: '2026-05-12T01:57:53Z'
source_etag: 'W/"eec197fbdf8186d24452e7fc9a29dbff"'
codex_cli_versions: ["0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0"]
codex_cli_versions_raw: ["codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0"]
---

# Auto-review – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/concepts/sandboxing/auto-review

Auto-review replaces manual approval at the sandbox boundary with a separate
reviewer agent. The main Codex agent still runs inside the same sandbox, with
the same approval policy and the same network and filesystem limits. The
difference is who reviews eligible escalation requests.

Auto-review only applies when approvals are interactive. In practice, that
means `approval_policy = "on-request"` or a granular approval policy that
still surfaces the relevant prompt category. With `approval_policy = "never"`,
there is nothing to review.

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
- Browser Use access to a new website or domain.

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
[policy\_template.md](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy_template.md)
and
[policy.md](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md).
That policy can be customized per enterprise with `guardian_policy_config` or
per user with local [`[auto_review].policy`](/codex/config-advanced#approval-policies-and-sandbox-modes).

## What the reviewer sees

The reviewer is itself a Codex agent with a narrower job than the main agent:
decide whether a specific boundary-crossing action should run.

The reviewer sees a compact transcript plus the exact approval request. That
typically includes user messages, surfaced assistant updates, relevant tool
calls and tool outputs, and the action now being proposed for approval. It can
also perform read-only checks to gather missing context, but it does so rarely.

Hidden assistant reasoning is not included. Auto-review sees retained
conversation items and tool evidence, not private chain-of-thought.

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
recent denials per thread. That approval is narrow: it applies to the exact
denied action, not similar future actions; it is recorded for one retry in the
same context; and the retry still goes through Auto-review. Under the hood,
Codex injects a developer-scoped approval marker for that exact action. The
reviewer then sees that explicit user override as context, but it still follows
policy and can deny again if policy says the user cannot overwrite that class of
denial.

## Configuration

For setup details, see
[Managed configuration](/codex/enterprise/managed-configuration#configure-automatic-review-policy).

The default reviewer policy is in the open-source Codex repository:
[core/src/guardian/policy.md](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md).
Enterprises can replace its tenant-specific section with
`guardian_policy_config` in managed requirements. Individual users can also set
a local
[`[auto_review].policy`](/codex/config-advanced#approval-policies-and-sandbox-modes)
in their `config.toml`, but managed requirements take precedence:

```
[auto_review]
policy = """
YOUR POLICY GOES HERE
"""
```

To customize the policy, copy the whole default policy wording first, then
iterate based on your individual risk profile.

## Reduce review volume without weakening security

Auto-review works best when the sandbox already covers your common safe
workflows. If too many mundane actions need review, fix the boundary first
instead of teaching the reviewer to approve noisy escalations forever.

In practice, the highest-leverage changes are:

- Add narrow
  [`writable_roots`](/codex/config-advanced#approval-policies-and-sandbox-modes)
  for scratch directories or neighboring repos you intentionally use.
- Add narrowly scoped [prefix rules](/codex/rules). Prefer precise command
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

