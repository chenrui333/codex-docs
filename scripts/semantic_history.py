"""Append semantic transactions without losing earlier events on the same day."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def record_event(path: Path, payload: dict, *, observed_at: str, legacy_report: str = "") -> dict:
    if path.exists():
        ledger = json.loads(path.read_text())
        if ledger.get("schema_version") != 1 or not isinstance(ledger.get("events"), list):
            raise ValueError("Invalid semantic history ledger")
    else:
        ledger = {"schema_version": 1, "events": []}
        if legacy_report:
            ledger["legacy_report"] = legacy_report
    events = ledger["events"]
    # Retrying an identical transaction adds neither a timestamp nor an event.
    if events and events[-1]["changes"] == payload:
        return ledger
    previous_id = events[-1]["id"] if events else ""
    identity = json.dumps({"previous_id": previous_id, "changes": payload}, sort_keys=True)
    event = {
        "id": hashlib.sha256(identity.encode()).hexdigest(),
        "previous_id": previous_id,
        "observed_at": observed_at,
        "changes": payload,
    }
    events.append(event)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    return ledger
