# Contributing

This repository mirrors upstream documentation and records release-matched CLI
observations. Contributions should improve the generators, validation, or the
usefulness of those records.

Read [AGENTS.md](AGENTS.md) for the full generated-file boundaries and transaction
invariants. Fix the responsible generator instead of hand-editing mirrored files.
Repository-authored documentation, tests, and workflow helpers are maintained here;
upstream prose and formatting remain upstream-owned.

## Local checks

Use Python 3.14, Node.js 24, Go, and `just`:

```sh
just setup
just lint
just test
git diff --check
```

`just lint` includes offline checks of repository-authored Markdown links,
Renovate JSON syntax/basic shape, and VERSION. It does not crawl upstream links
or lint the mirrored Markdown corpus.

For synchronizer changes, run `just check-strict`: it generates twice and checks
freshness, idempotence, and changed-file scope. Keep other repository files unchanged
while it runs. Report upstream outages honestly and run fixture tests; do not weaken
strict checks. `just sync-release` advances release state from a verified existing web
mirror without claiming current web health.

For feature snapshots, run `just feature-flags`, inspect and stage the intended output,
then run `just check-feature-flags`. Preserve the release tag, source commit, and
observation platform. See [README.md](README.md) for the other sync commands.

## Pull requests

Keep changes scoped. Explain behavior and provenance/freshness implications. Include
generated changes only when produced by the responsible generator; review the scope,
manifest hashes, and repeated-run stability. Use fixtures for failure cases instead
of live-network unit tests.

Sign off every commit with `git commit -s` to certify the
[Developer Certificate of Origin](https://developercertificate.org/). Never put tokens,
credentials, local private paths, sessions, history, or real user Codex state in
fixtures, generated output, logs, or PRs.
