---
source_type: 'developers'
source_area: 'codex_security'
source_url: 'https://developers.openai.com/codex/security/plugin'
source_last_modified: '2026-06-18T22:38:26Z'
source_etag: 'W/"0b99c21b058b94f31beba61b6d09dbad"'
codex_cli_versions: ["0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5"]
codex_cli_versions_raw: ["codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5"]
---

# Plugin quickstart – Codex Security | OpenAI Developers

Source: https://developers.openai.com/codex/security/plugin

Codex Security is a security-review plugin for Codex that scans your code for
vulnerabilities, validates plausible findings, and presents evidence and
remediation guidance in a reviewable workspace. Use it to find security issues
in code you own or have authorization to assess before they reach production.

This quickstart takes you through one recommended first run: an ordinary,
read-only scan of a local repository in the Codex app.

This page covers the plugin that runs in a local Codex thread. To scan a
connected GitHub repository in Codex web, see [Codex Security cloud
setup](/codex/security/setup).

## Install the plugin

Open the repository you want to assess in the Codex app, then install Codex
Security:

[Install the Codex Security plugin](codex://plugins/install/codex-security?marketplace=openai-curated)

After installation, start a new thread in that repository. Codex loads plugins
when the thread starts, so don’t continue in a thread that was already open.

## Run your first scan

For the best scan quality, use `gpt-5.5`
with `high` or `xhigh` reasoning effort.

[![
Your browser does not support the video tag.
](/videos/codex/security/scan-setup-to-findings-poster.webp)](/videos/codex/security/scan-setup-to-findings.mp4)

1. Ask for an ordinary scan

   Send this prompt in the new thread:

   ```
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

   ![Codex Security setup workspace configured to scan an entire codebase](/_astro/scan-setup.Bxb8klDo.webp)

   Configure the scan target, scan area, branch, and optional threat model
   guidance before starting the scan.
3. Let the scan finish

   The scan can take time. Keep the thread running until the workspace reports
   completion. If Codex identifies a configuration limitation, review the exact
   limitation and proposed change before allowing it to update your
   configuration.
4. Review the result

   Use the UI to browse findings or open the generated report for a complete,
   portable review.

   ![Completed Codex Security findings workspace for OWASP Juice Shop](/_astro/findings-workspace.B46Bfrsr.webp)

   Browse findings by severity, category, directory, patch status, and
   review status.

## What the scan creates

Every completed scan opens a findings workspace. Use it to review findings and
coverage without inspecting raw artifacts. The scan also creates:

- `report.md`, a complete portable report for sharing or archiving.
- Structured scan data in `scan-manifest.json`, `findings.json`, and
  `coverage.json` for automation and integrations. You normally don’t need to
  open these files yourself.

## Choose your next workflow

- [Run a standard or scoped scan](/codex/security/plugin/scans) when you want
  to scan a repository or one folder with the default workflow.
- [Run a deep scan](/codex/security/plugin/deep-scans) when you need a more
  comprehensive scan and can wait longer for it to finish.
- [Review code changes](/codex/security/plugin/code-changes) when the target is
  a pull request, commit, branch range, or working-tree patch.
- [Triage a backlog](/codex/security/plugin/triage-backlog) when you have
  existing security findings to review.
- [Fix and verify a finding](/codex/security/plugin/fix-findings) after you
  accept one finding for remediation.
- [Export or track findings](/codex/security/plugin/export-findings) when you
  need JSON, CSV, SARIF, an approval-gated Linear, GitHub, or Jira issue, or a
  private draft GitHub Security Advisory.

## Install from Codex CLI

To install the same plugin from the CLI, start Codex in the repository and open
the plugin browser:

```
codex
/plugins
```

Search for **Codex Security**, select `Install plugin`, and start a new thread.
Then use the same first-scan prompt.

