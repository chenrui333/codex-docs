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
  label="Install local Security plugin"
  icon="external"
  class="mb-8 mt-2"
/>

For your first local scan, start with the [Codex Security plugin
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
  The separate Codex Security Cloud plugin scans connected GitHub repositories
  in Codex cloud. For Codex sandboxing, approvals, network controls, and admin
  settings, see [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security).

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

## Codex Security Cloud

Codex Security Cloud is a plugin for scanning connected GitHub repositories
in Codex cloud. It's available in research preview on the web and in the
desktop app.

Open **Plugins** to find and install **Codex Security Cloud**. Follow
[Cloud setup](https://learn.chatgpt.com/docs/security/setup) to connect GitHub and start your first scan.

<CtaPillLink
  href="https://chatgpt.com/plugins"
  label="Find Codex Security Cloud"
  icon="external"
  class="my-8"
/>

<figure className="not-prose my-8">
  <CodexScreenshot
    alt="Codex Security Cloud overview with repository counts, finding statuses, and findings that need attention"
    lightSrc={cloudOverview.src}
    darkSrc={cloudOverview.src}
    variant="no-wallpaper"
    maxHeight="560px"
    imageClass="border border-subtle"
    panOnMobile
  />
  <figcaption className="mt-3 text-sm text-secondary">
    Track open findings and fixes across repositories. This example uses
    fictional repositories, findings, and counts.
  </figcaption>
</figure>

## How Codex Security Cloud works

Choose **One-Time Scan** to review a repository once, or **Continuous Scanning**
to monitor new commits. Codex uses repository context to identify likely
vulnerabilities and validates issues in an isolated environment when possible.

Use **Scans** to follow progress, **Findings** to review issues, and
**Repositories** to manage monitoring. Review proposed patches before
creating a pull request.

## Codex Security Cloud access and prerequisites

Use a workspace with Codex Security Cloud access, a connected GitHub
repository, and a compatible Codex cloud environment. You can connect GitHub
and create an environment during scan setup.

If access is unavailable, check with your workspace administrator.

## Related docs

- [Codex Security plugin quickstart](https://learn.chatgpt.com/docs/security/plugin) walks through installation and a first local scan.
- [Security workbench](https://learn.chatgpt.com/docs/security/plugin/workbench) explains saved scans, findings, repositories, and scan activity in the desktop app.
- [Codex Security CLI quickstart](https://learn.chatgpt.com/docs/security/cli) walks through setup, preflight, and a first terminal scan.
- [Run bulk security scans](https://learn.chatgpt.com/docs/security/cli/bulk-scans) explains GitHub discovery, CSV inventories, campaign results, and resume behavior.
- [Codex Security CLI FAQ](https://learn.chatgpt.com/docs/security/cli/faq) answers common questions about scans, findings, coverage, and costs.
- [Codex Security TypeScript SDK](https://learn.chatgpt.com/docs/security/sdk) explains how to run scans from an application or developer tool.
- [Codex Security Cloud setup](https://learn.chatgpt.com/docs/security/setup) details setup, scanning, and findings review.
- [Security Review](https://learn.chatgpt.com/docs/security/security-review) explains how to run in-depth security reviews on GitHub pull requests.
- [Improving the threat model](https://learn.chatgpt.com/docs/security/threat-model) explains how to tune scope, entry points, and criticality assumptions.
- [Codex Security Cloud FAQ](https://learn.chatgpt.com/docs/security/faq) covers common cloud product questions.
