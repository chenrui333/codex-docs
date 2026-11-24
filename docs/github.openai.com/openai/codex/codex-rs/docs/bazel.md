---
source_type: 'github'
source_area: 'github_rust'
source_url: 'https://raw.githubusercontent.com/openai/codex/3d86e43b075adeba2193ec5c22ac92f55afd82e6/codex-rs/docs/bazel.md'
source_etag: 'W/"ac2ce9854b4642f87b1eb54f7357d2a53029ea30532ef5e0ed5561b1b792abd8"'
upstream_source_ref: 'rust-v0.172.0'
upstream_source_commit: '3d86e43b075adeba2193ec5c22ac92f55afd82e6'
codex_cli_versions: ["0.125.0", "0.128.0", "0.129.0", "0.130.0", "0.131.0", "0.132.0", "0.133.0", "0.134.0", "0.135.0", "0.136.0", "0.137.0", "0.138.0", "0.139.0", "0.140.0", "0.141.0", "0.142.0", "0.142.1", "0.142.2", "0.142.3", "0.142.4", "0.142.5", "0.143.0", "0.144.0", "0.144.1", "0.144.3", "0.144.4", "0.144.5", "0.144.6", "0.145.0", "0.146.0", "0.146.1", "0.147.0", "0.148.0", "0.149.0", "0.151.0", "0.152.0", "0.152.1", "0.153.0", "0.153.2", "0.153.3", "0.153.4", "0.154.0", "0.155.0", "0.155.1", "0.156.0", "0.156.1", "0.157.0", "0.157.1", "0.158.0", "0.159.0", "0.159.1", "0.159.2", "0.159.3", "0.160.0", "0.160.1", "0.161.0", "0.162.0", "0.162.1", "0.163.0", "0.164.0", "0.165.0", "0.166.0", "0.167.0", "0.167.1", "0.167.2", "0.168.0", "0.169.0", "0.169.1", "0.170.0", "0.171.0", "0.172.0"]
codex_cli_versions_raw: ["codex-cli 0.125.0", "codex-cli 0.128.0", "codex-cli 0.129.0", "codex-cli 0.130.0", "codex-cli 0.131.0", "codex-cli 0.132.0", "codex-cli 0.133.0", "codex-cli 0.134.0", "codex-cli 0.135.0", "codex-cli 0.136.0", "codex-cli 0.137.0", "codex-cli 0.138.0", "codex-cli 0.139.0", "codex-cli 0.140.0", "codex-cli 0.141.0", "codex-cli 0.142.0", "codex-cli 0.142.1", "codex-cli 0.142.2", "codex-cli 0.142.3", "codex-cli 0.142.4", "codex-cli 0.142.5", "codex-cli 0.143.0", "codex-cli 0.144.0", "codex-cli 0.144.1", "codex-cli 0.144.3", "codex-cli 0.144.4", "codex-cli 0.144.5", "codex-cli 0.144.6", "codex-cli 0.145.0", "codex-cli 0.146.0", "codex-cli 0.146.1", "codex-cli 0.147.0", "codex-cli 0.148.0", "codex-cli 0.149.0", "codex-cli 0.151.0", "codex-cli 0.152.0", "codex-cli 0.152.1", "codex-cli 0.153.0", "codex-cli 0.153.2", "codex-cli 0.153.3", "codex-cli 0.153.4", "codex-cli 0.154.0", "codex-cli 0.155.0", "codex-cli 0.155.1", "codex-cli 0.156.0", "codex-cli 0.156.1", "codex-cli 0.157.0", "codex-cli 0.157.1", "codex-cli 0.158.0", "codex-cli 0.159.0", "codex-cli 0.159.1", "codex-cli 0.159.2", "codex-cli 0.159.3", "codex-cli 0.160.0", "codex-cli 0.160.1", "codex-cli 0.161.0", "codex-cli 0.162.0", "codex-cli 0.162.1", "codex-cli 0.163.0", "codex-cli 0.164.0", "codex-cli 0.165.0", "codex-cli 0.166.0", "codex-cli 0.167.0", "codex-cli 0.167.1", "codex-cli 0.167.2", "codex-cli 0.168.0", "codex-cli 0.169.0", "codex-cli 0.169.1", "codex-cli 0.170.0", "codex-cli 0.171.0", "codex-cli 0.172.0"]
---

# Bazel in codex-rs

This repository uses Bazel to build the Rust workspace under `codex-rs`.
Cargo remains the source of truth for crates and features, while Bazel
provides hermetic builds, toolchains, and cross-platform artifacts.

As of 6/1/2026, this setup is still experimental as we stabilize it.

## High-level layout

- `../MODULE.bazel` defines Bazel dependencies and Rust toolchains.
- `rules_rs` imports third-party crates from `codex-rs/Cargo.toml` and
  `codex-rs/Cargo.lock` via `crate.from_cargo(...)` and exposes them under
  `@crates`.
- `../defs.bzl` provides `codex_rust_crate`, which wraps `rust_library`,
  `rust_binary`, and `rust_test` so Bazel targets line up with Cargo conventions.
  It provides a sane set of defaults that work for most first-party crates, but may
  need tweaks in some cases.
- Each crate in `codex-rs/*/BUILD.bazel` typically uses `codex_rust_crate` and
  makes some adjustments if the crate needs additional compile-time or runtime data,
  or other customizations.

## Running Bazel locally

The repository root `justfile` exposes the common Bazel entry points:

```bash
just bazel-test
just bazel-clippy
```

Ordinary local `bazel` and `just` invocations run locally. The checked-in
Bazel configuration does not define third-party remote cache or execution
endpoints.

## Evolving the setup

When you add or change Rust dependencies, update the Cargo.toml/Cargo.lock as normal.
Then refresh the Bzlmod lockfile from the repo root:

```bash
just bazel-lock-update
```

This runs `bazel mod deps --lockfile_mode=update` and updates `MODULE.bazel.lock` if needed.
Commit the lockfile changes along with your Cargo lockfile update.

To verify lockfile alignment locally (the same check CI runs), use:

```bash
just bazel-lock-check
```

In some cases, an upstream crate may need a patch or a `crate.annotation` in `../MODULE.bzl`
to have it build in Bazel's sandbox or make it cross-compilation-friendly. If you see issues,
feel free to ping zbarsky or mbolin.

When you add a new crate or binary:

1. Add it to the Cargo workspace as usual.
2. Create a `BUILD.bazel` that calls `codex_rust_crate` (see nearby crates for
   examples).
3. If a dependency needs special handling (compile/runtime data, additional binaries
   for integration tests, env vars, etc) you may need to adjust the parameters to
   `codex_rust_crate` to configure it.
   One common customization is setting `test_tags = ["no-sandbox]` to run the test
   unsandboxed. Prefer to avoid it, but it is necessary in some cases such as when the
   test itself uses Seatbelt (the sandbox does as well, and it cannot be nested).
   To limit the blast radius, consider isolating such tests to a separate crate.

If you see build issue and are not sure how to apply the proper customizations, feel free to ping zbarsky or mbolin.

## References

- Bazel overview: https://bazel.build/
- Bzlmod (module system): https://bazel.build/external/overview
- rules_rust: https://github.com/bazelbuild/rules_rust
- rules_rs: https://github.com/bazelbuild/rules_rs
