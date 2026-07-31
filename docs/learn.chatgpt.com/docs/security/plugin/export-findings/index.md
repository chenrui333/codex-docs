---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin/export-findings'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0"]
---

# Export and track security findings

Source: https://learn.chatgpt.com/docs/security/plugin/export-findings

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use a completed Codex Security scan for either of these handoffs:

- **Export** creates a portable JSON, CSV, or SARIF file.
- **Track findings** prepares selected findings as Linear, GitHub, or Jira
  issues, or as one private draft GitHub Security Advisory. Codex checks for
  duplicates and waits for your approval before writing.

Neither workflow changes the sealed scan bundle.

Available artifact links and export formats depend on your Codex surface and
  installed plugin version. Check the [plugin
  changelog](https://learn.chatgpt.com/docs/security/plugin/changelog) before you use a format in
  automation.

## Export a portable artifact

In the desktop app, open a completed scan from **Security** > **Scans**. Use its
available artifact links to inspect `report.md`, `findings.json`,
`scan-manifest.json`, `coverage.json`, or a SARIF report when present.

To create another supported format, ask Codex to export findings from the
completed scan without modifying its sealed bundle:

```text
Export the findings from [completed scan directory] as [JSON, CSV, or SARIF]. Do not modify the sealed scan bundle or upload its contents.
```

Choose the format that fits your destination:

| Format | Use it for                                                        |
| ------ | ----------------------------------------------------------------- |
| JSON   | Preserve the sealed structured findings for tools and scripts.    |
| CSV    | Review findings and current local triage state in a spreadsheet.  |
| SARIF  | Send findings to tools that support the SARIF interchange format. |

<figure className="not-prose my-8">
  <CodexScreenshot
    alt="Completed Codex Security scan showing the real coverage, findings, manifest, Markdown, and SARIF artifacts"
    lightSrc={exportFindingsFormats.src}
    darkSrc={exportFindingsFormatsDark.src}
    maxHeight="360px"
  />
  <figcaption className="mt-3 text-sm text-secondary">
    Open the coverage, findings, scan manifest, Markdown report, or SARIF
    artifact from a completed scan.
  </figcaption>
</figure>

Select **Markdown report** to open `report.md` in your configured external
editor. The editor depends on your system settings; the example below shows the
generated report contents.

<figure className="not-prose my-8">
  <CodexScreenshot
    alt="Example generated security report showing the scan scope, threat model, and validated findings"
    lightSrc={exportFindingsReport.src}
    darkSrc={exportFindingsReportDark.src}
    maxHeight="600px"
  />
  <figcaption className="mt-3 text-sm text-secondary">
    Review the scan scope, threat model, validated findings, and detailed report
    links in the generated Markdown report.
  </figcaption>
</figure>

Use the returned artifact path. If another tool needs the complete scan
context, keep the original `scan-manifest.json`, `findings.json`, and
`coverage.json` together. Exporting doesn't upload findings to a code-scanning
service.

## Track selected findings

Run `$codex-security:track-findings` with one validated finding or an
explicitly selected batch of up to 25 findings from the same sealed scan. Each
run uses one provider and one destination. A private draft GitHub Security
Advisory accepts only one finding.

To prepare a Linear issue, send:

```text
Use $codex-security:track-findings to prepare finding [finding ID] from
[completed scan directory] for the Linear team [team] and project [project, if
any]. Check for duplicates and show me the exact issue title, body, metadata,
and destination. Do not create or update anything until I approve that payload.
```

To prepare a GitHub issue, send:

```text
Use $codex-security:track-findings to prepare finding [finding ID] from
[completed scan directory] for GitHub repository [owner/repository]. Check open
and closed issues for duplicates and show me the exact issue title, body,
metadata, repository visibility, and authenticated transport. Do not create or
update anything until I approve that payload.
```

To prepare a Jira issue, send:

```text
Use $codex-security:track-findings to prepare finding [finding ID] from
[completed scan directory] for Jira project [project key] as [issue type].
Check for duplicates and show me the exact issue summary, description,
metadata, and destination. Do not create or update anything until I approve
that payload.
```

Jira tracking requires the Atlassian Rovo plugin in Codex. Reusing an issue
requires read access; creating or updating one requires read and write access.

To prepare a private draft GitHub Security Advisory, send:

```text
Use $codex-security:track-findings to prepare finding [finding ID] from
[completed scan directory] as a private draft GitHub Security Advisory in
[owner/repository]. Verify the sealed source revision, repository, affected
paths, package metadata, and duplicate state. Show me the exact advisory
payload, authenticated GitHub CLI identity, and disclosure warnings. Do not
create anything until I approve that payload.
```

Draft advisories require one finding from a sealed `git_revision` scan, the
  verified public canonical source repository, and administrator access. The
  workflow doesn't batch, update, publish, or close advisories. Use an approved
  private issue destination when the source doesn't meet those requirements.

## Review the proposed write

<WorkflowSteps>

1. Confirm the finding ID and fingerprint came from the intended sealed scan.
2. Confirm the provider, exact Linear team, GitHub repository, Jira project, or
   advisory repository, and the live destination visibility.
3. Review the duplicate outcome: `create`, `reuse`, `update`, or `blocked`.
4. Read the complete proposed title, body, source locations, and provider
   metadata. Remove exploit detail or internal evidence that the destination
   shouldn't expose.
5. Approve only that exact payload. A changed destination, visibility, finding
   set, or body requires a new preview.

</WorkflowSteps>

Sensitive findings should go to a private destination. Creating an issue in an
internal or public GitHub repository requires an explicit visibility warning
and approval of the complete content. Treat a draft advisory description as
eventually public and remove credentials, private evidence, and unnecessary
exploit details before approval.

Review and approve external actions in the Codex conversation. Approval
doesn't create a separate issue or advisory screen in the Security workbench.

## Verify the tracked item

After you approve the proposed write, Codex rechecks the sealed source,
destination, access, and duplicate state. For a batch, it processes findings
one at a time and stops at the first uncertain result. Creation, update, or
reuse is complete only after Codex reads the exact issue back and verifies its
binding identifiers and content.

Keep the returned canonical issue or advisory URL with your triage record.
Continue with [Fix and verify a finding](https://learn.chatgpt.com/docs/security/plugin/fix-findings)
when the owner accepts the item for remediation.
