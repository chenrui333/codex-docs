---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/setup'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0"]
---

# Codex Security cloud setup

Source: https://learn.chatgpt.com/docs/security/setup

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

This page walks you from initial access to reviewed findings and remediation
pull requests in Codex Security cloud.

Confirm you've set up Codex cloud first. If not, see [Codex
  cloud](https://learn.chatgpt.com/docs/cloud) to get started.

## 1. Access and environment

Codex Security cloud scans GitHub repositories connected through
[Codex cloud](https://learn.chatgpt.com/docs/cloud).

- Confirm your workspace has access to Codex Security cloud.
- Confirm the repository you want to scan is available in Codex cloud.

Go to [Codex environments](https://chatgpt.com/codex/settings/environments) and check whether the repository already has an environment. If it doesn't, create one there before continuing.

<CtaPillLink
  href="https://chatgpt.com/codex/settings/environments"
  label="Open environments"
  icon="external"
  class="my-8"
/>

  <img
    src={createEnvironment.src}
    alt="Codex environments"
    class="block h-auto w-full"
  />

## 2. New security scan

After the environment exists, go to [Create a security scan](https://chatgpt.com/codex/security/scans/new) and choose the repository you just connected.

<CtaPillLink
  href="https://chatgpt.com/codex/security/scans/new"
  label="Create a security scan"
  icon="external"
  class="my-8"
/>

Codex Security scans repositories from newest commits backward first. It uses this to build and refresh scan context as new commits come in.

To configure a repository:

1. Select the GitHub organization.
2. Select the repository.
3. Select the branch you want to scan.
4. Select the environment.
5. Choose a **history window**. Longer windows provide more context, but backfill takes longer.
6. Click **Create**.

  <img
    src={createScan.src}
    alt="Create a security scan"
    class="block h-auto w-full"
  />

## 3. Initial scans can take a while

When you create the scan, Codex Security first runs a commit-level security pass across the selected history window.
The initial backfill can take a few hours, especially for larger repositories or longer windows.
If findings aren't visible right away, this is expected. Wait for the initial scan to finish before opening a ticket or troubleshooting.

Initial scan setup is automatic and thorough. This can take a few hours. Don’t
  be alarmed if the first set of findings is delayed.

## 4. Review scans and improve the threat model

<CtaPillLink
  href="https://chatgpt.com/codex/security/scans"
  label="Review scans"
  icon="external"
  class="my-8"
/>

  <img
    src={reviewThreatModel.src}
    alt="Threat model editor in Codex Security"
    class="block h-auto w-full"
  />

When the initial scan finishes, open the scan and review the threat model that was generated.
After initial findings appear, update the threat model so it matches your architecture, trust boundaries, and business context.
This helps Codex Security rank issues for your team.

If you want scan results to change, you can edit the threat model with your
  updated scope, priorities, and assumptions.

After initial findings appear, revisit the model so scan guidance stays aligned with current priorities.
Keeping it current helps Codex Security produce better suggestions.

For a deeper explanation of threat models and how they affect criticality and triage, see [Improving the threat model](https://learn.chatgpt.com/docs/security/threat-model).

## 5. Review findings and patch

After the initial backfill completes, review findings from the **Findings** view.

<CtaPillLink
  href="https://chatgpt.com/codex/security/findings"
  label="Open findings"
  icon="external"
  class="my-8"
/>

You can use two views:

- **Recommended Findings**: an evolving top 10 list of the most critical issues in the repo
- **All Findings**: a sortable, filterable table of findings across the repository

![Recommended findings view](https://learn.chatgpt.com/docs/security/images/aardvark_recommended_findings.png)

Click a finding to open its detail page, which includes:

- a concise description of the issue
- key metadata such as commit details and file paths
- contextual reasoning about impact
- relevant code excerpts
- call-path or data-flow context when available
- validation steps and validation output

You can review each finding and create a PR directly from the finding detail page.

<CtaPillLink
  href="https://chatgpt.com/codex/security/findings"
  label="Review findings and create a PR"
  icon="external"
  class="my-8"
/>

## Related docs

- [Codex Security](https://learn.chatgpt.com/docs/security) gives the product overview.
- [Codex Security cloud FAQ](https://learn.chatgpt.com/docs/security/faq) covers common cloud questions.
- [Improving the threat model](https://learn.chatgpt.com/docs/security/threat-model) explains how to improve scan context and finding prioritization.
