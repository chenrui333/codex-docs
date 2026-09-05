"""Pure, prompt-free projection of the release-bundled model catalog."""

from __future__ import annotations

import json
import re

SOURCE_PATH = "codex-rs/models-manager/models.json"
FIELDS = (
    "slug", "display_name", "description", "visibility", "priority",
    "minimal_client_version", "supported_in_api", "supported_reasoning_levels",
    "default_reasoning_level", "support_verbosity", "default_verbosity",
    "context_window", "max_context_window", "auto_compact_token_limit",
    "tool_mode", "shell_type", "apply_patch_tool_type", "multi_agent_version",
    "multi_agent_reasoning_effort", "input_modalities", "web_search_tool_type",
    "supports_search_tool", "supports_image_detail_original", "upgrade",
    "supports_parallel_tool_calls", "default_service_tier", "service_tiers",
)


def canonical(value):
    """Selected catalog lists are sets; source ordering is not a semantic event."""
    if isinstance(value, dict):
        return {key: canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, list):
        return sorted((canonical(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    return value


def project_models(payload: dict) -> list[dict]:
    models = payload.get("models")
    if not isinstance(models, list) or not models:
        raise ValueError("Bundled model catalog must contain a nonempty models list")
    result = []
    seen = set()
    for model in models:
        if not isinstance(model, dict):
            raise ValueError("Model catalog entry must be an object")
        slug = model.get("slug")
        if not isinstance(slug, str) or not slug or slug in seen:
            raise ValueError("Model catalog slug is missing or duplicated")
        if not isinstance(model.get("visibility"), str) or type(model.get("priority")) is not int:
            raise ValueError(f"Model {slug} lacks selection metadata")
        seen.add(slug)
        result.append({key: canonical(model[key]) for key in FIELDS if key in model})
    return sorted(result, key=lambda model: model["slug"])


def snapshot(payload: dict, *, version: str, source_ref: str, source_commit: str) -> dict:
    if not re.fullmatch(r"\d+\.\d+\.\d+", version) or source_ref != f"rust-v{version}":
        raise ValueError("Model catalog requires a stable release-matched ref")
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("Model catalog requires an immutable source commit")
    return {
        "schema_version": 1,
        "codex_cli_version": version,
        "source_ref": source_ref,
        "source_commit": source_commit,
        "source_path": SOURCE_PATH,
        "source_kind": "release_bundled_model_catalog",
        "models": project_models(payload),
    }


def changes(previous: dict, current: dict) -> dict:
    before = {model["slug"]: model for model in project_models(previous)} if previous else {}
    after = {model["slug"]: model for model in project_models(current)}
    changed = []
    for slug in sorted(before.keys() & after.keys()):
        fields = {key: {"before": before[slug].get(key), "after": after[slug].get(key)}
                  for key in FIELDS if before[slug].get(key) != after[slug].get(key)}
        if fields:
            changed.append({"slug": slug, "fields": fields})
    return {"added": sorted(after.keys() - before.keys()),
            "removed": sorted(before.keys() - after.keys()), "changed": changed}


def render_changes(diff: dict) -> list[str]:
    lines = []
    for key in ("added", "removed"):
        for slug in diff.get(key, []):
            lines.append(f"- {key.capitalize()}: `{slug}`")
    for model in diff.get("changed", []):
        for field, values in sorted(model["fields"].items()):
            before, after = (json.dumps(values[key], ensure_ascii=False, sort_keys=True) for key in ("before", "after"))
            lines.append(f"- `{model['slug']}` — `{field}`: `{before}` -> `{after}`")
    return lines + [""] if lines else []
