---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin/deep-scans'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0"]
---

# Run a deep security scan

Source: https://learn.chatgpt.com/docs/security/plugin/deep-scans

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Run a deep scan when you need a more thorough review and can allow for a longer
runtime. Deep scans search a repository more extensively and can reduce
variability between runs.

Start with a [standard scan](https://learn.chatgpt.com/docs/security/plugin/scans) to check your scope
and results. Then use a deep scan when you need a more thorough assessment.

## Choose between standard and deep scans

|                         | Standard scan                                      | Deep scan                                             |
| ----------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| Best for                | First runs and routine repository or folder review | More thorough reviews after a standard scan           |
| Variability             | Standard                                           | Reduced                                               |
| Scope                   | Repository or explicit folder                      | Repository or explicit folder                         |
| Runtime and resources   | Lower                                              | Higher                                                |
| Pull requests and diffs | Use the change-review workflow                     | Not supported; use the change-review workflow instead |

## Start the deep scan

For a repository-wide review, send:

```text
Use $codex-security:deep-security-scan to run a deep security scan of this repository.
```

For one component in a monorepo, identify the folder explicitly:

```text
Use $codex-security:deep-security-scan to run a deep security scan of /absolute/path/to/repository/services/payments.
```

For a scoped deep scan in the ChatGPT desktop app, the selected folder becomes
the **Codebase**. The scan area covers the entire selected folder.

## Confirm setup and preflight

<WorkflowSteps>

1. Confirm **Scan type** is `Codebase` and **Deep scan** is on.
2. Confirm that **Codebase** is the repository or exact folder you intended to
   scan.
3. Add threat-model guidance only for concrete attack vectors, sensitive
   application areas, or repository context that the code can't reveal.
4. Select **Start scan**.
5. Review the capability preflight. If it proposes a configuration change,
   review the exact change and let Codex apply it only if it matches your
   environment. Start a new chat if Codex tells you a restart is required.

</WorkflowSteps>

Deep scans require delegated workers and at least six usable worker slots. If
the current runtime doesn't meet those requirements, use a standard scan or
move the task to a runtime that passes the capability preflight.

On supported desktop-app versions, discovery workers inherit your selected
model and reasoning settings. Keep the scan active until Codex reports that it
is complete. Reopening or rerunning a saved scan doesn't pin the plugin version
or guarantee that work interrupted by an update will resume. Check the [plugin
changelog](https://learn.chatgpt.com/docs/security/plugin/changelog) before you update the plugin or
start another deep scan.

<VideoPlayer
  src="/videos/codex/security/deep-scan-progress.mp4"
  poster="/videos/codex/security/deep-scan-progress-poster.webp"
/>

## Review the result

Deep scans use the same findings workspace and complete scan directory as
standard scans. Start with `report.md`, which links to one detailed report for
each reportable finding and a structural hardening portfolio when findings
remain. Keep the linked `findings/` and `hardening/` directories with the
report when sharing or archiving the result.

Review the coverage summary before the findings. Even a deep scan has limits,
so check deferred surfaces and remaining proof gaps before drawing a
conclusion. For a finding you accept, continue with [Fix and verify a
finding](https://learn.chatgpt.com/docs/security/plugin/fix-findings).

To review a pull request, commit, branch range, or local patch, use [Review code
changes](https://learn.chatgpt.com/docs/security/plugin/code-changes). A deep scan never substitutes
for the diff-focused workflow.
