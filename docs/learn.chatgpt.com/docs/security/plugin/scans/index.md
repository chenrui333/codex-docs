---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin/scans'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0"]
---

# Run a Codex Security scan

Source: https://learn.chatgpt.com/docs/security/plugin/scans

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Start with a standard Codex Security scan for an initial review or a routine
repository or component assessment. It runs the full scan workflow once.

For a more thorough assessment, review the results and then run a [deep
scan](https://learn.chatgpt.com/docs/security/plugin/deep-scans). Deep scans take longer and search
more extensively.

## Choose the scan area

In the desktop app, open **Security**, select **Scans**, and select **+ Scan**.
Choose an existing repository or another folder, then select **Codebase**.

Scan the whole repository when you need broad coverage and the repository is a
reasonable review unit. For a monorepo, choose one folder when a service,
package, or component has a clear owner and security boundary.

You can also start a scan from a Codex conversation:

```text
Use $codex-security:security-scan to scan this repository for security vulnerabilities.
```

To focus that conversation on a particular folder, identify the component:

```text
Use $codex-security:security-scan to scan this repository for security vulnerabilities, focusing on the services/billing component.
```

For a large monorepo, start with one meaningful product or service boundary.

## Configure the scan

For the best scan quality, use `gpt-5.6-sol`
with `xhigh` reasoning effort.

<WorkflowSteps>

1. Select **Codebase** and leave **Deep scan** off.
2. Confirm the selected repository, current branch, and latest revision.
3. Set **Scan area** to the entire repository or choose one folder.
4. Choose a model and reasoning effort.
5. Open **Additional context** only when it changes the review. Useful context
   names attacker-controlled inputs, trust boundaries, sensitive actions, or a
   specific area to prioritize.
6. Select **Start scan**.

</WorkflowSteps>

Add `SECURITY.md` to the repository root for persistent security guidance.
Describe the threat model, security invariants, reportable finding criteria,
exclusions, and severity context. Add nested `SECURITY.md` files for
directory-specific guidance. When policies conflict, the file closest to the
code takes precedence. Codex Security treats these files as policy context,
not executable instructions.

Use `AGENTS.md` for supported build and validation commands and other
repository-specific instructions.

## Let the phases complete

A scan runs these phases in order:

1. **Threat modeling** identifies assets, entry points, trust boundaries, and
   security invariants.
2. **Finding discovery** reviews the requested code for plausible broken
   controls and source-to-sink paths.
3. **Validation** tests or otherwise checks each candidate and records evidence
   or proof gaps.
4. **Impact and path analysis** evaluates each candidate's realistic paths,
   impact, and severity.
5. **Reporting** records validated findings, coverage, and scan metadata.
   Detailed per-finding reports are available when requested.
6. **Structural hardening**, when requested, analyzes the finding set and
   creates design guidance.
7. **Finalization** validates the structured scan contract and generates
   `report.md`, including links to any detailed reports or hardening guidance.

The workbench shows the active scan phase and any progress the plugin reports.
Select **View activity** to inspect the Codex task. Wait for the complete
result instead of judging early candidates or stopping because one phase takes
longer than another.

## Review the completed scan

Review the result in this order:

1. Confirm the target, revision, and scan area.
2. Read reviewed surfaces and every explicit deferred or follow-up area.
3. For each finding, inspect the root control or sink, attacker-controlled
   input, validation method, remaining uncertainty, realistic reachability,
   severity rationale, and proposed remediation.
4. Dismiss findings whose evidence doesn't support the claimed path or impact.
5. Select one accepted finding before starting a fix.

<figure className="not-prose my-8">
  <CodexScreenshot
    alt="Codex Security finding showing its severity, validation status, root cause, and attack path"
    lightSrc={findingAttackPath.src}
    darkSrc={findingAttackPathDark.src}
    maxHeight="520px"
  />
  <figcaption className="mt-3 text-sm text-secondary">
    Review the finding's severity, validation status, root cause, and attack
    path.
  </figcaption>
</figure>

## Assess a first scan

Before scanning, choose two to four evaluation criteria, such as independent
discovery, evidence quality, false positives, or remediation quality. If you
test against a known finding, record whether you provided it to Codex or
withheld it from the scan.

Record the repository revision, plugin version, model, and reasoning effort.
Use this baseline to compare later scans after the code, security controls, or
scan settings change.

## Choose a scan cadence

Set your scan cadence based on the repository's risk and your team's capacity
to address findings. Scan at these points:

- **Baseline:** Run a standard scan when you onboard a repository, take
  ownership of a component, or need a starting point for a new threat model.
- **Code changes:** [Review code
  changes](https://learn.chatgpt.com/docs/security/plugin/code-changes) when a pull request or commit
  changes security-sensitive code or an external integration.
- **Regular review:** Set a recurring review interval based on your system's
  exposure and how often the code changes. Adjust it to your team's capacity to
  address findings.
- **After a fix:** [Fix and verify the
  finding](https://learn.chatgpt.com/docs/security/plugin/fix-findings). Confirm that the issue no
  longer reproduces and keep the original scan for comparison.

These scan triggers don't create an automated schedule.

## Reopen a previous scan

Open **Security**, then select a saved scan from **Scans** to review its
findings, coverage, and available report artifacts. To assess the latest code,
start a new scan for the same repository. The new scan doesn't replace the
earlier scan or its artifacts.

## Use the results

Use the Security workbench to review findings, coverage, and follow-up areas
without inspecting raw JSON. Open `report.md` when available for the readable
entry point to the complete scan directory. Keep the directory together when
you share or archive it: the report links to detailed reports in `findings/`
and structural hardening guidance in `hardening/` when those optional artifacts
are available.

Behind the workspace, each scan preserves `scan-manifest.json`, `findings.json`,
and `coverage.json` for automation and integrations. You normally don't need to
open these files yourself.

For portable artifacts or external issue tracking, see [Export or track
findings](https://learn.chatgpt.com/docs/security/plugin/export-findings).

## Next step

After you accept a finding, use [Fix and verify a
finding](https://learn.chatgpt.com/docs/security/plugin/fix-findings) to generate and review one
bounded patch. Don't ask Codex to fix every finding from a scan in one chat.
