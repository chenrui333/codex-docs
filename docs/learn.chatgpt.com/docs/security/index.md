---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Codex Security

Source: https://learn.chatgpt.com/docs/security

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex Security reviews code for vulnerabilities and reports evidence you can
use to investigate and fix them. Choose how to run it based on where your code
lives and how you want to review the results.

The **Overview** in Daybreak Defense Factory shows proposed fixes and tracks [open and fixed findings](https://learn.chatgpt.com/docs/security/findings-and-fixes) across your repositories.

> Illustration: Daybreak Overview with proposed fixes across three repositories, open findings by severity, and the daily trend for new and fixed findings.

## Choose where to start

| Use                      | When you want to                                                                              | Start here                                          |
| ------------------------ | --------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Daybreak Defense Factory | Scan a GitHub repository, review findings from other tools, and propose fixes with your team. | [Set up Daybreak](https://learn.chatgpt.com/docs/security/setup)            |
| Codex Security plugin    | Scan a local repository in Codex and work through findings interactively.                     | [Run your first local scan](https://learn.chatgpt.com/docs/security/plugin) |
| Codex Security CLI       | Run repeatable terminal scans or add checks to CI.                                            | [CLI quickstart](https://learn.chatgpt.com/docs/security/cli)               |
| Codex Security SDK       | Run scans and handle results in an application or developer tool.                             | [SDK guide](https://learn.chatgpt.com/docs/security/sdk)                    |

## Choose the next task

After a local scan, review its scope and findings before deciding what to do next.

| Task                                                  | Guide                                                               |
| ----------------------------------------------------- | ------------------------------------------------------------------- |
| Focus a scan on a service or add security context     | [Run a security scan](https://learn.chatgpt.com/docs/security/plugin/scans)                 |
| Run repeated reviews of the same repository or folder | [Run a deep scan](https://learn.chatgpt.com/docs/security/plugin/deep-scans)                |
| Check a pull request, commit, or local diff           | [Review code changes](https://learn.chatgpt.com/docs/security/plugin/code-changes)          |
| Assess findings from another scanner or issue tracker | [Triage a backlog](https://learn.chatgpt.com/docs/security/plugin/triage-backlog)           |
| Generate a patch and check whether it fixes the issue | [Fix and verify findings](https://learn.chatgpt.com/docs/security/plugin/fix-findings)      |
| Share results or assign remediation work              | [Export and track findings](https://learn.chatgpt.com/docs/security/plugin/export-findings) |

For automation, use the CLI guides to [scan repositories in
bulk](https://learn.chatgpt.com/docs/security/cli/bulk-scans) or [run scans in
CI](https://learn.chatgpt.com/docs/security/cli/ci). Look up commands and defaults in the
[CLI reference](https://learn.chatgpt.com/docs/security/cli/reference).

Codex Security scans application code. For permissions and sandbox controls
that govern Codex itself, see [Agent approvals and
security](https://learn.chatgpt.com/docs/agent-approvals-security).
