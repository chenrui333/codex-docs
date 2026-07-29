---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/cli/ci'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0"]
---

# Run Codex Security in CI

Source: https://learn.chatgpt.com/docs/security/cli/ci

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Run the Codex Security CLI in CI to review the exact changes in a pull request,
keep findings and coverage, and optionally fail the check at a chosen
severity. Start with advisory results, review scan quality and runtime, then
add a severity policy that fits your repository.

The Codex Security CLI is in beta and requires access. Follow the installation
  instructions provided with your access.

This guide uses GitHub Actions. The same scan and export commands work in other
CI systems.

## Prepare the workflow

Store an OpenAI API key as a repository or organization secret named
`CODEX_SECURITY_API_KEY`.

Map this secret directly to the scan step's `CODEX_API_KEY` environment
variable. Keep the credential scoped to that variable within the scan process.

Set the `CODEX_SECURITY_PACKAGE` repository or organization variable to an
approved package source provided with your access, such as a trusted archive
location or registry package specification. The source must be available to
the runner before it checks out the repository.

The runner needs:

- Node.js 22 or later.
- Python 3.10 or later.
- The Codex Security CLI, installed outside the repository checkout using the
  instructions provided with your access.
- The pull-request head and base history so Git can calculate the merge base.
- [GitHub Code Security](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/uploading-a-sarif-file-to-github)
  enabled for private or internal repositories when you upload SARIF.

The example skips pull requests from forks and Dependabot. These workflows
  don't receive normal Actions secrets, and Dependabot receives a read-only
  `GITHUB_TOKEN` by default. Keep scan credentials available only to trusted
  workflows.

## Add the GitHub Actions workflow

Create `.github/workflows/codex-security.yml`. Before checking out the pull
request, install the approved package under `$RUNNER_TEMP/codex-security` so
the trusted executable is available at
`$RUNNER_TEMP/codex-security/node_modules/.bin/codex-security`:

```yaml
name: Codex Security scan

on:
  pull_request:

jobs:
  codex-security:
    if: github.event.pull_request.head.repo.full_name == github.repository && github.actor != 'dependabot[bot]'
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write
    steps:
      - name: Set up Node.js
        uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020 # v7
        with:
          node-version: "26"

      - name: Set up Python
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7
        with:
          python-version: "3.14"

      - name: Install Codex Security
        env:
          CODEX_SECURITY_PACKAGE: ${{ vars.CODEX_SECURITY_PACKAGE }}
        run: |
          set -euo pipefail
          if test -z "$CODEX_SECURITY_PACKAGE"; then
            echo "Set the CODEX_SECURITY_PACKAGE repository or organization variable." >&2
            exit 1
          fi
          npm install \
            --prefix "$RUNNER_TEMP/codex-security" \
            --ignore-scripts \
            --no-audit \
            --no-fund \
            "$CODEX_SECURITY_PACKAGE"

      - name: Verify Codex Security
        env:
          CODEX_SECURITY_BIN: ${{ runner.temp }}/codex-security/node_modules/.bin/codex-security
        run: |
          set -euo pipefail
          test -x "$CODEX_SECURITY_BIN"
          "$CODEX_SECURITY_BIN" --version

      - name: Check out the pull request
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 0
          persist-credentials: false

      - name: Scan the pull request
        env:
          CODEX_API_KEY: ${{ secrets.CODEX_SECURITY_API_KEY }}
          CODEX_SECURITY_BIN: ${{ runner.temp }}/codex-security/node_modules/.bin/codex-security
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
          SCAN_DIR: ${{ runner.temp }}/codex-security-results
        run: |
          set -euo pipefail
          BASE_REVISION="$(git merge-base "$BASE_SHA" "$HEAD_SHA")"
          "$CODEX_SECURITY_BIN" scan . \
            --diff "$BASE_REVISION" \
            --head "$HEAD_SHA" \
            --output-dir "$SCAN_DIR" \
            --json > "$RUNNER_TEMP/codex-security.json"

      - name: Export SARIF
        id: export-sarif
        if: always()
        env:
          CODEX_SECURITY_BIN: ${{ runner.temp }}/codex-security/node_modules/.bin/codex-security
          SCAN_DIR: ${{ runner.temp }}/codex-security-results
          SARIF_FILE: ${{ runner.temp }}/codex-security.sarif
        run: |
          set -euo pipefail
          if test -f "$SCAN_DIR/scan-manifest.json"; then
            "$CODEX_SECURITY_BIN" export "$SCAN_DIR" \
              --export-format sarif \
              --source-root "$GITHUB_WORKSPACE" \
              --output "$SARIF_FILE"
            echo "available=true" >> "$GITHUB_OUTPUT"
          fi

      - name: Upload SARIF
        if: always() && steps.export-sarif.outputs.available == 'true'
        uses: github/codeql-action/upload-sarif@e4fba868fa4b1b91e1fdab776edc8cfbe6e9fb81 # v4
        with:
          sarif_file: ${{ runner.temp }}/codex-security.sarif
          ref: refs/pull/${{ github.event.pull_request.number }}/head
          sha: ${{ github.event.pull_request.head.sha }}
          category: codex-security

      - name: Preserve scan results
        if: always()
        uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7
        with:
          name: codex-security-results
          path: |
            ${{ runner.temp }}/codex-security-results
            ${{ runner.temp }}/codex-security.json
          if-no-files-found: warn
          retention-days: 7
```

