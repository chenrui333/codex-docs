#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .git ]]; then
  echo "Run this script from the repository root."
  exit 1
fi

if [[ ! -d .venv ]]; then
  echo "Missing .venv. Run: just setup"
  exit 1
fi

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

strict_sync="${VALIDATE_STRICT_SYNC:-0}"
if [[ "$strict_sync" == "1" ]]; then
  export CODEX_DOCS_STRICT_SYNC=1
fi

before="$tmpdir/status-before.bin"
after_first="$tmpdir/status-after-first.bin"
after_second="$tmpdir/status-after-second.bin"

status_snapshot() {
  git status --porcelain=v1 -z > "$1"
}

status_snapshot "$before"

. .venv/bin/activate
python scripts/fetch_codex_docs.py
status_snapshot "$after_first"

python scripts/fetch_codex_docs.py
status_snapshot "$after_second"

if ! cmp -s "$after_first" "$after_second"; then
  echo "Non-idempotent output: second sync changed repository state."
  echo "Current status:"
  git status --short
  exit 1
fi

if [[ "$strict_sync" == "1" ]]; then
  python - <<'PY'
import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.exists():
        print(f"Missing required strict sync report: {path}")
        sys.exit(1)
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        print(f"Unexpected strict sync report shape: {path}")
        sys.exit(1)
    return payload


def failure_count(value: object) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 1 if value else 0


summary = load_json(Path("docs/sync_summary.json"))
coverage = load_json(Path("docs/source_coverage.json"))
coverage_sync = coverage.get("sync", {})
if not isinstance(coverage_sync, dict):
    coverage_sync = {}

summary_failures = failure_count(summary.get("failure_count"))
coverage_failures = failure_count(coverage_sync.get("failure_count"))

if summary_failures or coverage_failures:
    print(
        "Strict sync validation failed: "
        f"sync_summary failure_count={summary_failures}, "
        f"source_coverage sync.failure_count={coverage_failures}."
    )
    sys.exit(1)

print("Strict sync validation passed: no recorded source failures.")
PY
fi

python - "$before" "$after_second" <<'PY'
import sys
from pathlib import Path

after_path = Path(sys.argv[2])


def parse_porcelain_z(blob: bytes) -> set[str]:
    entries = set()
    parts = blob.split(b"\0")
    i = 0
    while i < len(parts):
        part = parts[i]
        if not part:
            i += 1
            continue

        text = part.decode("utf-8", errors="replace")
        status = text[:2]
        path = text[3:] if len(text) >= 4 else ""

        # In -z mode, rename/copy stores old path in this record and new path
        # in the following NUL-delimited entry.
        if status and (status[0] in "RC" or status[1] in "RC"):
            if i + 1 < len(parts) and parts[i + 1]:
                path = parts[i + 1].decode("utf-8", errors="replace")
                i += 1

        if path:
            entries.add(path)
        i += 1

    return entries

after = parse_porcelain_z(after_path.read_bytes())
dirty = sorted(after)

allowed_prefixes = ("docs/", "dot_codex/", "system_prompts/", "weekly/")
bad = [path for path in dirty if not path.startswith(allowed_prefixes)]

if bad:
    print(
        "Changed-file scope violation. Dirty paths outside docs/, dot_codex/, "
        "system_prompts/, or weekly/:"
    )
    for path in bad:
        print(f"- {path}")
    sys.exit(1)

print("Validation passed: idempotent sync and expected changed-file scope.")
PY
