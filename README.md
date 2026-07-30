# codex-docs

Community-maintained periodic sync for Codex docs, inspired by `claude-code-docs`.

This repository mirrors Codex-focused content from official OpenAI sources and keeps a lightweight change history so updates are easy to review.

## What gets synced

- All documentation pages discovered under `learn.chatgpt.com/docs`, including the Codex changelog
- `developers.openai.com` Codex pages (`/codex/...`)
- Codex-related cookbook/resources pages (`/cookbook/...codex...`, `/resources/codex`)
- Markdown docs from `openai/codex` (README, CHANGELOG, `docs/*.md`, selected CLI/Rust docs)
- Linked platform tool guides referenced by mirrored Codex docs
- System skills materialized by the installed Codex CLI
- A sanitized `codex debug prompt-input` snapshot from the installed Codex CLI
- A generated `docs/codex_capabilities.json` inventory of mirrored capability surfaces

## Repository layout

- `docs/developers.openai.com/...` mirrored pages from the OpenAI Developers site
- `docs/learn.chatgpt.com/docs/...` mirrored documentation from ChatGPT Learn
- `docs/github.openai.com/openai/codex/...` mirrored markdown from `openai/codex`
- `docs/platform.openai.com/...` mirrored linked platform tool guides
- `dot_codex/skills/dot_system/...` mirrored Codex CLI system skills in installed-path shape
- `system_prompts/codex-cli/prompt-input.json` sanitized prompt input snapshot from `codex debug prompt-input`
- `docs/docs_manifest.json` hash manifest for change tracking, including Codex CLI version-history metadata
- `docs/codex_capabilities.json` generated capability inventory spanning system skills, prompt snapshots, and linked tool guides
- `docs/sync_summary.json` latest sync summary with the source snapshot for changed outputs
- `docs/source_coverage.json` sitemap coverage watchdog output
- `weekly/YYYY-MM-DD.md` digest files with category summary + raw changed paths

Generated Markdown files include YAML frontmatter with stable source metadata such as `source_type`, `source_area`, `source_url`, upstream `source_last_modified` when available, and `codex_cli_versions` history for the CLI versions where the file remained present.

## Automation

GitHub Actions workflow: `.github/workflows/update-docs.yml`

- Runs every 6 hours
- Executes `scripts/fetch_codex_docs.py`
- Commits and pushes when content changes are detected
- Uploads `docs/source_coverage.json` as a workflow artifact for visibility
- On sync failure, creates or updates a daily issue with sync summary + log tail

Coverage watchdog behavior:

- Records every discovered and mirrored ChatGPT Learn documentation URL, including Markdown and HTML-fallback counts
- Logs codex-related sitemap URL counts and deltas on each run
- Highlights newly discovered codex-related URLs in workflow logs
- Optional strict mode: set `CODEX_DOCS_STRICT_COVERAGE=1` to fail when new codex-related URLs are discovered but none are mirrored

Resiliency controls:

- `CODEX_DOCS_TIMEOUT_SECONDS` request timeout per call (default `30`)
- `CODEX_DOCS_MAX_RETRIES` max request attempts (default `3`)
- `CODEX_DOCS_RETRY_BACKOFF_SECONDS` exponential backoff base (default `1.5`)
- `CODEX_DOCS_STRICT_SYNC=1` fail the run if any source segment fails (otherwise partial-source runs are allowed and failures are recorded)
- `just check-strict` runs the idempotence check with strict sync failure enforcement
- ChatGPT Learn pages use the official Markdown endpoint when available and fall back to the canonical HTML page when it is not

Release workflow: `.github/workflows/release.yml`

- Creates a GitHub release from the root `VERSION` file (tag format `vX.Y.Z`)
- Triggers on `VERSION` changes or manual run via `workflow_dispatch`
- Keeps direct-push sync model unchanged

Optional helper workflow: `.github/workflows/propose-version-bump.yml`

- Runs monthly (and manual dispatch) to prepare a `VERSION` bump branch
- Skips duplicate work when an open bump PR with the same title already exists
- Opens or updates a tracking issue when the default Actions token cannot create PRs

Feature lifecycle workflow: `.github/workflows/update-feature-flags.yml`

- Runs daily (and manual dispatch) to snapshot current feature flags into `docs/feature-flags/`
- Uses both `codex features list` and `openai/codex` source files for lifecycle + semantics checks
- Commits updated snapshots on schedule/manual runs when drift is detected
- Enforces freshness on pull requests touching feature-flag automation/docs inputs

## Local usage

```bash
just setup
just lint
just test
just sync
just check
just check-strict
just feature-flags
just check-feature-flags
```

Local setup defaults to Python 3.14 to match CI. Set `CODEX_DOCS_PYTHON` to an equivalent Python 3.14 executable when needed. The actionlint recipe uses Go to run the same pinned actionlint release as CI.

## Notes

- This is a community mirror, not an official OpenAI repository.
- Content attribution remains with the original sources.
- If a source page structure changes, update `scripts/fetch_codex_docs.py` selectors and filters.
