# AGENTS Notes

## Scope
- This repository is a periodic mirror for Codex-related docs and references.
- Keep changes focused on sync automation, output quality, and release hygiene.

## Generated content boundaries
- Treat `docs/codex_capabilities.json`, `docs/developers.openai.com/**`, `docs/learn.chatgpt.com/**`, `docs/feature-flags/**`, `docs/github.openai.com/**`, `docs/platform.openai.com/**`, `dot_codex/skills/dot_system/**`, and `system_prompts/codex-cli/**` as generated output.
- Do not hand-edit mirrored docs, skills, or prompts unless doing a temporary emergency fix.
- If an output problem exists, fix `scripts/fetch_codex_docs.py` instead.

## Local workflow
1. Preferred command runner: use `just`.
2. Setup environment:
   - `just setup`
3. Run sync:
   - `just sync`
4. Validate local idempotence + scope:
   - `just check`
5. For feature-flag snapshot changes:
   - `just feature-flags`
   - `just check-feature-flags`

## Validation expectations
- After changing sync logic, run sync twice and confirm second run is idempotent (no new diffs).
- Verify `docs/docs_manifest.json` and `docs/sync_summary.json` are updated consistently, including Codex CLI version metadata for CLI-backed changes.
- Verify `docs/source_coverage.json` updates consistently and includes expected counts, including complete ChatGPT Learn discovery and mirror coverage.
- Keep `weekly/YYYY-MM-DD.md` generation deterministic for unchanged inputs.
- For feature-flag automation or source-input changes, verify `docs/feature-flags/**` with `just check-feature-flags`.

## CI behavior
- `.github/workflows/update-docs.yml` is direct-push sync to `main`.
- Keep direct-push model unless explicitly requested to move to PR-based flow.
- `.github/workflows/release.yml` creates versioned releases from the root `VERSION` file.
- `.github/workflows/propose-version-bump.yml` is an optional monthly/manual helper that opens a `VERSION` bump PR.
- `.github/workflows/update-feature-flags.yml` keeps `docs/feature-flags/**` snapshots fresh and enforces freshness on related pull requests.

## Runtime controls
- `CODEX_DOCS_TIMEOUT_SECONDS`, `CODEX_DOCS_MAX_RETRIES`, and `CODEX_DOCS_RETRY_BACKOFF_SECONDS` tune fetch behavior.
- `CODEX_DOCS_STRICT_SYNC=1` converts partial-source warnings into hard failures.
- `CODEX_DOCS_STRICT_COVERAGE=1` fails when new codex-related sitemap URLs are discovered but none are newly mirrored.

## Versioning and releases
- Bump `VERSION` using semantic versioning (`x.y.z`) for intentional releases.
- A `VERSION` change on `main` triggers release creation (`vX.Y.Z`).

## Commit guidance
- Keep commits scoped and operationally clear.
- Prefer messages like:
  - `chore: sync codex docs (YYYY-MM-DD)`
  - `ci: adjust docs sync workflow`
  - `feat: improve codex docs extraction`
