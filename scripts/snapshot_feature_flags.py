#!/usr/bin/env python3
"""Generate Codex feature-flag lifecycle snapshots for this docs mirror."""

from __future__ import annotations

import hashlib
import json
import os
import platform as host_platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Sequence
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = ROOT / "docs"
OUTPUT_DIR = DOCS_ROOT / "feature-flags"
OUTPUT_JSON = OUTPUT_DIR / "lifecycle.json"
OUTPUT_MD = OUTPUT_DIR / "lifecycle.md"
CONFIG_BASIC_DOC = (
    DOCS_ROOT
    / "learn.chatgpt.com"
    / "docs"
    / "config-file"
    / "config-basic"
    / "index.md"
)
CONFIG_REFERENCE_DOC = (
    DOCS_ROOT
    / "learn.chatgpt.com"
    / "docs"
    / "config-file"
    / "config-reference"
    / "index.md"
)

OSS_REPOSITORY = "openai/codex"
OSS_REPOSITORY_API_URL = f"https://api.github.com/repos/{OSS_REPOSITORY}"
OSS_RAW_BASE_URL = f"https://raw.githubusercontent.com/{OSS_REPOSITORY}"
OSS_FEATURES_RS_PATH = "codex-rs/features/src/lib.rs"
OSS_CLIENT_RS_PATH = "codex-rs/core/src/client.rs"
FEATURE_SOURCE_COMMIT_ENV = "CODEX_FEATURE_SOURCE_COMMIT"
ACTIONABLE_STAGES = ("stable", "experimental")
COMMIT_SHA_PATTERN = re.compile(r"[0-9a-f]{40}")
COMMAND_TIMEOUT_SECONDS = 120.0
HTTP_USER_AGENT = "codex-docs-feature-lifecycle/0.1 (+https://github.com/chenrui333/codex-docs)"
FEATURE_LIFECYCLE_SOURCE_TYPE = "feature_flag_snapshot"
FEATURE_LIFECYCLE_SOURCE_AREA = "feature_flags"
FEATURE_LIFECYCLE_SOURCE_URL = "generated://feature-flags/lifecycle"
FEATURE_LIFECYCLE_SOURCE_KIND = "generated_feature_flag_lifecycle"
FRONTMATTER_METADATA_ORDER = (
    "source_type",
    "source_area",
    "source_url",
    "source_kind",
    "codex_cli_versions",
    "codex_cli_versions_raw",
)


class SnapshotError(RuntimeError):
    """Raised when feature snapshot generation cannot continue."""


