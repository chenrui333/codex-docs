---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin/workbench'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0"]
---

# Use the Codex Security workbench

Source: https://learn.chatgpt.com/docs/security/plugin/workbench

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

The Security workbench brings your scans, findings, and repositories together
in the Codex desktop app. Codex performs scan analysis in a regular task, while
the workbench keeps the scan and its results available when you return.

In the ChatGPT desktop app, open the ChatGPT dropdown and select **Codex**.
Install and enable the [Codex Security plugin](https://learn.chatgpt.com/docs/security/plugin), then
select **Security** in the sidebar.

If **Security** doesn't appear, confirm that **Codex** is selected and the
  plugin is installed and enabled. Update the desktop app and plugin if needed,
  and check whether your workspace administrator allows the plugin.

## Start a scan

For the best scan quality, use `gpt-5.6-sol`
with `xhigh` reasoning effort.

<WorkflowSteps>

1. Open **Scans** and select **+ Scan**.
2. Select an existing repository or choose another folder.
3. Choose **Codebase** to scan a repository or **Changes** to review a
   Git-backed change.
4. For a standard codebase scan, select the entire repository or a folder.
5. For a deep scan, first select the repository or folder as the codebase, then
   turn on **Deep scan**. Deep scans review the entire selected codebase.
6. For a changes scan, select uncommitted changes, a commit, or a revision
   range. **Deep scan** isn't available for changes scans.
7. Choose a model and reasoning effort. Open **Additional context** to describe
   relevant attack vectors, focus areas, or other security context.
8. Select **Start scan**.

</WorkflowSteps>

<figure className="not-prose my-8">
  <CodexScreenshot
    alt="Codex Security workbench showing the setup for a new repository scan"
    lightSrc={scanOverview.src}
    darkSrc={scanOverviewDark.src}
    maxHeight="520px"
  />
  <figcaption className="mt-3 text-sm text-secondary">
    Choose a repository and configure a scan in the Security workbench.
  </figcaption>
</figure>

See [Run a security scan](https://learn.chatgpt.com/docs/security/plugin/scans), [Run a deep security
scan](https://learn.chatgpt.com/docs/security/plugin/deep-scans), or [Review code changes for
security](https://learn.chatgpt.com/docs/security/plugin/code-changes) for details about each scan
type.

## Follow scan progress

The scan page shows the current phase and any scan progress the plugin reports.
For a standard scan, phases include threat modeling, discovery, validation,
impact and path analysis, reporting, and finalization.

Select **View activity** to open the Codex task that runs the scan. You can
leave the workbench and return to **Scans** without losing a saved scan. To stop
work intentionally, open the scan and select **Stop scan**.

When the scan completes, open its results to review the target, revision,
findings, coverage, and available report artifacts.

<figure className="not-prose my-8">
  <CodexScreenshot
    alt="Completed Codex Security scan showing findings, scan coverage, and report artifacts"
    lightSrc={findingsWorkspace.src}
    darkSrc={findingsWorkspaceDark.src}
    maxHeight="520px"
  />
  <figcaption className="mt-3 text-sm text-secondary">
    Review findings, severity, scan coverage, and artifacts after a scan
    completes.
  </figcaption>
</figure>

## Review findings across scans

Open **Findings** to inspect saved findings across repositories and scans.
Search or filter the list, then select a finding to review its summary, source
evidence, validation, and impact.

Use **Summary** for the finding details and **Patch** when you want to generate,
review, apply, or verify a focused fix. See [Fix and verify security
findings](https://learn.chatgpt.com/docs/security/plugin/fix-findings) for the remediation workflow.

The **Findings** tab shows findings from saved Codex Security scans. Imported
  tickets and other existing security issues remain part of the separate
  [backlog triage workflow](https://learn.chatgpt.com/docs/security/plugin/triage-backlog).

## Inspect repository history

Open **Repositories** to browse available repositories and folders. Select a
repository to inspect its scan history, latest scanned revision, and open
findings. From repository details, open a previous scan or view the findings
associated with that repository.

If a repository has no scans, start a scan from its details or select **+ Scan**
in the workbench.

## Start a scan from a conversation

You can also ask Codex to run the installed Codex Security plugin in a regular
conversation. Scans that use the shared plugin workbench appear in **Scans**,
so you can return to their progress and results from the Security workbench.

For terminal-based scans and automation, see the [Codex Security CLI
quickstart](https://learn.chatgpt.com/docs/security/cli).
