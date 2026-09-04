---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Codex Security

Source: https://learn.chatgpt.com/docs/security

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex Security is an application security agent that helps security and
engineering teams find, confirm, and fix vulnerabilities. Use it in
Codex, from your terminal, through the TypeScript SDK, or with connected GitHub
repositories.

<CtaPillLink
  href="https://chatgpt.com/plugins/share/676aca3811d54fa7bcdef5255236b3c4"
  label="Install plugin in ChatGPT"
  icon="external"
  class="mb-8 mt-2"
/>

For a prescriptive first local scan, start with the [Codex Security plugin
quickstart](https://learn.chatgpt.com/docs/security/plugin).

## Use Codex Security in the desktop app

In the ChatGPT desktop app, open the ChatGPT dropdown and select **Codex**.
Install and enable the Codex Security plugin to open **Security** in the
sidebar. The Security workbench keeps your scans, findings, and repositories in
one place while Codex runs each scan in a task.

- Use **Scans** to start scans, follow their progress, and review saved results.
- Use **Findings** to inspect issues and evidence across completed scans.
- Use **Repositories** to review repository history and open findings.

See [Use the Security workbench](https://learn.chatgpt.com/docs/security/plugin/workbench) for the
complete desktop-app workflow.

### Explore plugin use cases

- [Run a security scan](https://learn.chatgpt.com/docs/security/plugin/scans) for a repository or one scoped folder.
- [Run a deep security scan](https://learn.chatgpt.com/docs/security/plugin/deep-scans) when you need broader review and can wait longer for it to finish.
- [Review code changes](https://learn.chatgpt.com/docs/security/plugin/code-changes) before you merge a pull request or branch.
- [Triage a backlog](https://learn.chatgpt.com/docs/security/plugin/triage-backlog) when you have existing security findings to review.
- [Fix and verify findings](https://learn.chatgpt.com/docs/security/plugin/fix-findings) with bounded patches for approved findings.
- [Export or track findings](https://learn.chatgpt.com/docs/security/plugin/export-findings) as portable artifacts or approval-gated tracking destinations.
- [Write vulnerability reports](https://learn.chatgpt.com/docs/security/plugin/vulnerability-reports) from supplied findings, disclosure notes, source, and PoCs.
- [Propose security hardening](https://learn.chatgpt.com/docs/security/plugin/security-hardening) from scan results or other security evidence.
- [See what's new](https://learn.chatgpt.com/docs/security/plugin/changelog) in the Codex Security plugin.

The desktop Security workbench and Codex CLI use the Codex Security plugin.
  Codex Security cloud scans connected GitHub repositories through Codex cloud.
  For Codex sandboxing, approvals, network controls, and admin settings, see
  [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security).

## Codex Security CLI and SDK

The CLI and TypeScript SDK are available as the public
[`@openai/codex-security`](https://github.com/openai/codex-security) package.
Run the CLI with `npx`:

```bash
npx @openai/codex-security --help
```

Running scans requires Codex Security access. For best results, use an account
verified for [Trusted Access for Cyber](https://chatgpt.com/cyber).

Use the same scanner as the plugin across repositories and over time. The CLI
discovers GitHub repositories, resumes bulk scans, tracks findings across
scans, and records false-positive feedback. Add your architecture and security
policies, set an estimated cost limit, or run checks in CI and before commits.
Use the TypeScript SDK to build scanning, progress reporting, and cost controls
into an application or developer tool.

- [Start with the CLI quickstart](https://learn.chatgpt.com/docs/security/cli) to set up the CLI,
  preflight a repository, and run a local scan.
- [Run bulk security scans](https://learn.chatgpt.com/docs/security/cli/bulk-scans) to discover GitHub
  repositories or run a resumable campaign from a CSV inventory.
- [Run scans in CI](https://learn.chatgpt.com/docs/security/cli/ci) to review pull-request changes,
  preserve artifacts, upload SARIF, and set a severity policy.
- [Read the CLI FAQ](https://learn.chatgpt.com/docs/security/cli/faq) for answers about scan history,
  false-positive feedback, coverage, and fix verification.
- [Use the CLI reference](https://learn.chatgpt.com/docs/security/cli/reference) to check supported
  commands, flags, output formats, artifacts, and exit codes.
- [Integrate the TypeScript SDK](https://learn.chatgpt.com/docs/security/sdk) to select targets,
  inspect results, track progress, and cancel scans from code.

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

Codex Security cloud works with connected GitHub repositories through Codex
cloud. If a repository isn't visible, confirm the repository is available in your
Codex cloud workspace or contact your OpenAI account team.

## Related docs

- [Codex Security plugin quickstart](https://learn.chatgpt.com/docs/security/plugin) walks through installation and a first local scan.
- [Security workbench](https://learn.chatgpt.com/docs/security/plugin/workbench) explains saved scans, findings, repositories, and scan activity in the desktop app.
- [Codex Security CLI quickstart](https://learn.chatgpt.com/docs/security/cli) walks through setup, preflight, and a first terminal scan.
- [Run bulk security scans](https://learn.chatgpt.com/docs/security/cli/bulk-scans) explains GitHub discovery, CSV inventories, campaign results, and resume behavior.
- [Codex Security CLI FAQ](https://learn.chatgpt.com/docs/security/cli/faq) answers common questions about scans, findings, coverage, and costs.
- [Codex Security TypeScript SDK](https://learn.chatgpt.com/docs/security/sdk) explains how to run scans from an application or developer tool.
- [Codex Security cloud setup](https://learn.chatgpt.com/docs/security/setup) details setup, scanning, and findings review.
- [Security Review](https://learn.chatgpt.com/docs/security/security-review) explains how to run in-depth security reviews on GitHub pull requests.
- [Improving the threat model](https://learn.chatgpt.com/docs/security/threat-model) explains how to tune scope, entry points, and criticality assumptions.
- [Codex Security cloud FAQ](https://learn.chatgpt.com/docs/security/faq) covers common cloud product questions.
