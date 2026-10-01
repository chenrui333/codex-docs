#!/usr/bin/env python3
"""Detect whether a direct-push writer was generated from stale main."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def fetch_remote_head(remote: str, branch: str) -> str:
    run_git(
        [
            "fetch",
            "--no-tags",
            remote,
            f"refs/heads/{branch}:refs/remotes/{remote}/{branch}",
        ]
    )
    return run_git(["rev-parse", f"refs/remotes/{remote}/{branch}"])


def is_stale(expected_sha: str, remote_sha: str) -> bool:
    return expected_sha.strip().lower() != remote_sha.strip().lower()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", default=os.environ.get("GITHUB_SHA", ""))
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--branch", default="main")
    args = parser.parse_args(argv)

    expected_sha = args.expected.strip().lower()
    if not expected_sha:
        print("error: an expected writer SHA is required", file=sys.stderr)
        return 2

    try:
        remote_sha = fetch_remote_head(args.remote, args.branch).lower()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    stale = is_stale(expected_sha, remote_sha)
    print(f"expected_sha={expected_sha}")
    print(f"remote_sha={remote_sha}")
    print(f"stale={str(stale).lower()}")
    if stale:
        print(
            "::notice::Skipping direct push because origin/main moved during generation; "
            "the next scheduled run will regenerate from the new head.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
