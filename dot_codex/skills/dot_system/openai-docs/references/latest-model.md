---
source_type: 'codex_cli_system_skill'
source_area: 'system_skill_openai_docs'
source_url: 'codex-cli://skills/.system/openai-docs/references/latest-model.md'
source_kind: 'installed_codex_cli'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0", "0.144.0", "0.144.1", "0.144.3", "0.144.4", "0.144.5", "0.144.6", "0.145.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0", "codex-cli 0.144.0", "codex-cli 0.144.1", "codex-cli 0.144.3", "codex-cli 0.144.4", "codex-cli 0.144.5", "codex-cli 0.144.6", "codex-cli 0.145.0"]
---

# Latest model guide

This file is a curated helper. Every recommendation here must be verified against current OpenAI docs before it is repeated to a user.

## Current model map

| Model ID | Use for |
| --- | --- |
| `gpt-5.6` | Latest/default GPT-5.6 alias; routes to Sol |
| `gpt-5.6-sol` | Flagship GPT-5.6 tier for hardest quality-first, coding, and reasoning workflows |
| `gpt-5.6-terra` | Mini-like GPT-5.6 tier for balanced cost, latency, and quality |
| `gpt-5.6-luna` | Nano-like GPT-5.6 tier for high-throughput, simple, or strict-latency tasks |
| `gpt-5.5` | Previous default text and reasoning model; use for existing GPT-5.5 integrations |
| `gpt-5.4` | Older default text and reasoning model; use for existing GPT-5.4 integrations |
| `gpt-5.4-mini` | Older lower-cost testing and lighter production workflows |
| `gpt-5.4-nano` | Older high-throughput simple tasks and classification |
| `gpt-4.1-mini` | Cheaper no-reasoning text |
| `gpt-4.1-nano` | Fastest and cheapest no-reasoning text |
| `gpt-5.3-codex` | Agentic coding, code editing, and tool-heavy coding workflows |
| `gpt-5.1-codex-mini` | Cheaper coding workflows |
| `gpt-image-2` | Best image generation and edit quality |
| `gpt-image-1.5` | Less expensive image generation and edit quality |
| `gpt-image-1-mini` | Cost-optimized image generation |
| `gpt-4o-mini-tts` | Text-to-speech |
| `gpt-4o-mini-transcribe` | Speech-to-text, fast and cost-efficient |
| `gpt-realtime-1.5` | Realtime voice and multimodal sessions |
| `gpt-realtime-mini` | Cheaper realtime sessions |
| `gpt-audio` | Chat Completions audio input and output |
| `gpt-audio-mini` | Cheaper Chat Completions audio workflows |
| `sora-2` | Faster iteration and draft video generation |
| `sora-2-pro` | Higher-quality production video |
| `omni-moderation-latest` | Text and image moderation |
| `text-embedding-3-large` | Higher-quality retrieval embeddings; default in this skill because no best-specific row exists |
| `text-embedding-3-small` | Lower-cost embeddings |

## Maintenance notes

- GPT-5.6 Pro is a Responses reasoning mode on the base model, not a separate `gpt-5.6-pro` slug. Verify the live model guide before recommending its request shape.
- This file will drift unless it is periodically re-verified against current OpenAI docs.
- If this file conflicts with current docs, the docs win.
