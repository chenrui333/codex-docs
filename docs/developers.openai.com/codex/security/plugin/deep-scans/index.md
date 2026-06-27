---
source_type: 'developers'
source_area: 'codex_security'
source_url: 'https://developers.openai.com/codex/security/plugin/deep-scans'
source_last_modified: '2026-06-18T22:38:26Z'
source_etag: 'W/"40ca5f296a56f9f4804dea9a7880b8e7"'
codex_cli_versions: ["0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3"]
codex_cli_versions_raw: ["codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3"]
---

# Run a deep security scan – Codex Security | OpenAI Developers

Source: https://developers.openai.com/codex/security/plugin/deep-scans

A deep scan is slower but more thorough than a standard scan. Use it when you
want to reduce variability and search more comprehensively.

Start with a [standard scan](/codex/security/plugin/scans). Once you’re
satisfied with the results, run a deep scan for a more thorough assessment.

## Choose between standard and deep scans

|  | Standard scan | Deep scan |
| --- | --- | --- |
| Best for | First runs and routine repository or folder review | More thorough reviews after a standard scan |
| Variability | Standard | Reduced |
| Scope | Repository or explicit folder | Repository or explicit folder |
| Runtime and resources | Lower | Higher |
| Pull requests and diffs | Use the change-review workflow | Not supported; use the change-review workflow instead |

## Start the deep scan

For a repository-wide review, send:

```
Use $codex-security:deep-security-scan to run a deep security scan of this repository.
```

For one component in a monorepo, identify the folder explicitly:

```
Use $codex-security:deep-security-scan to run a deep security scan of /absolute/path/to/repository/services/payments.
```

In the Codex app, a scoped deep scan resolves the selected folder as the
**Codebase** and shows its scan area as the entire selected target.

## Confirm setup and preflight

1. Confirm **Scan type** is `Codebase` and **Deep scan** is on.
2. Confirm that **Codebase** is the repository or exact folder you intended to
   scan.
3. Add threat-model guidance only for concrete attack vectors, sensitive
   application areas, or repository context that the code can’t reveal.
4. Select **Start scan**.
5. Review the capability preflight. If it proposes a configuration change,
   review the exact change and let Codex apply it only if it matches your
   environment. Start a new thread if Codex tells you a restart is required.

[![
Your browser does not support the video tag.
](/videos/codex/security/deep-scan-progress-poster.webp)](/videos/codex/security/deep-scan-progress.mp4)

## Review the result

Deep scans use the same findings workspace and generated `report.md` as standard
scans. Review the coverage summary before the findings. A deep scan searches
the code more extensively, but any deferred surface or proof gap still limits
the conclusion. For a finding you accept, continue with [Fix and verify a
finding](/codex/security/plugin/fix-findings).

To review a pull request, commit, branch range, or local patch, use [Review code
changes](/codex/security/plugin/code-changes). A deep scan never substitutes
for the diff-focused workflow.

