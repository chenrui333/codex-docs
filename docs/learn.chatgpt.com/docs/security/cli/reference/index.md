---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/cli/reference'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0", "0.148.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0"]
---

# Codex Security CLI reference

Source: https://learn.chatgpt.com/docs/security/cli/reference

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use this reference to check the supported `codex-security` commands, flags,
output formats, and exit behavior. For a guided first scan, start with the
[CLI quickstart](https://learn.chatgpt.com/docs/security/cli).

The `@openai/codex-security` package is public. Running scans requires Codex
  Security access. Scans use your local permissions and don't pause for
  approval. Before you start, review [Local scan
  permissions](#local-scan-permissions).

Run the CLI with `npx @openai/codex-security`.

## Command overview

```text
usage: codex-security [--version] <command> [options]
```

The CLI provides these commands:

| Command                       | Purpose                                               |
| ----------------------------- | ----------------------------------------------------- |
| `codex-security scan`         | Run a Codex Security scan.                            |
| `codex-security install-hook` | Install a Git pre-commit security scan.               |
| `codex-security bulk-scan`    | Discover repositories and run resumable bulk scans.   |
| `codex-security scans`        | List, inspect, compare, and retrieve saved scan logs. |
| `codex-security findings`     | Review and update saved security findings.            |
| `codex-security export`       | Export completed findings as CSV, JSON, or SARIF.     |
| `codex-security publish`      | Publish completed scan findings to Linear.            |
| `codex-security validate`     | Check one or more candidate security findings.        |
| `codex-security patch`        | Patch one or more security issues.                    |
| `codex-security login`        | Sign in, store credentials, or check sign-in status.  |
| `codex-security logout`       | Remove the stored sign-in.                            |
| `codex-security info`         | Show read-only SDK and bundled-plugin metadata.       |

The CLI also provides these integration commands:

| Command                      | Purpose                               |
| ---------------------------- | ------------------------------------- |
| `codex-security completions` | Generate shell completion scripts.    |
| `codex-security mcp`         | Register the CLI as an MCP server.    |
| `codex-security skills`      | Sync Codex Security skills to agents. |

List all available commands:

```bash
npx @openai/codex-security --help
```

Add `--help` to a command to inspect its arguments and options:

```bash
npx @openai/codex-security scan --help
```

`codex-security --version` prints the installed version and exits.
`codex-security info --json` reports the SDK and bundled-plugin versions.
Neither command requires Python.

### Discover commands and connect agents

Print the agent-readable command manifest:

```bash
npx @openai/codex-security --llms
```

Inspect the scan argument schema as JSON:

```bash
npx @openai/codex-security scan --schema --format json
```

Generate shell completions for Bash:

```bash
npx @openai/codex-security completions bash
```

Replace `bash` with `zsh` or `fish` for those shells.

Scan results support `--format toon|json|yaml|jsonl` and `--full-output`. This
framework-level `--format` is separate from `--export-format`, which selects
the format of an artifact exported from a completed scan. Global command help
also lists `md`, but scan results don't support Markdown output.

Register the CLI as an MCP server:

```bash
npx @openai/codex-security mcp add
```

Sync Codex Security skills to your agents:

```bash
npx @openai/codex-security skills add
```

MCP exposes only the read-only `info` metadata command. Scans, exports,
authentication, validation, and patching remain CLI-only.

## `codex-security scan`

Run a scan against a repository, selected paths, committed changes, or the
working tree.

```text
usage: codex-security scan [-h] [--auth {auto,chatgpt,api-key}]
                           [--provider {openai,openrouter,fireworks,amazon-bedrock}]
                           [--path PATH | --diff BASE | --working-tree]
                           [--head HEAD] [--base BASE]
                           [--knowledge-base PATH] [--scan-prompt-file FILE]
                           [--post-scan-prompt-file FILE]
                           [--mode {standard,deep}] [--workers N]
                           [--subagents N] [--stop-after-no-new N]
                           [--max-discovery-runs N] [--max-time-hours HOURS]
                           [--model MODEL]
                           [--effort {minimal,low,medium,high,xhigh,max}]
                           [--output-dir DIR]
                           [--archive-existing]
                           [--plugin-path PATH] [--python PATH]
                           [--codex KEY=VALUE] [--fail-on-severity LEVEL]
                           [--patch] [--patch-severity {critical,high,medium,low}]
                           [--create-pr]
                           [--max-cost USD] [--dry-run] [--headless] [--verbose]
                           [--json] [--format {toon,json,yaml,jsonl}]
                           [--full-output] [repository]
```

`repository` defaults to the current directory.

### Select scan authentication

Use `--auth auto`, the default, to select credentials automatically. When both
a ChatGPT sign-in and `OPENAI_API_KEY` or `CODEX_API_KEY` are available,
interactive scans with text output ask which credential to use. CI, JSON and
JSONL scans, and other scans without an interactive terminal use the
environment API key. Dry runs don't prompt or load credentials.

To use your stored credentials, pass `--auth chatgpt`:

```bash
npx @openai/codex-security scan . --auth chatgpt
```

To use an environment API key, pass `--auth api-key`:

```bash
npx @openai/codex-security scan . --auth api-key
```

To make stored credentials the automatic default, run
`unset OPENAI_API_KEY CODEX_API_KEY`.

### Use OpenRouter or Fireworks

Select OpenRouter with its API key and an explicit model:

```bash
export OPENROUTER_API_KEY="your-openrouter-api-key"
npx @openai/codex-security scan . \
  --provider openrouter \
  --model anthropic/claude-sonnet-4.5
```

Select Fireworks with its API key and an explicit model:

```bash
export FIREWORKS_API_KEY="your-fireworks-api-key"
npx @openai/codex-security scan . \
  --provider fireworks \
  --model accounts/fireworks/models/qwen3-235b-a22b
```

Both providers also support `bulk-scan`.

### Use Amazon Bedrock

Select Amazon Bedrock with `--provider amazon-bedrock` and specify an explicit
Bedrock model with `--model`:

```bash
npx @openai/codex-security scan . \
  --provider amazon-bedrock \
  --model openai.gpt-5.6-sol
```

Set `AWS_REGION` and authenticate with `AWS_BEARER_TOKEN_BEDROCK`, standard AWS
access keys, an AWS profile, web identity, container credentials, or the
default AWS credential chain. Bedrock scans use AWS credentials instead of
`--auth`, ChatGPT sign-in, or an OpenAI API key. Both `scan` and `bulk-scan`
support `--provider`.

### Select the scan target

Choose one target type for each scan.

| Argument                 | Description                                                                     |
| ------------------------ | ------------------------------------------------------------------------------- |
| `--path PATH`            | Scan a path relative to the repository. Repeat the flag for more paths.         |
| `--diff BASE`            | Scan committed changes from `BASE` to `--head`. The head defaults to `HEAD`.    |
| `--head HEAD`            | Set the head revision for `--diff`.                                             |
| `--working-tree`         | Scan staged and unstaged changes against `--base`. The base defaults to `HEAD`. |
| `--base BASE`            | Set the base revision for `--working-tree`.                                     |
| `--mode {standard,deep}` | Select the scan mode. The default is `standard`.                                |

`--path`, `--diff`, and `--working-tree` are mutually exclusive. `--head`
requires `--diff`, and `--base` requires `--working-tree`. Deep mode supports
repository and path targets.

Diff and working-tree scans require the repository argument to be the Git
worktree root. The selected refs must exist in that checkout.

Scan the entire repository:

```bash
npx @openai/codex-security scan .
```

Scan selected paths:

```bash
npx @openai/codex-security scan . --path src --path tests
```

Scan committed changes:

```bash
npx @openai/codex-security scan . --diff origin/main --head HEAD
```

Scan staged and unstaged changes:

```bash
npx @openai/codex-security scan . --working-tree --base HEAD
```

Run a deeper review of the repository:

```bash
npx @openai/codex-security scan . --mode deep
```

### Configure deep scans

Use these options with `--mode deep` to control worker concurrency and runtime:

| Argument                 | Description                                                                            |
| ------------------------ | -------------------------------------------------------------------------------------- |
| `--workers N`            | Limit on concurrent independent standard-scan workers. Defaults to `4`.                |
| `--subagents N`          | Subagents available to each worker. Defaults to `3`.                                   |
| `--stop-after-no-new N`  | Stop after `N` consecutive completed worker scans find no new issues. Defaults to `4`. |
| `--max-discovery-runs N` | Limit on total independent standard-scan runs. Defaults to `40`.                       |
| `--max-time-hours HOURS` | Worker execution time limit in hours. Defaults to `96`; accepts fractions.             |

`--subagents` accepts zero or a positive integer. `--max-time-hours` accepts a
positive number no greater than `96`. The remaining options require a positive
integer. These options aren't available for standard scans.

For example, use two workers, allow up to ten runs, and stop worker execution
after 1.5 hours:

```bash
npx @openai/codex-security scan . \
  --mode deep \
  --workers 2 \
  --subagents 0 \
  --stop-after-no-new 3 \
  --max-discovery-runs 10 \
  --max-time-hours 1.5
```

When the time limit expires, the scan stops unfinished workers, keeps completed
scan results, and aggregates them into the final report. If no worker finishes
source review, the scan records partial coverage and returns exit code `2`.

Set persistent defaults in `~/.codex/codex-security/config.toml`, or in
`$CODEX_HOME/codex-security/config.toml` when you set `CODEX_HOME`:

```toml
[deep_scan]
workers = 2
subagents = 0
stop_after_no_new = 3
max_discovery_runs = 10
max_time_hours = 1.5
```

Command-line options override these defaults. `scan --workers` controls
independent standard-scan workers within one deep scan; `bulk-scan --workers`
controls concurrent repository scans. Set `stop_after_consecutive_errors` only
in the TOML file; its default is `3`.

### Add security context

Use `--knowledge-base PATH` to provide architecture documents, threat models,
or security policies. Repeat the option for more files or directories:

```bash
npx @openai/codex-security scan . \
  --knowledge-base /path/to/architecture.md \
  --knowledge-base /path/to/security-policies
```

Supported documents include `.md`, `.markdown`, `.txt`, `.pdf`, and `.docx`
files. The CLI searches directories recursively, rejects linked input paths,
skips linked directory entries, and keeps extracted document content
outside the saved scan results.

### Add scan instructions

To add scan instructions, provide a text or Markdown file with
`--scan-prompt-file`. Use `--post-scan-prompt-file` to run follow-up
instructions in the same authenticated session after successful scans and
scans with incomplete coverage or errors:

```bash
npx @openai/codex-security scan . \
  --scan-prompt-file security-focus.md \
  --post-scan-prompt-file follow-up.md
```

For example, use the scan prompt to focus on authorization boundaries and ask
the follow-up to write a new `post-scan-summary.md` in the scan directory.
If the follow-up fails, the CLI reports a warning and keeps the completed scan.
The follow-up doesn't run after cancellation or when the scan reaches its cost
limit.

### Set output and policy options

Use these options to keep artifacts, preserve earlier results, or create a
machine-readable result.

| Argument                   | Description                                                                                                                  |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `--output-dir DIR`         | Write scan artifacts to a private directory outside the enclosing Git worktree. Defaults to persistent Codex Security state. |
| `--archive-existing`       | Move existing results to `DIR.previous-<timestamp>-<id>` and start with an empty output directory. Requires `--output-dir`.  |
| `--fail-on-severity LEVEL` | Return exit `1` when a completed scan reports a finding at or above `critical`, `high`, `medium`, or `low`.                  |
| `--patch`                  | Fix and verify selected findings after a complete scan.                                                                      |
| `--patch-severity LEVEL`   | Patch findings at or above `critical`, `high`, `medium`, or `low`. Defaults to `low`.                                        |
| `--create-pr`              | Commit verified patch files and open a GitHub pull request. Requires `--patch`.                                              |
| `--max-cost USD`           | Stop a scan when its estimated model cost exceeds the specified USD amount.                                                  |
| `--dry-run`                | Check the repository, target, knowledge base, output directory, and Codex configuration without starting a scan.             |
| `--headless`               | Show plain-text progress instead of the interactive scan dashboard.                                                          |
| `--verbose`                | Print redacted lifecycle, authentication, progress, and cost diagnostics to stderr.                                          |
| `--json`                   | Print manifest, findings, coverage, paths, and turn metadata as one JSON document.                                           |
| `--format FORMAT`          | Print the complete scan result as `toon`, `json`, `yaml`, or `jsonl`.                                                        |
| `--full-output`            | Print the complete result using the default structured output format.                                                        |

The cost limit is an estimate, not a hard spending cap. Requests already in
progress can finish slightly above the limit. If a deep scan reaches the limit
after Codex Security aggregates completed worker results, the CLI seals the
available results, marks coverage as `partial`, and returns exit code `2`.
Otherwise, it returns `2` and leaves any available partial output on disk.

When you omit `--output-dir`, results persist under
`$CODEX_HOME/state/plugins/codex-security/scans/<repository>`. `CODEX_HOME`
defaults to `~/.codex`. Set `CODEX_SECURITY_STATE_DIR` to keep results under
`$CODEX_SECURITY_STATE_DIR/scans/<repository>` instead. These directories can
contain source excerpts and vulnerability details, so manage their permissions
and retention accordingly.

The workbench keeps scan history in
`$CODEX_HOME/state/plugins/codex-security/workbench.sqlite3`. Setting
`CODEX_SECURITY_STATE_DIR` also moves the workbench database.

The output directory must be outside the scanned directory and any enclosing
Git worktree. A scan can replace an existing result directory with
`--archive-existing`.

To preserve earlier results before reusing an output directory:

```bash
npx @openai/codex-security scan . \
  --output-dir /path/outside/repository/results \
  --archive-existing
```

Scans are report-only by default. Add `--fail-on-severity` to evaluate a
severity policy in CI:

```bash
npx @openai/codex-security scan . \
  --diff origin/main \
  --output-dir /path/outside/repository/results \
  --json \
  --fail-on-severity high \
  > /path/outside/repository/codex-security.json
```

A dry run checks local inputs, including knowledge-base documents, without
loading credentials, starting Codex, or probing the plugin's Python
interpreter:

```bash
npx @openai/codex-security scan . \
  --output-dir /path/outside/repository/results \
  --dry-run
```

### Configure the runtime

Use runtime options when you need an explicit model, interpreter, plugin, or
Codex configuration value.

| Argument                                                  | Description                                                                                              |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `--auth {auto,chatgpt,api-key}`                           | Select the scan credentials. The default is `auto`.                                                      |
| `--provider {openai,openrouter,fireworks,amazon-bedrock}` | Select the inference provider. The default is `openai`.                                                  |
| `--model MODEL`                                           | Select the model. The default is `gpt-5.6-sol`. Required for OpenRouter, Fireworks, and Amazon Bedrock.  |
| `--effort {minimal,low,medium,high,xhigh,max}`            | Select the model's reasoning effort. The default is `xhigh`.                                             |
| `--plugin-path PATH`                                      | Use a Codex Security plugin directory or ZIP to override the bundled plugin.                             |
| `--python PATH`                                           | Select the Python interpreter for the plugin runtime.                                                    |
| `--codex KEY=VALUE`                                       | Override an isolated Codex configuration value. Values use TOML syntax. Repeat the flag for more values. |

To select a different model and reasoning effort without writing TOML:

```bash
npx @openai/codex-security scan . --model gpt-5.6-terra --effort high
```

Quote string values passed through `--codex` so the TOML parser receives a
string:

```bash
npx @openai/codex-security scan . --codex 'model="gpt-5.6-terra"'
```

## `codex-security install-hook`

Install a Git pre-commit security check for the current repository:

```bash
npx @openai/codex-security install-hook
```

The check scans staged and unstaged changes before each commit and blocks
high-severity findings or scan errors. It respects `core.hooksPath` and does
not replace an existing pre-commit script. Set a different severity threshold
when needed:

```bash
npx @openai/codex-security install-hook . --fail-on-severity medium
```

## `codex-security bulk-scan`

Discover and scan GitHub repositories, or run a resumable scan from a
repository CSV:

For a complete guide to GitHub discovery, CSV inventories, campaign results,
and containerized scans, see [Run bulk security
scans](https://learn.chatgpt.com/docs/security/cli/bulk-scans).

```text
usage: codex-security bulk-scan [input] [--output-dir DIR]
                                [--workers N] [--mode {standard,deep}]
                                [--provider {openai,openrouter,fireworks,amazon-bedrock}]
                                [--model MODEL]
                                [--effort {minimal,low,medium,high,xhigh,max}]
                                [--knowledge-base PATH]
                                [--scan-prompt-file FILE]
                                [--post-scan-prompt-file FILE]
                                [--max-attempts N] [--plugin-path PATH]
                                [--python PATH] [--codex KEY=VALUE]
```

Run `npx @openai/codex-security bulk-scan` without arguments to select
repositories interactively. This flow requires a GitHub CLI sign-in.

To choose a model and reasoning effort during interactive discovery:

```bash
npx @openai/codex-security bulk-scan --model gpt-5.6-terra --effort high
```

For a prepared repository list, provide a CSV and `--output-dir`:

```bash
npx @openai/codex-security bulk-scan repositories.csv \
  --output-dir /path/outside/repositories/security-scans \
  --workers 4
```

The CSV requires `id`, `repository`, and `revision` columns. Revisions must be
full commit hashes. Optional `scope`, `mode`, and `prompt` columns configure
individual repositories:

```csv
id,repository,revision,scope,mode,prompt
service,https://github.com/example/service.git,0123456789abcdef0123456789abcdef01234567,src,standard,Review authorization boundaries.
```

Use `--knowledge-base PATH` to share security documents across every
repository. Use `--scan-prompt-file FILE` to add shared scan instructions; the
CSV `prompt` column adds repository-specific instructions after that shared
prompt. `--post-scan-prompt-file FILE` runs follow-up instructions after each
scan, including scans with incomplete coverage or errors. It doesn't run after
cancellation or when a scan reaches its cost limit.

`--workers` limits simultaneous repository scans and defaults to `4`. `--mode`
defaults to `standard`, and `--max-attempts` defaults to `1`. Set
`--max-attempts` to retry repository or scan errors. Completed scans with
incomplete coverage aren't retried. Their results remain available, and the
command returns exit code `2`.

Run the same command again to resume from an existing output directory. The CLI
skips completed scans, including scans with incomplete coverage.

For containerized campaigns, see [Run bulk scans in
Docker](https://learn.chatgpt.com/docs/security/cli/bulk-scans#run-bulk-scans-in-docker).

## `codex-security scans`

### Find saved scans

List saved scans for the current directory:

```bash
npx @openai/codex-security scans
```

List scans for a different repository:

```bash
npx @openai/codex-security scans list /path/to/repository
```

Find scans stored under a specific output directory:

```bash
npx @openai/codex-security scans list --scan-root /path/outside/repository/results
```

### Inspect or repeat a scan

Show a saved scan's results and configuration:

```bash
npx @openai/codex-security scans show SCAN_ID
```

Add `--show-linked-findings` to include finding links from earlier scans.

Rerun the scan against the current checkout using its original configuration:

```bash
npx @openai/codex-security scans rerun SCAN_ID
```

The rerun requires the plugin version recorded by the original scan. If the
installed version differs, the command stops instead of running with a
different plugin.

### Inspect saved scan logs

Read the complete saved session events for a scan and its workers. These logs
aren't redacted and can contain source code or credentials, so review them
before sharing:

```bash
npx @openai/codex-security scans logs SCAN_ID
```

Add `--json` for a machine-formatted result containing full information.

### Match and compare findings

Compare two scans to find new, persisting, reopened, resolved, and unknown
findings:

```bash
npx @openai/codex-security scans compare PREVIOUS_SCAN_ID CURRENT_SCAN_ID
```

The comparison automatically matches findings that share the same root cause
and reuses saved matches. To save matches explicitly, use `scans match`:

```bash
npx @openai/codex-security scans match PREVIOUS_SCAN_ID CURRENT_SCAN_ID
```

A finding is unknown when the later scan has incomplete coverage or doesn't
cover the finding's original location. Add `--force` to `match` when you need to
recompute an existing match.

To match all completed scans for the current repository, including scans from
other checkouts:

```bash
npx @openai/codex-security scans match --all
```

Scan results can vary even when you rerun the same configuration. Matching and
comparison track changes; they don't make results deterministic or prove that a
vulnerability no longer exists. Use `validate` to recheck a security-critical
finding against the current code.

## `codex-security findings`

List open findings across the current repository's scans:

```bash
npx @openai/codex-security findings list
```

Pass a repository path to inspect another checkout:

```bash
npx @openai/codex-security findings list /path/to/repository
```

Add `--json` for structured output. The list identifies findings seen in the
latest scan and earlier findings that weren't confirmed in that scan.

Note that earlier findings remain open until resolved or dismissed (absence
from the latest scan is not interpreted as proof that it's fixed).

To record a reviewed finding as a false positive:

```text
usage: codex-security findings false-positive OCCURRENCE_ID
                       --reason REASON
```

Inspect the saved scan to identify the finding occurrence:

```bash
npx @openai/codex-security scans show SCAN_ID
```

Record a specific explanation for the false positive:

```bash
npx @openai/codex-security findings false-positive FINDING_OCCURRENCE_ID \
  --reason "The framework escapes this input before it reaches the query"
```

The reason must not be empty. Codex Security saves the decision for the
repository and provides it as context to future scans. Each scan independently
rechecks the current source, controls, and reachability. A previous decision
doesn't suppress a rule, path, or vulnerability class.

## `codex-security export`

Export CSV, JSON, or SARIF from a completed, sealed scan. Export validates the
scan artifacts before writing output and leaves the Codex runtime and
credentials untouched.

```text
usage: codex-security export [--export-format {csv,json,sarif}]
                             [--output FILE|-] [--source-root PATH]
                             [--python PATH] scan_dir
```

`scan_dir` is the completed scan directory.

| Argument                           | Description                                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------------------------- |
| `--export-format {csv,json,sarif}` | Select the export format. The default is `sarif`.                                           |
| `--output FILE\|-`                 | Write the selected format to a file or stdout. Defaults to a file in the current directory. |
| `--source-root PATH`               | Add source-line fingerprints to SARIF using a repository checkout.                          |
| `--python PATH`                    | Select the Python interpreter for the bundled exporter.                                     |

`--source-root` works only with `--export-format sarif`. JSON preserves
the sealed findings document. CSV contains portable finding columns and does
not include local workbench triage state.

Without `--output`, the CLI writes SARIF to `results.sarif`, JSON to
`findings.json`, and CSV to `findings.csv` in the current working directory.
Exports can contain source excerpts and vulnerability details. Run the command
outside the repository or pass `--output` with a private path outside the
scanned checkout.

Write SARIF to a file:

```bash
npx @openai/codex-security export /path/to/scan \
  --export-format sarif \
  --source-root /path/to/repository \
  --output /path/outside/repository/exports/results.sarif
```

Write SARIF to stdout:

```bash
npx @openai/codex-security export /path/to/scan \
  --export-format sarif \
  --source-root . \
  --output -
```

Export findings as JSON:

```bash
npx @openai/codex-security export /path/to/scan \
  --export-format json \
  --output /path/outside/repository/exports/findings.json
```

Export findings as CSV:

```bash
npx @openai/codex-security export /path/to/scan \
  --export-format csv \
  --output /path/outside/repository/exports/findings.csv
```

## `codex-security publish scan`

Publish every finding from a completed scan to Linear:

```text
usage: codex-security publish scan [SCAN_DIR] --to linear
                                   [--linear-team TEAM_ID]
                                   [--project PROJECT_ID]
                                   [--linear-api-key KEY]
                                   [--linear-assignee EMAIL_OR_USER_ID]
                                   [--dry-run] [--json]
```

`SCAN_DIR` must contain a completed, sealed scan. Omit it in an interactive
terminal to select a completed scan from local scan history. Creating issues
also requires the scan and its findings to exist in local scan history. A dry
run validates the sealed artifacts without this persistence check.

| Argument                             | Description                                                                                                                                                      |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--to linear`                        | Publish to Linear. This argument is required.                                                                                                                    |
| `--linear-team TEAM_ID`              | Select the Linear team. Uses `CODEX_SECURITY_LINEAR_TEAM` when omitted; one of them is required.                                                                 |
| `--project PROJECT_ID`               | Select a Linear project. Uses `CODEX_SECURITY_LINEAR_PROJECT` when omitted. If neither is set, issues are created directly in the team.                          |
| `--linear-api-key KEY`               | Use a Linear personal API key for direct publication. Uses `CODEX_SECURITY_LINEAR_API_KEY` when omitted.                                                         |
| `--linear-assignee EMAIL_OR_USER_ID` | Assign created issues by email address or Linear user ID. Requires `--linear-api-key` or `CODEX_SECURITY_LINEAR_API_KEY`. Issues remain unassigned when omitted. |
| `--dry-run`                          | Prepare issue payloads without starting Codex, contacting Linear, creating issues, or writing publication state.                                                 |
| `--json`                             | Write structured publication results to stdout. Progress remains on stderr.                                                                                      |

Linear issue descriptions and dry-run output can include source code snippets
  and vulnerability details. Publish only to an authorized Linear team or
  project, and treat saved output as sensitive.

Each non-dry-run invocation attempts to create a new issue for every finding.
Publishing the same scan again doesn't match, update, or reuse existing issues.
If some findings fail, the command preserves successfully created issues and
returns exit code `2`.
With `--json`, review the `created` and `failed` results before retrying to
avoid duplicates.

Preview the issue payloads before publishing:

```bash
npx @openai/codex-security publish scan /path/to/completed-scan \
  --to linear \
  --linear-team TEAM_ID \
  --dry-run \
  --json
```

### Publish with the connected Linear app

Without a Linear API key, the command starts Codex using your existing
configuration and connected Linear app. Sign in and connect Linear to your
Codex account before publishing:

```bash
npx @openai/codex-security login
npx @openai/codex-security publish scan /path/to/completed-scan \
  --to linear \
  --linear-team TEAM_ID \
  --project PROJECT_ID
```

### Publish with a Linear API key

Supplying `--linear-api-key` or `CODEX_SECURITY_LINEAR_API_KEY` publishes
directly through the Linear API and doesn't start Codex. Direct publication
leaves issues unassigned unless you select an assignee:

```bash
export CODEX_SECURITY_LINEAR_API_KEY=YOUR_LINEAR_PERSONAL_API_KEY
npx @openai/codex-security publish scan /path/to/completed-scan \
  --to linear \
  --linear-team TEAM_ID \
  --linear-assignee teammate@example.com
```

Command-line values override their matching environment variables. For API
keys, prefer `CODEX_SECURITY_LINEAR_API_KEY` over `--linear-api-key` because
command-line arguments can appear in shell history and process listings.

## `codex-security validate` and `codex-security patch`

Check whether a candidate finding is valid:

```bash
npx @openai/codex-security validate findings.json \
  "Possible SQL injection in src/query.ts:42"
```

Generate a fix with the bundled remediation skill:

```bash
npx @openai/codex-security patch findings.json \
  "Missing authorization check in src/routes.ts:18"
```

Each positional argument accepts literal text or a file path. These inputs use
the current directory. Use `validate` to recheck a finding after a fix or when a
later scan no longer reports it. Comparing scans alone doesn't prove that a fix
worked.

Use `--effort` to select reasoning effort for either command:

```bash
npx @openai/codex-security validate "Possible SQL injection" --effort high
```

### Patch findings after a scan

Use `scan --patch` to fix findings after a complete scan. This requires
`@openai/codex-security` 0.1.15 or later. The default severity threshold is
`low`. This command selects high and critical findings:

```bash
npx @openai/codex-security scan . --patch --patch-severity high --json
```

Verified and already-fixed findings don't trigger `--fail-on-severity`.

### Patch saved findings

Pass a finding or occurrence ID to patch its original repository, or select
findings from a saved scan:

```bash
npx @openai/codex-security patch OCCURRENCE_ID
npx @openai/codex-security patch --scan SCAN_ID --severity high --json
npx @openai/codex-security patch --scan latest --severity medium
```

`--scan latest` selects the latest completed scan for the current repository.
Saved-finding commands support `--json`; literal-text and file inputs don't.

Add `--create-pr` to commit only verified patch files and open a pull request
with the GitHub CLI:

```bash
npx @openai/codex-security patch --scan SCAN_ID --severity high --create-pr
```

If the push or pull request fails, run the printed `patch --resume-pr BRANCH`
command from the same repository to retry.

### Patch Linear issues

Set `CODEX_SECURITY_LINEAR_API_KEY` or `LINEAR_API_KEY` for a personal API key,
or `LINEAR_ACCESS_TOKEN` for an OAuth token. Prefer an environment variable to
`--linear-api-key KEY` to keep the key out of shell history.

Import an issue by ID or URL. Repeat `--linear-issue` to select more than one
issue:

```bash
npx @openai/codex-security patch --linear-issue SEC-123 --linear-issue SEC-124
```

Use `--linear-project` to select a project's open issues. Add `--linear-filter`
to narrow the selection:

```bash
npx @openai/codex-security patch --linear-project "Security backlog" \
  --linear-filter '{"labels":{"name":{"eq":"security"}}}'
```

The CLI excludes completed and canceled issues unless the filter sets `state`.
It doesn't change the Linear issues.

## `codex-security login`, `logout`, and `info`

Sign in interactively:

```bash
npx @openai/codex-security login
```

Use device authentication on a remote or headless machine:

```bash
npx @openai/codex-security login --device-auth
```

Check the current sign-in:

```bash
npx @openai/codex-security login status
```

Remove the stored sign-in:

```bash
npx @openai/codex-security logout
```

Store an API key by passing it on stdin:

```bash
printenv OPENAI_API_KEY | npx @openai/codex-security login --with-api-key
```

Store an enterprise access token:

```bash
printenv CODEX_ACCESS_TOKEN | npx @openai/codex-security login --with-access-token
```

Inspect read-only SDK and bundled-plugin metadata:

```bash
npx @openai/codex-security info --json
```

When you expose the CLI as an MCP server, `info` is the only available command.
Scans, exports, publication, sign-in, validation, and patching remain CLI-only.

## Read scan output

By default, scans send progress, completion summaries, and errors to stderr
without writing the complete scan result to stdout. Request `--json`,
`--format`, or `--full-output` to send structured scan results to stdout.

Interactive terminals show a live dashboard with the current scan phase,
reviewed files, activity, token usage, and estimated cost. CI and redirected
output use plain-text progress. Add `--headless` to use plain-text progress in
an interactive terminal:

```bash
npx @openai/codex-security scan . --headless
```

The dashboard also shows live session details. They aren't redacted and can
contain source code or credentials. Review them before sharing.

### Verbose diagnostics

Add `--verbose` to print redacted lifecycle, authentication, progress, and cost
diagnostics to stderr:

```bash
npx @openai/codex-security scan . --verbose
```

Set `CODEX_SECURITY_LOG_LEVEL=debug` to enable the same diagnostics without the
flag. `LOG_LEVEL=debug` also enables diagnostics when
`CODEX_SECURITY_LOG_LEVEL` is unset.

### Completion summary

A completed scan writes its open repository finding count, severity breakdown,
coverage, elapsed time, report path, and result directory to stderr. It
includes token usage and estimated cost when available:

```text
  REPORT    /path/to/scan/report.md

  FINDINGS  4 (3 confirmed this scan; 1 previously found; 1 critical, 2 high, 1 informational)
  COVERAGE  complete
  ELAPSED   1s
  TOKENS    1,250 input, 200 cached, 30 output
  RESULTS   /path/to/scan
```

Informational findings count toward the summary total. Severity policies
evaluate only `critical`, `high`, `medium`, and `low` findings from the current
scan, not earlier findings shown in the repository total.

### JSON output

`scan --json` writes one complete JSON document to stdout. Its top-level shape
is:

```text
manifest
repositoryFindings
findings
coverage
scanDir
threadId
reportPath
artifactsDir
sarifPath
cost
turn
  id
  status
  durationMs
  finalResponse
  usage
```

When [patching](#patch-findings-after-a-scan), JSON output also includes patch
results and any created pull request.

Progress, completion summaries, archive notices, and errors remain on stderr.
A completed scan still prints the full JSON result when a severity policy
returns exit `1` or incomplete coverage returns exit `2`.

`codex-security scan --json` emits one JSON document. `codex exec --json`
  emits a JSON Lines event stream. Use the output format that matches the
  command you run.

## Scan artifacts

A completed scan keeps the readable report and structured artifacts together:

```text
<scan-directory>/
├── scan-manifest.json
├── findings.json
├── coverage.json
├── report.md
├── artifacts/
└── exports/
    └── results.sarif       # when produced
```

The structured files serve different jobs:

| File                    | Contents                                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `scan-manifest.json`    | Scan identity, status, target, scope, producer, and sealed artifact records.                                                    |
| `findings.json`         | Finding identifiers, severity, confidence, taxonomy, locations, evidence, validation, data flow, reachability, and remediation. |
| `coverage.json`         | Reviewed surfaces, exclusions, deferred work, open questions, and coverage completeness.                                        |
| `report.md`             | Readable scan report.                                                                                                           |
| `artifacts/`            | Supporting scan artifacts.                                                                                                      |
| `exports/results.sarif` | SARIF generated during the scan, when present.                                                                                  |

Coverage completeness has three values:

- `complete`: The scan records complete coverage for its selected scope.
- `partial`: The scan records deferred work or other coverage limits.
- `unknown`: The scan reports coverage completeness as unknown.

Review deferred surfaces, explicit exclusions, and open questions before using
coverage as evidence for a security decision.

## Exit codes and signals

The CLI uses these exit codes:

| Exit  | Condition                                                                                                                                                                     |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`   | A scan completed with complete coverage and passed its severity policy, a bulk scan or publication completed without failures, or another command succeeded.                  |
| `1`   | A completed scan reports a finding at or above the configured severity.                                                                                                       |
| `2`   | The CLI found an input, runtime, or export error, a scan has incomplete coverage, a bulk scan has repositories with errors, or a publication has one or more failed findings. |
| `130` | Ctrl-C interrupted a scan or publication.                                                                                                                                     |
| `143` | SIGTERM terminated a scan or publication.                                                                                                                                     |

Any scan with `partial` or `unknown` coverage returns `2`, even without a
severity policy. When you request structured output, completed scans and
partial publications still write the available results to stdout. The CLI
prints the location of any partial output after an interruption or runtime
error.

## Local scan permissions

CLI and SDK scans run with your local operating-system permissions. Every scan
uses the `codex_security_scan` filesystem profile and sets `approvalPolicy` to
`"never"`. The profile permits reading the local filesystem and writing to
workspace roots and the selected scan state directory. Scans don't stop to
request interactive approval.

Settings supplied through CLI `--codex` or SDK `codexOverrides`, including
`approval_policy`, `sandbox_mode`, and filesystem permissions, can't replace
or restrict these scan controls. Host and network restrictions still apply.

Scan and workbench processes can inherit your environment, including unrelated
API tokens and cloud credentials. Scan only repositories you trust and have
permission to assess, and provide only the credentials the scan requires.

## Authentication and prerequisites

Set `OPENAI_API_KEY` or `CODEX_API_KEY`, sign in with
`npx @openai/codex-security login`, or use an existing file-backed Codex
sign-in. For OpenRouter or Fireworks, set the provider's API key and select a
model. For Amazon Bedrock, use a Bedrock API key or the standard AWS
credential chain instead.

For credential selection, see [Select scan
authentication](#select-scan-authentication).

For CI, keep the API key scoped to the scan step and use a trusted workflow.

The CLI requires Node.js 22 (22.13.0 or later), 24, or 26. Scans, bulk scans,
exports, scan history, and saved findings also require Python 3.10 or later.
Python 3.10 also requires `tomli`. Use `--python` with `scan`, `bulk-scan`, or
`export`, or set `PYTHON` for any Python-backed command.

Continue with the [CLI quickstart](https://learn.chatgpt.com/docs/security/cli), [bulk-scan
guide](https://learn.chatgpt.com/docs/security/cli/bulk-scans), [CLI FAQ](https://learn.chatgpt.com/docs/security/cli/faq), [CI
guide](https://learn.chatgpt.com/docs/security/cli/ci), or [TypeScript SDK guide](https://learn.chatgpt.com/docs/security/sdk).

### Plain-text aliases

- --output FILE|-
