---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin/scans'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0"]
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

Scan the whole repository when you need broad coverage and the repository is a
reasonable review unit:

```text
Use $codex-security:security-scan to scan this repository for security vulnerabilities.
```

Scan a folder when a monorepo is too large or one service, package, or component
has a clear owner and security boundary:

```text
Use $codex-security:security-scan to scan this repository for security vulnerabilities, focusing on the services/billing component.
```

For a large monorepo, start with one meaningful product or service boundary.

## Configure the scan

<WorkflowSteps>

1. Confirm **Scan type** is `Codebase` and leave **Deep scan** off.
2. Confirm the **Codebase**, **Current branch**, and **Last commit**.
3. Set **Scan area** to `Entire codebase` or enter one repository-relative
   folder.
4. Add threat-model guidance only when it changes the review. Useful guidance
   names attacker-controlled inputs, trust boundaries, sensitive actions, or a
   specific area to prioritize.
5. Select **Start scan**.

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
5. **Detailed reporting** creates one source-backed vulnerability report per
   reportable finding, with supporting proof-of-concept files when available.
6. **Structural hardening** analyzes the complete finding set and creates a
   design portfolio when reportable findings remain.
7. **Finalization** validates the structured scan contract and generates
   `report.md`, which links the detailed reports and hardening portfolio.

Codex reports phase and coverage progress as the scan runs. Wait for the
complete result instead of judging early candidates or stopping because one
phase takes longer than another.

## Review the completed scan

Review the result in this order:

1. Confirm the target, revision, and scan area.
2. Read reviewed surfaces and every explicit deferred or follow-up area.
3. For each finding, inspect the root control or sink, attacker-controlled
   input, validation method, remaining uncertainty, realistic reachability,
   severity rationale, and proposed remediation.
4. Dismiss findings whose evidence doesn't support the claimed path or impact.
5. Select one accepted finding before starting a fix.

  <figure>

      <img
        src={findingsWorkspace.src}
        alt="Completed Codex Security findings workspace for OWASP Juice Shop"
        className="block h-auto w-full"
      />

    <figcaption className="mt-3 text-sm text-secondary">
      The completed workspace summarizes scan status, coverage, severity, and
      artifacts before listing the findings.
    </figcaption>
  </figure>

  <figure>

      <img
        src={findingAttackPath.src}
        alt="Codex Security finding evidence and attack-path analysis for OWASP Juice Shop"
        className="block h-auto w-full"
      />

    <figcaption className="mt-3 text-sm text-secondary">
      A finding connects the relevant source to its entry point, reachability,
      likelihood, impact, and any limits or counterevidence.
    </figcaption>
  </figure>

## Reopen or rerun a previous scan

In the ChatGPT desktop app, open a completed scan from the security scan list
to review its saved findings workspace. To update the results, rerun the saved
configuration against the current code. The rerun creates a new scan and leaves
the earlier scan and its artifacts unchanged.

Scan history, rerun controls, and other workspace features depend on your Codex
surface and installed plugin version. A rerun doesn't pin that version or
guarantee that interrupted work will resume after a plugin update. Check the
[plugin changelog](https://learn.chatgpt.com/docs/security/plugin/changelog) before you start or rerun
a long-running scan.

## Use the results

Use the findings workspace to review findings, coverage, and follow-up areas
without inspecting raw JSON. Open `report.md` for the readable entry point to
the complete scan directory. Keep the directory together when you share or
archive it: the report links to detailed reports in `findings/` and, when
reportable findings exist, structural hardening guidance in `hardening/`.

Behind the workspace, each scan preserves `scan-manifest.json`, `findings.json`,
and `coverage.json` for automation and integrations. You normally don't need to
open these files yourself.

The findings workspace can also create portable JSON, CSV, and SARIF files. See
[Export or track findings](https://learn.chatgpt.com/docs/security/plugin/export-findings).

## Next step

After you accept a finding, use [Fix and verify a
finding](https://learn.chatgpt.com/docs/security/plugin/fix-findings) to generate and review one
bounded patch. Don't ask Codex to fix every finding from a scan in one chat.
