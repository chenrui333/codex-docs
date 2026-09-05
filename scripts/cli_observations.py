"""Deterministic unions of platform-scoped, immutable CLI observations."""

from __future__ import annotations

import copy
import re


def platform_key(observation: dict) -> str:
    environment = observation.get("observation_environment", observation)
    os_name, arch = environment.get("os"), environment.get("arch")
    if os_name not in {"linux", "darwin", "windows"} or not re.fullmatch(r"[a-z0-9_]+", str(arch or "")):
        raise ValueError("CLI observation requires a supported OS and architecture")
    return f"{'macos' if os_name == 'darwin' else os_name}-{arch}"


def validate(surface: dict) -> dict:
    platform_key(surface)
    version = surface.get("codex_cli_version", "")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version) or surface.get("source_ref") != f"rust-v{version}":
        raise ValueError("CLI observation requires a stable release-matched ref")
    if not re.fullmatch(r"[0-9a-f]{40}", surface.get("source_commit", "")):
        raise ValueError("CLI observation requires an immutable source commit")
    for field in ("commands", "global_options"):
        if not isinstance(surface.get(field), list):
            raise ValueError(f"CLI observation lacks {field}")
    return surface


def observation_metadata(surface: dict) -> dict:
    return {**surface["observation_environment"],
            "codex_cli_version": surface["codex_cli_version"],
            "source_ref": surface["source_ref"], "source_commit": surface["source_commit"]}


def merge_items(by_platform: dict, observations: dict, identity: str) -> list[dict]:
    groups = {}
    for platform, items in sorted(by_platform.items()):
        seen = set()
        for item in items:
            key = item.get(identity) if isinstance(item, dict) else None
            if not isinstance(key, str) or not key or key in seen:
                raise ValueError(f"Malformed or duplicate CLI {identity}")
            seen.add(key)
            groups.setdefault(key, {})[platform] = item
    merged = []
    for _, variants in sorted(groups.items()):
        # Descriptions may differ by platform; raw observations preserve each one.
        item = copy.deepcopy(next(iter(variants.values())))
        item["observed_on"] = {platform: observations[platform] for platform in variants}
        for child, child_key in (("options", "primary_flag"), ("subcommands", "name")):
            if any(child in variant for variant in variants.values()):
                item[child] = merge_items({platform: variant.get(child, []) for platform, variant in variants.items()},
                                          observations, child_key)
        merged.append(item)
    return merged


def aggregate(surfaces: dict[str, dict], metadata: dict) -> dict:
    if not surfaces:
        raise ValueError("Cannot aggregate zero CLI observations")
    for key, surface in surfaces.items():
        validate(surface)
        if platform_key(surface) != key:
            raise ValueError("CLI observation path does not match its platform")
    observations = {key: observation_metadata(surface) for key, surface in sorted(surfaces.items())}
    return {
        "schema_version": 3,
        "source_kind": "aggregated_cli_observation",
        "command": "codex --help; codex <command> --help",
        "usage": sorted({usage for surface in surfaces.values() for usage in surface.get("usage", [])}),
        "codex_cli_version": metadata["codex_cli_version"],
        "codex_cli_version_raw": metadata.get("codex_cli_version_raw", ""),
        "source_ref": metadata["codex_cli_release_ref"],
        "source_commit": metadata["codex_cli_source_commit"],
        "platform_observations": observations,
        "global_options": merge_items({key: surface["global_options"] for key, surface in surfaces.items()}, observations, "primary_flag"),
        "commands": merge_items({key: surface["commands"] for key, surface in surfaces.items()}, observations, "name"),
    }


def absence_reason(previous: dict, current: dict, ancestry: dict) -> str:
    versions = [previous.get("codex_cli_version", ""), current.get("codex_cli_version", "")]
    if not all(re.fullmatch(r"\d+\.\d+\.\d+", value) for value in versions):
        return "unknown_release_order"
    if tuple(map(int, versions[1].split("."))) <= tuple(map(int, versions[0].split("."))):
        return "not_newer_release"
    relationship = ancestry.get(f"{previous.get('source_commit', '')}...{current.get('source_commit', '')}", "unknown")
    return {"ancestor": "", "not_ancestor": "divergent_release_lineage"}.get(relationship, "unknown_release_lineage")


def platform_states(previous: dict, present_on: dict, observations: dict, ancestry: dict) -> dict:
    states = copy.deepcopy(previous)
    for platform, observation in observations.items():
        old = states.get(platform, {})
        if platform in present_on:
            states[platform] = {"status": "present", "active": True, "last_seen": present_on[platform]}
        elif not old:
            states[platform] = {"status": "absent", "active": False, "observation": observation,
                                "absence_reason": "never_observed"}
        elif old.get("active", True):
            reason = absence_reason(old.get("last_seen", {}), observation, ancestry)
            states[platform] = {**old, "status": "not_observed" if reason else "absent",
                                "active": bool(reason), "observation": observation}
            if reason:
                states[platform]["absence_reason"] = reason
            else:
                states[platform].pop("absence_reason", None)
                states[platform]["removed_in_version"] = observation["codex_cli_version"]
    return states
