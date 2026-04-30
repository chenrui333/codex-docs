---
source_type: 'github'
source_area: 'github_cli'
source_url: 'https://raw.githubusercontent.com/openai/codex/main/codex-cli/scripts/README.md'
source_etag: 'W/"fa7dd93991ef5360685f582a0924b65861f981e38d6525dcbabf49036800605a"'
codex_cli_versions: ["0.125.0", "0.128.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0"]
---

# npm releases

Use the staging helper in the repo root to generate npm tarballs for a release. For
example, to stage the CLI, responses proxy, and SDK packages for version `0.6.0`:

```bash
./scripts/stage_npm_packages.py \
  --release-version 0.6.0 \
  --package codex \
  --package codex-responses-api-proxy \
  --package codex-sdk
```

This downloads the native artifacts once, hydrates `vendor/` for each package, and writes
tarballs to `dist/npm/`.

When `--package codex` is provided, the staging helper builds the lightweight
`@openai/codex` meta package plus all platform-native `@openai/codex` variants
that are later published under platform-specific dist-tags.

If you need to invoke `build_npm_package.py` directly, run
`codex-cli/scripts/install_native_deps.py` first and pass `--vendor-src` pointing to the
directory that contains the populated `vendor/` tree.
