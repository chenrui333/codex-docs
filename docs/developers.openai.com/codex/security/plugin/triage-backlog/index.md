---
source_type: 'developers'
source_area: 'codex_security'
source_url: 'https://developers.openai.com/codex/security/plugin/triage-backlog'
source_last_modified: '2026-06-25T00:57:56Z'
source_etag: 'W/"5a87adfb342aa7886c72678769bd0946"'
codex_cli_versions: ["0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0"]
codex_cli_versions_raw: ["codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0"]
---

# Triage a backlog – Codex Security | OpenAI Developers

Source: https://developers.openai.com/codex/security/plugin/triage-backlog

Use `$codex-security:triage-finding` to review existing security findings
against the current repository. This workflow performs a read-only static
analysis: Codex treats each finding as an unproven claim and inspects repository
evidence without executing the code.

Run this workflow from a Codex project scoped to the repository you want to
assess. Codex must be able to read the repository’s source code. Jira, Linear,
and GitHub connectors provide finding data, but they don’t replace access to
the source code.

Under the hood, Codex starts from the cited code or version information. It
traces the claimed attacker-controlled source, relevant security controls,
dangerous sink, and reachable path. It also checks the product surface and trust
boundary, looks for counterevidence, and records proof gaps. Codex then returns
one verdict per finding and ranks the findings that need action or further
review.

This differs from `$codex-security:validation`, which can build or run code,
create a focused test or proof of concept, or exercise a real interface to
reproduce or disprove a finding. Use triage to classify and prioritize an
existing backlog. Use validation when runtime evidence could resolve a finding
that static evidence leaves uncertain.

Backlog triage starts from existing findings. To search the repository for new
vulnerabilities, [run a security scan](/codex/security/plugin/scans). Triage
doesn’t modify the repository or implement fixes.

## Choose the findings to triage

You can supply one finding or a collection from these sources:

| Source | What to provide | Requirements |
| --- | --- | --- |
| Pasted or local findings | SARIF results, a CVE or GHSA, an advisory, a scanner ticket, a bug bounty report, a Codex Security finding artifact, or a plain-language vulnerability claim. | No connector required. |
| Jira or Linear | Exact security or vulnerability issue URLs or identifiers, Jira JQL, or a Linear team, project, or search phrase. Codex retrieves the selected issue content before triage. | [Jira through Atlassian Rovo](codex://plugins/plugin_connector_692de805e3ec8191834719067174a384) or [Linear](codex://plugins/plugin_asdk_app_69a089a326dc8191b32a3f2553f5be2c) with read access. |
| GitHub | A repository and one finding source: code scanning, `Dependabot` vulnerabilities and malware, security advisories and private vulnerability reports, or all sources. If you don’t specify a repository, Codex uses the GitHub repository attached to the current Codex project when available. GitHub Issues aren’t included in the default GitHub sources; provide a specific issue or ask for GitHub Issues explicitly when you want to triage them. | [GitHub](codex://plugins/plugin_connector_1p_1a69035c238881919c4190932b2df699) with access to the selected repository and finding type. |

Codex keeps one result for every supplied finding, in input order, so each
source finding stays traceable. It doesn’t merge or drop findings that look
like duplicates.

## Run read-only triage

For pasted findings or local artifacts, send a prompt like:

```
Use $codex-security:triage-finding to triage these existing security findings against this repository:

[Paste the findings or provide the artifact path.]
```

For Jira or Linear issues, identify the issue set and keep the source system
read-only:

```
Use $codex-security:triage-finding to import and triage the security findings from [Jira or Linear issue URLs, identifiers, or query] against this repository.
Do not change the source issues.
```

For GitHub findings, name the repository and source:

```
Use $codex-security:triage-finding to import and triage [code scanning, Dependabot vulnerabilities and malware, security advisories and private vulnerability reports, or all] from [owner/repository] against this repository.
```

To use the GitHub repository attached to the current Codex project, specify
only the finding source:

```
Use $codex-security:triage-finding to import and triage [code scanning, Dependabot vulnerabilities and malware, security advisories and private vulnerability reports, or all] from GitHub against this repository. Use the GitHub repository attached to the current Codex project.
```

The workflow proceeds in this order:

1. Collect and organize the findings

   Codex retrieves any requested issue or GitHub content, preserves source
   identifiers and references, and creates one triage item per input. It builds
   the complete item list before assigning verdicts.
2. Confirm the repository context

   Codex resolves the current repository and revision when available. It reads
   `SECURITY.md` when present so supported versions, trusted inputs, product
   boundaries, and out-of-scope surfaces inform the assessment.
3. Inspect the static evidence

   For each finding, Codex traces the claimed attacker-controlled source,
   relevant security control, vulnerable sink, reachable path, and supported
   security boundary. It records supporting evidence, evidence against the
   claim, and proof gaps.
4. Assign verdicts and ranks

   Codex assigns a verdict and confidence to every finding. It ranks
   `confirmed` and `needs_review` findings by exploitability in separate queues.

## Review the results

| Verdict | What it means |
| --- | --- |
| `confirmed` | Repository evidence shows that the vulnerable path is reachable under the stated preconditions and crosses a supported security boundary. |
| `not_actionable` | Repository evidence rules out the claim, such as by showing an unaffected version, unreachable path, effective guard, or non-shipped surface. |
| `needs_review` | Repository evidence isn’t enough to decide because required information is missing, ambiguous, runtime-dependent, environment-dependent, or policy-dependent. |

Exploitability ranks use positive integers starting at `1`, independently
within each verdict queue. This keeps remediation priorities separate from
unresolved review work. Rank `1` is the most exploitable `confirmed` finding
or the highest-priority `needs_review` finding in that result set. The rank
isn’t a scanner severity score, and `not_actionable` findings aren’t ranked.

For each finding, review:

- the rationale for the verdict and rank
- supporting evidence and evidence against the claim
- open questions and remaining proof gaps
- the affected location and component
- the product surface and source trust level
- the recommended next step
- the [`$codex-security:fix-finding`](/codex/security/plugin/fix-findings)
  handoff, when the finding is `confirmed`

Triage is complete when every supplied finding has one result, Codex preserves
its source identifier, and any uncertainty is explicit. Jira, Linear, and other
backlog records remain unchanged unless you ask Codex to write back after
reviewing the triage results.

## Next steps

- `confirmed`: After a person accepts the finding for remediation, use
  [`$codex-security:fix-finding`](/codex/security/plugin/fix-findings) to fix and
  verify it. Triage prepares a prompt-ready handoff but doesn’t invoke the skill
  automatically.
- `needs_review`: If running code can resolve the proof gap, use
  `$codex-security:validation` to perform bounded dynamic validation. Pass
  the finding claim, affected locations, preconditions, static evidence, and
  proof gaps from the triage result:

  ```
  Use $codex-security:validation to dynamically validate finding [triage item ID or source ID] from the backlog triage result. Use the strongest realistic, bounded method, record exactly what was tested, and preserve any remaining proof gaps.
  ```

  Unlike triage, validation may build or run code, create a focused test or
  proof of concept, or exercise a real interface. Review the proposed commands
  before approving them and keep [Codex approval and security
  policies](/codex/agent-approvals-security) in place.
- `needs_review`: If the finding depends on product policy or deployment
  context, answer the listed open questions before changing code.
- `not_actionable`: Keep the evidence with your triage record. Codex doesn’t
  automatically close or update the source ticket.
- To look for vulnerabilities beyond the supplied backlog, [run a security
  scan](/codex/security/plugin/scans).