def run_command(argv: List[str], env: Dict[str, str] | None = None) -> str:
    try:
        proc = subprocess.run(
            argv,
            check=False,
            text=True,
            capture_output=True,
            env=env,
            timeout=command_timeout_seconds(),
        )
    except subprocess.TimeoutExpired as exc:
        joined = " ".join(argv)
        raise SnapshotError(
            f"Command timed out after {command_timeout_seconds():g} seconds ({joined})."
        ) from exc
    if proc.returncode != 0:
        joined = " ".join(argv)
        raise SnapshotError(
            f"Command failed ({joined}):\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout.strip()


def command_timeout_seconds() -> float:
    raw = os.environ.get("CODEX_DOCS_COMMAND_TIMEOUT_SECONDS", "").strip()
    if not raw:
        return COMMAND_TIMEOUT_SECONDS
    try:
        return max(float(raw), 0.1)
    except ValueError as exc:
        raise SnapshotError(
            "CODEX_DOCS_COMMAND_TIMEOUT_SECONDS must be a number."
        ) from exc


def codex_subprocess_env(base: Dict[str, str] | None = None) -> Dict[str, str]:
    env = dict(os.environ if base is None else base)
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        env.pop(name, None)
    return env


def fetch_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": HTTP_USER_AGENT})
    with urlopen(req, timeout=30) as resp:  # noqa: S310 (trusted static URLs)
        return resp.read().decode("utf-8")


def fetch_json(url: str) -> Dict[str, object]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": HTTP_USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=30) as resp:  # noqa: S310 (trusted GitHub API URL)
        payload = json.loads(resp.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise SnapshotError(f"Unexpected JSON object from {url}")
    return payload


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_codex_cli_version(version_raw: str) -> str:
    match = re.search(r"\b(\d+\.\d+\.\d+(?:[-+][^\s]+)?)\b", version_raw)
    return match.group(1) if match else version_raw.strip()


def validate_commit_sha(value: str, *, source: str) -> str:
    normalized = value.strip().lower()
    if not COMMIT_SHA_PATTERN.fullmatch(normalized):
        raise SnapshotError(f"{source} must be a full 40-character commit SHA.")
    return normalized


def feature_source_ref(codex_version_raw: str) -> str:
    version = parse_codex_cli_version(codex_version_raw)
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        raise SnapshotError(
            f"Could not derive an openai/codex release tag from {codex_version_raw!r}."
        )
    return f"rust-v{version}"


def resolve_tag_commit(
    source_ref: str,
    fetch_json_fn: Callable[[str], Dict[str, object]] = fetch_json,
) -> str:
    payload = fetch_json_fn(f"{OSS_REPOSITORY_API_URL}/git/ref/tags/{source_ref}")
    for _ in range(5):
        target = payload.get("object")
        if not isinstance(target, dict):
            raise SnapshotError(f"Tag {source_ref} did not contain an object target.")
        target_type = target.get("type")
        if target_type == "commit":
            return validate_commit_sha(str(target.get("sha", "")), source=f"Tag {source_ref}")
        if target_type != "tag":
            raise SnapshotError(
                f"Tag {source_ref} resolved to unsupported object type {target_type!r}."
            )
        target_url = target.get("url")
        if not isinstance(target_url, str) or not target_url.startswith(
            f"{OSS_REPOSITORY_API_URL}/git/tags/"
        ):
            raise SnapshotError(f"Tag {source_ref} contained an invalid tag object URL.")
        payload = fetch_json_fn(target_url)
    raise SnapshotError(f"Tag {source_ref} exceeded the tag dereference limit.")


def resolve_feature_source(
    codex_version_raw: str,
    override_commit: str | None = None,
    fetch_json_fn: Callable[[str], Dict[str, object]] = fetch_json,
) -> tuple[str, str]:
    source_ref = feature_source_ref(codex_version_raw)
    validated_override = None
    if override_commit:
        validated_override = validate_commit_sha(
            override_commit, source=FEATURE_SOURCE_COMMIT_ENV
        )
    resolved_commit = resolve_tag_commit(source_ref, fetch_json_fn)
    if validated_override and validated_override != resolved_commit:
        raise SnapshotError(
            f"{FEATURE_SOURCE_COMMIT_ENV} does not match {source_ref}: "
            f"expected {resolved_commit}, received {validated_override}."
        )
    return source_ref, resolved_commit


def source_url(commit: str, path: str) -> str:
    return f"{OSS_RAW_BASE_URL}/{commit}/{path}"


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        if value[0] == '"':
            try:
                return str(json.loads(value))
            except json.JSONDecodeError:
                pass
        return value[1:-1]
    return value


def parse_frontmatter_block(block: str) -> Dict[str, object]:
    parsed: Dict[str, object] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if not key:
            continue
        stripped = value.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            try:
                parsed[key] = [str(item) for item in json.loads(stripped)]
                continue
            except json.JSONDecodeError:
                pass
        parsed[key] = strip_quotes(value)
    return parsed


def split_markdown_frontmatter(text: str) -> tuple[Dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    metadata = parse_frontmatter_block(text[4:end])
    body = text[end + len("\n---\n") :]
    return metadata, body.lstrip("\n")


def yaml_scalar(value: object) -> str:
    if isinstance(value, list):
        return json.dumps([str(item) for item in value], ensure_ascii=False)
    return "'" + str(value).replace("'", "''") + "'"


def format_frontmatter(metadata: Dict[str, object], body: str) -> str:
    ordered_keys = [key for key in FRONTMATTER_METADATA_ORDER if metadata.get(key)]
    ordered_keys.extend(key for key in sorted(metadata) if key not in ordered_keys and metadata.get(key))
    lines = ["---"]
    lines.extend(f"{key}: {yaml_scalar(metadata[key])}" for key in ordered_keys)
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.lstrip("\n")


def metadata_values(value: object) -> List[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str) and value:
        return [value]
    return []


def append_unique(values: Sequence[str], value: str) -> List[str]:
    result: List[str] = []
    for item in values:
        if item and item not in result:
            result.append(item)
    if value and value not in result:
        result.append(value)
    return result


def codex_version_history_metadata(
    existing_metadata: Dict[str, object],
    codex_version_raw: str,
) -> Dict[str, List[str]]:
    version = parse_codex_cli_version(codex_version_raw)
    versions = metadata_values(existing_metadata.get("codex_cli_versions"))
    versions = append_unique(versions, version)

    raw_versions = metadata_values(existing_metadata.get("codex_cli_versions_raw"))
    raw_versions = append_unique(raw_versions, codex_version_raw)

    history: Dict[str, List[str]] = {}
    if versions:
        history["codex_cli_versions"] = versions
    if raw_versions:
        history["codex_cli_versions_raw"] = raw_versions
    return history


def parse_features_list(raw: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for line in raw.splitlines():
        line = line.rstrip()
        if not line:
            continue
        parts = re.split(r"\s{2,}", line)
        if len(parts) != 3:
            raise SnapshotError(f"Unexpected `codex features list` row format: {line!r}")
        key, stage, enabled = parts
        if enabled not in {"true", "false"}:
            raise SnapshotError(f"Unexpected enabled value in row: {line!r}")
        rows.append(
            {
                "key": key,
                "stage": stage,
                "enabled": enabled == "true",
            }
        )
    if not rows:
        raise SnapshotError("`codex features list` returned no rows.")
    return rows


def group_missing_in_docs(
    cli_features: Sequence[Dict[str, object]], docs_keys: Sequence[str]
) -> tuple[List[str], List[str], Dict[str, List[str]]]:
    documented = set(docs_keys)
    grouped: Dict[str, List[str]] = {}
    for item in cli_features:
        key = str(item["key"])
        if key in documented:
            continue
        stage = str(item["stage"])
        grouped.setdefault(stage, []).append(key)

    ordered_grouped = {
        stage: sorted(grouped[stage]) for stage in sorted(grouped)
    }
    missing = sorted(key for keys in ordered_grouped.values() for key in keys)
    actionable = sorted(
        key
        for stage in ACTIONABLE_STAGES
        for key in ordered_grouped.get(stage, [])
    )
    return missing, actionable, ordered_grouped


def parse_config_basic_feature_metadata(path: Path) -> Dict[str, str]:
    if not path.exists():
        raise SnapshotError(f"Required mirrored config document is missing: {path}")
    text = path.read_text()
    section_match = re.search(
        r"### Common feature flags\s+(.*?)(?:\n### |\Z)",
        text,
        flags=re.DOTALL,
    )
    if not section_match:
        raise SnapshotError(
            f"Could not find the Common feature flags section in {path}"
        )
    section_lines = section_match.group(1).splitlines()

    def table_cells(line: str) -> List[str] | None:
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            return None
        return [
            cell.strip().replace(r"\|", "|")
            for cell in re.split(r"(?<!\\)\|", stripped[1:-1])
        ]

    header_index = None
    header: List[str] = []
    for index, line in enumerate(section_lines):
        cells = table_cells(line)
        if cells is None:
            continue
        normalized = [cell.casefold() for cell in cells]
        if "key" in normalized or "maturity" in normalized:
            if normalized.count("key") != 1 or normalized.count("maturity") != 1:
                raise SnapshotError(
                    f"Feature flag table in {path} must contain exactly one Key and Maturity column"
                )
            header_index = index
            header = normalized
            break
    if header_index is None:
        raise SnapshotError(
            f"Could not find Key and Maturity columns in the feature flag table in {path}"
        )

    separator_index = header_index + 1
    if separator_index >= len(section_lines):
        raise SnapshotError(f"Feature flag table in {path} is missing its separator row")
    separator = table_cells(section_lines[separator_index])
    if (
        separator is None
        or len(separator) != len(header)
        or not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in separator)
    ):
        raise SnapshotError(f"Feature flag table in {path} has an invalid separator row")

    key_column = header.index("key")
    maturity_column = header.index("maturity")
    metadata: Dict[str, str] = {}
    for line in section_lines[separator_index + 1 :]:
        cells = table_cells(line)
        if cells is None:
            if metadata:
                break
            continue
        if len(cells) != len(header):
            raise SnapshotError(f"Feature flag table in {path} has a malformed row: {line!r}")
        key_match = re.fullmatch(r"`([a-z0-9_]+)`", cells[key_column])
        if not key_match:
            raise SnapshotError(f"Feature flag table in {path} has an invalid key cell: {line!r}")
        key = key_match.group(1)
        maturity = cells[maturity_column].strip().lower()
        if not maturity:
            raise SnapshotError(f"Feature flag {key!r} in {path} has no maturity label")
        if key in metadata:
            raise SnapshotError(f"Feature flag table in {path} contains duplicate key {key!r}")
        metadata[key] = maturity
    if not metadata:
        raise SnapshotError(f"Parsed zero feature keys from {path}")
    return dict(sorted(metadata.items()))


def parse_config_basic_feature_keys(path: Path) -> List[str]:
    return list(parse_config_basic_feature_metadata(path))


def find_documentation_stage_mismatches(
    cli_features: Sequence[Dict[str, object]], documented_stages: Dict[str, str]
) -> List[Dict[str, str]]:
    mismatches: List[Dict[str, str]] = []
    for item in cli_features:
        key = str(item["key"])
        documentation_stage = documented_stages.get(key)
        if documentation_stage is None:
            continue
        cli_stage = str(item["stage"]).lower()
        if cli_stage != documentation_stage:
            mismatches.append(
                {
                    "key": key,
                    "cli_stage": cli_stage,
                    "documentation_stage": documentation_stage,
                }
            )
    return sorted(mismatches, key=lambda item: item["key"])


def parse_config_reference_feature_keys(path: Path) -> List[str]:
    if not path.exists():
        raise SnapshotError(f"Required mirrored config document is missing: {path}")
    text = path.read_text()
    keys = sorted(
        set(re.findall(r'^\s*key:\s*["\']features\.([a-z0-9_]+)["\']\s*,?$', text, re.MULTILINE))
    )
    if not keys:
        raise SnapshotError(f"Parsed zero feature keys from {path}")
    return keys


def documentation_source_metadata(
    path: Path, feature_keys: Sequence[str]
) -> Dict[str, object]:
    try:
        rel_path = path.relative_to(ROOT).as_posix()
    except ValueError:
        rel_path = path.as_posix()
    return {
        "path": rel_path,
        "sha256": sha256_text(path.read_text()),
        "parsed_feature_key_count": len(feature_keys),
    }


def iter_feature_spec_blocks(features_rs_text: str) -> Iterable[str]:
    start_token = "FeatureSpec {"
    idx = 0
    while True:
        start = features_rs_text.find(start_token, idx)
        if start == -1:
            return
        depth = 0
        end = None
        for pos in range(start, len(features_rs_text)):
            char = features_rs_text[pos]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = pos + 1
                    break
        if end is None:
            return
        yield features_rs_text[start:end]
        idx = end


def feature_behavior(stage: str, default_expr: str, comment: str) -> Dict[str, object]:
    removed = stage == "removed"
    effective = "unknown"
    if removed:
        normalized = comment.lower()
        if any("when " not in clause and re.search(
            r"always[- ](?:on|enabled)|behavior is always|now always", clause
        ) for clause in re.split(r"[.;]\s*", normalized)):
            effective = "always_on"
        elif "no-op" in normalized or "deleted" in normalized:
            effective = "no_op"
    elif stage != "unknown":
        effective = "platform_dependent" if "cfg!" in default_expr or "platform-dependent" in stage else "feature_gated"
    return {
        "default_enabled": {"true": True, "false": False}.get(default_expr),
        "configurable": None if stage == "unknown" or "platform-dependent" in stage else not removed,
        "compatibility_flag": removed,
        "effective_behavior": effective,
        **({"behavior_evidence": comment} if removed and comment else {}),
    }


def parse_feature_defaults_from_source(features_rs_text: str) -> Dict[str, Dict[str, object]]:
    parsed: Dict[str, Dict[str, object]] = {}
    variant_comments = {
        match.group(2): " ".join(re.findall(r"///\s*(.*)", match.group(1)))
        for match in re.finditer(r"((?:[ \t]*///[^\n]*\n)+)[ \t]*(\w+)\s*,", features_rs_text)
    }
    for block in iter_feature_spec_blocks(features_rs_text):
        key_match = re.search(r'key:\s*"([^"]+)"', block)
        if not key_match:
            continue
        key = key_match.group(1)
        default_match = re.search(r"default_enabled:\s*([^,\n]+)", block)
        stage_expr = block
        stage_match = re.search(r"stage:\s*(.*?)(?:\n\s*default_enabled:|\Z)", block, flags=re.DOTALL)
        if stage_match:
            stage_expr = stage_match.group(1)
        stage_matches = re.findall(r"Stage::([A-Za-z]+)", stage_expr)
        normalized_stage_values = sorted(
            {
                {
                    "UnderDevelopment": "under development",
                    "Experimental": "experimental",
                    "Stable": "stable",
                    "Deprecated": "deprecated",
                    "Removed": "removed",
                }.get(match, match.lower())
                for match in stage_matches
            }
        )
        if not normalized_stage_values:
            normalized_stage = "unknown"
        elif len(normalized_stage_values) == 1:
            normalized_stage = normalized_stage_values[0]
        else:
            normalized_stage = (
                f"{'/'.join(normalized_stage_values)} (platform-dependent)"
            )
        default_expr = default_match.group(1).strip() if default_match else "unknown"
        variant = re.search(r"id:\s*Feature::(\w+)", block)
        comment = variant_comments.get(variant.group(1), "") if variant else ""
        parsed[key] = {
            "default_enabled_expr": default_expr,
            "stage_from_source": normalized_stage,
            **feature_behavior(normalized_stage, default_expr, comment),
        }
    return parsed


def derive_websocket_precedence(client_rs_text: str) -> Dict[str, object]:
    v2_rule = "(_, true) => Some(ResponsesWebsocketVersion::V2)"
    v1_rule = "(true, false) => Some(ResponsesWebsocketVersion::V1)"
    none_rule = "(false, false) => None"
    detected = all(rule in client_rs_text for rule in (v2_rule, v1_rule, none_rule))

    header_v1_match = re.search(
        r'OPENAI_BETA_RESPONSES_WEBSOCKETS:\s*&str\s*=\s*"([^"]+)"', client_rs_text
    )
    header_v2_match = re.search(
        r'RESPONSES_WEBSOCKETS_V2_BETA_HEADER_VALUE:\s*&str\s*=\s*"([^"]+)"',
        client_rs_text,
    )

    return {
        "detected": detected,
        "rules": {
            "v2_precedence_rule": v2_rule,
            "v1_rule": v1_rule,
            "none_rule": none_rule,
        },
        "openai_beta_headers": {
            "responses_websockets": header_v1_match.group(1) if header_v1_match else "unknown",
            "responses_websockets_v2": header_v2_match.group(1) if header_v2_match else "unknown",
        },
    }


def render_markdown(
    codex_version: str,
    source_ref: str,
    source_commit: str,
    cli_features: List[Dict[str, object]],
    docs_keys: List[str],
    source_defaults: Dict[str, Dict[str, object]],
    missing_in_docs: List[str],
    actionable_missing_in_docs: List[str],
    missing_in_docs_by_stage: Dict[str, List[str]],
    stale_in_docs: List[str],
    ws_precedence: Dict[str, object],
    source_hashes: Dict[str, str],
    documentation_sources: Dict[str, Dict[str, object]] | None = None,
    documentation_stage_mismatches: List[Dict[str, str]] | None = None,
    observation_environment: Dict[str, str] | None = None,
) -> str:
    docs_key_set = set(docs_keys)
    lines: List[str] = []
    lines.append("# Feature Flag Lifecycle Snapshot")
    lines.append("")
    lines.append("Generated by `scripts/snapshot_feature_flags.py`.")
    lines.append("")
    lines.append(f"- Codex CLI version: `{codex_version}`")
    lines.append(f"- Source release: `{source_ref}` at `{source_commit}`")
    if observation_environment:
        lines.append(f"- Observed platform: `{observation_environment['os']}/{observation_environment['arch']}`")
    lines.append("- Inputs:")
    lines.append(
        "  - `codex features list` from an isolated temporary `CODEX_HOME` (observed default values + lifecycle stage labels)"
    )
    lines.append(
        "  - release-matched `openai/codex` source (`features/src/lib.rs`, `client.rs`) for semantic checks"
    )
    lines.append("  - mirrored docs (`config-basic`, `config-reference`) for coverage comparison")
    lines.append("")
    lines.append("## Current CLI Feature Snapshot")
    lines.append("")
    lines.append("| Key | CLI Stage | CLI Default | In Docs | Source Stage | Source Default | Configurable | Effective Behavior |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in cli_features:
        key = str(row["key"])
        defaults = source_defaults.get(
            key, {"default_enabled_expr": "unknown", "stage_from_source": "unknown"}
        )
        in_docs = "yes" if key in docs_key_set else "no"
        enabled = "true" if row["enabled"] else "false"
        lines.append(
            f"| `{key}` | `{row['stage']}` | `{enabled}` | `{in_docs}` | "
            f"`{defaults['stage_from_source']}` | `{defaults['default_enabled_expr']}` | "
            f"`{str(defaults.get('configurable', 'unknown')).lower()}` | `{defaults.get('effective_behavior', 'unknown')}` |"
        )
    lines.append("")
    lines.append("Removed keys are compatibility inputs, not configurable features. A true CLI default does not establish effective behavior. `always_on` requires an explicit source comment; otherwise removed-key behavior may remain `unknown`. Deprecated keys remain separately labeled by stage. Platform-dependent defaults retain their source expression.")
    lines.append("")
    lines.append("## Coverage Gaps")
    lines.append("")
    lines.append(f"- Missing in docs across all lifecycle stages: `{len(missing_in_docs)}`")
    lines.append(
        f"- Actionable missing in docs (`stable`, `experimental`): `{len(actionable_missing_in_docs)}`"
    )
    for stage in ACTIONABLE_STAGES:
        keys = missing_in_docs_by_stage.get(stage, [])
        lines.append(f"  - `{stage}`: `{len(keys)}`")
        for key in keys:
            lines.append(f"    - `{key}`")
    lines.append("- Informational missing in docs:")
    informational_stages = [
        stage for stage in missing_in_docs_by_stage if stage not in ACTIONABLE_STAGES
    ]
    if not informational_stages:
        lines.append("  - none")
    for stage in informational_stages:
        keys = missing_in_docs_by_stage[stage]
        lines.append(f"  - `{stage}`: `{len(keys)}`")
        for key in keys:
            lines.append(f"    - `{key}`")
    lines.append(f"- Present in docs but not in current CLI list: `{len(stale_in_docs)}`")
    if stale_in_docs:
        for key in stale_in_docs:
            lines.append(f"  - `{key}`")
    stage_mismatches = documentation_stage_mismatches or []
    lines.append(f"- Documentation maturity mismatches: `{len(stage_mismatches)}`")
    for mismatch in stage_mismatches:
        lines.append(
            f"  - `{mismatch['key']}`: CLI `{mismatch['cli_stage']}`, "
            f"docs `{mismatch['documentation_stage']}`"
        )
    lines.append("")
    lines.append("## Websocket Flag Semantics")
    lines.append("")
    if ws_precedence.get("detected"):
        lines.append(
            "- `responses_websockets_v2 = true` takes precedence over `responses_websockets`."
        )
        lines.append("- `responses_websockets = true` and `responses_websockets_v2 = false` selects v1.")
        lines.append("- both false disables websocket transport.")
    else:
        lines.append("- Could not detect websocket precedence rules from source.")
    headers = ws_precedence.get("openai_beta_headers", {})
    lines.append(
        f"- Beta header (`responses_websockets`): `{headers.get('responses_websockets', 'unknown')}`"
    )
    lines.append(
        f"- Beta header (`responses_websockets_v2`): `{headers.get('responses_websockets_v2', 'unknown')}`"
    )
    lines.append("")
    lines.append("## Source Fingerprints")
    lines.append("")
    lines.append(f"- Release tag: `{source_ref}`")
    lines.append(f"- Source commit: `{source_commit}`")
    lines.append(f"- `features/src/lib.rs` sha256: `{source_hashes['features_rs_sha256']}`")
    lines.append(f"- `client.rs` sha256: `{source_hashes['client_rs_sha256']}`")
    for label, metadata in sorted((documentation_sources or {}).items()):
        lines.append(
            f"- `{metadata['path']}` sha256: `{metadata['sha256']}` "
            f"({metadata['parsed_feature_key_count']} parsed keys; `{label}`)"
        )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_markdown_document(
    codex_version: str,
    source_ref: str,
    source_commit: str,
    cli_features: List[Dict[str, object]],
    docs_keys: List[str],
    source_defaults: Dict[str, Dict[str, object]],
    missing_in_docs: List[str],
    actionable_missing_in_docs: List[str],
    missing_in_docs_by_stage: Dict[str, List[str]],
    stale_in_docs: List[str],
    ws_precedence: Dict[str, object],
    source_hashes: Dict[str, str],
    documentation_sources: Dict[str, Dict[str, object]] | None = None,
    documentation_stage_mismatches: List[Dict[str, str]] | None = None,
    observation_environment: Dict[str, str] | None = None,
) -> str:
    existing_metadata: Dict[str, object] = {}
    if OUTPUT_MD.exists():
        existing_metadata, _ = split_markdown_frontmatter(OUTPUT_MD.read_text())

    body = render_markdown(
        codex_version=codex_version,
        source_ref=source_ref,
        source_commit=source_commit,
        cli_features=cli_features,
        docs_keys=docs_keys,
        source_defaults=source_defaults,
        missing_in_docs=missing_in_docs,
        actionable_missing_in_docs=actionable_missing_in_docs,
        missing_in_docs_by_stage=missing_in_docs_by_stage,
        stale_in_docs=stale_in_docs,
        ws_precedence=ws_precedence,
        source_hashes=source_hashes,
        documentation_sources=documentation_sources,
        documentation_stage_mismatches=documentation_stage_mismatches,
        observation_environment=observation_environment,
    )
    metadata: Dict[str, object] = {
        "source_type": FEATURE_LIFECYCLE_SOURCE_TYPE,
        "source_area": FEATURE_LIFECYCLE_SOURCE_AREA,
        "source_url": FEATURE_LIFECYCLE_SOURCE_URL,
        "source_kind": FEATURE_LIFECYCLE_SOURCE_KIND,
    }
    metadata.update(codex_version_history_metadata(existing_metadata, codex_version))
    return format_frontmatter(metadata, body)


def write_json(path: Path, payload: Dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def build_snapshot() -> tuple[Dict[str, object], str]:
    codex_version = run_command(["codex", "--version"], env=codex_subprocess_env())
    source_ref, source_commit = resolve_feature_source(
        codex_version, os.environ.get(FEATURE_SOURCE_COMMIT_ENV)
    )
    with tempfile.TemporaryDirectory(prefix="codex-features-home-") as tmp_home:
        isolated_env = codex_subprocess_env()
        isolated_env["CODEX_HOME"] = tmp_home
        features_raw = run_command(["codex", "features", "list"], env=isolated_env)
    cli_features = parse_features_list(features_raw)

    basic_docs_metadata = parse_config_basic_feature_metadata(CONFIG_BASIC_DOC)
    basic_docs_keys = list(basic_docs_metadata)
    reference_docs_keys = parse_config_reference_feature_keys(CONFIG_REFERENCE_DOC)
    docs_keys = sorted(set(basic_docs_keys) | set(reference_docs_keys))
    if not docs_keys:
        raise SnapshotError("Parsed zero documentation feature keys")
    documentation_sources = {
        "config_basic": documentation_source_metadata(
            CONFIG_BASIC_DOC, basic_docs_keys
        ),
        "config_reference": documentation_source_metadata(
            CONFIG_REFERENCE_DOC, reference_docs_keys
        ),
    }
    cli_keys = [str(item["key"]) for item in cli_features]
    (
        missing_in_docs,
        actionable_missing_in_docs,
        missing_in_docs_by_stage,
    ) = group_missing_in_docs(cli_features, docs_keys)
    stale_in_docs = sorted([key for key in docs_keys if key not in set(cli_keys)])
    documentation_stage_mismatches = find_documentation_stage_mismatches(
        cli_features, basic_docs_metadata
    )

    features_rs_url = source_url(source_commit, OSS_FEATURES_RS_PATH)
    client_rs_url = source_url(source_commit, OSS_CLIENT_RS_PATH)
    features_rs = fetch_text(features_rs_url)
    client_rs = fetch_text(client_rs_url)
    source_defaults = parse_feature_defaults_from_source(features_rs)
    ws_precedence = derive_websocket_precedence(client_rs)
    source_hashes = {
        "features_rs_sha256": sha256_text(features_rs),
        "client_rs_sha256": sha256_text(client_rs),
    }

    observation_environment = {"os": sys.platform, "arch": host_platform.machine().lower()}
    payload: Dict[str, object] = {
        "schema_version": 3,
        "observation_environment": observation_environment,
        "codex_cli_version": codex_version,
        "source_ref": source_ref,
        "source_commit": source_commit,
        "cli_features": cli_features,
        "docs_feature_keys": docs_keys,
        "documentation_sources": documentation_sources,
        "coverage": {
            "actionable_stages": list(ACTIONABLE_STAGES),
            "actionable_missing_in_docs": actionable_missing_in_docs,
            "missing_in_docs": missing_in_docs,
            "missing_in_docs_by_stage": missing_in_docs_by_stage,
            "stale_in_docs": stale_in_docs,
            "documentation_stage_mismatches": documentation_stage_mismatches,
        },
        "source_defaults": source_defaults,
        "websocket_precedence": ws_precedence,
        "source_fingerprints": source_hashes,
        "source_urls": {
            "features_rs": features_rs_url,
            "client_rs": client_rs_url,
        },
    }

    markdown = render_markdown_document(
        codex_version=codex_version,
        source_ref=source_ref,
        source_commit=source_commit,
        cli_features=cli_features,
        docs_keys=docs_keys,
        source_defaults=source_defaults,
        missing_in_docs=missing_in_docs,
        actionable_missing_in_docs=actionable_missing_in_docs,
        missing_in_docs_by_stage=missing_in_docs_by_stage,
        stale_in_docs=stale_in_docs,
        ws_precedence=ws_precedence,
        source_hashes=source_hashes,
        documentation_sources=documentation_sources,
        documentation_stage_mismatches=documentation_stage_mismatches,
        observation_environment=observation_environment,
    )

    return payload, markdown


def main() -> int:
    try:
        payload, markdown = build_snapshot()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        write_json(OUTPUT_JSON, payload)
        OUTPUT_MD.write_text(markdown)

        print(f"Wrote {OUTPUT_JSON.relative_to(ROOT)}")
        print(f"Wrote {OUTPUT_MD.relative_to(ROOT)}")
        print(f"Missing in docs: {len(payload["coverage"]["missing_in_docs"])}")
        print(f"Actionable missing in docs: {len(payload["coverage"]["actionable_missing_in_docs"])}")
        print(
            "Documentation maturity mismatches: "
            f"{len(payload['coverage']['documentation_stage_mismatches'])}"
        )
        return 0
    except SnapshotError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
