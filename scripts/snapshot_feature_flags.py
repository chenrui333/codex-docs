#!/usr/bin/env python3
"""Generate Codex feature-flag lifecycle snapshots for this docs mirror."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List, Sequence
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = ROOT / "docs"
OUTPUT_DIR = DOCS_ROOT / "feature-flags"
OUTPUT_JSON = OUTPUT_DIR / "lifecycle.json"
OUTPUT_MD = OUTPUT_DIR / "lifecycle.md"
CONFIG_BASIC_DOC = DOCS_ROOT / "developers.openai.com" / "codex" / "config-basic" / "index.md"
CONFIG_REFERENCE_DOC = (
    DOCS_ROOT / "developers.openai.com" / "codex" / "config-reference" / "index.md"
)

OSS_FEATURES_RS_URL = (
    "https://raw.githubusercontent.com/openai/codex/main/codex-rs/features/src/lib.rs"
)
OSS_CLIENT_RS_URL = "https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/src/client.rs"
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
    proc = subprocess.run(argv, check=False, text=True, capture_output=True, env=env)
    if proc.returncode != 0:
        joined = " ".join(argv)
        raise SnapshotError(
            f"Command failed ({joined}):\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout.strip()


def codex_subprocess_env(base: Dict[str, str] | None = None) -> Dict[str, str]:
    env = dict(os.environ if base is None else base)
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        env.pop(name, None)
    return env


def fetch_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": HTTP_USER_AGENT})
    with urlopen(req, timeout=30) as resp:  # noqa: S310 (trusted static URLs)
        return resp.read().decode("utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_codex_cli_version(version_raw: str) -> str:
    match = re.search(r"\b(\d+\.\d+\.\d+(?:[-+][^\s]+)?)\b", version_raw)
    return match.group(1) if match else version_raw.strip()


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


def parse_config_basic_feature_keys(path: Path) -> List[str]:
    if not path.exists():
        return []
    text = path.read_text()
    section_match = re.search(
        r"### Supported features\s+(.*?)(?:\n### |\Z)",
        text,
        flags=re.DOTALL,
    )
    if not section_match:
        return []
    section = section_match.group(1)
    return sorted(set(re.findall(r"\|\s*`([a-z0-9_]+)`\s*\|", section)))


def parse_config_reference_feature_keys(path: Path) -> List[str]:
    if not path.exists():
        return []
    text = path.read_text()
    return sorted(set(re.findall(r"\|\s*`features\.([a-z0-9_]+)`\s*\|", text)))


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


def parse_feature_defaults_from_source(features_rs_text: str) -> Dict[str, Dict[str, str]]:
    parsed: Dict[str, Dict[str, str]] = {}
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
        parsed[key] = {
            "default_enabled_expr": default_match.group(1).strip() if default_match else "unknown",
            "stage_from_source": normalized_stage,
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
    cli_features: List[Dict[str, object]],
    docs_keys: List[str],
    source_defaults: Dict[str, Dict[str, str]],
    missing_in_docs: List[str],
    stale_in_docs: List[str],
    ws_precedence: Dict[str, object],
    source_hashes: Dict[str, str],
) -> str:
    docs_key_set = set(docs_keys)
    lines: List[str] = []
    lines.append("# Feature Flag Lifecycle Snapshot")
    lines.append("")
    lines.append("Generated by `scripts/snapshot_feature_flags.py`.")
    lines.append("")
    lines.append(f"- Codex CLI version: `{codex_version}`")
    lines.append("- Inputs:")
    lines.append(
        "  - `codex features list` from an isolated temporary `CODEX_HOME` (runtime behavior + lifecycle stage labels)"
    )
    lines.append("  - `openai/codex` source (`features/src/lib.rs`, `client.rs`) for semantic checks")
    lines.append("  - mirrored docs (`config-basic`, `config-reference`) for coverage comparison")
    lines.append("")
    lines.append("## Current CLI Feature Snapshot")
    lines.append("")
    lines.append("| Key | CLI Stage | Enabled | In Docs | Source Stage | Source Default |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in cli_features:
        key = str(row["key"])
        defaults = source_defaults.get(
            key, {"default_enabled_expr": "unknown", "stage_from_source": "unknown"}
        )
        in_docs = "yes" if key in docs_key_set else "no"
        enabled = "true" if row["enabled"] else "false"
        lines.append(
            f"| `{key}` | `{row['stage']}` | `{enabled}` | `{in_docs}` | "
            f"`{defaults['stage_from_source']}` | `{defaults['default_enabled_expr']}` |"
        )
    lines.append("")
    lines.append("## Coverage Gaps")
    lines.append("")
    lines.append(f"- Missing in docs: `{len(missing_in_docs)}`")
    if missing_in_docs:
        for key in missing_in_docs:
            lines.append(f"  - `{key}`")
    lines.append(f"- Present in docs but not in current CLI list: `{len(stale_in_docs)}`")
    if stale_in_docs:
        for key in stale_in_docs:
            lines.append(f"  - `{key}`")
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
    lines.append(f"- `features/src/lib.rs` sha256: `{source_hashes['features_rs_sha256']}`")
    lines.append(f"- `client.rs` sha256: `{source_hashes['client_rs_sha256']}`")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_markdown_document(
    codex_version: str,
    cli_features: List[Dict[str, object]],
    docs_keys: List[str],
    source_defaults: Dict[str, Dict[str, str]],
    missing_in_docs: List[str],
    stale_in_docs: List[str],
    ws_precedence: Dict[str, object],
    source_hashes: Dict[str, str],
) -> str:
    existing_metadata: Dict[str, object] = {}
    if OUTPUT_MD.exists():
        existing_metadata, _ = split_markdown_frontmatter(OUTPUT_MD.read_text())

    body = render_markdown(
        codex_version=codex_version,
        cli_features=cli_features,
        docs_keys=docs_keys,
        source_defaults=source_defaults,
        missing_in_docs=missing_in_docs,
        stale_in_docs=stale_in_docs,
        ws_precedence=ws_precedence,
        source_hashes=source_hashes,
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


def main() -> int:
    try:
        codex_version = run_command(["codex", "--version"], env=codex_subprocess_env())
        with tempfile.TemporaryDirectory(prefix="codex-features-home-") as tmp_home:
            isolated_env = codex_subprocess_env()
            isolated_env["CODEX_HOME"] = tmp_home
            features_raw = run_command(["codex", "features", "list"], env=isolated_env)
        cli_features = parse_features_list(features_raw)

        docs_keys = sorted(
            set(parse_config_basic_feature_keys(CONFIG_BASIC_DOC))
            | set(parse_config_reference_feature_keys(CONFIG_REFERENCE_DOC))
        )
        cli_keys = [str(item["key"]) for item in cli_features]
        missing_in_docs = sorted([key for key in cli_keys if key not in set(docs_keys)])
        stale_in_docs = sorted([key for key in docs_keys if key not in set(cli_keys)])

        features_rs = fetch_text(OSS_FEATURES_RS_URL)
        client_rs = fetch_text(OSS_CLIENT_RS_URL)
        source_defaults = parse_feature_defaults_from_source(features_rs)
        ws_precedence = derive_websocket_precedence(client_rs)
        source_hashes = {
            "features_rs_sha256": sha256_text(features_rs),
            "client_rs_sha256": sha256_text(client_rs),
        }

        payload: Dict[str, object] = {
            "codex_cli_version": codex_version,
            "cli_features": cli_features,
            "docs_feature_keys": docs_keys,
            "coverage": {
                "missing_in_docs": missing_in_docs,
                "stale_in_docs": stale_in_docs,
            },
            "source_defaults": source_defaults,
            "websocket_precedence": ws_precedence,
            "source_fingerprints": source_hashes,
            "source_urls": {
                "features_rs": OSS_FEATURES_RS_URL,
                "client_rs": OSS_CLIENT_RS_URL,
            },
        }

        markdown = render_markdown_document(
            codex_version=codex_version,
            cli_features=cli_features,
            docs_keys=docs_keys,
            source_defaults=source_defaults,
            missing_in_docs=missing_in_docs,
            stale_in_docs=stale_in_docs,
            ws_precedence=ws_precedence,
            source_hashes=source_hashes,
        )

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        write_json(OUTPUT_JSON, payload)
        OUTPUT_MD.write_text(markdown)

        print(f"Wrote {OUTPUT_JSON.relative_to(ROOT)}")
        print(f"Wrote {OUTPUT_MD.relative_to(ROOT)}")
        print(f"Missing in docs: {len(missing_in_docs)}")
        return 0
    except SnapshotError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
