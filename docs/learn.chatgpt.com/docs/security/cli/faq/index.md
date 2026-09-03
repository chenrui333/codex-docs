---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/cli/faq'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0"]
---

# Codex Security CLI FAQ

Source: https://learn.chatgpt.com/docs/security/cli/faq

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Find answers to common questions about scanning repositories and managing
security findings from the terminal. For installation and a first scan, start
with the [CLI quickstart](https://learn.chatgpt.com/docs/security/cli).

## Repository scans

### Who can use the CLI

The `@openai/codex-security` package is public.

Running scans requires Codex Security access. For best results, use an account
verified for [Trusted Access for Cyber](https://chatgpt.com/cyber).

### Why does a scan use an API key after sign-in

When your environment includes `OPENAI_API_KEY` or `CODEX_API_KEY`, scans
without an interactive terminal and JSON and JSONL scans use the environment
API key by default, even after a successful ChatGPT or access-token login.
Interactive scans with text output ask you to choose when a ChatGPT sign-in is
also available. Dry runs don't prompt or load credentials.

To use your stored credentials for a scan, select them explicitly:

```bash
npx @openai/codex-security scan . --auth chatgpt
```

To require an API key from `OPENAI_API_KEY` or `CODEX_API_KEY`:

```bash
npx @openai/codex-security scan . --auth api-key
```

To make your stored credentials the automatic default, run
`unset OPENAI_API_KEY CODEX_API_KEY`. For all supported authentication modes,
see the [CLI reference](https://learn.chatgpt.com/docs/security/cli/reference#select-scan-authentication).

### How does bulk repository scanning work

Sign in with GitHub CLI:

```bash
gh auth login
```

Discover and select repositories from a GitHub account or organization:

```bash
npx @openai/codex-security bulk-scan
```

For a prepared list, provide a repository CSV and an output directory:

```bash
npx @openai/codex-security bulk-scan repositories.csv \
  --output-dir /path/outside/repositories/security-scans \
  --workers 4
```

See [Run bulk security scans](https://learn.chatgpt.com/docs/security/cli/bulk-scans) for GitHub
discovery, the CSV format, campaign results, and available options.

### Can an interrupted bulk scan resume

Yes. Run the same bulk-scan command with the original CSV and output directory.
Codex Security skips completed repositories.

Add `--max-attempts 3` to retry temporary repository or scan errors:

```bash
npx @openai/codex-security bulk-scan repositories.csv \
  --output-dir /path/outside/repositories/security-scans \
  --workers 4 \
  --max-attempts 3
```

A completed scan with `partial` or `unknown` coverage keeps its results and
causes the campaign to exit with code `2`. It isn't retried, even with
`--max-attempts`.

### How can a scan use architecture and security policies

Pass architecture documents, threat models, or security policies with
`--knowledge-base`:

```bash
npx @openai/codex-security scan . \
  --knowledge-base /path/to/architecture.md \
  --knowledge-base /path/to/security-policies
```

Codex Security uses these documents as context for the current scan. For
supported file types and directory behavior, see [Add security
context](https://learn.chatgpt.com/docs/security/cli/reference#add-security-context).

## Findings and coverage

### Where can teams find earlier scan results

List saved scans for your repository:

```bash
npx @openai/codex-security scans list /path/to/repository
```

Use a scan ID from the results to inspect its findings:

```bash
npx @openai/codex-security scans show SCAN_ID
```

Each completed scan keeps its report, findings, coverage, and supporting
artifacts together. See [Scan
artifacts](https://learn.chatgpt.com/docs/security/cli/reference#scan-artifacts) for the full layout.

To inspect saved scan and worker events, run `scans logs SCAN_ID`. These logs
aren't redacted and can contain source code or credentials.

### What if the CLI can't save scan history

Codex Security keeps scan history in a workbench database. If the default
state directory isn't writable, choose a private directory outside the
repository:

```bash
export CODEX_SECURITY_STATE_DIR=/path/outside/repository/codex-security-state
```

### How do scans distinguish new and known findings

List the open findings from all scans of a repository:

```bash
npx @openai/codex-security findings list /path/to/repository
```

The list identifies findings confirmed in the latest scan and earlier open
findings that the scan didn't confirm.

Compare findings across the two scans:

```bash
npx @openai/codex-security scans compare PREVIOUS_SCAN_ID CURRENT_SCAN_ID
```

The comparison automatically matches findings by root cause, reuses saved
matches, and identifies new, persisting, reopened, resolved, and unknown
findings. A finding counts as resolved only when the later scan covers its
original target and affected path without coverage gaps.

### How does false-positive feedback work

Inspect the saved scan to find the occurrence ID:

```bash
npx @openai/codex-security scans show SCAN_ID
```

Record why that finding doesn't apply:

```bash
npx @openai/codex-security findings false-positive FINDING_OCCURRENCE_ID \
  --reason "The framework escapes this input before it reaches the query"
```

Future scans of the same repository receive that explanation as context. They
still independently check the current source, controls, and reachability. A
dismissal doesn't suppress a rule, path, or vulnerability class.

For command details, see the [findings
reference](https://learn.chatgpt.com/docs/security/cli/reference#codex-security-findings).

### Why can repeat scans return different findings

AI-assisted scans can vary, even with the same scan configuration. Start by
rerunning your baseline scan:

```bash
npx @openai/codex-security scans rerun BASELINE_SCAN_ID
```

The rerun keeps the original scan configuration and requires the same plugin
version. If the installed plugin has changed, the command stops.

Compare the baseline with the new scan:

```bash
npx @openai/codex-security scans compare BASELINE_SCAN_ID REPEAT_SCAN_ID
```

Provide shared architecture and security guidance when missing context may
contribute to the variation. Matching can identify the same underlying finding
across runs, but it doesn't make scans deterministic. Directly recheck any
important finding that disappears.

### How can a team confirm that a fix worked

After applying a fix, rerun the original scan:

```bash
npx @openai/codex-security scans rerun BEFORE_SCAN_ID
```

Compare the original findings with the new scan:

```bash
npx @openai/codex-security scans compare BEFORE_SCAN_ID AFTER_SCAN_ID
```

Confirm that the new scan covers the original target and affected path without
coverage gaps. Then directly recheck the original finding against the current
checkout:

```bash
npx @openai/codex-security validate /path/to/original/findings.json \
  "Recheck the SQL injection in src/orders.ts:42 against the current code"
```

A missing finding or scan comparison alone doesn't prove that a fix worked.

### What does incomplete coverage mean

Coverage can be `complete`, `partial`, or `unknown`. Review `coverage.json`
for excluded paths, deferred surfaces, and open questions before treating a
scan as evidence of review.

Scans with partial or unknown coverage return exit code `2`, even without a
severity policy. They still keep any available findings and coverage. A later
scan can't establish that an earlier finding no longer exists when it doesn't
cover that finding's original path.

## Automation and cost

### How do deep-scan time limits work

Set a worker deadline when starting a deep scan:

```bash
npx @openai/codex-security scan . --mode deep --max-time-hours 1.5
```

The default is `96` hours. Use any positive value up to `96`, including
fractions. At the deadline, Codex Security stops unfinished workers, keeps
completed standard-scan results, and aggregates them into the final report. If
no worker finishes source review, the report records partial coverage and the
CLI returns exit code `2`.

For persistent settings or bulk campaigns, set `max_time_hours` under
`[deep_scan]` in the [deep-scan
configuration](https://learn.chatgpt.com/docs/security/cli/reference#configure-deep-scans).

### How do scan cost limits work

Set an estimated cost limit in USD before starting the scan:

```bash
npx @openai/codex-security scan . --max-cost 5
```

The limit is an estimate, not a hard spending cap. Requests already in
progress can finish above it. If a deep scan reaches the limit after Codex
Security aggregates completed worker results, the CLI saves the completed
report with partial coverage and exits with code `2`. Otherwise, it preserves
any available partial output.

### Can scans check commits and pull requests

Install a pre-commit security check for staged and unstaged changes:

```bash
npx @openai/codex-security install-hook
```

For pull-request checks, scan the committed changes and set a severity
threshold:

```bash
npx @openai/codex-security scan . \
  --diff origin/main \
  --fail-on-severity high
```

A complete scan returns exit code `1` when it finds an issue at or above the
selected severity. See [Run scans in CI](https://learn.chatgpt.com/docs/security/cli/ci) for the
complete GitHub Actions workflow, artifact handling, and SARIF export.

### Can another application run scans directly

Yes. Use the [TypeScript SDK](https://learn.chatgpt.com/docs/security/sdk) to start scans, select
targets, inspect findings and coverage, track progress, and apply cost controls
from an application or developer tool.
