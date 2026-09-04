---
source_type: 'codex_cli_system_skill'
source_area: 'system_skill_openai_docs'
source_url: 'codex-cli://skills/.system/openai-docs/references/latest-model.md'
source_kind: 'installed_codex_cli'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0", "0.144.0", "0.144.1", "0.144.3", "0.144.4", "0.144.5", "0.144.6", "0.145.0", "0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0", "codex-cli 0.144.0", "codex-cli 0.144.1", "codex-cli 0.144.3", "codex-cli 0.144.4", "codex-cli 0.144.5", "codex-cli 0.144.6", "codex-cli 0.145.0", "codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2"]
codex_cli_release_ref: 'rust-v0.153.2'
codex_cli_source_commit: '657a993cbee87acf52d14b758ce49dbd46d1b8eb'
---

# Latest model fallback

This is a compact, non-authoritative fallback, not a source for current availability, prices, aliases, or defaults. First search for and fetch current official model guidance at `https://developers.openai.com/api/docs/guides/latest-model` and the relevant official model page. The fetched official documentation wins if this snapshot has drifted. Disclose any use of this fallback.

## GPT-5.6 family

| Model ID | Documented workload to verify against the current model page |
| --- | --- |
| `gpt-5.6` | GPT-5.6 family alias; verify its currently documented routing and availability. |
| `gpt-5.6-sol` | Quality-first flagship, reasoning, and difficult coding work. |
| `gpt-5.6-terra` | Balanced quality, latency, and cost. |
| `gpt-5.6-luna` | High-throughput, lower-latency work. |

Use `https://developers.openai.com/api/docs/guides/upgrading-to-gpt-5p6-sol` for an actual GPT-5.6 migration and `https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6` for requested GPT-5.6 prompting. Open and read the relevant page before recommending a request shape, reasoning setting, endpoint, tool behavior, or migration.

## Explicitly requested existing models

| Model ID | Boundary |
| --- | --- |
| `gpt-4.1` | Preserve only when the user explicitly requests this model or existing migration target; search and fetch its own current official guide. |
| `gpt-5.4` | Preserve only when the user explicitly requests this model or existing migration target; search and fetch its own current official guide. |

Do not promote a legacy model as the current default, substitute it into an unrelated task, or replace an explicitly requested legacy target with GPT-5.6. Recommend a specialized image, audio, realtime, coding, moderation, or embedding model only after verifying the requested modality against current official documentation.

Verify GPT-5.6 Pro against current official Responses and model documentation before describing model IDs, reasoning modes, request parameters, or account availability; do not invent a separate `gpt-5.6-pro` model slug.
