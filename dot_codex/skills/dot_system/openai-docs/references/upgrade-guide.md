---
source_type: 'codex_cli_system_skill'
source_area: 'system_skill_openai_docs'
source_url: 'codex-cli://skills/.system/openai-docs/references/upgrade-guide.md'
source_kind: 'installed_codex_cli'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0", "0.144.0", "0.144.1", "0.144.3", "0.144.4", "0.144.5", "0.144.6", "0.145.0", "0.146.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0", "codex-cli 0.144.0", "codex-cli 0.144.1", "codex-cli 0.144.3", "codex-cli 0.144.4", "codex-cli 0.144.5", "codex-cli 0.144.6", "codex-cli 0.145.0", "codex-cli 0.146.0"]
---

# Model upgrade guidance

Use this file only as a bundled routing fallback when the live migration guide cannot be fetched.

For latest, current, default, or unspecified-model upgrades:

1. Run `scripts/resolve-latest-model-info`.
2. Fetch the returned `migrationGuideUrl` and `promptingGuideUrl` exactly.
3. Treat the live guides as canonical.
4. If remote retrieval fails, disclose that bundled fallback guidance is being used.

For an explicit GPT-5.6 Sol or GPT-5.6-family migration:

1. Preserve the user's explicit target; do not run the latest-model resolver.
2. Fetch the live GPT-5.6 model guidance:

   https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6

3. Read `references/upgrading-to-gpt-5p6-sol.md` for skill-specific migration judgment.
4. Read `references/prompting-guide.md` only when prompt changes are needed.

For another explicit model target, preserve that target and fetch its current official guidance. Do not reuse GPT-5.6-specific defaults, API shapes, or compatibility rules for a different model.
