---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/cli'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0"]
---

# Codex Security CLI quickstart

Source: https://learn.chatgpt.com/docs/security/cli

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex Security helps security and engineering teams find, confirm, and fix
vulnerabilities. Use its command-line interface (CLI) to scan
repositories you own or have permission to assess, review findings over time,
and check changes before they land.

The `@openai/codex-security` package is public. Running scans requires Codex
  Security access. For an interactive scan in Codex, start with the [Codex
  Security plugin quickstart](https://learn.chatgpt.com/docs/security/plugin). For connected GitHub
  repositories, see [Codex Security cloud setup](https://learn.chatgpt.com/docs/security/setup).

## Check the prerequisites

The CLI requires Node.js 22 (22.13.0 or later), 24, or 26. Scans, bulk scans,
exports, scan history, and saved findings also require Python 3.10 or later.
For more detail, see [Authentication and
prerequisites](https://learn.chatgpt.com/docs/security/cli/reference#authentication-and-prerequisites).

## Set up and verify the CLI

Run the CLI with `npx` and check its version:

```bash
npx @openai/codex-security --version
```

To see both the package version and the version of its bundled plugin, run:

```bash
npx @openai/codex-security info --json
```

See the [CLI and SDK releases](https://github.com/openai/codex-security/releases)
for package changes.

List the available commands:

```bash
npx @openai/codex-security --help
```

See also [CLI reference](https://learn.chatgpt.com/docs/security/cli/reference).

## Sign in

For local use, sign in with your ChatGPT account:

```bash
npx @openai/codex-security login
```

On a remote or headless machine, use device authentication:

```bash
npx @openai/codex-security login --device-auth
```

For CI and other automated workflows, set an OpenAI API key:

```bash
export OPENAI_API_KEY="<your-api-key>"
```

For AWS credentials, see [Amazon Bedrock
setup](https://learn.chatgpt.com/docs/security/cli/reference#use-amazon-bedrock). For [OpenRouter or
Fireworks](https://learn.chatgpt.com/docs/security/cli/reference#use-openrouter-or-fireworks), set the
provider's API key and select a model with `--provider` and `--model`.

To use your ChatGPT sign-in when an API key is also set, select it explicitly:

```bash
npx @openai/codex-security scan . --auth chatgpt
```

To require the environment API key, select API-key authentication:

```bash
npx @openai/codex-security scan . --auth api-key
```

Depending on your account and repository, full-repository scans may also
require [Trusted Access for Cyber](https://chatgpt.com/cyber).

## Prepare a scan

Choose a repository you trust and have permission to assess. Scans use your
local operating-system permissions and don't pause for approval. Scan
processes can inherit your environment, so remove unrelated credentials before
you start. See [Local scan
permissions](https://learn.chatgpt.com/docs/security/cli/reference#local-scan-permissions).

Choose a directory outside the repository for the scan results:

```bash
REPOSITORY=/path/to/repository
SCAN_DIR=/path/outside/repository/codex-security-results
```

If you omit `--output-dir`, Codex Security saves results in its own persistent
state directory. Results can include source excerpts and vulnerability details,
so choose a private location and an appropriate retention policy.

If the default state directory isn't writable, select a writable directory
outside the scanned repository:

```bash
export CODEX_SECURITY_STATE_DIR=/path/outside/repository/codex-security-state
```

Check the repository, target, and output directory before starting a scan:

```bash
npx @openai/codex-security scan "$REPOSITORY" --output-dir "$SCAN_DIR" --dry-run
```

The dry run checks local inputs, including any `--knowledge-base` paths,
without starting Codex, loading credentials, or probing the plugin's Python
interpreter.

## Run your first scan

Run a standard scan and keep its results in the selected directory:

```bash
npx @openai/codex-security scan "$REPOSITORY" --output-dir "$SCAN_DIR"
```

Interactive terminals show a live scan dashboard. Add `--headless` to show
plain progress lines instead. CI and terminals without an interactive session
use plain progress automatically.

The dashboard also shows live session details. These can contain source code
or credentials, so review them before sharing.

By default, the CLI writes scan progress and its completion summary to stderr.
It doesn't print the full scan result to stdout. A completed scan prints a
summary like this:

```text
  REPORT    /path/outside/repository/codex-security-results/report.md

  FINDINGS  2 (2 confirmed this scan; 0 previously found; 1 high, 1 medium)
  COVERAGE  complete
  ELAPSED   42s
  RESULTS   /path/outside/repository/codex-security-results
```

Token usage and estimated cost appear when available. To print the complete
result as machine-readable JSON, request structured output explicitly:

```bash
npx @openai/codex-security scan "$REPOSITORY" --output-dir "$SCAN_DIR" --json
```

Scans are report-only by default, so findings remain available for local
review. You may want to add a severity threshold when you are ready to [run scans in
CI](https://learn.chatgpt.com/docs/security/cli/ci).

## Choose a model and reasoning effort

Scans use `gpt-5.6-sol` with `xhigh` reasoning effort by default. Select a
different model and effort when the task requires them:

```bash
npx @openai/codex-security scan "$REPOSITORY" \
  --model gpt-5.6-terra \
  --effort high
```

Supported effort levels are `minimal`, `low`, `medium`, `high`, `xhigh`, and
`max`.

## Review the results

Open `report.md` for the readable result. The scan directory also contains the
structured files used by automation:

```text
codex-security-results/
├── scan-manifest.json
├── findings.json
├── coverage.json
├── report.md
├── artifacts/
└── exports/
    └── results.sarif       # when produced
```

- `scan-manifest.json` records the target, scope, producer, and sealed
  artifacts.
- `findings.json` records severity, confidence, locations, evidence, and
  remediation for each finding.
- `coverage.json` records reviewed surfaces, exclusions, deferred work, open
  questions, and coverage completeness.

Coverage can be `complete`, `partial`, or `unknown`. Read any deferred areas or
open questions before treating the scan as evidence of review.
The [CLI reference](https://learn.chatgpt.com/docs/security/cli/reference#scan-artifacts) describes
the full artifact and output contract.

## Review and patch findings

After a complete interactive scan with findings, the CLI offers a finding
browser. Review the evidence and choose which findings to fix. You can find
the saved tasks in the Codex desktop app.

To patch high and critical findings without the browser:

```bash
npx @openai/codex-security scan "$REPOSITORY" \
  --patch --patch-severity high --json
```

Add `--create-pr` to commit verified patches and open a GitHub pull request.

You can also patch saved findings or import Linear issues. See the
[`validate` and `patch` reference](https://learn.chatgpt.com/docs/security/cli/reference#codex-security-validate-and-codex-security-patch).

## Choose the next scan

Use a path scan when a repository contains separate services or packages:

```bash
npx @openai/codex-security scan "$REPOSITORY" \
  --path services/billing \
  --path packages/auth
```

Review committed changes between the base revision and `HEAD`:

```bash
npx @openai/codex-security scan "$REPOSITORY" --diff origin/main --head HEAD
```

Review staged and unstaged changes against `HEAD`:

```bash
npx @openai/codex-security scan "$REPOSITORY" --working-tree --base HEAD
```

Diff and working-tree scans expect the repository argument to be the Git
worktree root. Fetch the selected revisions before starting a diff scan.

Use deep mode when a repository or path needs broader review:

```bash
npx @openai/codex-security scan "$REPOSITORY" --mode deep
```

To control workers, subagents, and when the scan stops:

```bash
npx @openai/codex-security scan "$REPOSITORY" \
  --mode deep \
  --workers 2 \
  --subagents 0 \
  --stop-after-no-new 3 \
  --max-discovery-runs 10 \
  --max-time-hours 1.5
```

These options require deep mode, which supports repository and path targets,
not diff or working-tree scans. Here, `--workers` controls independent
standard-scan workers within one scan; `bulk-scan --workers` controls concurrent
repository scans. `--max-time-hours` accepts a positive number up to `96`,
including fractional hours. At the limit, the scan stops unfinished workers,
preserves completed scan results, and aggregates them into the final report.

## Add architecture and security context

Provide architecture documents, threat models, or security policies as scan
context. This helps Codex Security evaluate findings against how your system
actually works:

```bash
npx @openai/codex-security scan "$REPOSITORY" \
  --knowledge-base /path/to/architecture.md \
  --knowledge-base /path/to/security-policies
```

## Add custom scan instructions

Add instructions that focus the scan on your security priorities. Use a
second file for follow-up instructions:

```bash
npx @openai/codex-security scan "$REPOSITORY" \
  --scan-prompt-file /path/to/scan.md \
  --post-scan-prompt-file /path/to/follow-up.md
```

The follow-up runs in the same authenticated session after successful scans
and scans with incomplete coverage or errors. If the follow-up fails, the CLI
reports a warning and keeps the completed scan. It doesn't run after
cancellation or a scan that reaches its cost limit. Both options also work
with `bulk-scan`; a CSV `prompt` column adds repository-specific instructions.

## Set a scan budget

Use `--max-cost` to stop a scan when its estimated model cost exceeds a limit
in USD:

```bash
npx @openai/codex-security scan "$REPOSITORY" --max-cost 5
```

Requests already in progress can finish slightly above the limit. If a deep
scan reaches the limit after Codex Security aggregates completed worker
results, the CLI saves the completed report, marks its coverage as `partial`,
and returns exit code `2`. If the scan can't produce a completed report, any
available partial output stays on disk.

## Scan changes before each commit

Install a Git pre-commit security check for your repository:

```bash
npx @openai/codex-security install-hook
```

The check scans staged and unstaged changes before each commit. It blocks
high-severity findings and scan errors without replacing an existing
pre-commit script.

## Scan repositories in bulk

Sign in to GitHub before discovering repositories:

```bash
gh auth login
```

Discover and select repositories from your GitHub account or organization:

```bash
npx @openai/codex-security bulk-scan
```

The interactive flow excludes archived repositories and forks. It asks you to
confirm the selected repositories before scanning.

To scan a prepared repository list, provide a CSV and an output directory:

```bash
npx @openai/codex-security bulk-scan repositories.csv \
  --output-dir /path/outside/repositories/security-scans \
  --workers 4
```

Run the same command again to resume an existing bulk scan. Codex Security
skips completed repositories. Add `--max-attempts 3` when you want to retry
temporary repository or scan errors.

For GitHub discovery, CSV preparation, campaign results, and Docker setup, see
[Run bulk security scans](https://learn.chatgpt.com/docs/security/cli/bulk-scans).

## Run bulk scans in Docker

If your access includes the Codex Security Docker image, use the supplied
hardened Compose configuration and security profile on a Linux Docker host.
The host must support unprivileged user namespace creation. Supply a repository
CSV, keep results and sign-in state in persistent mounted directories, and
provide credentials through your environment or a secret manager:

```bash
docker compose run --rm codex-security \
  bulk-scan /input/repositories.csv \
  --output-dir /output \
  --workers 4
```

The container runs bulk scans without interactive prompts. Use the CLI outside
Docker when you want to discover repositories interactively. For private
repositories, provide `GH_TOKEN` or `GITHUB_TOKEN` through your environment or
secret manager. The [sign-in requirements](#sign-in), including account and
repository access, also apply to containerized scans.

## Revisit a saved scan

List the saved scans for your repository:

```bash
npx @openai/codex-security scans list "$REPOSITORY"
```

Copy a scan ID from the results to inspect its findings and configuration:

```bash
npx @openai/codex-security scans show SCAN_ID
```

To inspect the saved events from a scan and its workers:

```bash
npx @openai/codex-security scans logs SCAN_ID
```

Saved logs aren't redacted and can contain source code or credentials. Review
them before sharing.

List open findings across the repository's scans:

```bash
npx @openai/codex-security findings list "$REPOSITORY"
```

An earlier finding stays open when the latest scan doesn't confirm it.

To mark a reviewed finding as a false positive, explain why the finding doesn't
apply:

```bash
npx @openai/codex-security findings false-positive FINDING_OCCURRENCE_ID \
  --reason "The route already checks permissions"
```

Later scans consider that explanation but still recheck the current code.

Run the same scan against the current checkout using its original configuration:

```bash
npx @openai/codex-security scans rerun SCAN_ID
```

Compare two scans to find new, persisting, reopened, resolved, or unknown
findings:

```bash
npx @openai/codex-security scans compare PREVIOUS_SCAN_ID CURRENT_SCAN_ID
```

The comparison automatically matches findings by root cause and reuses saved
matches.

For the bulk-scan CSV format, scan-history filters, and command options, see
the [CLI reference](https://learn.chatgpt.com/docs/security/cli/reference).

Continue with the workflow that fits your goal:

- [Run bulk security scans](https://learn.chatgpt.com/docs/security/cli/bulk-scans) to discover GitHub
  repositories or scan a pinned CSV inventory.
- [Read the CLI FAQ](https://learn.chatgpt.com/docs/security/cli/faq) for answers about scan history,
  false-positive feedback, coverage, and fix verification.
- [Run scans in CI](https://learn.chatgpt.com/docs/security/cli/ci) to review pull requests, preserve
  results, and set a severity policy.
- [Use the CLI reference](https://learn.chatgpt.com/docs/security/cli/reference) to check every flag,
  output format, artifact, and exit code.
- [Integrate the TypeScript SDK](https://learn.chatgpt.com/docs/security/sdk) to run scans from an
  application or developer tool.
