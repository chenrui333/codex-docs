---
source_type: 'codex_cli_system_skill'
source_area: 'system_skill_openai_docs'
source_url: 'codex-cli://skills/.system/openai-docs/references/model-selection.md'
source_kind: 'installed_codex_cli'
codex_cli_versions: ["0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0"]
codex_cli_versions_raw: ["codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0"]
codex_cli_release_ref: 'rust-v0.152.0'
codex_cli_source_commit: '316795b3cf2a45e90d121d9f46499d4658b2645c'
---

# Model selection

Use this route for model recommendations, comparisons, and latest/current/default choices when the user is not requesting a migration or prompting guidance.

1. Search current official OpenAI documentation for the exact requested workload and any explicitly named model; then open or fetch the relevant official page. For current or latest family guidance, use `https://developers.openai.com/api/docs/guides/latest-model`.
2. Use any available official documentation or first-party-domain search. Read the actual source; do not make a recommendation from a search snippet, guessed default, or bundled snapshot.
3. Match the documented model to the user's requested modality, quality, latency, cost, context, and workload. Distinguish flagship, balanced, high-throughput, coding, audio, image, or other specialized roles only when the fetched current documentation supports the distinction.
4. Preserve an explicitly requested model or existing target. Cite the current official page and state uncertainty about availability, pricing, limits, or account access.

Pure model selection does not require migration metadata. **Do not run the resolver.**

Read `references/latest-model.md` only when fetched current official sources cannot answer the question. Disclose that bundled fallback guidance was used and may be outdated.
