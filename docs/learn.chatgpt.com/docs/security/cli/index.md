---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/cli'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
---

# Codex Security CLI quickstart

Source: https://learn.chatgpt.com/docs/security/cli

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Run a standard scan of a local repository with the standalone Codex Security
CLI. This quickstart ends with a saved report you can review and revisit.
For scans inside a Codex conversation, use the [Codex Security
plugin](https://learn.chatgpt.com/docs/security/plugin).

## Check the prerequisites

You need Node.js 22 (22.13.0 or later), 24, or 26, plus Python 3.10 or later.
Python 3.10 also needs `tomli`. Scans using OpenAI inference require Codex Security access.
Depending on your account and repository, full-repository scans may also
require [Trusted Access for Cyber](https://chatgpt.com/cyber).

The CLI runs with your operating-system permissions and doesn't pause for
approval.
Scan processes can inherit your environment, so remove unrelated credentials
before starting. See [Local scan
permissions](https://learn.chatgpt.com/docs/security/cli/reference#local-scan-permissions).

## Set up and verify the CLI

Run the public package with `npx`:

```bash
npx @openai/codex-security --version
```

The command prints the installed package version. Use `info --json` to check
the bundled plugin version, or `--help` to list commands. Package changes are
listed in the [CLI and SDK releases](https://github.com/openai/codex-security/releases).

## Sign in

Sign in with your ChatGPT account:

```bash
npx @openai/codex-security login
```

On a machine without a browser, add `--device-auth` and follow the displayed
sign-in instructions. Use `--auth chatgpt` in the scan commands below to select
that sign-in even when your environment also contains an API key.

For API keys and other providers, see [Select scan
authentication](https://learn.chatgpt.com/docs/security/cli/reference#select-scan-authentication).
For Amazon Bedrock, use [AWS credentials and model
access](https://learn.chatgpt.com/docs/security/cli/reference#use-amazon-bedrock) instead of a ChatGPT
sign-in or OpenAI API key.

## Prepare a scan

Replace these paths with your repository and a new results directory outside
its Git worktree:

```bash
REPOSITORY=/path/to/repository
SCAN_DIR=/path/outside/repository/codex-security-results
```

Results can include source excerpts and vulnerability details. Choose a private
location. If you omit `--output-dir`, the CLI uses its persistent state directory.

Check the target and output location:

```bash
npx @openai/codex-security scan "$REPOSITORY" \
  --auth chatgpt --output-dir "$SCAN_DIR" --dry-run
```

A successful dry run confirms the local inputs. It doesn't start a scan, load
credentials, or check the plugin's Python interpreter, so it doesn't establish
that authentication and runtime setup will succeed.

## Run your first scan

Remove `--dry-run` to start the scan:

```bash
npx @openai/codex-security scan "$REPOSITORY" \
  --auth chatgpt --output-dir "$SCAN_DIR"
```

An interactive terminal shows a live dashboard. Non-interactive terminals show progress
lines. Add `--headless` to use progress lines in an interactive terminal too.
The dashboard and saved logs can contain source code or credentials. Review
them before sharing.

When the scan finishes, stderr includes the report path, finding count, and
elapsed time. For example:

```text
  REPORT    /path/outside/repository/codex-security-results/report.md

  FINDINGS  2 (2 confirmed this scan; 0 previously found; 1 high, 1 medium)
  ELAPSED   42s
  RESULTS   /path/outside/repository/codex-security-results
```

By default, the severity of a finding doesn't cause a scan to fail. For
machine-readable stdout, add `--json`. To make findings fail a CI check, set a
[severity policy](https://learn.chatgpt.com/docs/security/cli/ci#choose-a-severity-policy).

## Review the results

Open `report.md` from the reported directory. Confirm the target and revision,
then read the coverage before reviewing individual findings.

Check `scan.status` in `scan-manifest.json` to confirm that the scan completed.
Review `coverage.json` for reviewed surfaces, excluded paths, deferred work,
and open questions.

A completed scan exits with `0` unless findings meet a configured severity
threshold, which returns `1`. Coverage gaps don't change the exit code, so
exit `0` doesn't mean every file was reviewed. Input, execution, result-integrity,
or required-output failures return `2`. The
[CLI reference](https://learn.chatgpt.com/docs/security/cli/reference#exit-codes-and-signals) explains
the exit codes.

For each finding, check the affected code, attacker prerequisites, validation
evidence, and remaining uncertainty. A source-based finding doesn't necessarily
include a successful runtime reproduction. Select a finding for remediation
only after its evidence supports the claimed issue.

Keep the scan directory together when sharing or archiving it. It contains
`scan-manifest.json`, `findings.json`, and `coverage.json` alongside the report
and supporting artifacts. See [Scan
artifacts](https://learn.chatgpt.com/docs/security/cli/reference#scan-artifacts) for the full layout.

## Revisit a saved scan

List scans for the repository:

```bash
npx @openai/codex-security scans list "$REPOSITORY"
```

Copy a scan ID from the results:

```bash
npx @openai/codex-security scans show SCAN_ID
```

After a complete interactive scan with findings, the CLI also offers a finding
browser. Review the evidence there before choosing a fix. For saved findings,
use the [validate and patch
commands](https://learn.chatgpt.com/docs/security/cli/reference#codex-security-validate-and-codex-security-patch).

## Choose the next scan

| Goal                                     | Guide                                                                                    |
| ---------------------------------------- | ---------------------------------------------------------------------------------------- |
| Scan selected paths or a diff            | [Select the scan target](https://learn.chatgpt.com/docs/security/cli/reference#select-the-scan-target)           |
| Use deep scans or limit their runtime    | [Configure deep scans](https://learn.chatgpt.com/docs/security/cli/reference#configure-deep-scans)               |
| Supply architecture or security policies | [Add security context](https://learn.chatgpt.com/docs/security/cli/reference#add-security-context)               |
| Change the model or reasoning effort     | [Configure the runtime](https://learn.chatgpt.com/docs/security/cli/reference#configure-the-runtime)             |
| Set an estimated cost limit              | [Output and policy options](https://learn.chatgpt.com/docs/security/cli/reference#set-output-and-policy-options) |
| Scan multiple repositories               | [Bulk scans](https://learn.chatgpt.com/docs/security/cli/bulk-scans)                                             |
| Check pull requests automatically        | [CI guide](https://learn.chatgpt.com/docs/security/cli/ci)                                                       |

For authentication problems, repeat-scan differences, or false-positive
feedback, see the [CLI FAQ](https://learn.chatgpt.com/docs/security/cli/faq).
