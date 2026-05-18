---
source_type: 'github'
source_area: 'github_docs'
source_url: 'https://raw.githubusercontent.com/openai/codex/main/docs/agents_md.md'
source_etag: 'W/"06f117ede2b232d44da360094b1416dbe24a93f8364a56928937f83d5815a283"'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0"]
---

# AGENTS.md

For information about AGENTS.md, see [this documentation](https://developers.openai.com/codex/guides/agents-md).

## Hierarchical agents message

When the `child_agents_md` feature flag is enabled (via `[features]` in `config.toml`), Codex appends additional guidance about AGENTS.md scope and precedence to the user instructions message and emits that message even when no AGENTS.md is present.