The workflow checks out the pull-request head, calculates its merge base, and
scans the committed changes between those revisions. Full history keeps the
target exact. `persist-credentials: false` keeps the repository token out of
the checked-out Git configuration. Installing the CLI before checkout and
running its absolute path keeps repository-controlled executables away from
the scan credential. Pinning each action to a verified commit prevents an
upstream tag change from changing the workflow.

`--json` writes one complete JSON document to stdout, so the workflow can save
it directly. Progress, completion summaries, and errors remain on stderr. This
differs from `codex exec --json`, which emits a JSON Lines event stream.

The export step reads a completed, sealed scan and writes SARIF. It leaves the
Codex runtime and credentials untouched. Scan artifacts can contain vulnerable
source snippets, evidence, and remediation details. Choose access controls and a
short retention window appropriate for your repository.

## Choose a severity policy

The above workflow is report-only because it omits `--fail-on-severity`.
Once you are ready to make findings affect the check, add a threshold to the
scan command:

```bash
"$CODEX_SECURITY_BIN" scan . \
  --diff origin/main \
  --output-dir /path/outside/repository/results \
  --fail-on-severity high
```

The supported thresholds are `critical`, `high`, `medium`, and `low`. A
threshold includes findings at that severity and above.

The scan step uses these exit codes:

| Exit  | Meaning                                                                                 |
| ----- | --------------------------------------------------------------------------------------- |
| `0`   | The scan completed with complete coverage, and any configured policy passed.            |
| `1`   | The completed scan contains a finding at or above the threshold.                        |
| `2`   | The CLI found an input or runtime error, or the completed scan has incomplete coverage. |
| `130` | Ctrl-C interrupted the scan.                                                            |
| `143` | SIGTERM terminated the scan.                                                            |

A scan with `partial` or `unknown` coverage returns `2`, even without a severity
policy. The CLI still writes its available findings and coverage. Review the
deferred areas in `coverage.json` before treating the check as conclusive.

## Retry with an existing result directory

Use a fresh runner directory for each CI job. For a persistent or self-hosted
runner, preserve an earlier result with `--archive-existing`:

```bash
"$CODEX_SECURITY_BIN" scan . \
  --diff origin/main \
  --output-dir /path/outside/repository/results \
  --archive-existing
```

The command archives the earlier results and starts with an empty scan directory.

## Troubleshoot a CI scan

- **Unknown Git ref or unexpected diff:** Fetch the base and head history,
  calculate the merge base, and pass both revisions explicitly.
- **Protected or non-empty output directory:** Choose a private directory
  outside the enclosing Git worktree. Use `--archive-existing` when the
  directory already contains results.
- **Missing credentials:** Confirm the `CODEX_SECURITY_API_KEY` repository
  secret is available to the trusted workflow and mapped directly to the scan
  step's `CODEX_API_KEY` environment variable.
- **Python setup error:** Confirm that the runner uses Python 3.10 or later.
- **Incomplete coverage:** Review `coverage.json`, including deferred surfaces
  and open questions, then rerun with an appropriate target or environment.
- **SARIF export error:** Confirm that the scan completed and the full scan
  directory is available. Export validates the sealed artifacts before writing
  SARIF.
- **SARIF upload error:** For a private or internal repository, confirm that
  your organization turned on GitHub Code Security for the repository and the
  workflow grants `actions: read`, `contents: read`, and
  `security-events: write`.

For every command, flag, artifact, and output field, see the [CLI
reference](https://learn.chatgpt.com/docs/security/cli/reference). For an interactive plugin-based CI
review, see [Review code changes for security](https://learn.chatgpt.com/docs/security/plugin/code-changes#automate-reviews-in-cicd).
