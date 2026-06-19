---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/collections/security'
source_last_modified: '2026-06-18T23:48:24Z'
source_etag: 'W/"3a26446f93e7fb38b78d3a9f08503fb5"'
codex_cli_versions: ["0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0"]
codex_cli_versions_raw: ["codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0"]
---

# Security – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/use-cases/collections/security

Codex can help engineering and security teams assess authorized code, gather
evidence, and turn reviewed findings into focused fixes. These use cases cover
repository scans, change reviews, dependency incidents, and vulnerability
remediation.

## Assess a repository

Use the Codex Security plugin to run a comprehensive scan across an authorized
repository, review plausible findings, and produce reports that support human
triage. Comprehensive scans take longer because they repeat discovery across
independent workers.

[![](/codex/use-cases/deep-security-scan.webp)

### Run a deep security scan

Use the Codex Security plugin to run a more comprehensive audit of a repository or scoped...

Engineering  Quality](/codex/use-cases/deep-security-scan)

## Review changes before merge

Ask Codex to inspect a pull request, branch, commit, or working-tree diff for
security regressions and return evidence tied to the changed code.

[![](/codex/use-cases/scan-code-changes-for-security.webp)

### Scan code changes for security

Use the Codex Security plugin to examine a Git-backed change set, validate plausible...

Engineering  Quality](/codex/use-cases/scan-code-changes-for-security)

## Audit dependency incidents

Turn a public package or supply chain advisory into a read-only repository
audit covering manifests, lock files, scripts, workflows, and exposure paths.

[![](/codex/use-cases/dependency-incident-audits.webp)

### Audit dependency incidents

Use Codex to turn a public package or supply chain advisory into a read-only audit, then...

Engineering  Quality](/codex/use-cases/dependency-incident-audits)

## Remediate reviewed findings

Bring Codex an approved finding from a security report, advisory, or ticket,
then have it make a minimal fix and verify that the vulnerable behavior no
longer reproduces.

[![](/codex/use-cases/remediate-vulnerability-backlog.webp)

### Remediate a vulnerability backlog

Bring in approved findings from ticketing tools or vulnerability reporting systems, then use...

Engineering  Quality](/codex/use-cases/remediate-vulnerability-backlog)

