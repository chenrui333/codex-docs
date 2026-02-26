set shell := ["bash", "-ueo", "pipefail", "-c"]

default:
    @just --list

setup:
    python3 -m venv .venv
    . .venv/bin/activate && pip install -r scripts/requirements.txt

sync:
    . .venv/bin/activate && python scripts/fetch_codex_docs.py

check:
    ./scripts/validate_sync.sh

feature-flags:
    python3 scripts/snapshot_feature_flags.py

check-feature-flags:
    python3 scripts/snapshot_feature_flags.py
    git diff --exit-code -- docs/feature-flags/
