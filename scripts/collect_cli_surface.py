#!/usr/bin/env python3
"""Collect help only, in an isolated home, for a workflow platform artifact."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

import requests

if __package__:
    from . import cli_observations
    from . import fetch_codex_docs as sync
else:
    import cli_observations
    import fetch_codex_docs as sync


def collect() -> dict:
    binary = shutil.which("codex")
    if not binary:
        raise RuntimeError("CLI is not installed")
    with tempfile.TemporaryDirectory(prefix="cli-observation-") as directory:
        root = Path(directory)
        home, workspace = root / "home", root / "workspace"
        (home / ".codex").mkdir(parents=True)
        workspace.mkdir()
        environment = sync.isolated_codex_subprocess_env()
        environment.update(HOME=str(home), CODEX_HOME=str(home / ".codex"), NO_COLOR="1", TZ="UTC")
        raw = sync.run_local_command([binary, "--version"], env=environment, cwd=workspace).strip()
        metadata = {"codex_cli_version": sync.parse_codex_cli_version(raw), "codex_cli_version_raw": raw}
        item = sync.build_cli_surface_snapshot(binary, environment, workspace, metadata)
        if sync.run_local_command([binary, "--version"], env=environment, cwd=workspace).strip() != raw:
            raise RuntimeError("Installed CLI changed during observation")
    _, metadata = sync.add_cli_release_provenance(requests.Session(), [], metadata)
    payload = json.loads(item.content)
    payload.update(source_ref=metadata["codex_cli_release_ref"], source_commit=metadata["codex_cli_source_commit"])
    return cli_observations.validate(payload)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    payload = collect()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    path = args.output_dir / f"{cli_observations.platform_key(payload)}.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
