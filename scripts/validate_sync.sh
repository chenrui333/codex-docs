#!/usr/bin/env bash
set -euo pipefail

if [[ ! -e .git ]]; then
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

before="$tmpdir/tree-before.json"
after_first="$tmpdir/tree-after-first.json"
after_second="$tmpdir/tree-after-second.json"

content_snapshot() {
  python3 - "$1" <<'PY'
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


root = Path.cwd()
output = Path(sys.argv[1])
entries = {}

for directory, directory_names, file_names in os.walk(root):
    directory_names[:] = sorted(name for name in directory_names if name not in {".git", ".venv"})
    for name in sorted(file_names):
        path = Path(directory) / name
        rel = path.relative_to(root)
        if rel.parts[0] in {".git", ".venv"}:
            continue
        mode = stat.S_IMODE(path.lstat().st_mode)
        if path.is_symlink():
            entries[str(rel)] = {"mode": mode, "symlink": str(path.readlink())}
            continue

        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        entries[str(rel)] = {"mode": mode, "sha256": digest.hexdigest()}

output.write_text(json.dumps(entries, sort_keys=True))
PY
}

content_snapshot "$before"

. .venv/bin/activate
python scripts/fetch_codex_docs.py
content_snapshot "$after_first"

python scripts/fetch_codex_docs.py
content_snapshot "$after_second"

if ! cmp -s "$after_first" "$after_second"; then
  echo "Non-idempotent output: second sync changed repository state."
  python3 - "$after_first" "$after_second" <<'PY'
import json
import sys
from pathlib import Path


first = json.loads(Path(sys.argv[1]).read_text())
second = json.loads(Path(sys.argv[2]).read_text())
for path in sorted(set(first) | set(second)):
    if first.get(path) != second.get(path):
        print(f"- {path}")
PY
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
import json
import sys
from pathlib import Path

before = json.loads(Path(sys.argv[1]).read_text())
after = json.loads(Path(sys.argv[2]).read_text())
changed = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))

allowed_prefixes = ("docs/", "dot_codex/", "system_prompts/", "weekly/")
bad = [path for path in changed if not path.startswith(allowed_prefixes)]

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
