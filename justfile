set shell := ["bash", "-ueo", "pipefail", "-c"]

actionlint_version := "v1.7.7"
python := env_var_or_default("CODEX_DOCS_PYTHON", "python3.14")

default:
    @just --list

setup:
    {{python}} -m venv .venv
    . .venv/bin/activate && python -m pip install -r scripts/requirements.txt -r scripts/requirements-dev.txt

lint: lint-actions lint-python

lint-actions:
    go run github.com/rhysd/actionlint/cmd/actionlint@{{actionlint_version}} .github/workflows/*.yml

lint-python:
    . .venv/bin/activate && ruff check scripts tests

test: test-python test-node

test-python:
    . .venv/bin/activate && coverage erase
    . .venv/bin/activate && coverage run -m unittest discover -s tests -v
    . .venv/bin/activate && coverage report

test-node:
    node --test tests/*.cjs

sync:
    . .venv/bin/activate && python scripts/fetch_codex_docs.py
    . .venv/bin/activate && python scripts/check_codex_freshness.py

freshness:
    . .venv/bin/activate && python scripts/check_codex_freshness.py

check:
    ./scripts/validate_sync.sh

check-strict:
    VALIDATE_STRICT_SYNC=1 ./scripts/validate_sync.sh

feature-flags:
    {{python}} scripts/snapshot_feature_flags.py

check-feature-flags:
    {{python}} scripts/snapshot_feature_flags.py
    git diff --exit-code -- docs/feature-flags/
