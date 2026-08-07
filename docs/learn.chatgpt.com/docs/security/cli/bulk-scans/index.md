---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/cli/bulk-scans'
source_kind: 'learn_markdown'
codex_cli_versions: ["0.146.0", "0.146.1", "0.147.0"]
codex_cli_versions_raw: ["codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0"]
---

# Run bulk security scans

Source: https://learn.chatgpt.com/docs/security/cli/bulk-scans

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use `npx @openai/codex-security bulk-scan` to review repositories in one
campaign. Discover repositories from your personal GitHub account or an
organization, or provide a CSV that pins every repository to an exact Git
revision.

The `@openai/codex-security` package is public. Running scans requires Codex
  Security access. Follow the [CLI quickstart](https://learn.chatgpt.com/docs/security/cli) to install
  the CLI and sign in.

## Choose a repository source

| Source           | When to use it                                                                          |
| ---------------- | --------------------------------------------------------------------------------------- |
| GitHub discovery | Choose repositories interactively from your personal GitHub account or an organization. |
| CSV inventory    | Run a repeatable, automated campaign against exact repository revisions.                |

Both workflows save progress, preserve per-repository results, and let you
resume a campaign after an interruption.

## Discover GitHub repositories

Sign in with GitHub CLI:

```bash
gh auth login
```

Start an interactive bulk scan:

```bash
npx @openai/codex-security bulk-scan
```

The CLI guides you through these steps:

1. Choose your personal GitHub account or an organization.
2. Review repositories active within the last 90 days.
3. Search the repository list and select repositories to scan.
4. Choose a directory for scan results.
5. Review the selected repositories and confirm the campaign.

Discovery excludes archived repositories and forks. The CLI records the exact
default-branch commit for each selected repository in
`<output-directory>/repositories.csv`. No scans start until you confirm the
selection.

To use GitHub Enterprise Server, first sign in to your GitHub host:

```bash
gh auth login --hostname github.example.com
```

Set `GH_HOST` when you start repository discovery:

```bash
GH_HOST=github.example.com npx @openai/codex-security bulk-scan
```

Interactive discovery requires a terminal. For CI, containers, or a prepared
repository list, use a CSV inventory instead.

## Create a repository CSV

Create a CSV with one row for each repository and pinned revision:

```csv
id,repository,revision,scope,mode
payments,https://github.com/example/payments.git,0123456789abcdef0123456789abcdef01234567,services/api,standard
identity,https://github.com/example/identity.git,fedcba9876543210fedcba9876543210fedcba98,,deep
```

The CSV supports these columns:

| Column       | Required | Description                                                                                                |
| ------------ | -------- | ---------------------------------------------------------------------------------------------------------- |
| `id`         | Yes      | Unique repository identifier. Use letters, numbers, periods, hyphens, or underscores.                      |
| `repository` | Yes      | HTTPS URL, SSH URL, or local repository path. Relative paths resolve from the CSV directory.               |
| `revision`   | Yes      | Full 40- or 64-character Git commit SHA. Branch names, tags, and shortened commit hashes aren't supported. |
| `scope`      | No       | A repository-relative directory to scan. Omit the value to scan the full repository.                       |
| `mode`       | No       | `standard` or `deep`. Omit the value to use the command's selected mode.                                   |

To find a local repository's full commit SHA, run:

```bash
git -C /path/to/repository rev-parse HEAD
```

## Run a campaign from CSV

Pass the CSV and a private output directory outside the repositories:

```bash
npx @openai/codex-security bulk-scan repositories.csv \
  --output-dir /path/outside/repositories/security-scans \
  --workers 4
```

`--workers` controls the number of concurrent repository scans and defaults to
`4`. Use `--mode deep` to select deep scanning for rows without their own
`mode`. Each CSV row can still choose its own scan mode and repository scope.

The CLI checks out each pinned revision, scans the selected target, records the
result, and removes the temporary repository checkout. A repository counts as
complete only when its scan has complete coverage and all required result
artifacts exist.

## Choose a model and reasoning effort

Bulk scans use `gpt-5.6-sol` with `xhigh` reasoning effort by default. To
choose another model and effort for a CSV campaign:

```bash
npx @openai/codex-security bulk-scan repositories.csv \
  --output-dir /path/outside/repositories/security-scans \
  --workers 4 \
  --model gpt-5.6-terra \
  --effort high
```

The same options work during interactive repository discovery:

```bash
npx @openai/codex-security bulk-scan --model gpt-5.6-terra --effort high
```

Supported effort levels are `minimal`, `low`, `medium`, `high`, and `xhigh`.

## Review campaign results

The output directory contains the pinned campaign, an append-only results
ledger, and separate artifacts for each repository and attempt:

```text
security-scans/
├── manifest.json
├── results.jsonl
├── checkouts/
└── artifacts/
    ├── payments/
    │   └── attempt-1/
    │       ├── scan-manifest.json
    │       ├── findings.json
    │       ├── coverage.json
    │       └── report.md
    └── identity/
        └── attempt-1/
            ├── scan-manifest.json
            ├── findings.json
            ├── coverage.json
            └── report.md
```

- `manifest.json` records the repositories, pinned revisions, scopes, and scan
  modes in the campaign.
- `results.jsonl` records each repository attempt, its status, artifact
  directory, and any available cost or error details.
- `report.md` provides a readable report for one repository attempt.
- `findings.json` and `coverage.json` record that attempt's findings and
  reviewed scope.

Export one completed repository scan when you need a portable result:

```bash
npx @openai/codex-security export \
  /path/outside/repositories/security-scans/artifacts/payments/attempt-1 \
  --export-format sarif \
  --output /path/outside/repositories/payments.sarif
```

Results can contain source excerpts and vulnerability details. Keep the
output directory private, outside scanned repositories, and subject to an
appropriate retention policy.

## Resume a campaign

Run the original command with the same CSV and output directory:

```bash
npx @openai/codex-security bulk-scan repositories.csv \
  --output-dir /path/outside/repositories/security-scans \
  --workers 4
```

The CLI resumes repositories that still need work. It skips a completed
repository only when the corresponding receipt and all required scan artifacts
still exist.

Don't change the repository inventory for an existing output directory. The CLI
checks the pinned manifest and rejects a different campaign. Use a new output
directory when you change repositories, revisions, scopes, or scan modes.

## Retry repository errors

Use `--max-attempts` to retry a repository after a temporary checkout or scan
error:

```bash
npx @openai/codex-security bulk-scan repositories.csv \
  --output-dir /path/outside/repositories/security-scans \
  --workers 4 \
  --max-attempts 3
```

The default is one attempt per repository. Every attempt receives its own
receipt and artifact directory.

Bulk scans use these exit codes:

| Exit code | Meaning                                                                                                               |
| --------- | --------------------------------------------------------------------------------------------------------------------- |
| `0`       | Every repository completed successfully.                                                                              |
| `2`       | A repository couldn't complete, a scan had incomplete coverage, or the command encountered an input or runtime error. |
| `130`     | Ctrl-C interrupted the campaign.                                                                                      |
| `143`     | SIGTERM terminated the campaign.                                                                                      |

## Run bulk scans in Docker

The [Codex Security
repository](https://github.com/openai/codex-security) includes a hardened
Compose configuration for automated CSV campaigns on a Linux Docker host. The
host must support unprivileged user namespace creation.

Keep the repository CSV, scan results, and sign-in state mounted in persistent
directories. Supply OpenAI credentials through the environment or a secret
manager. For private GitHub repositories, provide `GH_TOKEN` or `GITHUB_TOKEN`
the same way.

Run the image with the mounted CSV and output directory:

```bash
docker compose run --rm codex-security \
  bulk-scan /input/repositories.csv \
  --output-dir /output \
  --workers 4
```

Use the same mounted CSV and output directory to resume the campaign. For
GitHub Enterprise Server, set `CODEX_SECURITY_GIT_HOST` to your GitHub host.

For every available flag, see the [bulk-scan command
reference](https://learn.chatgpt.com/docs/security/cli/reference#codex-security-bulk-scan). For common
questions about scan coverage and findings, see the [CLI
FAQ](https://learn.chatgpt.com/docs/security/cli/faq).
