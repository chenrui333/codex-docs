---
source_type: 'codex_cli_system_skill'
source_area: 'system_skill_openai_docs'
source_url: 'codex-cli://skills/.system/openai-docs/references/latest-model.md'
source_kind: 'installed_codex_cli'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0", "0.144.0", "0.144.1", "0.144.3", "0.144.4", "0.144.5", "0.144.6", "0.145.0", "0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2", "0.153.3", "0.153.4", "0.154.0", "0.155.0", "0.155.1", "0.156.0", "0.156.1", "0.157.0", "0.157.1", "0.158.0", "0.159.0", "0.159.1", "0.159.2", "0.159.3", "0.160.0", "0.160.1", "0.161.0", "0.162.0", "0.162.1", "0.163.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0", "codex-cli 0.144.0", "codex-cli 0.144.1", "codex-cli 0.144.3", "codex-cli 0.144.4", "codex-cli 0.144.5", "codex-cli 0.144.6", "codex-cli 0.145.0", "codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2", "codex-cli 0.153.3", "codex-cli 0.153.4", "codex-cli 0.154.0", "codex-cli 0.155.0", "codex-cli 0.155.1", "codex-cli 0.156.0", "codex-cli 0.156.1", "codex-cli 0.157.0", "codex-cli 0.157.1", "codex-cli 0.158.0", "codex-cli 0.159.0", "codex-cli 0.159.1", "codex-cli 0.159.2", "codex-cli 0.159.3", "codex-cli 0.160.0", "codex-cli 0.160.1", "codex-cli 0.161.0", "codex-cli 0.162.0", "codex-cli 0.162.1", "codex-cli 0.163.0"]
codex_cli_release_ref: 'rust-v0.163.0'
codex_cli_source_commit: '83086188ae0614bd882818ff1aa23f3194962012'
---

# Latest model fallback

This is a compact, non-authoritative fallback, not a source for current availability, prices, aliases, or defaults. First search for and fetch current official model guidance at `https://developers.openai.com/api/docs/guides/latest-model` and the relevant official model page. The fetched official documentation wins if this snapshot has drifted. Disclose any use of this fallback.

## Source model descriptions

| Model ID | Official source description |
| --- | --- |
| `gpt-6-astra` | For the most demanding reasoning, coding, and professional work. |
| `gpt-6.1-sol` | Near-Astra performance for complex work at a lower cost. |
| `gpt-6-luna` | Strong performance for focused, high-volume tasks. |

Use `https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#migration-quickstart` for an actual GPT-6 migration and `https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#prompting-best-practices` for requested GPT-6 prompting. Open and read the relevant page before recommending a request shape, reasoning setting, endpoint, tool behavior, or migration.

Verify GPT-6 Pro against current official Responses and model documentation before describing model IDs, reasoning modes, request parameters, or account availability; do not invent a separate `gpt-6-pro` model slug.
