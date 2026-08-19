---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin/fix-findings'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0"]
---

# Fix and verify security findings

Source: https://learn.chatgpt.com/docs/security/plugin/fix-findings

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use Codex Security to turn an accepted security finding into a focused,
verified patch. You can work in the Security workbench or run the remediation
workflow from a prompt, the command line, or CI/CD. Codex validates the issue
and, when testing is safe and practical, adds a focused regression test that
fails before the fix and passes after it. It also checks that legitimate
behavior still works. If a regression test is unsafe or infeasible, Codex
records the proof gap and provides the strongest repeatable validation
artifact instead.

Start with one accepted finding and review the proposed patch and verification
evidence. If the workflow meets your standards, process other accepted
findings one at a time in separate Codex tasks or CI/CD jobs. Keeping each task
scoped makes its code changes and evidence easier to review.

## Fix a finding in the UI

Open an accepted finding from **Findings** or a completed scan in **Scans**.
Review its evidence, then use **Patch** to generate, review, apply, and verify
one focused fix.

<WorkflowSteps variant="headings">

1. Generate a focused patch

   Open the finding, select the **Patch** tab, and select **Generate patch**.
   Codex validates or reproduces the issue when feasible and writes a patch
   artifact without modifying the selected checkout.

2. Review the proposed diff

   Read every changed source, regression test, and validation artifact. Reject
   broad refactors, unrelated cleanup, or changes that weaken another security
   control.

3. Apply the patch locally

   Select **Apply patch** only after the diff is acceptable. Codex applies the
   exact generated patch to the working tree and records that state. Review the
   working-tree diff before continuing.

4. Verify the fix

   Select **Verify fix**. Codex reruns the original reproducer or the strongest
   available exploit check. If a regression test is safe and practical, Codex
   checks that it fails before the fix and passes after it. If the test is
   unsafe or infeasible, Codex records the proof gap and provides the
   strongest repeatable validation artifact instead. It also checks
   legitimate behavior, nearby bypasses, and relevant repository tests.

5. Close the finding deliberately

   Verification doesn't automatically close a finding. Review the commands,
   results, and remaining proof gap, then close the finding with an accurate
   reason or keep it open for more work.

</WorkflowSteps>

<figure className="not-prose my-8">
  <CodexScreenshot
    alt="Native Codex Security workbench showing the generated patch for an accepted finding"
    lightSrc={fixFindingPatch.src}
    darkSrc={fixFindingPatchDark.src}
    maxHeight="460px"
  />
  <figcaption className="mt-3 text-sm text-secondary">
    Review the generated security fix before applying it to your checkout.
  </figcaption>
</figure>

## Fix a finding from the CLI

Use the Codex CLI for an accepted finding from a scan, ticket, advisory,
disclosure, security assessment, or internal review.

Install Codex Security in the `CODEX_HOME` that `codex exec` uses before you
run these commands. A fresh CI runner doesn't include marketplace plugins by
default.

```text
Use $codex-security:fix-finding to fix finding <finding-id> from <report-path>. Validate the issue, make the smallest safe change, and add a focused regression test that fails before the fix and passes after it. If that test is unsafe or infeasible, record the proof gap and provide the strongest repeatable validation artifact instead. Verify that the issue no longer reproduces.
```

Include the known source, sink, attacker input, impact, expected invariant,
reproducer, affected files, and validation command. Codex can inspect the
repository for missing technical details. It should ask before assuming a
product policy or intended security invariant.

For an automated run, check out the code, make the finding report available,
and install the plugin in the runner's `CODEX_HOME`. Then enable workspace
writes and pass the prompt to `codex exec`:

```bash
codex exec --sandbox workspace-write 'Use $codex-security:fix-finding to fix finding <finding-id> from <report-path>. Validate the issue, make the smallest safe change, and add a focused regression test that fails before the fix and passes after it. If that test is unsafe or infeasible, record the proof gap and provide the strongest repeatable validation artifact instead. Verify that the issue no longer reproduces.'
```

## Scan and fix findings in CI/CD

Install Codex Security in the runner's `CODEX_HOME` before you invoke either
skill. The commands below use the installed plugin; they don't install it.

In CI/CD, separate the change scan from remediation and require the scan to
leave the checkout unchanged. Preserve the completed scan directory as a job
artifact, review the findings, and start a separate Codex task or job for each
finding accepted for remediation.

By default, `codex exec` uses a read-only sandbox. Run both the change scan and
remediation with `--sandbox workspace-write`. The scan needs that permission
to save temporary artifacts, but its prompt must still require `Do not modify
the checkout`. Remediation needs the same permission to write the focused
patch and verification evidence. See [Permissions and
safety](https://learn.chatgpt.com/docs/non-interactive-mode#permissions-and-safety).

For each scan and accepted finding:

1. Resolve the base and head revisions for the change.
2. Run `$codex-security:security-diff-scan` against that diff without modifying
   the checkout.
3. Preserve the complete scan directory and select the findings to fix.
4. Invoke `$codex-security:fix-finding` once for each accepted finding, passing
   its finding ID and completed scan directory.
5. Generate one focused patch and add a regression test that fails before the
   fix and passes after it. If that test is unsafe or infeasible, record the
   proof gap and use the strongest repeatable validation artifact instead.
6. Verify the original issue and legitimate behavior. Return each patch, test
   or fallback validation artifact, verification command, and any proof gap
   independently.

First, scan the change without modifying the checkout:

```bash
codex exec --sandbox workspace-write 'Use $codex-security:security-diff-scan to review changes from <base-revision> to <head-revision> for security regressions. Do not modify the checkout.'
```

Then fix one accepted finding from the completed scan:

```bash
codex exec --sandbox workspace-write 'Use $codex-security:fix-finding to fix finding <finding-id> from <completed-scan-directory>. Validate the finding, generate one minimal patch, and add a focused regression test that fails before the fix and passes after it. If that test is unsafe or infeasible, record the proof gap and provide the strongest repeatable validation artifact instead. Verify that the issue no longer reproduces.'
```

Repeat the second command in an independent task or job for each remaining
accepted finding. After verification, merge each patch through your normal
code-review and release process. To hand findings to another team before
remediation, see [Export or track
findings](https://learn.chatgpt.com/docs/security/plugin/export-findings).
