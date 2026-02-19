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
- `weekly/YYYY-MM-DD.md` digest files written when changes are detected

## Automation

GitHub Actions workflow: `.github/workflows/update-docs.yml`

- Runs every 6 hours
- Executes `scripts/fetch_codex_docs.py`
- Commits and pushes when content changes are detected

Release workflow: `.github/workflows/release.yml`

- Creates a GitHub release from the root `VERSION` file (tag format `vX.Y.Z`)
- Triggers on `VERSION` changes or manual run via `workflow_dispatch`
- Keeps direct-push sync model unchanged

## Local usage

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/fetch_codex_docs.py
```

## Notes

- This is a community mirror, not an official OpenAI repository.
- Content attribution remains with the original sources.
- If a source page structure changes, update `scripts/fetch_codex_docs.py` selectors and filters.
