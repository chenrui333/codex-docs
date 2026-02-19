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
