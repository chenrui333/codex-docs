---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Codex Security plugin quickstart

Source: https://learn.chatgpt.com/docs/security/plugin

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex Security scans your code for vulnerabilities and validates plausible
findings. For each reportable issue, it gives you the evidence and remediation
guidance you need to review the result. Scan only code you own or have
permission to assess.

Follow this quickstart to install the plugin and run a standard, read-only scan
of a local repository in Codex.

This page covers the Codex Security plugin in the desktop app or Codex CLI. To
  scan a connected GitHub repository in Codex cloud, see [Codex Security cloud
  setup](https://learn.chatgpt.com/docs/security/setup).

## Install the plugin

<ContentModeSwitch group="codex-surface" id="app">

1. Open [Codex in the ChatGPT desktop app](https://learn.chatgpt.com/docs/app).
2. Open **Plugins**, search for **Codex Security**, or use the button below:

     <ButtonLink
       href="codex://plugins/install/codex-security?marketplace=openai-curated"
       color="primary"
       variant="solid"
       size="lg"
       pill
     >
       Install the Codex Security plugin
     </ButtonLink>

3. Confirm the plugin is enabled, then open **Security** in the sidebar.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

1. In your terminal, go to the repository you want to assess and start Codex:

```bash
   codex
```

2. Enter `/plugins`, search for **Codex Security**, and select **Install
   plugin**.
3. Enter `/new` to start a new chat for the repository.

</ContentModeSwitch>

Check the [plugin changelog](https://learn.chatgpt.com/docs/security/plugin/changelog) before you rely
  on a feature or start a long-running scan. If **Security** doesn't appear in
  the desktop-app sidebar, update the app and plugin and confirm that the plugin
  is enabled.

## Run your first scan

For the best scan quality, use `gpt-5.6-sol`
with `xhigh` reasoning effort.

<ContentModeSwitch group="codex-surface" id="app">

<figure className="not-prose my-8">
  <CodexScreenshot
    alt="Native Codex Security workbench showing the new scan setup before a repository scan starts"
    lightSrc={scanOverview.src}
    darkSrc={scanOverviewDark.src}
    maxHeight="520px"
  />
  <figcaption className="mt-3 text-sm text-secondary">
    Choose a repository and configure a new security scan before you start it.
  </figcaption>
</figure>

<WorkflowSteps variant="headings">

1. Open the scan setup

   Select **Security** in the sidebar, open **Scans**, and select **+ Scan**.

2. Choose the codebase and scan area

   Select an existing repository or use another folder. Choose **Codebase**,
   leave **Deep scan** off, and select the entire repository or one folder.
   Confirm that the branch and revision identify the code you intended to scan.

3. Add relevant context

   Choose the model and reasoning effort. Open **Additional context** only when
   you need to describe a specific attack vector, security-sensitive area, or
   repository detail that should guide the review.

   <figure className="not-prose my-6">
     <CodexScreenshot
       alt="Native Codex Security scan setup with additional context enabled and example attack vectors, focus areas, and security guidance"
       lightSrc={scanSetup.src}
       darkSrc={scanSetupDark.src}
       maxHeight="460px"
     />
     <figcaption className="mt-3 text-sm text-secondary">
       Turn on additional context to describe attack vectors, focus areas, and
       relevant security guidance.
     </figcaption>
   </figure>

4. Start the scan

   Select **Start scan** and follow the scan phases in the Security workbench.
   Select **View activity** to inspect the Codex task that performs the scan.

5. Review the result

   Open the completed scan to inspect findings, coverage, and available report
   artifacts. Use **Findings** to review issues across scans or **Repositories**
   to inspect a repository's scan history.

   <figure className="not-prose my-6">
     <CodexScreenshot
       alt="Completed Codex Security scan showing findings in the native workbench"
       lightSrc={findingsWorkspace.src}
       darkSrc={findingsWorkspaceDark.src}
       maxHeight="520px"
     />
     <figcaption className="mt-3 text-sm text-secondary">
       Review scan results, findings, and coverage in the Security workbench.
     </figcaption>
   </figure>

</WorkflowSteps>

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

<WorkflowSteps variant="headings">

1. Ask for a standard scan

   Send this prompt in the new chat:

```text
   Run a Codex Security scan on this repository.
```

2. Let the scan finish

   Codex runs the scan in the terminal without opening a setup workspace. Keep
   the task running until Codex reports that it is complete. If Codex identifies
   a configuration limitation, review the limitation and the exact proposed
   change before you approve a configuration update.

3. Review the result

   Review the summary in the terminal, then open the generated `report.md` for
   the complete result.

</WorkflowSteps>

</ContentModeSwitch>

## What the scan creates

<ContentModeSwitch group="codex-surface" id="app">

Completed scans remain available in **Scans**. Review their findings and
coverage in the Security workbench, or inspect related findings and repository
history in **Findings** and **Repositories**. The scan also creates the files
below.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

Every completed scan reports a summary in the terminal and creates the files
below.

</ContentModeSwitch>

- `report.md`, the primary readable entry point to the scan results.
- `findings/<slug>/`, when detailed vulnerability reports and supporting
  proof-of-concept files are available.
- `hardening/`, when structural hardening guidance and supporting proposals or
  diagrams are available.
- Structured scan data in `scan-manifest.json`, `findings.json`, and
  `coverage.json` for automation and integrations. You can review scan results
  without opening these files.

Keep the full scan directory together when sharing or archiving results so the
links from `report.md` continue to work.

## Choose your next workflow

- [Use the Security workbench](https://learn.chatgpt.com/docs/security/plugin/workbench) to manage
  saved scans, findings, repositories, and scan activity in the desktop app.
- [Run a scan from the CLI](https://learn.chatgpt.com/docs/security/cli) if you have beta access and
  need a repeatable terminal workflow with structured results.
- [Run a standard or scoped scan](https://learn.chatgpt.com/docs/security/plugin/scans) to review a
  repository or one folder with the default workflow.
- [Assess a first scan](https://learn.chatgpt.com/docs/security/plugin/scans#assess-a-first-scan)
  to check the results against known issues and decide when to scan again.
- [Run a deep scan](https://learn.chatgpt.com/docs/security/plugin/deep-scans) for a more thorough scan
  when you can allow for a longer runtime.
- [Review code changes](https://learn.chatgpt.com/docs/security/plugin/code-changes) to assess a pull
  request, commit, branch range, or working-tree patch.
- [Triage a backlog](https://learn.chatgpt.com/docs/security/plugin/triage-backlog) to review existing
  security findings.
- [Fix and verify a finding](https://learn.chatgpt.com/docs/security/plugin/fix-findings) after you
  accept one finding for remediation.
- [Export or track findings](https://learn.chatgpt.com/docs/security/plugin/export-findings) to create
  JSON, CSV, SARIF, an approval-gated Linear, GitHub, or Jira issue, or a private
  draft GitHub Security Advisory.
- [Write vulnerability reports](https://learn.chatgpt.com/docs/security/plugin/vulnerability-reports)
  to turn supplied findings, disclosure notes, source, and PoCs into
  self-contained reports.
- [Propose security hardening](https://learn.chatgpt.com/docs/security/plugin/security-hardening) to
  consider structural or architectural options based on scan results or other
  security evidence.
