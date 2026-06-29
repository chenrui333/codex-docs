---
source_type: 'developers'
source_area: 'codex_use_case'
source_url: 'https://developers.openai.com/codex/use-cases/scan-code-changes-for-security'
source_last_modified: '2026-06-18T23:13:09Z'
source_etag: 'W/"b5c2ef6705d8c931294655f8c7b1f6ff"'
codex_cli_versions: ["0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4"]
codex_cli_versions_raw: ["codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4"]
---

# Scan code changes for security | Codex use cases

Source: https://developers.openai.com/codex/use-cases/scan-code-changes-for-security

Codex use cases

![](/assets/OpenAI-black-wordmark.svg)

![Codex](/assets/OAI_Codex-Lockup_Fallback_Black.svg)

Codex use case

# Scan code changes for security

Review a pull request or local diff for security regressions.

Difficulty **Intermediate**

Time horizon **30m**

Use the Codex Security plugin to examine a Git-backed change set, validate plausible security regressions, and produce an evidence-based report before merge.

## Best for

- Pull requests that touch authentication, authorization, parsing, file access, secrets, or privileged workflows.
- Release branches or local patches that need a security-focused check before merge.
- Reviewers who need findings anchored to changed code and directly supporting files.

# Contents

[← All use cases](/codex/use-cases)

Copy page   [Export as PDF](/codex/use-cases/scan-code-changes-for-security/?export=pdf)

Use the Codex Security plugin to examine a Git-backed change set, validate plausible security regressions, and produce an evidence-based report before merge.

Intermediate

30m

Related links

[Security change-review guide](/codex/security/plugin/code-changes)  [Review GitHub pull requests](/codex/use-cases/github-code-reviews)  [Agent approvals and security](/codex/agent-approvals-security)

## Best for

- Pull requests that touch authentication, authorization, parsing, file access, secrets, or privileged workflows.
- Release branches or local patches that need a security-focused check before merge.
- Reviewers who need findings anchored to changed code and directly supporting files.

## Skills & Plugins

- [Codex Security:security Diff Scan](/codex/security/plugin/code-changes)

  Review a pull request, commit, branch diff, or working-tree patch for security regressions with validation and attack-path evidence.

| Skill | Why use it |
| --- | --- |
| [Codex Security:security Diff Scan](/codex/security/plugin/code-changes) | Review a pull request, commit, branch diff, or working-tree patch for security regressions with validation and attack-path evidence. |

## Starter prompt

Use $codex-security:security-diff-scan to review this PR, commit, branch diff, or working-tree patch for security regressions.
Scope and rules:
- Target: [this pull request / commit SHA / branch diff from BASE to HEAD / the current working-tree patch]
- I am authorized to assess this repository and change set.
- Pay particular attention to [auth, input handling, secrets, filesystem, network, dependencies, or other sensitive surface].
Return the final Markdown report and any Codex app review directives for findings that require human review.

Open in the Codex app

Use $codex-security:security-diff-scan to review this PR, commit, branch diff, or working-tree patch for security regressions.
Scope and rules:
- Target: [this pull request / commit SHA / branch diff from BASE to HEAD / the current working-tree patch]
- I am authorized to assess this repository and change set.
- Pay particular attention to [auth, input handling, secrets, filesystem, network, dependencies, or other sensitive surface].
Return the final Markdown report and any Codex app review directives for findings that require human review.

## Review the change instead of the whole repository

Use a security diff scan when a pull request, commit, branch, or local patch
changes a sensitive code path. The Codex Security plugin uses repository
context to understand the change, then keeps finding discovery and validation
focused on the diff and directly supporting code.

This workflow complements ordinary code review. Use it when you want evidence
about security regressions, not a general style or test review.

## Run a focused pass

1. Open the repository and check out or describe the exact Git-backed change set to review.
2. Complete the [Codex Security plugin quickstart](/codex/security/plugin) and specify the pull request, commit, branch diff, or working-tree patch in the starter prompt.
3. Name high-risk surfaces in the change, such as authentication, parsers, file paths, network requests, or credential handling.
4. Run the prompt without requesting a fix so the first result remains a review artifact.
5. Check each reported affected line, validation result, and stated proof gap before deciding whether to remediate.

## Follow through on a finding

A useful report distinguishes a reachable, supported security finding from a
suspicion that still needs confirmation and can include Codex app review
directives for affected lines. For an actionable result, open a new bounded
fix task with the finding identifier or the relevant report section.
See [Remediate a vulnerability backlog](/codex/use-cases/remediate-vulnerability-backlog)
for the fix-and-validation loop.

For change selectors, diff scope, and result review, see [Review code changes
for security](/codex/security/plugin/code-changes).

## Related use cases

[![](/codex/use-cases/deep-security-scan.webp)

### Run a deep security scan

Use the Codex Security plugin to run a more comprehensive audit of a repository or scoped...

Engineering  Quality](/codex/use-cases/deep-security-scan)[![](/codex/use-cases/dependency-incident-audits.webp)

### Audit dependency incidents

Use Codex to turn a public package or supply chain advisory into a read-only audit, then...

Engineering  Quality](/codex/use-cases/dependency-incident-audits)[![](/codex/use-cases/remediate-vulnerability-backlog.webp)

### Remediate a vulnerability backlog

Bring in approved findings from ticketing tools or vulnerability reporting systems, then use...

Engineering  Quality](/codex/use-cases/remediate-vulnerability-backlog)

