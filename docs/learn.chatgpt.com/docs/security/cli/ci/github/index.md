---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/cli/ci/github'
source_kind: 'learn_markdown'
---

# Run Codex Security in GitHub Actions

Source: https://learn.chatgpt.com/docs/security/cli/ci/github

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Run Codex Security in GitHub Actions to review pull-request changes or scan
your repository on a schedule. The Action installs the CLI, saves structured
reports, and adds a job summary and source annotations. Start with advisory
results, then configure enforcement after reviewing coverage and scan quality.

## Prepare the workflow

Running scans requires Codex Security access. To add your OpenAI API key:

1. In your GitHub repository, open **Settings → Secrets and variables → Actions**.
2. Select **New repository secret**.
3. Enter `CODEX_SECURITY_API_KEY` as the name and paste your OpenAI API key as
   the value. Save the secret.

The workflow examples below pass this secret to the Codex Security Action
automatically. You don't need to put your API key in the workflow file.

Run the workflow only for repositories and pull requests you trust. Scans use
the runner's local permissions and don't pause for approval. Keep unrelated
credentials and deployment steps in separate jobs.

## Add the GitHub Actions workflow

**Scan costs:** These workflows use your API key and may incur charges. The
  scheduled example omits `max-cost`. The pull-request workflow sets an
  estimated threshold of $5 per scan. The cost of requests already in progress
  can exceed that threshold. See [Set an optional scan
  budget](#set-an-optional-scan-budget).

### Scan the repository on a schedule

The workflow below scans your default branch every Monday at 07:23 UTC. You
can also run it manually from GitHub's **Actions** tab. It uses an x64
GitHub-hosted Ubuntu 24.04 runner and sets up the required sandbox automatically.

1. In your repository, select **Add file → Create new file**.
2. Name the file `.github/workflows/codex-security-repository.yml`.
3. Paste the workflow below and commit it to your default branch.

```yaml
name: Codex Security repository

on:
  workflow_dispatch:
  schedule:
    - cron: "23 7 * * 1" # Mondays at 07:23 UTC

permissions:
  contents: read

jobs:
  security:
    runs-on: ubuntu-24.04
    timeout-minutes: 120
    steps:
      - name: Check out the repository
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false

      - name: Scan the repository
        id: security
        uses: openai/codex-security@a98b35d7eef9f85c298c86229445bb64ac427aaf # action-v0.9.1
        with:
          scope: repository
          model: gpt-6-sol
          # For approved Daybreak Blue access, uncomment the next input.
          # cyber-access-program: daybreak_blue
          effort: high
          fail-on-severity: none
          upload-artifacts: "true"
        env:
          OPENAI_API_KEY: ${{ secrets.CODEX_SECURITY_API_KEY }}
```

The Action checks the Codex sandbox before using the scan credential. On a
GitHub-hosted Ubuntu 24.04 VM, it installs the required packages and loads the
AppArmor profile if needed. On self-hosted runners and in job containers,
provide a working sandbox, Linux x64, Node.js 24, and Python 3.11 or later.

To run the workflow manually, open **Actions → Codex Security repository →
Run workflow**. Open a completed run to review the summary, annotations, and
downloadable reports.

Findings are report-only because `fail-on-severity` is `none`. Scanner and
required reporting errors still fail the job.

To scan selected folders, add newline-separated literal paths to the scan
step's `with` block:

```yaml
paths: |
  src/api
  src/auth
```

Paths require `scope: repository` and do not expand globs. For diff scans, omit
`paths`. Keep `persist-credentials: false` and run the scan
immediately after checkout.

### Scan pull-request changes

1. Copy the [pull-request workflow](https://github.com/openai/codex-security/blob/a98b35d7eef9f85c298c86229445bb64ac427aaf/github-action/examples/pull-request.yml)
   to `.github/workflows/codex-security-pr.yml`. Replace
   `REPLACE_WITH_REVIEWED_COMMIT` with `a98b35d7eef9f85c298c86229445bb64ac427aaf`, the distribution commit for `action-v0.9.1`.
2. Choose a model your API key can access. The template sets a $5 threshold for estimated
   scan costs and fails on high or critical findings. For advisory findings, set
   `fail-on-severity: none`.
3. Open a PR from a branch in the same repository. Under **Checks**, open
   **Scan changes** to review the results. The workflow also reports a check
   named for the target branch, such as **Codex Security / main**.

The workflow checks the PR head, target branch, and live base revision before
scanning and again before accepting the result. If the base advances, update
the PR branch to trigger a fresh scan. To enforce this at merge time, follow the [branch protection and freshness requirements](https://github.com/openai/codex-security/blob/a98b35d7eef9f85c298c86229445bb64ac427aaf/github-action/README.md#scan-pull-requests).

The scan job skips fork PRs, so they cannot pass this workflow's required
check. To scan Dependabot PRs, also save `CODEX_SECURITY_API_KEY` as a [Dependabot secret](https://docs.github.com/en/code-security/reference/supply-chain-security/troubleshoot-dependabot/dependabot-on-actions#accessing-secrets).

The scanner reads applicable `SECURITY.md` guidance from the checkout,
including policy changes in the PR. Review those changes alongside the code.

### Configure optional Daybreak access

If your organization has approval for [Trusted Access for
Cyber](https://learn.chatgpt.com/docs/cyber-safety#trusted-access-for-cyber), select the program and a
compatible model in the scan step's `with` block:

```yaml
model: gpt-6-sol
cyber-access-program: daybreak_blue
```

Use an API key from a project enabled for Daybreak Blue with access to
`gpt-6-sol`.

The input also accepts `daybreak_red` for projects with Red access. To select
standard safeguards, set `cyber-access-program` to `standard`. Omitting the
input uses the CLI defaults. See the Action's [Daybreak access guidance](https://github.com/openai/codex-security/blob/a98b35d7eef9f85c298c86229445bb64ac427aaf/github-action/README.md#daybreak-access-and-refusals).

A refusal or safety block that aborts the scan fails the Action, including when
`fail-on-severity` is `none`. That input controls findings policy, not scanner
errors.

### Set an optional scan budget

The scheduled workflow omits `max-cost`. To set a threshold, add a positive
USD amount with the `max-cost` input. For direct CLI scans, use `--max-cost`.

The cost limit requires CLI pricing support for the selected model. The cost of
requests already in progress can exceed the estimated threshold. Review findings and
`scan-manifest.json` if a scan stops at the threshold. See
[output and policy options](https://learn.chatgpt.com/docs/security/cli/reference#set-output-and-policy-options)
for cost-limit behavior.

### Save reports and upload SARIF

Set `upload-artifacts: "true"` to save downloadable reports. The default
retention is seven days. Reports can contain source snippets, vulnerability
evidence, and remediation details. Choose a retention window and repository
access appropriate for your code. The Action uploads only validated reports
on its allowlist; do not recursively upload its `results-directory` output.

SARIF upload is optional. For private or internal repositories, enable [GitHub Code Security](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/integrate-with-existing-tools/upload-sarif-file) before uploading. The scan job needs these permissions for SARIF upload:

```yaml
permissions:
  contents: read
  security-events: write
  actions: read # Required for private repositories
  pull-requests: read # Required only in the PR workflow
```

Then add this step after the scan in either workflow:

```yaml
- name: Upload security findings
  if: ${{ always() && steps.security.outputs.sarif-upload-ready == 'true' }}
  uses: github/codeql-action/upload-sarif@b96794f015dfd88f77b49b1c93e0fa7110f94c63 # v4.38.0
  with:
    sarif_file: ${{ steps.security.outputs.sarif-path }}
    sha: ${{ steps.security.outputs.scanned-sha }}
    ref: ${{ steps.security.outputs.analysis-ref }}
    category: codex-security-repository
```

For the PR workflow, use `category: codex-security-pr` so each scope has a
distinct category. Keep `id: security` on the scan step. Complete, validated
reports remain available for upload when findings fail the severity policy.
SARIF is not uploaded for failed or interrupted scans, empty diffs, or dry
runs.

See the Action's [input
and output reference](https://github.com/openai/codex-security/blob/a98b35d7eef9f85c298c86229445bb64ac427aaf/github-action/README.md#inputs) for all settings, status fields, and report paths.

## Choose a severity policy

The scheduled workflow starts with `fail-on-severity: none`. To fail on high or
critical findings from a completed scan, use the PR workflow's setting:

```yaml
fail-on-severity: high
```

For each protected target branch, require the matching check from the GitHub
Actions app, such as **Codex Security / main** on `main`. GitHub treats
a [conditionally skipped job as successful](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks#handling-skipped-but-required-checks).
The workflow's required check also verifies that the scan job ran. It accepts
a completed scan or a verified empty diff. To block empty diffs too,
[require a successful, completed scan](#require-a-successful-completed-scan).

The Action follows the CLI outcome:

- Exit code `0` sets `scan-status: completed` and `policy-status: passed`.
- Exit code `1` sets `scan-status: completed` and `policy-status: failed`;
  the step fails on findings at or above the configured severity.
- Exit code `2` or an interrupted process sets `scan-status: failed` and
  `policy-status: not-evaluated`; the step fails.
- Invalid or missing required reports, a changed checkout, failures to upload
  requested artifacts, and runtime cleanup failures also fail the step.

### Require a successful, completed scan

For a stricter policy, add a separate gate that runs even if the scan job
fails or GitHub skips it. A step inside the scan job can't check a skipped job
because none of its steps run.

The PR workflow exposes the scan status through the `security` job:

```yaml
outputs:
  scan-status: ${{ steps.security.outputs.scan-status }}
```

Then add this job under `jobs`, alongside the existing `security` job:

```yaml
security-gate:
  name: ${{ github.event.action == 'edited' && github.event.changes.base == null && 'metadata / ' || '' }}Codex Security gate / ${{ github.event.pull_request.base.ref }}
  needs: security
  if: always() && (github.event.action != 'edited' || github.event.changes.base != null)
  runs-on: ubuntu-24.04
  steps:
    - name: Require a successful, completed scan
      env:
        SCAN_RESULT: ${{ needs.security.result }}
        SCAN_STATUS: ${{ needs.security.outputs.scan-status }}
      run: test "$SCAN_RESULT" = success && test "$SCAN_STATUS" = completed
```

For each protected branch, require its gate alongside its scan check. For
`main`, require **Codex Security gate / main** and **Codex Security / main**. The gate requires both a successful scan job and
`scan-status: completed`. Checking both preserves failures from the severity
policy, reporting, and cleanup, even when the scan itself completed.

With the example's exclusions, this gate blocks fork PRs. It also blocks
empty diffs and dry runs, which the Action marks as `skipped`. The gate
doesn't scan excluded PRs. Choose this policy only if these cases should
prevent merging.

## Troubleshoot a scan

- **Unknown Git ref or unexpected diff:** Check out the PR head with
  `fetch-depth: 0`.
- **Missing credentials:** Confirm that `CODEX_SECURITY_API_KEY` is available to
  the trusted workflow and mapped to the scan step's `OPENAI_API_KEY`
  environment variable.
- **Python setup error:** The Action requires Python 3.11 or later.
- **Missing SARIF:** Inspect `scan-status`, `report-status`, and
  `sarif-upload-ready`. If optional SARIF is missing, the Action warns without
  changing the scan outcome; requested artifact-upload failures still fail the
  job.
- **SARIF upload error:** Confirm that your organization has enabled GitHub Code
  Security for the repository and that the workflow grants `actions: read`,
  `contents: read`, and `security-events: write`.

For every command, flag, artifact, and output field, see the [CLI
reference](https://learn.chatgpt.com/docs/security/cli/reference). For other providers, see the
[CI/CD overview](https://learn.chatgpt.com/docs/security/cli/ci).
