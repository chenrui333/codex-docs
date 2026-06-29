---
source_type: 'developers'
source_area: 'codex_security'
source_url: 'https://developers.openai.com/codex/security'
source_last_modified: '2026-06-18T22:37:52Z'
source_etag: 'W/"814330dc1da3d759f44aa3bf60fd7c8e"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4"]
---

# Security – Codex | OpenAI Developers

Source: https://developers.openai.com/codex/security

[Install plugin in Codex App](https://chatgpt.com/plugins/share/676aca3811d54fa7bcdef5255236b3c4)

For a prescriptive first local scan, start with the [Codex Security plugin
quickstart](/codex/security/plugin).

### Explore plugin use cases

- [Run a security scan](/codex/security/plugin/scans) for a repository or one scoped folder.
- [Run a deep security scan](/codex/security/plugin/deep-scans) when you need a more comprehensive scan and can wait longer for it to finish.
- [Review code changes](/codex/security/plugin/code-changes) before you merge a pull request or branch.
- [Triage a backlog](/codex/security/plugin/triage-backlog) when you have existing security findings to review.
- [Fix and verify findings](/codex/security/plugin/fix-findings) with bounded patches for approved findings.
- [Export or track findings](/codex/security/plugin/export-findings) as portable artifacts or approval-gated tracking destinations.
- [See what’s new](/codex/security/plugin/changelog) in the Codex Security plugin.

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

- [Codex Security plugin quickstart](/codex/security/plugin) walks through installation and a first local scan.
- [Codex Security cloud setup](/codex/security/setup) details setup, scanning, and findings review.
- [Improving the threat model](/codex/security/threat-model) explains how to tune scope, attack surface, and criticality assumptions.
- [FAQ](/codex/security/faq) covers common product questions.

