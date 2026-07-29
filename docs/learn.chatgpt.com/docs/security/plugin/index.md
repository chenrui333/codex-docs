---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0"]
---

# Codex Security plugin quickstart

Source: https://learn.chatgpt.com/docs/security/plugin

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex Security scans your code for vulnerabilities and validates plausible
findings. For each reportable issue, it gives you the evidence and remediation
guidance you need to review the result. Scan only code you own or have
permission to assess.

Follow this quickstart to install the plugin and run a read-only scan of a local
repository in Codex.

This page covers the plugin that runs in a local Codex chat. To scan a
  connected GitHub repository in Codex cloud, see [Codex Security cloud
  setup](https://learn.chatgpt.com/docs/security/setup).

## Install the plugin

<ContentModeSwitch group="codex-surface" id="app">

1. Open the repository you want to assess in Codex in the [ChatGPT desktop
   app](https://chatgpt.com/download/).
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

3. Start a new Codex chat for that repository. Don't continue an existing chat.

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

## Run your first scan

For the best scan quality, use `gpt-5.6-sol`
with `xhigh` reasoning effort.

<ContentModeSwitch group="codex-surface" id="app">

<VideoPlayer
  src="/videos/codex/security/scan-setup-to-findings.mp4"
  poster="/videos/codex/security/scan-setup-to-findings-poster.webp"
/>

<WorkflowSteps variant="headings">

1. Ask for an ordinary scan

   Send this prompt in the new chat:

```text
   Run a Codex Security scan on this repository.
```

2. Confirm the setup

   Codex opens a setup workspace before it starts. For your first run, use these
   settings:
   - **Scan type:** `Codebase`
   - **Deep scan:** Off
   - **Scan area:** `Entire codebase`
   - **Threat model scoping guidance:** Leave blank unless you already know a
     specific attack vector or application area that deserves priority.

   Confirm that **Codebase**, **Current branch**, and **Last commit** identify
   the repository you intended to scan. Then select **Start scan**.

   <figure className="not-prose my-6">

       <img
         src={scanSetup.src}
         alt="Codex Security setup workspace configured to scan an entire codebase"
         className="block h-auto w-full"
       />

     <figcaption className="mt-3 text-sm text-secondary">
       Configure the scan target, scan area, branch, and optional threat model
       guidance before starting the scan.
     </figcaption>
   </figure>

3. Let the scan finish

   Keep the scan running until the workspace reports that it is complete. If
   Codex identifies a configuration limitation, review the limitation and the
   exact proposed change before you approve a configuration update.

4. Review the result

   Use the UI to browse findings, or open `report.md` as the entry point to the
   complete scan directory.

   <figure className="not-prose my-6">

       <img
         src={findingsWorkspace.src}
         alt="Completed Codex Security findings workspace for OWASP Juice Shop"
         className="block h-auto w-full"
       />

     <figcaption className="mt-3 text-sm text-secondary">
       Browse findings by severity, category, directory, patch status, and
       review status.
     </figcaption>
   </figure>

</WorkflowSteps>

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

<WorkflowSteps variant="headings">

1. Ask for an ordinary scan

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

Every completed scan opens a findings workspace. Use it to review findings and
coverage without inspecting raw artifacts. The scan also creates the files
below.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

Every completed scan reports a summary in the terminal and creates the files
below.

</ContentModeSwitch>

- `report.md`, the primary readable entry point to the scan results.
- `findings/<slug>/`, with one detailed vulnerability report per reportable
  finding and supporting proof-of-concept files when available.
- `hardening/`, with a structural hardening portfolio and supporting proposals
  or diagrams when the scan has reportable findings.
- Structured scan data in `scan-manifest.json`, `findings.json`, and
  `coverage.json` for automation and integrations. You normally don't need to
  open these files yourself.

Keep the full scan directory together when sharing or archiving results so the
links from `report.md` continue to work.

## Choose your next workflow

- [Run a scan from the CLI](https://learn.chatgpt.com/docs/security/cli) if you have beta access and
  need a repeatable terminal workflow with structured results.
- [Run a standard or scoped scan](https://learn.chatgpt.com/docs/security/plugin/scans) to review a
  repository or one folder with the default workflow.
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
