---
source_type: 'github'
source_area: 'github_docs'
source_url: 'https://raw.githubusercontent.com/openai/codex/main/docs/config.md'
source_etag: 'W/"48dfe8612428c39649c5fe6adb86cd853ef07f1bc8dd185b67f86470f5293d45"'
codex_cli_versions: ["0.125.0", "0.128.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0"]
---

# Configuration

For basic configuration instructions, see [this documentation](https://developers.openai.com/codex/config-basic).

For advanced configuration instructions, see [this documentation](https://developers.openai.com/codex/config-advanced).

For a full configuration reference, see [this documentation](https://developers.openai.com/codex/config-reference).

## Commit attribution

Codex can add a [git trailer](https://git-scm.com/docs/git-interpret-trailers) to
generated commit messages so commits make Codex's involvement explicit. This
behavior is gated by the `codex_git_commit` feature flag; the top-level
`commit_attribution` setting is only used when that feature is enabled.

Add the following to `~/.codex/config.toml`:

```toml
commit_attribution = "Codex <noreply@openai.com>"

[features]
codex_git_commit = true
```

When enabled, Codex appends a `Co-authored-by:` trailer using the configured
attribution value. If `commit_attribution` is omitted, Codex uses
`Codex <noreply@openai.com>`. Set `commit_attribution = ""` to disable the
trailer while leaving the feature flag enabled.
