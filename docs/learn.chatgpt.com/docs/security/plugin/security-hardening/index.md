---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin/security-hardening'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1"]
---

# Propose security hardening

Source: https://learn.chatgpt.com/docs/security/plugin/security-hardening

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use `$codex-security:propose-security-hardening` to turn a collection of
security evidence into structural or architectural hardening options. The
workflow can analyze a completed Codex Security scan or start from supplied
findings, disclosure reports, incident reviews, assessment documents, and
source code.

The result is a design portfolio, not a patch, and doesn't prove that it fixes a
vulnerability. Codex changes the repository only after you select an option and
explicitly ask it to make that change.

## Prepare the evidence

Provide the workflow with:

- A scan directory or an explicit collection of findings and reports.
- The target source tree and relevant revision or snapshot when available.
- PoCs, traces, incident evidence, or assessment material that supports the
  findings.
- Constraints for performance, memory, compatibility, reliability, operations,
  delivery time, or change scope.

The workflow uses the evidence to identify repeated broken invariants, dispersed
controls, privileged choke points, weak isolation boundaries, and recurring
remediation patterns. It can also conclude that local fixes are more
proportionate than an architectural change.

## Run the workflow

Send a prompt like:

```text
Use $codex-security:propose-security-hardening to analyze [scan directory or finding paths] against [source tree and revision]. Develop evidence-backed structural hardening options with engineering tradeoffs, before-and-after diagrams, a migration plan, and an implementation handoff. Do not modify the repository.
```

## Review the portfolio

A useful portfolio should:

- Connect each proposed change to concrete findings, source, and threat-model
  evidence.
- Describe the current design and the security invariants the new design should
  preserve.
- Compare distinct options, including residual risk, performance,
  reliability, operations, compatibility, and migration cost.
- Recommend an option only when the evidence supports it, with explicit
  assumptions and open questions.
- Include rollout, validation, rollback, and implementation guidance.
- Separate observed facts, inferences, and proposed design properties.

Review the evidence and tradeoffs before choosing an option. An architecture
diagram or design recommendation doesn't replace validation of the original
findings or the implemented fix.

## Use hardening guidance from a scan

When a standard, deep, or change scan has reportable findings, Codex runs this
workflow once after the detailed vulnerability reports are ready. It writes the
portfolio to `hardening/hardening.md`, structured analysis to
`hardening/hardening.json`, and supporting proposals or diagrams under
`hardening/`. The scan links the portfolio from `report.md`.

Keep the full scan directory together so those links remain usable. To review
the individual reports that inform the portfolio, see [Write vulnerability
reports](https://learn.chatgpt.com/docs/security/plugin/vulnerability-reports).
