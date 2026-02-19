# codex-docs

Community-maintained periodic sync for Codex docs, inspired by `claude-code-docs`.

This repository mirrors Codex-focused content from official OpenAI sources and keeps a lightweight change history so updates are easy to review.

## What gets synced

- `developers.openai.com` Codex pages (`/codex/...`)
- Codex-related cookbook/resources pages (`/cookbook/...codex...`, `/resources/codex`)
- Markdown docs from `openai/codex` (README, CHANGELOG, `docs/*.md`, selected CLI/Rust docs)

## Repository layout

- `docs/developers.openai.com/...` mirrored pages from the OpenAI Developers site
- `docs/github.openai.com/openai/codex/...` mirrored markdown from `openai/codex`
- `docs/docs_manifest.json` hash manifest for change tracking
- `docs/sync_summary.json` latest sync summary
- `docs/source_coverage.json` sitemap coverage watchdog output
- `weekly/YYYY-MM-DD.md` digest files with category summary + raw changed paths

## Automation

GitHub Actions workflow: `.github/workflows/update-docs.yml`

- Runs every 6 hours
- Executes `scripts/fetch_codex_docs.py`
- Commits and pushes when content changes are detected
- Uploads `docs/source_coverage.json` as a workflow artifact for visibility
- On sync failure, creates or updates a daily issue with sync summary + log tail

Coverage watchdog behavior:

- Logs codex-related sitemap URL counts and deltas on each run
- Highlights newly discovered codex-related URLs in workflow logs
- Optional strict mode: set `CODEX_DOCS_STRICT_COVERAGE=1` to fail when new codex-related URLs are discovered but none are mirrored

Resiliency controls:

- `CODEX_DOCS_TIMEOUT_SECONDS` request timeout per call (default `30`)
- `CODEX_DOCS_MAX_RETRIES` max request attempts (default `3`)
- `CODEX_DOCS_RETRY_BACKOFF_SECONDS` exponential backoff base (default `1.5`)
- `CODEX_DOCS_STRICT_SYNC=1` fail the run if any source segment fails (otherwise partial-source runs are allowed and failures are recorded)

Release workflow: `.github/workflows/release.yml`

- Creates a GitHub release from the root `VERSION` file (tag format `vX.Y.Z`)
- Triggers on `VERSION` changes or manual run via `workflow_dispatch`
- Keeps direct-push sync model unchanged

Optional helper workflow: `.github/workflows/propose-version-bump.yml`

- Runs monthly (and manual dispatch) to propose a `VERSION` bump PR
- Skips creating duplicates when an open bump PR with the same title already exists

## Local usage

```bash
just setup
just sync
just check
```

## Notes

- This is a community mirror, not an official OpenAI repository.
- Content attribution remains with the original sources.
- If a source page structure changes, update `scripts/fetch_codex_docs.py` selectors and filters.
