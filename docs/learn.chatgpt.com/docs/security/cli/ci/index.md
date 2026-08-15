---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/cli/ci'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0"]
---

# Run Codex Security in CI

Source: https://learn.chatgpt.com/docs/security/cli/ci

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Run the Codex Security CLI in CI to review the exact changes in a pull request
or merge request, keep findings and coverage, and optionally fail the check at
a chosen severity. Start with advisory results, review scan quality and
runtime, then add a severity policy that fits your repository.

Install the public `@openai/codex-security` package. Running scans still
  requires Codex Security access.

This guide includes examples for GitHub Actions and GitLab CI/CD. The same scan
and export commands work in other CI systems.

## Prepare the workflow

Store an OpenAI API key in your CI provider's secret store as
`CODEX_SECURITY_API_KEY`.

Map this secret directly to the scan step's `OPENAI_API_KEY` environment
variable. Keep the credential scoped to the scan process and use
`--auth api-key` to select it explicitly.

Run the workflow only for repositories and pull requests you trust. Scans use
the runner's local permissions and don't pause for approval. Scan processes
can inherit the job environment, so keep unrelated tokens and cloud
credentials out of it.

The runner needs:

- Node.js 22 (22.13.0 or later), 24, or 26.
- Python 3.10 or later.
- The published `@openai/codex-security` package, installed outside the
  repository checkout.
- The pull-request or merge-request head and base history so Git can calculate
  the merge base.

## Add the GitHub Actions workflow

For private or internal repositories, enable
[GitHub Code Security](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/uploading-a-sarif-file-to-github)
before you upload SARIF.

Create `.github/workflows/codex-security.yml`. Before checking out the pull
request, install `@openai/codex-security` under
`$RUNNER_TEMP/codex-security` so the trusted executable is available at
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
        run: |
          set -euo pipefail
          npm install \
            --prefix "$RUNNER_TEMP/codex-security" \
            --ignore-scripts \
            --no-audit \
            --no-fund \
            @openai/codex-security

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
          OPENAI_API_KEY: ${{ secrets.CODEX_SECURITY_API_KEY }}
          CODEX_SECURITY_BIN: ${{ runner.temp }}/codex-security/node_modules/.bin/codex-security
          CODEX_SECURITY_STATE_DIR: ${{ runner.temp }}/codex-security-state
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
          SCAN_DIR: ${{ runner.temp }}/codex-security-results
        run: |
          set -euo pipefail
          BASE_REVISION="$(git merge-base "$BASE_SHA" "$HEAD_SHA")"
          "$CODEX_SECURITY_BIN" scan . \
            --diff "$BASE_REVISION" \
            --head "$HEAD_SHA" \
            --auth api-key \
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
the scan credential. `--auth api-key` explicitly selects the scoped API key.
The scan saves its history in a writable state directory outside the
repository.

`--json` writes one complete JSON document to stdout, so the workflow can save
it directly. Progress, completion summaries, and errors remain on stderr. This
differs from `codex exec --json`, which emits a JSON Lines event stream.

The export step reads a completed, sealed scan and writes SARIF. It leaves the
Codex runtime and credentials untouched. Scan artifacts can contain vulnerable
source snippets, evidence, and remediation details. Choose access controls and a
short retention window appropriate for your repository.

## Add the GitLab CI/CD pipeline

