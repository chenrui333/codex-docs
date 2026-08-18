---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/plugin/deep-scans'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0"]
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

## Configure deep-scan runtime

To control a deep scan's concurrency and duration, create or edit
`~/.codex/codex-security/config.toml`. If you set `CODEX_HOME`, use
`$CODEX_HOME/codex-security/config.toml` instead.

For example, this profile runs a shorter scan with limited concurrency:

```toml
[deep_scan]
workers = 2
subagents = 0
stop_after_no_new = 3
max_discovery_runs = 10
max_time_hours = 1.5
```

| Setting                         | Default | Description                                                                                                        |
| ------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------ |
| `workers`                       | `4`     | Number of independent standard-scan workers allowed to run at the same time. Legacy `"auto"` also resolves to `4`. |
| `subagents`                     | `3`     | Number of subagents each worker may start. Set `0` to disable them.                                                |
| `stop_after_no_new`             | `4`     | Stop after this many consecutive completed worker scans produce no new findings.                                   |
| `stop_after_consecutive_errors` | `3`     | Stop after this many consecutive worker errors.                                                                    |
| `max_discovery_runs`            | `40`    | Limit the number of independent standard-scan runs before aggregation.                                             |
| `max_time_hours`                | `96`    | Limit worker execution to a positive number of hours up to `96`; use fractions as needed.                          |

Lower values can reduce scan time and token use but may miss findings.
Configuration changes apply to new deep scans, not scans already in progress.

When the time limit expires, Codex Security stops unfinished workers, keeps
completed scan results, and aggregates them into the final report. If no worker
finishes source review before the deadline, the report records partial
coverage.

The `max_time_hours` setting requires plugin version `0.1.19` or later. See the
[plugin changelog](https://learn.chatgpt.com/docs/security/plugin/changelog) for release details.

## Start the deep scan

In the desktop app, open **Security**, select **Scans**, and select **+ Scan**.
Choose a repository or another folder, select **Codebase**, and turn on
**Deep scan**. The scan covers the entire selected repository or folder.

You can also start a repository-wide deep scan from a Codex conversation:

```text
Use $codex-security:deep-security-scan to run a deep security scan of this repository.
```

For one component in a monorepo, identify the folder explicitly:

```text
Use $codex-security:deep-security-scan to run a deep security scan of /absolute/path/to/repository/services/payments.
```

For a scoped deep scan in the desktop app, select the folder as the codebase.
The scan covers the entire selected folder.

## Confirm setup and preflight

For the best scan quality, use `gpt-5.6-sol`
with `xhigh` reasoning effort.

<WorkflowSteps>

1. Select **Codebase** and turn on **Deep scan**.
2. Confirm that the repository or selected folder is the code you intended to
   scan.
3. Choose a model and reasoning effort.
4. Open **Additional context** for concrete attack vectors, sensitive
   application areas, or repository context that the code can't reveal.
5. Select **Start scan**.

</WorkflowSteps>

Deep scan workers inherit your selected model and reasoning settings. Each
worker runs a complete standard scan, and Codex Security aggregates the
completed results. Follow the saved scan from **Scans**, or select **View
activity** to inspect its Codex task. Check the [plugin
changelog](https://learn.chatgpt.com/docs/security/plugin/changelog) before you update the plugin or
start a long-running scan.

<figure className="not-prose my-8">
  <CodexScreenshot
    alt="Native Codex Security workbench showing a deep scan and its active review phase"
    lightSrc={deepScanProgress.src}
    darkSrc={deepScanProgressDark.src}
    maxHeight="520px"
  />
  <figcaption className="mt-3 text-sm text-secondary">
    Track the active deep-scan phase and inspect its Codex activity before
    reviewing the completed result.
  </figcaption>
</figure>

## Review the result

Deep scans use the same saved scan details and complete scan directory as
standard scans. Open the completed scan in **Scans** or review its findings in
**Findings**. The generated `report.md` links to detailed vulnerability reports
or structural hardening guidance when you request those outputs.
Keep any linked `findings/` and `hardening/` directories with the report when
sharing or archiving the result.

Review the coverage summary before the findings. Even a deep scan has limits,
so check deferred surfaces and remaining proof gaps before drawing a
conclusion. For a finding you accept, continue with [Fix and verify a
finding](https://learn.chatgpt.com/docs/security/plugin/fix-findings).

To review a pull request, commit, branch range, or local patch, use [Review code
changes](https://learn.chatgpt.com/docs/security/plugin/code-changes). A deep scan never substitutes
for the diff-focused workflow.
