---
source_type: 'developers'
source_area: 'codex_security'
source_url: 'https://developers.openai.com/codex/security'
source_last_modified: '2026-05-28T18:51:28Z'
source_etag: 'W/"abc2d55c1fdb28c15a5816e923c91e5e"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0"]
---

# Security – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/security

[Install plugin in Codex App](https://chatgpt.com/plugins/share/676aca3811d54fa7bcdef5255236b3c4)

For installation steps, supported skills, and review boundaries, see the
[Codex Security plugin guide](/codex/security/plugin).

### Explore plugin use cases

- [Run a deep security scan](/codex/use-cases/deep-security-scan) to perform a higher-recall repository-wide audit.
- [Scan code changes for security](/codex/use-cases/scan-code-changes-for-security) before you merge a pull request or branch.
- [Remediate a vulnerability backlog](/codex/use-cases/remediate-vulnerability-backlog) with bounded fixes for approved findings.

The plugin runs in your Codex thread. Codex Security cloud scans connected
GitHub repositories through Codex Web. For Codex sandboxing, approvals,
network controls, and admin settings, see [Agent approvals &
security](/codex/agent-approvals-security).

## Codex Security cloud

Codex Security cloud is currently in research preview. It scans connected
GitHub repositories for likely security issues.

It helps teams:

1. **Find likely vulnerabilities** by using a repo-specific threat model and real code context.
2. **Reduce noise** by validating findings before you review them.
3. **Move findings toward fixes** with ranked results, evidence, and suggested patch options.

## How Codex Security cloud works

Codex Security scans connected repositories commit by commit.
It builds scan context from your repo, checks likely vulnerabilities against that context, and validates high-signal issues in an isolated environment before surfacing them.

You get a workflow focused on:

- repo-specific context instead of generic signatures
- validation evidence that helps reduce false positives
- suggested fixes you can review in GitHub

## Codex Security cloud access and prerequisites

Codex Security is available for ChatGPT Enterprise, Edu, Business, and Pro users. It works with connected GitHub repositories through Codex Web. If you need access or a repository isn’t visible, confirm the repository is available through your Codex Web workspace or contact your OpenAI account team.

## Related docs

- [Codex Security plugin guide](/codex/security/plugin) covers local repository and diff-review workflows in Codex.
- [Codex Security cloud setup](/codex/security/setup) covers setup, scanning, and findings review.
- [Improving the threat model](/codex/security/threat-model) explains how to tune scope, attack surface, and criticality assumptions.
- [FAQ](/codex/security/faq) covers common product questions.

