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

python - "$before" "$after_second" <<'PY'
import sys
from pathlib import Path

before_path = Path(sys.argv[1])
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

before = parse_porcelain_z(before_path.read_bytes())
after = parse_porcelain_z(after_path.read_bytes())
introduced = sorted(after - before)

allowed_prefixes = ("docs/", "weekly/")
bad = [path for path in introduced if not path.startswith(allowed_prefixes)]

if bad:
    print("Changed-file scope violation. New dirty paths outside docs/ or weekly/:")
    for path in bad:
        print(f"- {path}")
    sys.exit(1)

print("Validation passed: idempotent sync and expected changed-file scope.")
PY
