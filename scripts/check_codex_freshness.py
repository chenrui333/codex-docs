#!/usr/bin/env python3
"""Compare the canonical Codex mirror with the latest stable upstream release."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict

import requests

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "docs" / "freshness.json"
SYNC_SUMMARY = ROOT / "docs" / "sync_summary.json"
SOURCE_COVERAGE = ROOT / "docs" / "source_coverage.json"
FEATURE_LIFECYCLE = ROOT / "docs" / "feature-flags" / "lifecycle.json"
REPOSITORY_API = "https://api.github.com/repos/openai/codex"
DEFAULT_GRACE_HOURS = 12.0
USER_AGENT = "codex-docs-freshness/1 (+https://github.com/chenrui333/codex-docs)"
VERSION_PATTERN = re.compile(r"(?<!\d)(\d+\.\d+\.\d+)(?!\d)")
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}")


class FreshnessError(RuntimeError):
    """Raised when freshness inputs are unavailable or malformed."""


def parse_version(value: str) -> str:
    match = VERSION_PATTERN.search(value)
    if not match:
        raise FreshnessError(f"Could not parse a stable semantic version from {value!r}")
    return match.group(1)


def version_tuple(value: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in parse_version(value).split("."))


def load_json(path: Path) -> Dict[str, object]:
    try:
        payload = json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise FreshnessError(f"Required freshness input is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FreshnessError(f"Required freshness input is invalid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise FreshnessError(f"Required freshness input is not an object: {path}")
    return payload


def github_headers() -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_json(url: str) -> Dict[str, object]:
    response = requests.get(url, headers=github_headers(), timeout=30)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise FreshnessError(f"Unexpected JSON response from {url}")
    return payload


def validate_commit(value: object, source: str) -> str:
    commit = str(value or "").lower()
    if not COMMIT_PATTERN.fullmatch(commit):
        raise FreshnessError(f"{source} did not resolve to a full commit SHA")
    return commit


def resolve_tag_commit(
    tag: str,
    fetch_json_fn: Callable[[str], Dict[str, object]] = fetch_json,
) -> str:
    payload = fetch_json_fn(f"{REPOSITORY_API}/git/ref/tags/{tag}")
    for _ in range(5):
        target = payload.get("object")
        if not isinstance(target, dict):
            raise FreshnessError(f"Tag {tag} did not contain an object target")
        target_type = target.get("type")
        if target_type == "commit":
            return validate_commit(target.get("sha"), f"Tag {tag}")
        if target_type != "tag":
            raise FreshnessError(
                f"Tag {tag} resolved to unsupported object type {target_type!r}"
            )
        target_url = target.get("url")
        if not isinstance(target_url, str) or not target_url.startswith(
            f"{REPOSITORY_API}/git/tags/"
        ):
            raise FreshnessError(f"Tag {tag} contained an invalid tag object URL")
        payload = fetch_json_fn(target_url)
    raise FreshnessError(f"Tag {tag} exceeded the tag dereference limit")


def latest_stable_release(
    fetch_json_fn: Callable[[str], Dict[str, object]] = fetch_json,
) -> Dict[str, object]:
    release = fetch_json_fn(f"{REPOSITORY_API}/releases/latest")
    if release.get("draft") or release.get("prerelease"):
        raise FreshnessError("GitHub latest release unexpectedly returned a non-stable release")
    tag = str(release.get("tag_name", ""))
    version = parse_version(tag)
    published_at = str(release.get("published_at", ""))
    if not published_at:
        raise FreshnessError(f"Stable release {tag} has no published_at timestamp")
    return {
        "version": version,
        "tag": tag,
        "published_at": published_at,
        "source_commit": resolve_tag_commit(tag, fetch_json_fn),
        "url": str(release.get("html_url", "")),
        "provenance": "github_release_metadata",
    }


def installed_cli_version() -> Dict[str, str]:
    environment = dict(os.environ)
    for key in ("GH_TOKEN", "GITHUB_TOKEN", "OPENAI_API_KEY"):
        environment.pop(key, None)
    result = subprocess.run(
        ["codex", "--version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
        env=environment,
    )
    if result.returncode != 0:
        raise FreshnessError(
            f"codex --version failed with exit code {result.returncode}: {result.stderr.strip()}"
        )
    raw = result.stdout.strip()
    return {
        "version": parse_version(raw),
        "version_raw": raw,
        "command": "codex --version",
        "provenance": "installed_cli_observation",
    }


def parse_timestamp(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise FreshnessError(f"Invalid timestamp {value!r}") from exc


def comparison_status(
    observed: str,
    expected: str,
    *,
    grace_elapsed: bool,
) -> str:
    if observed == expected:
        return "pass"
    if version_tuple(observed) > version_tuple(expected):
        return "fail"
    return "fail" if grace_elapsed else "warning"


def make_check(
    name: str,
    observed: str,
    expected: str,
    *,
    grace_elapsed: bool,
) -> Dict[str, object]:
    return {
        "name": name,
        "status": comparison_status(
            observed, expected, grace_elapsed=grace_elapsed
        ),
        "observed": observed,
        "expected": expected,
    }


def build_report(
    *,
    latest_release: Dict[str, object],
    installed_cli: Dict[str, str],
    summary: Dict[str, object],
    coverage: Dict[str, object],
    feature_snapshot: Dict[str, object],
    now: datetime,
    grace_hours: float,
    resolve_tag_commit_fn: Callable[[str], str] = resolve_tag_commit,
) -> Dict[str, object]:
    release_version = parse_version(str(latest_release["version"]))
    release_published = parse_timestamp(str(latest_release["published_at"]))
    grace_elapsed = (now.astimezone(timezone.utc) - release_published).total_seconds() >= (
        grace_hours * 3600
    )

    source_metadata = summary.get("source_metadata", {})
    coverage_cli = coverage.get("codex_cli", {})
    if not isinstance(source_metadata, dict) or not isinstance(coverage_cli, dict):
        raise FreshnessError("Sync reports do not contain Codex CLI source metadata")
    summary_version = parse_version(str(source_metadata.get("codex_cli_version", "")))
    coverage_version = parse_version(str(coverage_cli.get("version", "")))
    feature_raw = str(feature_snapshot.get("codex_cli_version", ""))
    feature_version = parse_version(feature_raw)
    feature_ref = str(feature_snapshot.get("source_ref", ""))
    feature_commit = validate_commit(
        feature_snapshot.get("source_commit"), "Feature snapshot"
    )

    checks = [
        make_check(
            "installed_cli_matches_latest_stable",
            installed_cli["version"],
            release_version,
            grace_elapsed=grace_elapsed,
        ),
        make_check(
            "canonical_mirror_matches_latest_stable",
            summary_version,
            release_version,
            grace_elapsed=grace_elapsed,
        ),
        make_check(
            "source_coverage_matches_latest_stable",
            coverage_version,
            release_version,
            grace_elapsed=grace_elapsed,
        ),
        make_check(
            "feature_snapshot_matches_latest_stable",
            feature_version,
            release_version,
            grace_elapsed=grace_elapsed,
        ),
    ]
    expected_feature_commit = resolve_tag_commit_fn(feature_ref)
    checks.append(
        {
            "name": "feature_snapshot_commit_matches_release_tag",
            "status": "pass" if feature_commit == expected_feature_commit else "fail",
            "observed": feature_commit,
            "expected": expected_feature_commit,
        }
    )

    statuses = {str(check["status"]) for check in checks}
    overall = "stale" if "fail" in statuses else "warning" if "warning" in statuses else "fresh"
    return {
        "schema_version": 1,
        "status": overall,
        "release_grace_hours": grace_hours,
        "release_grace_elapsed": grace_elapsed,
        "latest_stable_release": latest_release,
        "installed_cli": installed_cli,
        "canonical_mirror": {
            "version": summary_version,
            "coverage_version": coverage_version,
            "last_successful_full_sync_at": str(summary.get("generated_at", "")),
            "provenance": "generated_sync_metadata",
        },
        "feature_flag_snapshot": {
            "version": feature_version,
            "version_raw": feature_raw,
            "source_ref": feature_ref,
            "source_commit": feature_commit,
            "provenance": "release_matched_cli_and_source_snapshot",
        },
        "checks": checks,
    }


def write_if_changed(path: Path, payload: Dict[str, object]) -> None:
    content = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text() == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--grace-hours",
        type=float,
        default=float(os.environ.get("CODEX_FRESHNESS_GRACE_HOURS", DEFAULT_GRACE_HOURS)),
    )
    args = parser.parse_args(argv)

    try:
        release = latest_stable_release()
        report = build_report(
            latest_release=release,
            installed_cli=installed_cli_version(),
            summary=load_json(SYNC_SUMMARY),
            coverage=load_json(SOURCE_COVERAGE),
            feature_snapshot=load_json(FEATURE_LIFECYCLE),
            now=datetime.now(timezone.utc),
            grace_hours=max(args.grace_hours, 0.0),
        )
        write_if_changed(args.output, report)
    except (FreshnessError, OSError, requests.RequestException) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(
        f"Codex freshness: {report['status']} "
        f"(mirror={report['canonical_mirror']['version']}, "
        f"latest={report['latest_stable_release']['version']})"
    )
    if args.strict and report["status"] == "stale":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
