---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/faq'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Codex Security Cloud FAQ

Source: https://learn.chatgpt.com/docs/security/faq

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

This FAQ covers the Codex Security Cloud plugin. For local scans and workflows that run in
a Codex task, see the [Codex Security plugin quickstart](https://learn.chatgpt.com/docs/security/plugin).

{/* vale Microsoft.Auto = NO */}
{/* vale Vale.Spelling = NO */}

## Getting started

### What is Codex Security Cloud?

Codex Security Cloud scans connected GitHub repositories, validates likely
vulnerabilities, and presents findings with evidence and remediation guidance.
Use its plugin on the web or in the desktop app to run repository scans and
monitor new commits.

### How do I open Codex Security Cloud?

Open **Plugins** to find and install **Codex Security Cloud**, then open it.
See [Cloud setup](https://learn.chatgpt.com/docs/security/setup) for the full workflow.

### Is this the same plugin as local Codex Security?

No. The Codex Security Cloud plugin scans connected GitHub repositories in
Codex cloud. The [Codex Security plugin](https://learn.chatgpt.com/docs/security/plugin) runs local
scans in a Codex task.

### What if access is unavailable?

Check with your workspace administrator.

### How does Codex Security work?

Codex Security runs analysis in an ephemeral, isolated container and temporarily clones the target repository. It performs code-level analysis and returns structured findings with a description, file and location, criticality, root cause, and a suggested remediation.

For findings with verification steps, it runs commands or tests in the sandbox and attaches the results as evidence.

### Does it replace SAST?

No. Codex Security complements SAST. It adds semantic, LLM-based reasoning and automated validation, while existing SAST tools still provide broad deterministic coverage.

## Billing

### How are Cloud scans billed?

Repository scans and continuous scans set up after October 1, 2026, at
12:53 PM Pacific are billed based on token usage at your plan's rates, in
credits or USD depending on your billing plan. For
[eligible accounts](#do-i-get-a-free-scanning-period-or-free-scanning-credits),
free scanning credits apply before paid usage is billed.

This usage is not covered by your plan's included usage allowance.

Continuous scans set up before that cutoff are free for 14 days, until
October 15, 2026. After that, they are billed at regular token rates under
your account's billing plan if you enable paid usage. Otherwise, they pause.

### Do I get a free scanning period or free scanning credits?

What you receive depends on whether your account had continuous scanning set
up before October 1, 2026, at 12:53 PM Pacific:

- If it did, your covered continuous scans remain free until October 15, 2026.
  This free period doesn't cover repository scans or continuous scanning set
  up after October 1, 2026, at 12:53 PM Pacific.
- If it didn't, eligible accounts receive $500 in free scanning credits
  instead of the free continuous-scanning period.

### How do free scanning credits work?

Repository scans and continuous scanning use the same free balance. In a
workspace, everyone shares that balance. These free scanning credits don't
expire.

When the free balance runs out, further scanning is billed under your
account's or workspace's billing plan.

### What happens when the free continuous-scanning period ends?

Select **Keep scans running** and enable paid usage to continue these scans
after the free period. They are then billed at regular token rates under
your account's or workspace's billing plan.

If you opt out or don't enable paid usage, those scans pause when the free
period ends. Select **Re-enable scans** to enable paid usage afterward.
In a workspace, ask a workspace owner to make this choice if you don't have
permission.

### Where can I see token usage and charges?

Open a scan in **Scans** to review its token usage and cost. Hover over the
token count to see input, cached input, and output tokens. Cached input is
included in the input count, not added on top of it.

Usage shows the cost before free scanning credits or billing exemptions,
along with any amount covered by free scanning credits.

Scans marked "Exempt from billing. No charges apply." incur no charges,
even when they show token usage and cost.

## Features

### What is the analysis pipeline?

1. **Analysis** builds a threat model for the repository.
2. **Scanning** reviews the repository once or monitors commit changes for likely issues.
3. **Validation** tries to reproduce likely vulnerabilities in a sandbox to reduce false positives.
4. **Remediation** provides guidance and, where available, proposed patches to review before opening a PR.

### What languages are supported?

Codex Security is language-agnostic. In practice, performance depends on the model's reasoning ability for the language and framework used by the repository.

### What outputs do I get after the scan completes?

You get ranked findings with criticality, validation evidence, remediation guidance, and a proposed patch when one is available.

### How is customer code isolated?

Each analysis and validation job runs in an ephemeral Codex container with session-scoped tools. Artifacts are extracted for review, and the container is torn down after the job completes.

### Does Codex Security auto-apply patches?

No. When a finding has a proposed patch, review it before selecting **Create draft pull request**.

### Does the project need to be built for scanning?

No. Codex Security can produce findings from repository and commit context without a compile step. During auto-validation, it may try to build the project inside the container if that helps reproduce the issue. For environment setup details, see [Codex cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment).

### How does Codex Security reduce false positives and avoid broken patches?

Codex Security uses two stages. First, the model ranks likely issues. Then auto-validation tries to reproduce each issue in a clean container. Findings that successfully reproduce are marked as validated, which helps reduce false positives before human review.

### How do repository scans and commit monitoring differ?

A **Repository** scan runs once across the repository. **Commit changes**
monitors new commits and can review existing commit history. See
[Monitor new commits](https://learn.chatgpt.com/docs/security/setup#5-monitor-new-commits).

### How long do scans take?

Scan time varies with repository size and validation work. Check **Scans** for
progress and status.

### Can I pause commit monitoring?

Yes. Open **Repositories**, select the repository, and open **Monitoring
settings**. Set monitoring to **Paused** and select **Save**.

### What is a threat model?

A threat model is the scan-time security context for a repository. It combines a concise project overview with attack-surface details such as entry points, trust boundaries, auth assumptions, and risky components. For more detail, see [Improving the threat model](https://learn.chatgpt.com/docs/security/threat-model).

### How is a threat model generated?

Codex Security analyzes the repository's code to summarize its architecture and security entry points.

### Does it replace manual security review?

No. Codex Security accelerates review and helps rank findings, but it does not replace code-level validation, exploitability checks, or human threat assessment.

### Can I edit the threat model?

For a monitored repository, Codex Security creates the initial threat model. Open the repository's **Monitoring settings** to update it as the architecture, risks, and business context change. For the editing workflow, see [Improving the threat model](https://learn.chatgpt.com/docs/security/threat-model).

### What does the proposed patch contain?

The proposed patch contains a minimal actionable diff with filename and line context when a remediation can be generated for the finding.

### Does the patch directly modify my PR branch?

No. The workflow generates a diff, patch file, or suggested change for maintainers and reviewers to inspect before applying.

## Validation

### What is auto-validation?

Auto-validation is the phase that tries to reproduce a suspected issue in an isolated container. It records whether reproduction succeeded or failed and captures logs, commands, and related artifacts as evidence.

### What happens if validation fails?

The finding remains unvalidated. Logs and reports still capture what was attempted so engineers can retry, investigate further, or adjust the reproduction steps.

{/* vale Microsoft.Auto = YES */}
{/* vale Vale.Spelling = YES */}