GitLab can ingest
[SARIF 2.1.0 reports](https://docs.gitlab.com/ci/yaml/artifacts_reports/#artifactsreportssarif)
on GitLab Ultimate 19.2 or later. Add a masked and hidden
`CODEX_SECURITY_API_KEY` CI/CD variable before you run the pipeline.

Add the `security` stage and Codex Security job to the root `.gitlab-ci.yml`.
Keep any existing stages and jobs in the file. The example scans merge-request
changes by default. Set `CODEX_SECURITY_FULL_SCAN_DEFAULT_BRANCH` to `"true"`
to also scan the complete default branch:

```yaml
variables:
  CODEX_SECURITY_FULL_SCAN_DEFAULT_BRANCH: "false"

stages:
  - test
  - security

codex-security:
  stage: security
  image: node:26-bookworm-slim
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event" && $CI_MERGE_REQUEST_SOURCE_PROJECT_ID == $CI_PROJECT_ID'
      variables:
        CODEX_SECURITY_SCAN_SCOPE: "diff"
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH && $CODEX_SECURITY_FULL_SCAN_DEFAULT_BRANCH == "true"'
      variables:
        CODEX_SECURITY_SCAN_SCOPE: "full"
  variables:
    GIT_DEPTH: "0"
    CODEX_SECURITY_CLI_DIR: "/tmp/codex-security-cli"
  before_script:
    - |
      set -eu
      apt-get update -qq
      apt-get install -y -qq --no-install-recommends \
        ca-certificates \
        git \
        python3 \
        ripgrep
      npm install \
        --prefix "$CODEX_SECURITY_CLI_DIR" \
        --ignore-scripts \
        --no-audit \
        --no-fund \
        @openai/codex-security
      export CODEX_SECURITY_BIN="$CODEX_SECURITY_CLI_DIR/node_modules/.bin/codex-security"
      test -x "$CODEX_SECURITY_BIN"
      "$CODEX_SECURITY_BIN" --version
  script:
    - |
      set -eu
      if test -z "${CODEX_SECURITY_API_KEY:-}"; then
        echo "Set the CODEX_SECURITY_API_KEY CI/CD variable." >&2
        exit 2
      fi

      codex_security_api_key="$CODEX_SECURITY_API_KEY"
      unset CODEX_SECURITY_API_KEY

      case "${CODEX_SECURITY_SCAN_SCOPE:-}" in
        diff)
          BASE_SHA="$CI_MERGE_REQUEST_DIFF_BASE_SHA"
          HEAD_SHA="$CI_COMMIT_SHA"
          BASE_REVISION="$(git merge-base "$BASE_SHA" "$HEAD_SHA")"
          set -- --diff "$BASE_REVISION" --head "$HEAD_SHA"
          echo "Scanning committed changes from $BASE_REVISION to $HEAD_SHA."
          ;;
        full)
          set -- --mode standard
          echo "Scanning the complete default branch at $CI_COMMIT_SHA."
          ;;
        *)
          echo "Unsupported Codex Security scan scope: ${CODEX_SECURITY_SCAN_SCOPE:-unset}" >&2
          exit 2
          ;;
      esac

      export CODEX_SECURITY_STATE_DIR="/tmp/codex-security-state-$CI_JOB_ID"
      SCAN_DIR="/tmp/codex-security-results-$CI_JOB_ID"
      JSON_FILE="/tmp/codex-security-$CI_JOB_ID.json"
      SARIF_FILE="/tmp/codex-security-$CI_JOB_ID.sarif"

      install -d -m 700 "$CODEX_SECURITY_STATE_DIR" "$SCAN_DIR"

      set +e
      OPENAI_API_KEY="$codex_security_api_key" \
        "$CODEX_SECURITY_BIN" scan . \
          "$@" \
          --auth api-key \
          --output-dir "$SCAN_DIR" \
          --json > "$JSON_FILE"
      scan_exit="$?"
      set -e
      unset codex_security_api_key

      install -d -m 700 codex-security-artifacts/results
      cp -R "$SCAN_DIR"/. codex-security-artifacts/results/
      if test -s "$JSON_FILE"; then
        cp "$JSON_FILE" codex-security-artifacts/codex-security.json
      fi
      printf '%s\n' "$scan_exit" > codex-security-artifacts/scan-exit-code.txt

      export_exit=0
      if test -f "$SCAN_DIR/scan-manifest.json"; then
        set +e
        "$CODEX_SECURITY_BIN" export "$SCAN_DIR" \
          --export-format sarif \
          --source-root "$CI_PROJECT_DIR" \
          --output "$SARIF_FILE"
        export_exit="$?"
        set -e
        if test -s "$SARIF_FILE"; then
          cp "$SARIF_FILE" codex-security-artifacts/codex-security.sarif
        fi
      fi

      if test "$scan_exit" -ne 0; then
        exit "$scan_exit"
      fi
      exit "$export_exit"
  artifacts:
    when: always
    access: maintainer
    expire_in: 7 days
    paths:
      - codex-security-artifacts/
    reports:
      sarif: codex-security-artifacts/codex-security.sarif
```

By default, the job runs only for merge requests from branches in the same
project, so fork pipelines don't receive the scan credential. Set
`CODEX_SECURITY_FULL_SCAN_DEFAULT_BRANCH` to `"true"` at the group, project, or
pipeline level to also run a standard full scan on the default branch. Full
scans take longer and cost more than diff scans.

`GIT_DEPTH: "0"` provides the history needed to calculate the merge base from
`CI_MERGE_REQUEST_DIFF_BASE_SHA` and `CI_COMMIT_SHA` for merge-request scans.

The job installs the CLI under `/tmp`, runs it by absolute path, and exposes the
API key only to the scan process. `artifacts: when: always` preserves the SARIF
report when the scan fails, while `artifacts:access: maintainer` limits access
to detailed scan results.

Changes to `.gitlab-ci.yml` can expose CI/CD variables, so review pipeline
changes before running the job. If you
[protect `CODEX_SECURITY_API_KEY`](https://docs.gitlab.com/ci/pipelines/merge_request_pipelines/#control-access-to-protected-variables-and-runners),
GitLab makes it available only for same-project merge requests between
protected branches and only when the user can access the target branch.

## Choose a severity policy

Both examples are report-only because they omit `--fail-on-severity`. Once you
are ready to make findings affect the check, add a threshold to the scan
command:

```bash
"$CODEX_SECURITY_BIN" scan . \
  --diff origin/main \
  --output-dir /path/outside/repository/results \
  --fail-on-severity high
```

The supported thresholds are `critical`, `high`, `medium`, and `low`. A
threshold includes findings from the current scan at that severity and above.
Earlier open findings shown in the repository summary don't affect the policy.

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
- **Missing credentials:** Confirm that `CODEX_SECURITY_API_KEY` is available to
  the trusted workflow or pipeline and mapped directly to the scan process's
  `OPENAI_API_KEY` environment variable.
- **Scan history error:** Set `CODEX_SECURITY_STATE_DIR` to a writable
  directory outside the repository.
- **Python setup error:** Confirm that the runner uses Python 3.10 or later.
- **Incomplete coverage:** Review `coverage.json`, including deferred surfaces
  and open questions, then rerun with an appropriate target or environment.
- **SARIF export error:** Confirm that the scan completed and the full scan
  directory is available. Export validates the sealed artifacts before writing
  SARIF.
- **SARIF upload error:** For GitHub Actions, confirm that your organization
  turned on GitHub Code Security for the repository and the workflow grants
  `actions: read`, `contents: read`, and `security-events: write`. For GitLab
  CI/CD, confirm that the project uses GitLab Ultimate 19.2 or later and that
  the job uploads a SARIF 2.1.0 file through `artifacts:reports:sarif`.

For every command, flag, artifact, and output field, see the [CLI
reference](https://learn.chatgpt.com/docs/security/cli/reference). For an interactive plugin-based CI
review, see [Review code changes for security](https://learn.chatgpt.com/docs/security/plugin/code-changes#automate-reviews-in-cicd).
