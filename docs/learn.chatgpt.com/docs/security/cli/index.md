---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/cli'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0"]
---

# Codex Security CLI quickstart

Source: https://learn.chatgpt.com/docs/security/cli

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex Security helps security and engineering teams find, confirm, and fix
vulnerabilities. Use its command-line interface (CLI) to scan
repositories you own or have permission to assess, review findings over time,
and check changes before they land.

The Codex Security CLI and SDK are in beta and require access. Follow the
  installation instructions provided with your access. For an interactive scan
  in Codex, start with the [Codex Security plugin
  quickstart](https://learn.chatgpt.com/docs/security/plugin). For connected GitHub repositories, see
  [Codex Security cloud setup](https://learn.chatgpt.com/docs/security/setup).

## Check the prerequisites

The CLI requires Node.js 22 or later. Running a scan or exporting findings also
requires Python 3.10 or later. For more detail, see [Authentication and
prerequisites](https://learn.chatgpt.com/docs/security/cli/reference#authentication-and-prerequisites).

## Set up and verify the CLI

Follow the installation instructions provided for your Codex Security access.
Check the installed version:

```bash
npx codex-security --version
```

List the available commands:

```bash
npx codex-security --help
```

Use `npx codex-security scan --help` or `npx codex-security export --help` for the
complete command help. The [CLI reference](https://learn.chatgpt.com/docs/security/cli/reference)
covers each argument, output format, and exit code.

## Sign in

For local use, sign in with your ChatGPT account:

```bash
npx codex-security login
```

On a remote or headless machine, use device authentication:

```bash
npx codex-security login --device-auth
```

For CI and other automated workflows, use an OpenAI API key instead:

```bash
export OPENAI_API_KEY="<your-api-key>"
```

Keep API keys in your shell or secret manager. Codex Security can also reuse an
existing file-backed Codex sign-in.

Depending on your account and repository, full-repository scans may also
require [Trusted Access for Cyber](https://chatgpt.com/cyber). Signing in or
setting an API key doesn't grant that access.

## Prepare a scan

Choose a repository to scan and a directory to write results.

```bash
REPOSITORY=/path/to/repository
SCAN_DIR=/path/outside/repository/codex-security-results
```

If you omit `--output-dir`, Codex Security saves results in its own persistent
state directory. Results can include source excerpts and vulnerability details,
so choose a private location and an appropriate retention policy.

Check the repository, target, and output directory before starting a scan:

```bash
npx codex-security scan "$REPOSITORY" --output-dir "$SCAN_DIR" --dry-run
```

The dry run checks local inputs without starting Codex, loading credentials,
or probing the plugin's Python interpreter.

## Run your first scan

Run a standard scan and keep its results in the selected directory:

```bash
npx codex-security scan "$REPOSITORY" --output-dir "$SCAN_DIR"
```

The CLI writes the scan result to stdout and sends progress and its completion
summary to stderr. A completed scan prints a summary like this:

```text
codex-security: Findings: 2 (1 high, 1 medium). Coverage: complete.
codex-security: Elapsed: 42s. Workers: 3/6.
codex-security: Results: /path/outside/repository/codex-security-results
codex-security: Next: codex-security export /path/outside/repository/codex-security-results --export-format sarif
```

For a local package installation, run the suggested export command with
`npx codex-security`.

Scans are report-only by default, so findings remain available for local
review. You may want to add a severity threshold when you are ready to [run scans in
CI](https://learn.chatgpt.com/docs/security/cli/ci).

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

## Choose the next scan

Use a path scan when a repository contains separate services or packages:

```bash
npx codex-security scan "$REPOSITORY" --path services/billing --path packages/auth
```

Review committed changes between the base revision and `HEAD`:

```bash
npx codex-security scan "$REPOSITORY" --diff origin/main --head HEAD
```

Review staged and unstaged changes against `HEAD`:

```bash
npx codex-security scan "$REPOSITORY" --working-tree --base HEAD
```

Diff and working-tree scans expect the repository argument to be the Git
worktree root. Fetch the selected revisions before starting a diff scan.

Use deep mode when a repository or path needs broader review:

```bash
npx codex-security scan "$REPOSITORY" --mode deep
```

## Add architecture and security context

Provide architecture documents, threat models, or security policies as scan
context. This helps Codex Security evaluate findings against how your system
actually works:

```bash
npx codex-security scan "$REPOSITORY" \
  --knowledge-base /path/to/architecture.md \
  --knowledge-base /path/to/security-policies
```

## Set a scan budget

Use `--max-cost` to stop a scan when its estimated model cost exceeds a limit
in USD:

```bash
npx codex-security scan "$REPOSITORY" --max-cost 5
```

Requests already in progress can finish above the limit. Codex Security keeps
the available results when a scan stops.

## Scan changes before each commit

Install a Git pre-commit security check for your repository:

```bash
npx codex-security install-hook
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
npx codex-security bulk-scan
```

The interactive flow excludes archived repositories and forks. It asks you to
confirm the selected repositories before scanning.

To scan a prepared repository list, provide a CSV and an output directory:

```bash
npx codex-security bulk-scan repositories.csv \
  --output-dir /path/outside/repositories/security-scans \
  --workers 4
```

Run the same command again to resume an existing bulk scan. Completed
repositories with intact result artifacts aren't scanned again. Add
`--max-attempts 3` when you want to retry temporary repository or scan errors.

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

The container runs bulk scans without prompts. Use the CLI outside Docker when
you want to discover repositories interactively. For private repositories,
provide `GH_TOKEN` or `GITHUB_TOKEN` through your environment or secret
manager. The [sign-in requirements](#sign-in), including account and repository
access, also apply to containerized scans.

## Revisit a saved scan

List the saved scans for your repository:

```bash
npx codex-security scans list "$REPOSITORY"
```

Copy a scan ID from the results to inspect its findings and configuration:

```bash
npx codex-security scans show SCAN_ID
```

Run the same scan against the current checkout using its original configuration:

```bash
npx codex-security scans rerun SCAN_ID
```

To compare two scans, first match findings that share the same root cause:

```bash
npx codex-security scans match PREVIOUS_SCAN_ID CURRENT_SCAN_ID
```

Then check which findings are new, persisting, reopened, resolved, or unknown:

```bash
npx codex-security scans compare PREVIOUS_SCAN_ID CURRENT_SCAN_ID
```

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
