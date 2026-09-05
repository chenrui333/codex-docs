# AGENTS Notes

## Scope
- This repository is a periodic mirror for Codex-related docs and references.
- Keep changes focused on sync automation, output quality, and release hygiene.

## Generated content boundaries
- Treat `docs/codex_capabilities.json`, `docs/codex_cli_surface.json`, `docs/cli-surface/**`, `docs/codex_models.json`, `docs/docs_manifest.json`, `docs/sync_summary.json`, `docs/source_coverage.json`, `docs/freshness.json`, `docs/developers.openai.com/**`, `docs/learn.chatgpt.com/**`, `docs/feature-flags/**`, `docs/github.openai.com/**`, `docs/platform.openai.com/**`, `dot_codex/skills/dot_system/**`, `system_prompts/codex-cli/**`, `weekly/events/**`, and `weekly/YYYY-MM-DD.md` as generated output.
- Do not hand-edit mirrored docs, skills, or prompts unless doing a temporary emergency fix.
- Fix the responsible generator and regenerate affected output. `scripts/fetch_codex_docs.py` coordinates sync; `scripts/model_catalog.py`, `scripts/cli_observations.py`, and `scripts/semantic_history.py` own the pure model, platform, and event transformations. `scripts/collect_cli_surface.py` collects help observations; `scripts/snapshot_feature_flags.py` builds feature snapshots.

## Local workflow
1. Preferred command runner: use `just`.
2. Setup environment:
   - `just setup`
3. Run offline quality checks:
   - `just lint`
   - `just test`
4. Run sync:
   - `just sync` for full source discovery, or `just sync-release` for strict release-only generation using a verified existing web mirror.
5. Validate local idempotence + scope:
   - `just check-strict` for two full strict syncs, freshness, idempotence, and changed-file scope. `just check` is the non-strict local variant.
6. For feature-flag snapshot changes:
   - `just feature-flags`
   - `just check-feature-flags`

## Validation expectations
- After changing sync logic, run sync twice and confirm second run is idempotent (no new diffs).
- Verify `docs/docs_manifest.json` and `docs/sync_summary.json` are updated consistently, including Codex CLI version metadata for CLI-backed changes.
- Verify `docs/source_coverage.json` updates consistently and includes expected counts, including complete ChatGPT Learn discovery and mirror coverage.
- Preserve existing events in `weekly/events/YYYY-MM-DD.json`; daily Markdown is their deterministic rollup. Repeated identical syncs must add neither events nor timestamp-only changes. Do not rewrite older daily reports during migration.
- Keep web content provenance independent of CLI releases. Existing web-page CLI-version lists are frozen historical observations; new web pages must not acquire them.
- Model catalogs and feature snapshots must match the CLI release tag and immutable source commit. Model provenance mismatches fail freshness even inside the release-lag grace period.
- CLI removals require a newer descendant release on every previously observed platform. Unknown/divergent ancestry or an unavailable collector must retain last-known-good evidence; semantic history must not report false removals.
- Run CLI introspection in temporary isolated homes with sanitized subprocess environments; never capture real credentials, sessions, history, or inherited GitHub tokens.
- Keep the repository otherwise unchanged while `just check-strict` runs: its scope check snapshots the whole working tree.
- For feature-flag automation or source-input changes, verify `docs/feature-flags/**` with `just check-feature-flags`; snapshots must use the source commit resolved from the CLI release tag.

## CI behavior
- `.github/workflows/update-docs.yml` collects Linux/macOS CLI observations, then runs separate release-state and full-web direct-push transactions to `main`. Each transaction is fail-closed; a web outage must not invalidate an already verified release commit.
- Release-only sync must validate cached web content against its manifest and reject partial diagnostic state. Missing platform artifacts preserve prior observations.
- Release, web, and feature writers share `docs-writer-main` concurrency and verify the actual checkout base before pushing. Preserve both guards.
- Coverage distinguishes current web discovery from retained last-known-good state. Release freshness does not assert current web health; no-op runs must not rewrite success timestamps.
- Keep direct-push model unless explicitly requested to move to PR-based flow.
- `.github/workflows/release.yml` creates versioned releases from the root `VERSION` file.
- `.github/workflows/propose-version-bump.yml` is an optional monthly/manual helper that opens a `VERSION` bump PR.
- `.github/workflows/update-feature-flags.yml` keeps `docs/feature-flags/**` snapshots fresh and enforces freshness on related pull requests.

## Runtime controls
- `CODEX_DOCS_TIMEOUT_SECONDS`, `CODEX_DOCS_COMMAND_TIMEOUT_SECONDS`, `CODEX_DOCS_MAX_RETRIES`, and `CODEX_DOCS_RETRY_BACKOFF_SECONDS` tune fetch and subprocess behavior.
- `CODEX_DOCS_STRICT_SYNC=1` converts partial-source warnings into hard failures and is mandatory in scheduled automation.
- `CODEX_DOCS_STRICT_COVERAGE=1` fails when new codex-related sitemap URLs are discovered but none are newly mirrored.

## Versioning and releases
- Bump `VERSION` using semantic versioning (`x.y.z`) for intentional releases.
- A `VERSION` change on `main` triggers release creation (`vX.Y.Z`).

## Commit guidance
- Keep commits scoped and operationally clear; always use `git commit -s` for DCO sign-off.
- Keep branch names and commit messages task-specific; do not include `codex` in them.
- Prefer messages like:
  - `chore: sync release state (YYYY-MM-DD)`
  - `ci: adjust docs sync workflow`
  - `feat: improve documentation extraction`
