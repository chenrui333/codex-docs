---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin/scans'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Run a Codex Security scan

Source: https://learn.chatgpt.com/docs/security/plugin/scans

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use a standard scan to review a repository or folder.
If you haven't installed the plugin, start with the [plugin
quickstart](https://learn.chatgpt.com/docs/security/plugin).

For repeated reviews of the same scope, use a [deep
scan](https://learn.chatgpt.com/docs/security/plugin/deep-scans). For a pull request or local diff,
[review code changes](https://learn.chatgpt.com/docs/security/plugin/code-changes).

## Choose the scan area

In the desktop app, open **Security**, select **Scans**, and select **+ Scan**.
Choose an existing repository or another folder, then select **Codebase**.

Scan the whole repository, or select a folder to review one service or package
in a monorepo.

You can also start a scan from a Codex conversation:

```text
Use $codex-security:security-scan to scan this repository for security vulnerabilities.
```

To focus that conversation on a particular folder, identify the component:

```text
Use $codex-security:security-scan to scan only services/billing in this repository for security vulnerabilities.
```

## Configure the scan

For the best scan quality, use `gpt-5.6-sol`
with `xhigh` reasoning effort.

<WorkflowSteps>

1. Select **Codebase** and leave **Deep scan** off.
2. Confirm the selected repository, current branch, and latest revision.
3. Set **Scan area** to the entire repository or choose one folder.
4. Choose a model and reasoning effort.
5. Use **Additional context** to describe attacker-controlled inputs, trust
   boundaries, sensitive actions, or an area to prioritize.
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

## Follow scan progress

The workbench shows the current phase and reported progress. Select **View
activity** to inspect the Codex task. Review the final result after the scan
finishes, since findings can change while Codex checks the evidence.

## Review the completed scan

Check the target, revision, scan area, and any areas the scan deferred. For each
finding, review the attack path, failed control, supported impact, validation
method, and unresolved questions. Source analysis can support a finding without
a runtime reproduction. If execution could resolve an open question, ask Codex
to validate that finding.

When dismissing a finding, record why it doesn't apply. To address an accepted
finding, [generate and verify a fix](https://learn.chatgpt.com/docs/security/plugin/fix-findings).

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

## Use your first scan as a baseline

To compare scans, record the revision, plugin version, model, and reasoning
effort. If you're testing against a known vulnerability, also record whether
you supplied it to Codex or withheld it.

## Reopen a previous scan

Open **Security**, then select a saved scan from **Scans** to review its
findings, coverage, and available report artifacts. To assess the latest code,
start a new scan for the same repository. The new scan doesn't replace the
earlier scan or its artifacts.

## Use the results

Open `report.md` for a portable report, and keep its scan directory together
when sharing or archiving it. Use [Export and track
findings](https://learn.chatgpt.com/docs/security/plugin/export-findings) for other formats or issue
tracking.
