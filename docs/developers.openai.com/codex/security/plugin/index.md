---
source_type: 'developers'
source_area: 'codex_security'
source_url: 'https://developers.openai.com/codex/security/plugin'
source_last_modified: '2026-05-28T18:57:31Z'
source_etag: 'W/"772379012d01e3a9352762c35f5794de"'
codex_cli_versions: ["0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0"]
codex_cli_versions_raw: ["codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0"]
---

# Plugin – Codex Security | OpenAI Developers

Source: https://developers.openai.com/codex/security/plugin

The Codex Security plugin adds security-review workflows to Codex for code that
you have authorization to assess. Use it from an open repository to investigate
a codebase, review a change set for security regressions, confirm plausible
findings, and prepare minimal fixes for review.

This page covers the installable plugin that runs in your Codex thread. For
the research-preview product that scans connected GitHub repositories through
Codex Web, see [Codex Security](/codex/security).

## Install the plugin

[Install the Codex Security plugin](codex://plugins/install/codex-security?marketplace=openai-curated)

After installation, start a new thread in the repository you want to
assess.

1. Open Codex

   Start Codex from your repository:

   ```
   codex
   ```
2. Open the plugin browser

   Enter:

   ```
   /plugins
   ```
3. Install Codex Security

   Search for **Codex Security**, open it, and select `Install plugin`.
4. Start a new thread

   Start a new thread in the repository you are authorized to review.

## Choose a security workflow

Choose the narrowest workflow that answers your question. A diff-focused scan
is faster to review than a repository-wide scan; a deep scan intentionally uses
more time and tokens to search for more candidate findings.

| Goal | Skill | Scope and output |
| --- | --- | --- |
| Review a repository or one scoped path | `$codex-security:security-scan` | Runs threat modeling, finding discovery, validation, attack-path analysis, and produces Markdown and HTML reports. |
| Run a higher-recall audit | `$codex-security:deep-security-scan` | Repeats repository-wide discovery with delegated workers before validation and reporting. Use it only for an entire repository. |
| Review a change before merge | `$codex-security:security-diff-scan` | Reviews a pull request, commit, branch diff, or working-tree patch and produces a Markdown report grounded in changed code. |
| Fix one finding | `$codex-security:fix-finding` | Reproduces or validates one plausible finding, makes a minimal fix when needed, and checks that the vulnerable behavior no longer reproduces. |

For example, to scan a repository:

```
Use $codex-security:security-scan to scan this repository for security
vulnerabilities. Keep the scan grounded in code evidence, validate plausible
findings where feasible, and return the final report paths. Do not modify code.
```

To review the current change instead:

```
Use $codex-security:security-diff-scan to review the current branch diff for
security regressions. Keep the review scoped to changed code and directly
supporting files. Do not modify code.
```

## Review the result and fix findings

Repository scans use a staged workflow:

1. **Threat modeling** identifies entry points, trust boundaries, sensitive
   actions, and risky components.
2. **Finding discovery** looks for concrete source-to-sink paths or broken
   controls in the requested scope.
3. **Validation** tests or otherwise verifies plausible findings and records
   evidence or proof gaps.
4. **Attack-path analysis** traces exploitable paths and rates severity for
   findings that survive validation.
5. **Reporting** writes findings, affected locations, validation evidence,
   remediation guidance, and review directives to artifacts.

An ordinary repository scan or a deep scan writes `report.md` and a readable
`report.html` within its scan directory. A diff scan writes a focused Markdown
report. Review affected files, evidence, assumptions, and severity before
starting remediation.

When a finding is actionable, ask for a bounded fix:

```
Use $codex-security:fix-finding to fix finding [finding ID or report
reference]. Add focused regression coverage, verify legitimate behavior still
works, and show that the original issue no longer reproduces. Do not broaden
the change beyond this finding.
```

## Keep security work authorized and reviewable

Run scans only against repositories, diffs, and systems that you own or that
your organization authorizes you to assess. A finding is an input to review,
not an instruction to merge code or test unrelated targets.

- Keep the first scan read-only unless you explicitly ask Codex to prepare a
  fix.
- Review commands that build, run, or reproduce behavior before approving
  them, especially in unfamiliar repositories.
- Review every proposed patch and validation result before merging it.
- Keep repository instructions and approval policies in place while using the
  plugin. For details, see [Agent approvals and security](/codex/agent-approvals-security).

## Explore security use cases

- [Run a deep security scan](/codex/use-cases/deep-security-scan)
- [Scan code changes for security](/codex/use-cases/scan-code-changes-for-security)
- [Remediate a vulnerability backlog](/codex/use-cases/remediate-vulnerability-backlog)

