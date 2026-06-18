---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/deep-security-scan'
source_last_modified: '2026-06-05T17:42:54Z'
source_etag: 'W/"4d05fd8f9152c2498e50d19646394e88"'
codex_cli_versions: ["0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0"]
codex_cli_versions_raw: ["codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0"]
---

# Run a deep security scan | Codex use cases

Source: https://developers.openai.com/codex/use-cases/deep-security-scan

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Run a deep security scan

Search an authorized repository deeply for plausible vulnerabilities.

Difficulty **Advanced**

Time horizon **Long-running**

Use the Codex Security plugin to run a higher-recall, repository-wide audit that repeats discovery, validates candidates, and produces reviewable report artifacts.

## Best for

- Application security reviews of a complete repository that you own or are authorized to assess.
- High-recall reviews where additional runtime and token use are appropriate for finding more candidate issues.
- Security teams that need traceable finding evidence before deciding what to remediate.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/deep-security-scan/?export=pdf)

Use the Codex Security plugin to run a higher-recall, repository-wide audit that repeats discovery, validates candidates, and produces reviewable report artifacts.

Advanced

Long-running

Related links

[Codex Security plugin](/codex/security/plugin)  [Agent approvals and security](/codex/agent-approvals-security)  [Codex cyber safety](/codex/concepts/cyber-safety)

## Best for

- Application security reviews of a complete repository that you own or are authorized to assess.
- High-recall reviews where additional runtime and token use are appropriate for finding more candidate issues.
- Security teams that need traceable finding evidence before deciding what to remediate.

## Skills & Plugins

- [Codex Security:deep Security Scan](/codex/security/plugin)

  Run repeated repository-wide security discovery passes, validate surviving findings, analyze attack paths, and create reviewable reports.

| Skill | Why use it |
| --- | --- |
| [Codex Security:deep Security Scan](/codex/security/plugin) | Run repeated repository-wide security discovery passes, validate surviving findings, analyze attack paths, and create reviewable reports. |

## Starter prompt

/goal Run a deep security scan on this repository. Do not stop until all required steps are complete and the final report is ready.
Scope and rules:
- I am authorized to assess this repository.
- Treat the entire repository as in scope.
- Use the Codex Security plugin's deep scan workflow; do not broaden this into a diff or scoped-path review.
- Keep the scan read-only; do not modify code, open pull requests, or test external targets.
Return the final Markdown and HTML report paths and summarize the findings that require human review first.

Open in the Codex app

/goal Run a deep security scan on this repository. Do not stop until all required steps are complete and the final report is ready.
Scope and rules:
- I am authorized to assess this repository.
- Treat the entire repository as in scope.
- Use the Codex Security plugin's deep scan workflow; do not broaden this into a diff or scoped-path review.
- Keep the scan read-only; do not modify code, open pull requests, or test external targets.
Return the final Markdown and HTML report paths and summarize the findings that require human review first.

## Choose a deep repository review

Use a deep scan when you need high-recall vulnerability discovery across a
complete repository and can budget for a longer run. The Codex Security plugin
repeats discovery passes before validating and prioritizing findings, so this
workflow takes more time and tokens than an ordinary scan.

A deep scan is for an entire repository. To review one package or directory,
use `$codex-security:security-scan`. To review a pull request, commit, branch
diff, or working-tree patch, use
[$codex-security:security-diff-scan](/codex/use-cases/scan-code-changes-for-security).

## Prepare an authorized scan

1. Open the repository in Codex and install the [Codex Security plugin](/codex/security/plugin).
2. Confirm that you own the repository or have authorization to assess it.
3. Add repository-specific architecture, trust-boundary, build, test, and validation guidance in `AGENTS.md` when it will improve the review.
4. Run the starter prompt and let the scan complete its repeated discovery, validation, attack-path analysis, and final reporting stages.
5. Review the final reports before asking Codex to change code or reproduce a finding further.

## Review evidence before remediation

The final result should identify affected locations, why the behavior is
reachable, what validation Codex performed, any remaining proof gaps, and a
bounded remediation direction. Distinguish findings without validation evidence
from validated findings.

Start remediation only for a finding you have selected and reviewed. Use
[Remediate a vulnerability backlog](/codex/use-cases/remediate-vulnerability-backlog)
to fix findings one at a time with focused regression validation.

## Related use cases

[![](/codex/use-cases/scan-code-changes-for-security.webp)

### Scan code changes for security

Use the Codex Security plugin to examine a Git-backed change set, validate plausible...

Engineering  Quality](/codex/use-cases/scan-code-changes-for-security)[![](/codex/use-cases/dependency-incident-audits.webp)

### Audit dependency incidents

Use Codex to turn a public package or supply chain advisory into a read-only audit, then...

Engineering  Quality](/codex/use-cases/dependency-incident-audits)[![](/codex/use-cases/remediate-vulnerability-backlog.webp)

### Remediate a vulnerability backlog

Bring in approved findings from ticketing tools or vulnerability reporting systems, then use...

Engineering  Quality](/codex/use-cases/remediate-vulnerability-backlog)

