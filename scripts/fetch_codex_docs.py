#!/usr/bin/env python3
"""Sync Codex-focused docs from official OpenAI documentation sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import platform as host_platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Collection, Dict, Iterable, List, Sequence, Tuple
from urllib.parse import ParseResult, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as to_markdown

if __package__:
    from . import cli_observations, model_catalog, semantic_history, snapshot_feature_flags
else:
    import cli_observations
    import model_catalog
    import semantic_history
    import snapshot_feature_flags

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
WEEKLY_DIR = ROOT / "weekly"
MANIFEST_PATH = DOCS_DIR / "docs_manifest.json"
SUMMARY_PATH = DOCS_DIR / "sync_summary.json"
COVERAGE_PATH = DOCS_DIR / "source_coverage.json"
CAPABILITIES_PATH = DOCS_DIR / "codex_capabilities.json"
CAPABILITIES_REL_PATH = str(CAPABILITIES_PATH.relative_to(DOCS_DIR))
CLI_SURFACE_PATH = DOCS_DIR / "codex_cli_surface.json"
CLI_SURFACE_REL_PATH = str(CLI_SURFACE_PATH.relative_to(DOCS_DIR))
MODELS_REL_PATH = "codex_models.json"
MODEL_SOURCE_TYPE = "codex_model_catalog"
FEATURE_LIFECYCLE = DOCS_DIR / "feature-flags" / "lifecycle.json"
DEVELOPERS_ROOT = DOCS_DIR / "developers.openai.com"
LEARN_ROOT = DOCS_DIR / "learn.chatgpt.com"
GITHUB_ROOT = DOCS_DIR / "github.openai.com" / "openai" / "codex"
PLATFORM_ROOT = DOCS_DIR / "platform.openai.com"
SYSTEM_SKILLS_ROOT = ROOT / "dot_codex" / "skills" / "dot_system"
SYSTEM_PROMPTS_ROOT = ROOT / "system_prompts" / "codex-cli"

SYSTEM_SKILL_OUTPUT_PREFIX = "dot_codex/skills/dot_system/"
SYSTEM_PROMPT_OUTPUT_PREFIX = "system_prompts/codex-cli/"
ROOT_OUTPUT_PREFIXES = ("dot_codex/", "system_prompts/")
CLI_PLATFORM_SOURCE_TYPE = "codex_cli_platform_observation"
CODEX_CLI_SOURCE_TYPES = {
    CLI_PLATFORM_SOURCE_TYPE,
    "codex_cli_system_skill",
    "codex_cli_prompt_input",
    "codex_cli_surface",
}
PLATFORM_TOOL_GUIDE_SOURCE_TYPE = "platform_tool_guide"
LEARN_SOURCE_TYPE = "learn"
CAPABILITY_INVENTORY_SOURCE_TYPE = "capability_inventory"
CLI_SURFACE_SOURCE_TYPE = "codex_cli_surface"
WEEKLY_REPORT_SOURCE_TYPE = "weekly_sync_report"
WEEKLY_REPORT_SOURCE_AREA = "weekly"
WEEKLY_REPORT_SOURCE_KIND = "generated_weekly_report"
SOURCE_METADATA_KEYS = (
    "source_area",
    "source_kind",
    "source_last_modified",
    "source_etag",
    "source_redirect_url",
    "upstream_source_ref",
    "upstream_source_commit",
    "codex_cli_versions",
    "codex_cli_versions_raw",
    "codex_cli_release_ref",
    "codex_cli_source_commit",
    "codex_cli_version",
    "codex_cli_version_raw",
    "codex_cli_command",
    "codex_prompt_snapshot_command",
)

PERMANENT_MISSING_HTTP_STATUSES = (404, 410)
SOURCE_STATE_SEMANTICS = {
    "available": {
        "strict_failure": False,
        "preserve_last_known_good": False,
        "meaning": "The discovered source was fetched and mirrored successfully.",
    },
    "redirected": {
        "strict_failure": False,
        "preserve_last_known_good": False,
        "meaning": "The source redirected successfully; the final canonical URL is recorded.",
    },
    "confirmed_tombstone": {
        "strict_failure": False,
        "preserve_last_known_good": False,
        "meaning": (
            "Every attempted canonical representation of a sitemap-discovered page returned "
            "HTTP 404 or 410. It is recorded as a stale/tombstoned sitemap entry and is no "
            "longer mirrored."
        ),
    },
    "removed_from_sitemap": {
        "strict_failure": False,
        "preserve_last_known_good": False,
        "meaning": (
            "A previously discovered page disappeared from a complete sitemap fetch and is "
            "treated as an intentional upstream removal."
        ),
    },
    "transient_page_failure": {
        "strict_failure": True,
        "preserve_last_known_good": True,
        "meaning": "A page failed with a network, timeout, rate-limit, or server error.",
    },
    "sitemap_unavailable": {
        "strict_failure": True,
        "preserve_last_known_good": True,
        "meaning": "A sitemap or sitemap index could not be fetched completely.",
    },
    "source_unavailable": {
        "strict_failure": True,
        "preserve_last_known_good": True,
        "meaning": "A complete canonical source family could not be built.",
    },
    "extractor_or_malformed_source": {
        "strict_failure": True,
        "preserve_last_known_good": True,
        "meaning": "Fetched content could not be parsed or produced an invalid source shape.",
    },
    "partial_coverage": {
        "strict_failure": True,
        "preserve_last_known_good": True,
        "meaning": "Only part of a source family was fetched; its prior mirror is preserved.",
    },
}
PROMPT_VOLATILE_KEYS = {"internal_chat_message_metadata_passthrough"}
SAFE_CODEX_ENV_KEYS = {
    "COMSPEC",
    "LANG",
    "LC_ALL",
    "PATH",
    "PATHEXT",
    "SSL_CERT_DIR",
    "SSL_CERT_FILE",
    "SYSTEMROOT",
    "TMPDIR",
}
CLI_OPTION_CONFIG_KEYS = {
    "--ask-for-approval": ["approval_policy"],
    "--local-provider": ["oss_provider"],
    "--model": ["model"],
    "--oss": ["oss_provider"],
    "--sandbox": ["sandbox_mode"],
}

SITEMAP_INDEX_URL = "https://developers.openai.com/sitemap-index.xml"
LEARN_SITEMAP_INDEX_URL = "https://learn.chatgpt.com/sitemap-index.xml"
GITHUB_TREE_URL_TEMPLATE = (
    "https://api.github.com/repos/openai/codex/git/trees/{ref}?recursive=1"
)
GITHUB_REPOSITORY_API_URL = "https://api.github.com/repos/openai/codex"
GITHUB_RAW_URL_TEMPLATE = "https://raw.githubusercontent.com/openai/codex/{ref}/{path}"
PLATFORM_TOOL_GUIDE_URLS = (
    "https://developers.openai.com/api/docs/guides/tools-apply-patch",
    "https://developers.openai.com/api/docs/guides/tools-computer-use",
    "https://developers.openai.com/api/docs/guides/tools-shell",
    "https://platform.openai.com/docs/guides/tools-web-search",
)
DEVELOPERS_REDIRECT_ALIASES = {
    "/cookbook/examples/gpt-5/codex_prompting_guide.ipynb": "https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide",
    "/cookbook/gpt-5-1-codex-max-prompting-guide": "https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide",
    "/cookbook/gpt-5-1-codex-max_prompting_guide": "https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide",
    "/cookbook/gpt-5-codex-prompting-guide": "https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide",
    "/cookbook/gpt-5-codex_prompting_guide": "https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide",
}
USER_AGENT = "codex-docs-sync/0.1 (+https://github.com/chenrui333/codex-docs)"

LOG = logging.getLogger("fetch_codex_docs")

DEVELOPERS_CONTENT_SELECTORS: Sequence[str] = (
    "article#mainContent",
    "article.prose-content",
    "main article",
    "main",
    "article",
    "body",
)
NOISY_EXACT_LINES = {
    "Copy PageMore page actions",
    "Copy Page",
    "More page actions",
}
NOISY_LINE_PATTERNS = (
    re.compile(r"^Choose an option\s*$", flags=re.IGNORECASE),
)
WEEKLY_CATEGORY_RULES: Sequence[Tuple[str, str]] = (
    ("System Skills", SYSTEM_SKILL_OUTPUT_PREFIX),
    ("System Prompts", SYSTEM_PROMPT_OUTPUT_PREFIX),
    ("ChatGPT Learn Docs", "learn.chatgpt.com/docs/"),
    ("Developers Codex", "developers.openai.com/codex/"),
    ("Developers Cookbook", "developers.openai.com/cookbook/"),
    ("Developers Resources", "developers.openai.com/resources/"),
    ("API Tool Guides", "developers.openai.com/api/docs/guides/"),
    ("Platform Tool Guides", "platform.openai.com/docs/guides/"),
    ("GitHub Core Docs", "github.openai.com/openai/codex/docs/"),
    ("GitHub Other Docs", "github.openai.com/openai/codex/"),
)
DEVELOPERS_CODEX_SOURCE_AREAS = {
    "agent-approvals-security": "codex_security",
    "app": "codex_app",
    "app-server": "codex_app",
    "auth": "codex_auth",
    "changelog": "codex_changelog",
    "cli": "codex_cli_docs",
    "cloud": "codex_cloud",
    "codex-for-oss-terms": "codex_open_source",
    "concepts": "codex_concept",
    "config-advanced": "codex_cli_docs",
    "config-basic": "codex_cli_docs",
    "config-reference": "codex_cli_docs",
    "config-sample": "codex_cli_docs",
    "custom-prompts": "codex_cli_docs",
    "enterprise": "codex_enterprise",
    "feature-maturity": "codex_reference",
    "github-action": "codex_integration",
    "guides": "codex_guide",
    "hooks": "codex_cli_docs",
    "ide": "codex_ide",
    "integrations": "codex_integration",
    "learn": "codex_guide",
    "mcp": "codex_cli_docs",
    "memories": "codex_memory",
    "models": "codex_reference",
    "noninteractive": "codex_cli_docs",
    "open-source": "codex_open_source",
    "plugins": "codex_cli_docs",
    "pricing": "codex_reference",
    "prompting": "codex_cli_docs",
    "quickstart": "codex_cli_docs",
    "remote-connections": "codex_cli_docs",
    "rules": "codex_cli_docs",
    "sdk": "codex_sdk",
    "security": "codex_security",
    "skills": "codex_cli_docs",
    "speed": "codex_reference",
    "subagents": "codex_cli_docs",
    "tracks": "codex_track",
    "use-cases": "codex_use_case",
    "videos": "codex_media",
    "windows": "codex_app",
    "workflows": "codex_reference",
}


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        LOG.warning("Invalid integer for %s=%r. Falling back to %d.", name, raw, default)
        return default


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        LOG.warning("Invalid float for %s=%r. Falling back to %.2f.", name, raw, default)
        return default


REQUEST_TIMEOUT_SECONDS = _env_float("CODEX_DOCS_TIMEOUT_SECONDS", 30.0)
REQUEST_MAX_RETRIES = max(_env_int("CODEX_DOCS_MAX_RETRIES", 3), 1)
REQUEST_BACKOFF_SECONDS = max(_env_float("CODEX_DOCS_RETRY_BACKOFF_SECONDS", 1.5), 0.0)
COMMAND_TIMEOUT_SECONDS = max(
    _env_float("CODEX_DOCS_COMMAND_TIMEOUT_SECONDS", 120.0), 0.1
)
STRICT_SYNC_MODE = os.environ.get("CODEX_DOCS_STRICT_SYNC", "0") == "1"


@dataclass(frozen=True)
class ManagedFile:
    rel_path: str
    source_type: str
    source_url: str
    content: str | bytes
    source_metadata: Dict[str, object] | None = None


@dataclass(frozen=True)
class SourceTombstone(Exception):
    """A sitemap-advertised canonical page returned a permanent missing status."""

    url: str
    status_code: int
    endpoint_statuses: Tuple[int, ...] = ()

    def as_coverage(self) -> Dict[str, object]:
        return {
            "url": self.url,
            "status_code": self.status_code,
            "endpoint_statuses": list(self.endpoint_statuses),
            "state": "confirmed_tombstone",
            "confirmation": "all_attempted_representations_http_404_or_410",
        }


class SourceContentError(RuntimeError):
    """A fetched source had an unexpected or malformed representation."""


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_content(content: str | bytes) -> str:
    payload = content.encode("utf-8") if isinstance(content, str) else content
    return hashlib.sha256(payload).hexdigest()


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    cleaned = ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=path,
        params="",
        query="",
        fragment="",
    )
    return urlunparse(cleaned)


def parse_sitemap_loc_tags(
    xml_text: str,
    *,
    source_url: str,
    expected_root: str,
) -> List[str]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise SourceContentError(f"Malformed sitemap XML from {source_url}: {exc}") from exc

    root_name = root.tag.rsplit("}", 1)[-1]
    if root_name != expected_root:
        raise SourceContentError(
            f"Unexpected sitemap root from {source_url}: expected {expected_root}, got {root_name}"
        )

    locations = [
        str(element.text).strip()
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] == "loc" and element.text and element.text.strip()
    ]
    if not locations:
        raise SourceContentError(f"Sitemap from {source_url} did not contain any loc entries")
    return locations


def keep_developers_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc != "developers.openai.com":
        return False

    path = parsed.path.rstrip("/")
    if not path:
        return False

    prefixes = [
        "/codex",
        "/resources/codex",
        "/cookbook/topic/codex",
        "/cookbook/articles/codex",
        "/cookbook/examples/codex",
    ]

    if any(path == prefix or path.startswith(prefix + "/") for prefix in prefixes):
        return True

    if path == "/cookbook/articles/codex_exec_plans":
        return True

    if path == "/cookbook/examples/gpt-5/codex_prompting_guide":
        return True

    if path.startswith("/blog/") and path != "/blog/topic/codex" and "codex" in path.lower():
        return True

    return False


def developers_skipped_url_detail(url: str) -> Dict[str, str] | None:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    if path in DEVELOPERS_REDIRECT_ALIASES:
        return {
            "url": url,
            "classification": "redirect_alias",
            "reason": "Redirects to an already mirrored canonical cookbook guide.",
            "canonical_url": DEVELOPERS_REDIRECT_ALIASES[path],
        }

    if path == "/blog/topic/codex":
        return {
            "url": url,
            "classification": "blog_index",
            "reason": "Blog listing pages are intentionally excluded from the docs mirror.",
        }

    if path.startswith("/community/"):
        return {
            "url": url,
            "classification": "community_page",
            "reason": "Community pages are intentionally excluded from the docs mirror.",
        }

    if path == "/learn/codex":
        return {
            "url": url,
            "classification": "learn_index",
            "reason": "Learning index pages are intentionally excluded from the docs mirror.",
        }

    if path == "/learn/developers-codex-plugin":
        return {
            "url": url,
            "classification": "chatgpt_plugin_page",
            "reason": "ChatGPT plugin guidance is covered by the ChatGPT Learn mirror.",
        }

    if path.startswith("/showcase/"):
        return {
            "url": url,
            "classification": "showcase_page",
            "reason": "Showcase pages are intentionally excluded from the docs mirror.",
        }

    if path.startswith("/training/"):
        return {
            "url": url,
            "classification": "training_page",
            "reason": "Interactive course landing pages are excluded from the versioned docs mirror.",
        }

    return None


def count_details_by_classification(details: Sequence[Dict[str, str]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in details:
        classification = item.get("classification", "unknown")
        counts[classification] = counts.get(classification, 0) + 1
    return {key: counts[key] for key in sorted(counts)}


def is_codex_related_developers_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc != "developers.openai.com":
        return False
    path = parsed.path.rstrip("/")
    if not path:
        return False
    return "codex" in path.lower()


def fetch_response(
    session: requests.Session,
    url: str,
    headers: Dict[str, str] | None = None,
    allowed_statuses: Collection[int] = (),
) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(1, REQUEST_MAX_RETRIES + 1):
        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS, headers=headers)
            if response.status_code in allowed_statuses:
                return response
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            last_error = exc
            if attempt >= REQUEST_MAX_RETRIES:
                break
            sleep_seconds = REQUEST_BACKOFF_SECONDS * (2 ** (attempt - 1))
            LOG.warning(
                "Request failed (attempt %d/%d) for %s: %s. Retrying in %.2fs",
                attempt,
                REQUEST_MAX_RETRIES,
                url,
                exc,
                sleep_seconds,
            )
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

    assert last_error is not None  # pragma: no cover - defensive
    raise last_error


def fetch_text(session: requests.Session, url: str, headers: Dict[str, str] | None = None) -> str:
    return fetch_response(session, url, headers=headers).text


def fetch_bytes(session: requests.Session, url: str, headers: Dict[str, str] | None = None) -> bytes:
    return fetch_response(session, url, headers=headers).content


def normalize_http_datetime(value: str) -> str:
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return value
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def response_source_metadata(response: requests.Response) -> Dict[str, str]:
    metadata: Dict[str, str] = {}
    last_modified = response.headers.get("Last-Modified", "").strip()
    if last_modified:
        metadata["source_last_modified"] = normalize_http_datetime(last_modified)
    etag = response.headers.get("ETag", "").strip()
    if etag:
        metadata["source_etag"] = etag
    return metadata


def response_content_type(response: requests.Response) -> str:
    return response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()


def validate_text_response(
    response: requests.Response,
    *,
    source_url: str,
    allowed_content_types: Collection[str],
) -> str:
    content_type = response_content_type(response)
    if content_type not in allowed_content_types:
        rendered_type = content_type or "missing"
        raise SourceContentError(
            f"Unexpected Content-Type {rendered_type!r} from {source_url}"
        )
    if not response.text.strip():
        raise SourceContentError(f"Empty response body from {source_url}")
    return content_type


def response_redirect_metadata(
    response: requests.Response, requested_url: str
) -> Dict[str, str]:
    final_url = canonicalize_url(str(getattr(response, "url", "") or requested_url))
    requested = canonicalize_url(requested_url)
    if final_url and final_url != requested:
        return {"source_redirect_url": final_url}
    return {}


def fetch_text_with_source_metadata(session: requests.Session, url: str) -> Tuple[str, Dict[str, str]]:
    response = fetch_response(session, url)
    return response.text, response_source_metadata(response)


def fetch_json(session: requests.Session, url: str, headers: Dict[str, str] | None = None) -> Dict[str, object]:
    payload = json.loads(fetch_text(session, url, headers=headers))
    return payload if isinstance(payload, dict) else {}


def github_api_token() -> str:
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        token = os.environ.get(name, "").strip()
        if token:
            return token
    return ""


def github_api_headers() -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = github_api_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def github_raw_url(path: str, ref: str = "main") -> str:
    return GITHUB_RAW_URL_TEMPLATE.format(ref=ref, path=path)


def resolve_github_tag_commit(session: requests.Session, source_ref: str) -> str:
    payload = fetch_json(
        session,
        f"{GITHUB_REPOSITORY_API_URL}/git/ref/tags/{source_ref}",
        headers=github_api_headers(),
    )
    for _ in range(5):
        target = payload.get("object")
        if not isinstance(target, dict):
            raise RuntimeError(f"Tag {source_ref} did not contain an object target")
        target_type = target.get("type")
        if target_type == "commit":
            commit = str(target.get("sha", "")).lower()
            if not re.fullmatch(r"[0-9a-f]{40}", commit):
                raise RuntimeError(f"Tag {source_ref} did not resolve to a full commit")
            return commit
        if target_type != "tag":
            raise RuntimeError(
                f"Tag {source_ref} resolved to unsupported type {target_type!r}"
            )
        target_url = target.get("url")
        if not isinstance(target_url, str) or not target_url.startswith(
            f"{GITHUB_REPOSITORY_API_URL}/git/tags/"
        ):
            raise RuntimeError(f"Tag {source_ref} contained an invalid tag object URL")
        payload = fetch_json(session, target_url, headers=github_api_headers())
    raise RuntimeError(f"Tag {source_ref} exceeded the dereference limit")


def add_cli_release_provenance(
    session: requests.Session,
    files: Sequence[ManagedFile],
    metadata: Dict[str, str],
) -> Tuple[List[ManagedFile], Dict[str, str]]:
    version = metadata.get("codex_cli_version", "")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        raise RuntimeError(f"Cannot resolve a release tag for Codex CLI {version!r}")
    source_ref = f"rust-v{version}"
    source_commit = resolve_github_tag_commit(session, source_ref)
    enriched_metadata = {
        **metadata,
        "codex_cli_release_ref": source_ref,
        "codex_cli_source_commit": source_commit,
    }
    enriched_files = [
        ManagedFile(
            rel_path=item.rel_path,
            source_type=item.source_type,
            source_url=item.source_url,
            content=item.content,
            source_metadata={**(item.source_metadata or {}), **enriched_metadata},
        )
        for item in files
    ]
    return enriched_files, enriched_metadata


def run_local_command(
    args: Sequence[str],
    *,
    cwd: Path | None = None,
    env: Dict[str, str] | None = None,
) -> str:
    try:
        result = subprocess.run(
            list(args),
            cwd=str(cwd) if cwd else None,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        joined = " ".join(args)
        raise RuntimeError(
            f"{joined} timed out after {COMMAND_TIMEOUT_SECONDS:g} seconds"
        ) from exc
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(f"{' '.join(args)} failed with exit code {result.returncode}: {stderr}")
    return result.stdout


def codex_subprocess_env(base: Dict[str, str] | None = None) -> Dict[str, str]:
    env = dict(os.environ if base is None else base)
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        env.pop(name, None)
    return env


def isolated_codex_subprocess_env(
    base: Dict[str, str] | None = None,
) -> Dict[str, str]:
    source = os.environ if base is None else base
    return {key: value for key, value in source.items() if key in SAFE_CODEX_ENV_KEYS}


def parse_codex_cli_version(version_raw: str) -> str:
    match = re.search(r"\b(\d+\.\d+\.\d+(?:[-+][^\s]+)?)\b", version_raw)
    return match.group(1) if match else version_raw.strip()


def encode_dot_path(path: Path) -> str:
    parts = [f"dot_{part[1:]}" if part.startswith(".") else part for part in path.parts]
    return Path(*parts).as_posix()


def source_area_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def developers_source_area(url: str) -> str:
    parsed = urlparse(url)
    segments = [segment for segment in parsed.path.split("/") if segment]
    if not segments:
        return "developers"

    if segments[0] == "cookbook":
        return "cookbook"
    if segments[0] == "blog":
        return "codex_blog"
    if segments[0] == "resources":
        return "resource"
    if segments[0] != "codex":
        return source_area_slug(segments[0]) or "developers"
    if len(segments) == 1:
        return "codex_overview"

    return DEVELOPERS_CODEX_SOURCE_AREAS.get(segments[1], f"codex_{source_area_slug(segments[1])}")


def learn_source_area(url: str) -> str:
    parsed = urlparse(url)
    segments = [segment for segment in parsed.path.split("/") if segment]
    if len(segments) <= 1:
        return "learn_docs"
    return f"learn_{source_area_slug(segments[1])}"


def github_source_area(url: str) -> str:
    parsed = urlparse(url)
    match = re.match(r"^/openai/codex/[^/]+/(.+)$", parsed.path)
    path = match.group(1) if match else parsed.path.lstrip("/")
    if path.startswith("docs/"):
        return "github_docs"
    if path.startswith("codex-cli/"):
        return "github_cli"
    if path.startswith("codex-rs/"):
        return "github_rust"
    return "github_root"


def system_skill_source_area(rel_path: str) -> str:
    skill_rel = rel_path.removeprefix(SYSTEM_SKILL_OUTPUT_PREFIX)
    skill_name = skill_rel.split("/", 1)[0]
    if not skill_name or skill_name.endswith(".marker"):
        return "system_skill_inventory"
    return f"system_skill_{source_area_slug(skill_name)}"


def source_area_for_managed_file(item: ManagedFile) -> str:
    if item.source_type == "developers":
        return developers_source_area(item.source_url)
    if item.source_type == LEARN_SOURCE_TYPE:
        return learn_source_area(item.source_url)
    if item.source_type == "github":
        return github_source_area(item.source_url)
    if item.source_type == PLATFORM_TOOL_GUIDE_SOURCE_TYPE:
        return f"tool_guide_{capability_name_from_tool_guide_url(item.source_url)}"
    if item.source_type == "codex_cli_system_skill":
        return system_skill_source_area(item.rel_path)
    if item.source_type == "codex_cli_prompt_input":
        return "system_prompt"
    if item.source_type == CLI_SURFACE_SOURCE_TYPE:
        return "codex_cli_surface"
    if item.source_type == CAPABILITY_INVENTORY_SOURCE_TYPE:
        return "capability_inventory"
    return source_area_slug(item.source_type) or "unknown"


def add_source_area_metadata(managed_files: Sequence[ManagedFile]) -> List[ManagedFile]:
    enriched: List[ManagedFile] = []
    for item in managed_files:
        metadata = dict(item.source_metadata or {})
        metadata["source_area"] = source_area_for_managed_file(item)
        enriched.append(
            ManagedFile(
                rel_path=item.rel_path,
                source_type=item.source_type,
                source_url=item.source_url,
                content=item.content,
                source_metadata=metadata,
            )
        )
    return enriched


def sanitize_prompt_text(text: str, replacements: Sequence[Tuple[str, str]]) -> str:
    sanitized = text
    for old, new in replacements:
        sanitized = sanitized.replace(old, new)
    sanitized = re.sub(r"<current_date>[^<]+</current_date>", "<current_date>YYYY-MM-DD</current_date>", sanitized)
    sanitized = re.sub(r"<shell>[^<]+</shell>", "<shell>bash</shell>", sanitized)
    sanitized = re.sub(r"<timezone>[^<]+</timezone>", "<timezone>Etc/UTC</timezone>", sanitized)
    return sanitized


def sanitize_prompt_payload(value, replacements: Sequence[Tuple[str, str]]):
    if isinstance(value, str):
        return sanitize_prompt_text(value, replacements)
    if isinstance(value, list):
        return [sanitize_prompt_payload(item, replacements) for item in value]
    if isinstance(value, dict):
        return {
            key: sanitize_prompt_payload(item, replacements)
            for key, item in value.items()
            if key not in PROMPT_VOLATILE_KEYS
        }
    return value


def load_existing_coverage() -> Dict[str, object]:
    if not COVERAGE_PATH.exists():
        return {}

    try:
        payload = json.loads(COVERAGE_PATH.read_text())
    except json.JSONDecodeError:
        LOG.warning("Existing coverage report is invalid JSON and will be recreated")
        return {}

    if isinstance(payload, dict):
        return payload
    return {}


def discover_developers_urls(session: requests.Session) -> Tuple[List[str], Dict[str, object]]:
    LOG.info("Discovering Codex URLs from %s", SITEMAP_INDEX_URL)
    index_xml = fetch_text(session, SITEMAP_INDEX_URL)
    sitemap_urls = parse_sitemap_loc_tags(
        index_xml,
        source_url=SITEMAP_INDEX_URL,
        expected_root="sitemapindex",
    )
    mirrored_urls: set[str] = set()
    codex_related_urls: set[str] = set()
    sitemap_fetch_errors: List[Dict[str, str]] = []

    for sitemap_url in sitemap_urls:
        try:
            sitemap_xml = fetch_text(session, sitemap_url)
            sitemap_page_urls = parse_sitemap_loc_tags(
                sitemap_xml,
                source_url=sitemap_url,
                expected_root="urlset",
            )
        except (requests.RequestException, SourceContentError) as exc:
            LOG.warning("Skipping sitemap %s due to error: %s", sitemap_url, exc)
            sitemap_fetch_errors.append(
                {
                    "source": "developers",
                    "stage": "sitemap_fetch",
                    "state": (
                        "sitemap_unavailable"
                        if isinstance(exc, requests.RequestException)
                        else "extractor_or_malformed_source"
                    ),
                    "url": sitemap_url,
                    "error": str(exc),
                }
            )
            continue

        for raw_url in sitemap_page_urls:
            cleaned = canonicalize_url(raw_url)
            if is_codex_related_developers_url(cleaned):
                codex_related_urls.add(cleaned)
            if keep_developers_url(cleaned):
                mirrored_urls.add(cleaned)

    mirrored_sorted = sorted(mirrored_urls)
    codex_related_sorted = sorted(codex_related_urls)
    skipped_codex_related = sorted(set(codex_related_sorted) - set(mirrored_sorted))
    skipped_codex_related_details: List[Dict[str, str]] = []
    unclassified_skipped_codex_related: List[str] = []
    for skipped_url in skipped_codex_related:
        detail = developers_skipped_url_detail(skipped_url)
        if detail:
            skipped_codex_related_details.append(detail)
        else:
            unclassified_skipped_codex_related.append(skipped_url)

    previous_coverage = load_existing_coverage()
    previous_developers = previous_coverage.get("developers", {})
    previous_codex_related = set()
    previous_mirrored = set()
    previous_unclassified_skipped = set()
    if isinstance(previous_developers, dict):
        previous_codex_related = set(previous_developers.get("codex_related_urls", []))
        previous_mirrored = set(previous_developers.get("mirrored_urls", []))
        previous_unclassified_skipped = set(previous_developers.get("unclassified_skipped_codex_related_urls", []))

    new_codex_related = sorted(set(codex_related_sorted) - previous_codex_related)
    new_mirrored = sorted(set(mirrored_sorted) - previous_mirrored)
    removed_codex_related_candidates = sorted(
        previous_codex_related - set(codex_related_sorted)
    )
    removed_mirrored_candidates = sorted(previous_mirrored - set(mirrored_sorted))
    removed_codex_related = (
        removed_codex_related_candidates if not sitemap_fetch_errors else []
    )
    removed_mirrored = removed_mirrored_candidates if not sitemap_fetch_errors else []
    new_unclassified_skipped = sorted(set(unclassified_skipped_codex_related) - previous_unclassified_skipped)

    LOG.info(
        "Coverage watchdog: codex-related=%d mirrored=%d skipped=%d unclassified=%d",
        len(codex_related_sorted),
        len(mirrored_sorted),
        len(skipped_codex_related),
        len(unclassified_skipped_codex_related),
    )

    if new_codex_related:
        LOG.warning(
            "Coverage watchdog: discovered %d new codex-related URLs. Review filters if needed:\n%s",
            len(new_codex_related),
            "\n".join(f"- {item}" for item in new_codex_related[:30]),
        )
    if new_mirrored:
        LOG.info(
            "Coverage watchdog: newly mirrored %d URLs:\n%s",
            len(new_mirrored),
            "\n".join(f"- {item}" for item in new_mirrored[:30]),
        )

    strict_coverage = os.environ.get("CODEX_DOCS_STRICT_COVERAGE", "0") == "1"
    if strict_coverage and new_unclassified_skipped and not new_mirrored:
        raise RuntimeError(
            "Strict coverage mode failed: new unclassified codex-related URLs were discovered but none were mirrored."
        )

    coverage = {
        "generated_at": now_utc_iso(),
        "source_state_semantics": SOURCE_STATE_SEMANTICS,
        "developers": {
            "sitemap_index_url": SITEMAP_INDEX_URL,
            "sitemap_urls": sitemap_urls,
            "codex_related_urls": codex_related_sorted,
            "mirrored_urls": mirrored_sorted,
            "skipped_codex_related_urls": skipped_codex_related,
            "skipped_codex_related_url_details": skipped_codex_related_details,
            "skipped_codex_related_url_counts_by_classification": count_details_by_classification(
                skipped_codex_related_details
            ),
            "unclassified_skipped_codex_related_urls": unclassified_skipped_codex_related,
            "new_codex_related_urls_since_last_run": new_codex_related,
            "new_mirrored_urls_since_last_run": new_mirrored,
            "new_unclassified_skipped_codex_related_urls_since_last_run": new_unclassified_skipped,
            "removed_codex_related_urls_since_last_run": removed_codex_related,
            "removed_mirrored_urls_since_last_run": removed_mirrored,
            "unconfirmed_removed_urls_due_to_partial_sitemap": (
                removed_codex_related_candidates if sitemap_fetch_errors else []
            ),
            "counts": {
                "sitemap_urls": len(sitemap_urls),
                "codex_related_urls": len(codex_related_sorted),
                "mirrored_urls": len(mirrored_sorted),
                "skipped_codex_related_urls": len(skipped_codex_related),
                "classified_skipped_codex_related_urls": len(skipped_codex_related_details),
                "unclassified_skipped_codex_related_urls": len(unclassified_skipped_codex_related),
                "sitemap_fetch_errors": len(sitemap_fetch_errors),
            },
            "sitemap_fetch_errors": sitemap_fetch_errors,
        },
    }

    return mirrored_sorted, coverage


def is_learn_doc_url(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    return parsed.netloc == "learn.chatgpt.com" and (path == "/docs" or path.startswith("/docs/"))


def discover_learn_urls(
    session: requests.Session,
) -> Tuple[List[str], Dict[str, object], List[Dict[str, str]]]:
    LOG.info("Discovering documentation URLs from %s", LEARN_SITEMAP_INDEX_URL)
    index_xml = fetch_text(session, LEARN_SITEMAP_INDEX_URL)
    sitemap_urls = sorted(
        {
            canonicalize_url(url)
            for url in parse_sitemap_loc_tags(
                index_xml,
                source_url=LEARN_SITEMAP_INDEX_URL,
                expected_root="sitemapindex",
            )
        }
    )

    discovered_urls: set[str] = set()
    sitemap_fetch_errors: List[Dict[str, str]] = []
    for sitemap_url in sitemap_urls:
        try:
            sitemap_xml = fetch_text(session, sitemap_url)
            sitemap_page_urls = parse_sitemap_loc_tags(
                sitemap_xml,
                source_url=sitemap_url,
                expected_root="urlset",
            )
        except (requests.RequestException, SourceContentError) as exc:
            LOG.warning("Skipping Learn sitemap %s due to error: %s", sitemap_url, exc)
            sitemap_fetch_errors.append(
                {
                    "source": LEARN_SOURCE_TYPE,
                    "stage": "sitemap_fetch",
                    "state": (
                        "sitemap_unavailable"
                        if isinstance(exc, requests.RequestException)
                        else "extractor_or_malformed_source"
                    ),
                    "url": sitemap_url,
                    "error": str(exc),
                }
            )
            continue

        for raw_url in sitemap_page_urls:
            cleaned = canonicalize_url(raw_url)
            if is_learn_doc_url(cleaned):
                discovered_urls.add(cleaned)

    discovered_sorted = sorted(discovered_urls)
    previous_coverage = load_existing_coverage()
    previous_learn = previous_coverage.get("learn", {})
    previous_discovered: set[str] = set()
    if isinstance(previous_learn, dict):
        previous_discovered = set(previous_learn.get("discovered_urls", []))
    new_discovered = sorted(set(discovered_sorted) - previous_discovered)
    removed_discovered_candidates = sorted(previous_discovered - set(discovered_sorted))
    removed_discovered = (
        removed_discovered_candidates if not sitemap_fetch_errors else []
    )

    if new_discovered:
        LOG.info(
            "Learn coverage: discovered %d new documentation URLs:\n%s",
            len(new_discovered),
            "\n".join(f"- {item}" for item in new_discovered[:30]),
        )

    coverage = {
        "sitemap_index_url": LEARN_SITEMAP_INDEX_URL,
        "sitemap_urls": sitemap_urls,
        "discovered_urls": discovered_sorted,
        "new_discovered_urls_since_last_run": new_discovered,
        "removed_from_sitemap_urls_since_last_run": removed_discovered,
        "unconfirmed_removed_urls_due_to_partial_sitemap": (
            removed_discovered_candidates if sitemap_fetch_errors else []
        ),
        "sitemap_fetch_errors": sitemap_fetch_errors,
        "counts": {
            "sitemap_urls": len(sitemap_urls),
            "discovered_urls": len(discovered_sorted),
            "sitemap_fetch_errors": len(sitemap_fetch_errors),
        },
    }
    return discovered_sorted, coverage, sitemap_fetch_errors


def developers_url_to_rel_path(url: str) -> str:
    parsed = urlparse(url)
    segments = [segment for segment in parsed.path.split("/") if segment]
    if not segments:
        segments = ["root"]
    path = DEVELOPERS_ROOT.joinpath(*segments, "index.md")
    return str(path.relative_to(DOCS_DIR))


def learn_url_to_rel_path(url: str) -> str:
    parsed = urlparse(url)
    segments = [segment for segment in parsed.path.split("/") if segment]
    if not segments:
        segments = ["root"]
    path = LEARN_ROOT.joinpath(*segments, "index.md")
    return str(path.relative_to(DOCS_DIR))


def platform_url_to_rel_path(url: str) -> str:
    parsed = urlparse(url)
    segments = [segment for segment in parsed.path.split("/") if segment]
    if not segments:
        segments = ["root"]
    root = PLATFORM_ROOT
    if parsed.netloc == "developers.openai.com":
        root = DEVELOPERS_ROOT
    path = root.joinpath(*segments, "index.md")
    return str(path.relative_to(DOCS_DIR))


def platform_markdown_url(url: str) -> str:
    return f"{url.rstrip('/')}.md"


def tool_guide_slug(url: str) -> str:
    return Path(urlparse(url).path.rstrip("/")).name


def tool_guide_aliases(url: str) -> List[str]:
    base_urls = {url.rstrip("/")}
    slug = tool_guide_slug(url)
    if slug.startswith("tools-"):
        base_urls.add(f"https://platform.openai.com/docs/guides/{slug}")
        base_urls.add(f"https://developers.openai.com/api/docs/guides/{slug}")
    aliases: set[str] = set()
    for item in base_urls:
        aliases.add(item)
        aliases.add(platform_markdown_url(item))
    return sorted(aliases)


def strip_mdx_imports(text: str) -> str:
    output: List[str] = []
    skipping_import = False
    for line in text.splitlines():
        stripped = line.strip()
        if not skipping_import and stripped.startswith("import "):
            skipping_import = not stripped.endswith(";")
            continue
        if skipping_import:
            if stripped.endswith(";"):
                skipping_import = False
            continue
        output.append(line)
    return "\n".join(output)


def markdown_with_source(url: str, raw_markdown: str, default_title: str) -> str:
    normalized = normalize_markdown(strip_mdx_imports(raw_markdown))
    lines = normalized.splitlines()
    title = default_title
    body = normalized.strip()
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip() or default_title
        body = "\n".join(lines[1:]).strip()
    return f"# {title}\n\nSource: {url}\n\n{body}\n"


def html_to_markdown(url: str, html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    title = _extract_title(soup)
    main = select_developers_content_root(soup)
    prune_developers_noise(main)

    markdown_body = to_markdown(str(main), heading_style="ATX", bullets="-")
    markdown_body = normalize_markdown(markdown_body)

    if not markdown_body.strip():
        markdown_body = normalize_markdown(main.get_text("\n", strip=True))

    if title:
        heading_pattern = rf"^#\s+{re.escape(title)}\s*\n+"
        markdown_body = re.sub(heading_pattern, "", markdown_body, count=1, flags=re.IGNORECASE)
        markdown_body = normalize_markdown(markdown_body)

    heading = f"# {title or 'Codex Docs'}"
    source_line = f"Source: {url}"
    return f"{heading}\n\n{source_line}\n\n{markdown_body.rstrip()}\n"


def keep_github_markdown_path(path: str) -> bool:
    root_files = {
        "README.md",
        "CHANGELOG.md",
        "AGENTS.md",
        "SECURITY.md",
        "LICENSE",
    }
    if path in root_files:
        return True

    if path.startswith("docs/") and path.endswith(".md"):
        return True

    if path.startswith("codex-cli/") and path.endswith(".md"):
        return True

    if path.startswith("codex-rs/docs/") and path.endswith(".md"):
        return True

    codex_rs_top = {"codex-rs/README.md", "codex-rs/config.md"}
    if path in codex_rs_top:
        return True

    return False


def discover_github_paths(
    session: requests.Session, source_commit: str = "main"
) -> List[str]:
    LOG.info("Discovering markdown files from openai/codex GitHub tree")
    payload = fetch_json(
        session,
        GITHUB_TREE_URL_TEMPLATE.format(ref=source_commit),
        headers=github_api_headers(),
    )
    tree = payload.get("tree", [])

    paths = [
        entry["path"]
        for entry in tree
        if entry.get("type") == "blob" and keep_github_markdown_path(entry.get("path", ""))
    ]
    return sorted(set(paths))


def github_path_to_rel_path(path: str) -> str:
    output_path = GITHUB_ROOT / path
    return str(output_path.relative_to(DOCS_DIR))


def manifest_paths_for_source_type(source_type: str) -> List[str]:
    if not MANIFEST_PATH.exists():
        return []

    try:
        payload = json.loads(MANIFEST_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        LOG.warning("Could not read existing manifest for preserved %s coverage: %s", source_type, exc)
        return []

    sources = payload.get("sources", {})
    if not isinstance(sources, dict):
        return []

    paths: List[str] = []
    for rel_path, entry in sources.items():
        if isinstance(rel_path, str) and isinstance(entry, dict) and entry.get("source_type") == source_type:
            paths.append(rel_path)
    return sorted(paths)


def coverage_paths_for_source(
    current_files: Sequence[ManagedFile],
    source_type: str,
    preserve_missing_sources: set[str],
) -> List[str]:
    paths = {item.rel_path for item in current_files}
    if source_type in preserve_missing_sources:
        paths.update(manifest_paths_for_source_type(source_type))
    return sorted(paths)


def system_skill_path_to_rel_path(path: Path) -> str:
    return f"{SYSTEM_SKILL_OUTPUT_PREFIX}{encode_dot_path(path)}"


def normalize_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n")
    filtered_lines: List[str] = []
    for line in text.split("\n"):
        stripped = line.strip()
        if "/codex/colorcons/" in stripped and "Copied" in stripped:
            without_icons = re.sub(r"!\[[^\]]*\]\(/codex/colorcons/[^)]+\)", "", stripped)
            prompts = [chunk.strip() for chunk in without_icons.split("Copied") if chunk.strip()]
            if prompts:
                filtered_lines.extend(f"- {prompt}" for prompt in prompts)
                continue

        if stripped in NOISY_EXACT_LINES:
            continue
        if any(pattern.match(stripped) for pattern in NOISY_LINE_PATTERNS):
            continue
        filtered_lines.append(line.rstrip())

    deduped_lines: List[str] = []
    for line in filtered_lines:
        if deduped_lines and line.strip() and line == deduped_lines[-1]:
            continue
        deduped_lines.append(line)

    lines = deduped_lines
    normalized = "\n".join(lines)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip() + "\n"


def _extract_title(soup: BeautifulSoup) -> str | None:
    title = None
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    return title


def select_developers_content_root(soup: BeautifulSoup):
    for selector in DEVELOPERS_CONTENT_SELECTORS:
        candidates = soup.select(selector)
        if not candidates:
            continue
        candidate = max(candidates, key=lambda node: len(node.get_text(" ", strip=True)))
        if candidate.get_text(" ", strip=True):
            return candidate
    return soup


def prune_developers_noise(root) -> None:
    for selector in (
        "script",
        "style",
        "noscript",
        "svg",
        "canvas",
        "nav",
        "header",
        "footer",
        "[role='navigation']",
        "[aria-label='Breadcrumb']",
        "button[role='radio']",
        "button[role='menuitemradio']",
    ):
        for node in root.select(selector):
            node.decompose()

    for node in root.select("div.fixed.inset-0.hidden"):
        node.decompose()

    def has_segmented_control_class(tokens) -> bool:
        if not tokens:
            return False
        if isinstance(tokens, str):
            return "SegmentedControlOption" in tokens
        return any("SegmentedControlOption" in token for token in tokens)

    for node in root.find_all(class_=has_segmented_control_class):
        node.decompose()

    for image in root.find_all("img"):
        classes = set(image.get("class") or [])
        if "hidden" in classes and any(token.startswith("dark:") and token.endswith("block") for token in classes):
            image.decompose()


def load_existing_manifest() -> Dict[str, Dict[str, object]]:
    if not MANIFEST_PATH.exists():
        return {}

    try:
        payload = json.loads(MANIFEST_PATH.read_text())
    except json.JSONDecodeError:
        LOG.warning("Existing manifest is invalid JSON and will be recreated")
        return {}

    sources = payload.get("sources", {})
    if not isinstance(sources, dict):
        return {}

    parsed: Dict[str, Dict[str, object]] = {}
    for rel_path, meta in sources.items():
        if isinstance(meta, dict):
            parsed_meta: Dict[str, object] = {}
            for key, value in meta.items():
                if isinstance(value, list):
                    parsed_meta[str(key)] = [str(item) for item in value]
                elif isinstance(value, (str, int, float, bool)):
                    parsed_meta[str(key)] = str(value)
            parsed_meta["sha256"] = str(meta.get("sha256", ""))
            parsed_meta["source_url"] = str(meta.get("source_url", ""))
            parsed_meta["source_type"] = str(meta.get("source_type", ""))
            parsed[rel_path] = parsed_meta
    return parsed


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_file_if_changed(path: Path, content: str | bytes) -> bool:
    if isinstance(content, bytes):
        if path.exists() and path.read_bytes() == content:
            return False

        ensure_parent(path)
        path.write_bytes(content)
        return True

    if path.exists() and path.read_text() == content:
        return False

    ensure_parent(path)
    path.write_text(content)
    return True


def output_path_for_rel_path(rel_path: str) -> Path:
    rel = Path(rel_path)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"Unsafe managed output path: {rel_path}")

    if rel_path.startswith(ROOT_OUTPUT_PREFIXES):
        return ROOT / rel

    return DOCS_DIR / rel


def remove_empty_directories(start: Path) -> None:
    if not start.exists():
        return

    for child in sorted(start.rglob("*"), reverse=True):
        if child.is_dir():
            try:
                child.rmdir()
            except OSError:
                pass


def build_developers_files(
    session: requests.Session,
) -> Tuple[List[ManagedFile], Dict[str, object], List[Dict[str, str]]]:
    managed: List[ManagedFile] = []
    fetch_errors: List[Dict[str, str]] = []
    tombstones: List[Dict[str, object]] = []
    redirects: List[Dict[str, str]] = []
    developers_urls, coverage = discover_developers_urls(session)
    for url in developers_urls:
        try:
            response = fetch_response(
                session, url, allowed_statuses=PERMANENT_MISSING_HTTP_STATUSES
            )
            if response.status_code in PERMANENT_MISSING_HTTP_STATUSES:
                tombstones.append(
                    SourceTombstone(
                        url=url,
                        status_code=response.status_code,
                        endpoint_statuses=(response.status_code,),
                    ).as_coverage()
                )
                continue
            source_metadata = response_source_metadata(response)
            redirect_metadata = response_redirect_metadata(response, url)
            source_metadata.update(redirect_metadata)
            if redirect_metadata:
                redirects.append(
                    {
                        "url": url,
                        "redirect_url": redirect_metadata["source_redirect_url"],
                        "state": "redirected",
                    }
                )
            validate_text_response(
                response,
                source_url=url,
                allowed_content_types={"text/html", "application/xhtml+xml"},
            )
            content = html_to_markdown(url, response.text)
        except requests.RequestException as exc:
            LOG.warning("Skipping developers URL %s due to error: %s", url, exc)
            fetch_errors.append(
                {
                    "source": "developers",
                    "stage": "page_fetch",
                    "state": "transient_page_failure",
                    "url": url,
                    "error": str(exc),
                }
            )
            continue
        except SourceContentError as exc:
            LOG.warning("Skipping malformed developers URL %s: %s", url, exc)
            fetch_errors.append(
                {
                    "source": "developers",
                    "stage": "page_extract",
                    "state": "extractor_or_malformed_source",
                    "url": url,
                    "error": str(exc),
                }
            )
            continue

        rel_path = developers_url_to_rel_path(url)
        managed.append(
            ManagedFile(
                rel_path=rel_path,
                source_type="developers",
                source_url=url,
                content=content,
                source_metadata=source_metadata,
            )
        )

    developers_section = coverage.get("developers", {})
    if isinstance(developers_section, dict):
        developers_section["page_fetch_errors"] = fetch_errors
        developers_section["tombstoned_urls"] = tombstones
        developers_section["redirected_urls"] = redirects
        counts = developers_section.get("counts", {})
        if isinstance(counts, dict):
            counts["page_fetch_errors"] = len(fetch_errors)
            counts["tombstoned_urls"] = len(tombstones)
            counts["redirected_urls"] = len(redirects)
        else:
            developers_section["counts"] = {"page_fetch_errors": len(fetch_errors)}

    return managed, coverage, fetch_errors


def fetch_learn_page(
    session: requests.Session,
    url: str,
) -> Tuple[str, Dict[str, object], str]:
    markdown_url = f"{url}.md"
    markdown_response = fetch_response(
        session, markdown_url, allowed_statuses=PERMANENT_MISSING_HTTP_STATUSES
    )
    content_type = response_content_type(markdown_response)
    markdown_missing = markdown_response.status_code in PERMANENT_MISSING_HTTP_STATUSES
    if not markdown_missing and content_type in {"text/markdown", "text/plain"}:
        validate_text_response(
            markdown_response,
            source_url=markdown_url,
            allowed_content_types={"text/markdown", "text/plain"},
        )
        metadata: Dict[str, object] = response_source_metadata(markdown_response)
        metadata.update(response_redirect_metadata(markdown_response, markdown_url))
        metadata["source_kind"] = "learn_markdown"
        content = markdown_with_source(url, markdown_response.text, default_title="ChatGPT Learn Docs")
        return content, metadata, "markdown"

    if not markdown_missing:
        LOG.info("Learn Markdown endpoint returned %s for %s; using HTML fallback", content_type or "unknown", url)

    html_response = fetch_response(
        session, url, allowed_statuses=PERMANENT_MISSING_HTTP_STATUSES
    )
    if html_response.status_code in PERMANENT_MISSING_HTTP_STATUSES:
        if not markdown_missing:
            raise SourceContentError(
                f"HTML representation returned HTTP {html_response.status_code} for {url}, "
                f"but {markdown_url} remained available with unexpected Content-Type "
                f"{(content_type or 'missing')!r}"
            )
        raise SourceTombstone(
            url=url,
            status_code=html_response.status_code,
            endpoint_statuses=(markdown_response.status_code, html_response.status_code),
        )
    validate_text_response(
        html_response,
        source_url=url,
        allowed_content_types={"text/html", "application/xhtml+xml"},
    )
    metadata = response_source_metadata(html_response)
    metadata.update(response_redirect_metadata(html_response, url))
    metadata["source_kind"] = "learn_html_fallback"
    return html_to_markdown(url, html_response.text), metadata, "html_fallback"


def build_learn_files(
    session: requests.Session,
) -> Tuple[List[ManagedFile], Dict[str, object], List[Dict[str, str]]]:
    managed: List[ManagedFile] = []
    learn_urls, coverage, sitemap_fetch_errors = discover_learn_urls(session)
    fetch_errors = list(sitemap_fetch_errors)
    mirrored_urls: List[str] = []
    markdown_urls: List[str] = []
    html_fallback_urls: List[str] = []
    page_fetch_errors: List[Dict[str, str]] = []
    tombstones: List[Dict[str, object]] = []
    redirects: List[Dict[str, str]] = []

    for url in learn_urls:
        try:
            content, source_metadata, fetch_mode = fetch_learn_page(session, url)
        except SourceTombstone as tombstone:
            LOG.info(
                "Recording sitemap tombstone for Learn URL %s (HTTP %d)",
                url,
                tombstone.status_code,
            )
            tombstones.append(tombstone.as_coverage())
            continue
        except requests.RequestException as exc:
            LOG.warning("Skipping Learn URL %s due to error: %s", url, exc)
            failure = {
                "source": LEARN_SOURCE_TYPE,
                "stage": "page_fetch",
                "state": "transient_page_failure",
                "url": url,
                "error": str(exc),
            }
            page_fetch_errors.append(failure)
            fetch_errors.append(failure)
            continue
        except SourceContentError as exc:
            LOG.warning("Skipping malformed Learn URL %s: %s", url, exc)
            failure = {
                "source": LEARN_SOURCE_TYPE,
                "stage": "page_extract",
                "state": "extractor_or_malformed_source",
                "url": url,
                "error": str(exc),
            }
            page_fetch_errors.append(failure)
            fetch_errors.append(failure)
            continue

        mirrored_urls.append(url)
        redirect_url = source_metadata.get("source_redirect_url")
        if isinstance(redirect_url, str) and redirect_url:
            redirects.append(
                {"url": url, "redirect_url": redirect_url, "state": "redirected"}
            )
        if fetch_mode == "markdown":
            markdown_urls.append(url)
        else:
            html_fallback_urls.append(url)
        managed.append(
            ManagedFile(
                rel_path=learn_url_to_rel_path(url),
                source_type=LEARN_SOURCE_TYPE,
                source_url=url,
                content=content,
                source_metadata=source_metadata,
            )
        )

    coverage["mirrored_urls"] = mirrored_urls
    coverage["markdown_urls"] = markdown_urls
    coverage["html_fallback_urls"] = html_fallback_urls
    coverage["page_fetch_errors"] = page_fetch_errors
    coverage["tombstoned_urls"] = tombstones
    coverage["redirected_urls"] = redirects
    counts = coverage.get("counts", {})
    if not isinstance(counts, dict):
        counts = {}
        coverage["counts"] = counts
    counts.update(
        {
            "mirrored_urls": len(mirrored_urls),
            "markdown_pages": len(markdown_urls),
            "html_fallback_pages": len(html_fallback_urls),
            "page_fetch_errors": len(page_fetch_errors),
            "tombstoned_urls": len(tombstones),
            "redirected_urls": len(redirects),
        }
    )
    return managed, coverage, fetch_errors


def build_github_files(
    session: requests.Session,
    source_ref: str = "main",
    source_commit: str = "main",
) -> Tuple[List[ManagedFile], List[Dict[str, str]]]:
    managed: List[ManagedFile] = []
    fetch_errors: List[Dict[str, str]] = []

    for path in discover_github_paths(session, source_commit):
        raw_url = github_raw_url(path, source_commit)
        try:
            raw_text, source_metadata = fetch_text_with_source_metadata(session, raw_url)
        except requests.RequestException as exc:
            LOG.warning("Skipping GitHub path %s due to error: %s", path, exc)
            fetch_errors.append(
                {
                    "source": "github",
                    "stage": "page_fetch",
                    "state": "transient_page_failure",
                    "url": raw_url,
                    "error": str(exc),
                }
            )
            continue

        rel_path = github_path_to_rel_path(path)
        content = normalize_markdown(raw_text)
        managed.append(
            ManagedFile(
                rel_path=rel_path,
                source_type="github",
                source_url=raw_url,
                content=content,
                source_metadata={
                    **source_metadata,
                    "upstream_source_ref": source_ref,
                    "upstream_source_commit": source_commit,
                },
            )
        )

    return managed, fetch_errors


def referenced_platform_tool_guides(source_files: Sequence[ManagedFile]) -> Dict[str, List[str]]:
    referenced: Dict[str, set[str]] = {}
    for item in source_files:
        if isinstance(item.content, bytes):
            text = item.content.decode("utf-8", errors="ignore")
        else:
            text = item.content
        for url in PLATFORM_TOOL_GUIDE_URLS:
            if any(alias in text for alias in tool_guide_aliases(url)):
                referenced.setdefault(url, set()).add(item.rel_path)
    return {url: sorted(paths) for url, paths in sorted(referenced.items())}


def build_platform_tool_guide_files(
    session: requests.Session,
    source_files: Sequence[ManagedFile],
) -> Tuple[List[ManagedFile], List[Dict[str, str]], Dict[str, List[str]]]:
    managed: List[ManagedFile] = []
    fetch_errors: List[Dict[str, str]] = []
    referenced_by_url = referenced_platform_tool_guides(source_files)
    referenced_urls = sorted(referenced_by_url)
    if not referenced_urls:
        return managed, fetch_errors, referenced_by_url

    LOG.info("Mirroring %d linked tool guide(s)", len(referenced_urls))
    for url in referenced_urls:
        fetch_url = platform_markdown_url(url)
        try:
            raw_markdown, source_metadata = fetch_text_with_source_metadata(session, fetch_url)
        except requests.RequestException as exc:
            LOG.warning("Skipping platform tool guide %s due to error: %s", url, exc)
            fetch_errors.append(
                {
                    "source": PLATFORM_TOOL_GUIDE_SOURCE_TYPE,
                    "stage": "page_fetch",
                    "state": "transient_page_failure",
                    "url": fetch_url,
                    "error": str(exc),
                }
            )
            continue

        managed.append(
            ManagedFile(
                rel_path=platform_url_to_rel_path(url),
                source_type=PLATFORM_TOOL_GUIDE_SOURCE_TYPE,
                source_url=url,
                content=markdown_with_source(url, raw_markdown, default_title="Platform Tool Guide"),
                source_metadata=source_metadata,
            )
        )

    return managed, fetch_errors, referenced_by_url


def managed_file_text(item: ManagedFile) -> str:
    if isinstance(item.content, bytes):
        return item.content.decode("utf-8", errors="replace")
    return item.content


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        if value[0] == '"':
            try:
                unquoted = str(json.loads(value))
                while '\\"' in unquoted:
                    unquoted = unquoted.replace('\\"', '"')
                return unquoted
            except json.JSONDecodeError:
                pass
        unquoted = value[1:-1]
        if value[0] == "'":
            unquoted = unquoted.replace("''", "'")
        while '\\"' in unquoted:
            unquoted = unquoted.replace('\\"', '"')
        return unquoted
    return value


def parse_simple_frontmatter(text: str) -> Dict[str, str]:
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        return {}
    parsed: Dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in {"name", "description"}:
            parsed[key] = strip_quotes(value)
    return parsed


FRONTMATTER_METADATA_ORDER = (
    "source_type",
    "source_area",
    "source_url",
    "source_kind",
    "source_last_modified",
    "source_etag",
    "source_redirect_url",
    "upstream_source_ref",
    "upstream_source_commit",
    "codex_cli_versions",
    "codex_cli_versions_raw",
    "codex_cli_release_ref",
    "codex_cli_source_commit",
    "report_date",
    "name",
    "description",
)
PRESERVED_FRONTMATTER_SOURCE_KEYS = (
    "source_last_modified",
    "source_etag",
    "source_redirect_url",
)
PRESERVED_MANIFEST_SOURCE_KEYS = ("source_last_modified", "source_etag")


def parse_frontmatter_block(block: str) -> Dict[str, object]:
    parsed: Dict[str, object] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key:
            stripped = value.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                try:
                    parsed[key] = [str(item) for item in json.loads(stripped)]
                    continue
                except json.JSONDecodeError:
                    pass
            parsed[key] = strip_quotes(value)
    return parsed


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


def existing_version_values(
    metadata: Dict[str, object],
    list_key: str,
    legacy_keys: Sequence[str],
) -> List[str]:
    values = metadata_values(metadata.get(list_key))
    for key in legacy_keys:
        raw_value = metadata.get(key)
        for item in metadata_values(raw_value):
            values = append_unique(values, item)
    return values


def codex_cli_version_history_metadata(
    existing_metadata: Dict[str, object],
    codex_cli_metadata: Dict[str, str],
) -> Dict[str, List[str]]:
    version = codex_cli_metadata.get("codex_cli_version", "")
    versions = existing_version_values(
        existing_metadata,
        "codex_cli_versions",
        ("codex_cli_version", "captured_with_codex_cli_version"),
    )
    versions = append_unique(versions, version)

    version_raw = codex_cli_metadata.get("codex_cli_version_raw", "")
    raw_versions = existing_version_values(
        existing_metadata,
        "codex_cli_versions_raw",
        ("codex_cli_version_raw", "captured_with_codex_cli_version_raw"),
    )
    raw_versions = append_unique(raw_versions, version_raw)

    history: Dict[str, List[str]] = {}
    if versions:
        history["codex_cli_versions"] = versions
    if raw_versions:
        history["codex_cli_versions_raw"] = raw_versions
    return history


def split_markdown_frontmatter(text: str) -> Tuple[Dict[str, object], str]:
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


def markdown_frontmatter_metadata(
    item: ManagedFile,
    codex_cli_metadata: Dict[str, str],
) -> Tuple[Dict[str, object], Dict[str, object]]:
    source_metadata = dict(item.source_metadata or {})
    frontmatter: Dict[str, object] = {
        "source_type": item.source_type,
        "source_url": item.source_url,
    }
    for key in (
        "source_area",
        "source_kind",
        "source_last_modified",
        "source_etag",
        "source_redirect_url",
        "upstream_source_ref",
        "upstream_source_commit",
        "codex_cli_release_ref",
        "codex_cli_source_commit",
    ):
        if source_metadata.get(key):
            frontmatter[key] = source_metadata[key]

    for key in (
        "source_area",
        "source_kind",
        "source_last_modified",
        "source_etag",
        "source_redirect_url",
        "upstream_source_ref",
        "upstream_source_commit",
        "codex_cli_release_ref",
        "codex_cli_source_commit",
    ):
        if frontmatter.get(key):
            source_metadata[key] = frontmatter[key]
    return frontmatter, source_metadata


def apply_codex_version_history(
    metadata: Dict[str, object],
    source_metadata: Dict[str, object],
    existing_metadata: Dict[str, object],
    codex_cli_metadata: Dict[str, str],
) -> None:
    history = codex_cli_version_history_metadata(existing_metadata, codex_cli_metadata)
    metadata.update(history)
    source_metadata.update(history)


def annotate_markdown_file(item: ManagedFile, codex_cli_metadata: Dict[str, str]) -> ManagedFile:
    raw_text = managed_file_text(item)
    source_frontmatter, body = split_markdown_frontmatter(raw_text)
    metadata, source_metadata = markdown_frontmatter_metadata(item, codex_cli_metadata)

    existing_path = output_path_for_rel_path(item.rel_path)
    existing_frontmatter: Dict[str, object] = {}
    if existing_path.exists():
        existing_frontmatter, existing_body = split_markdown_frontmatter(existing_path.read_text())
        if existing_body == body:
            for key in PRESERVED_FRONTMATTER_SOURCE_KEYS:
                if existing_frontmatter.get(key):
                    metadata[key] = existing_frontmatter[key]
                    source_metadata[key] = existing_frontmatter[key]

    # Web content is not generated by the installed CLI. Freeze historical
    # observation lists in place; new release observations live in the ledger.
    history_context = (
        {} if item.source_type in {"developers", LEARN_SOURCE_TYPE, PLATFORM_TOOL_GUIDE_SOURCE_TYPE}
        else codex_cli_metadata
    )
    apply_codex_version_history(metadata, source_metadata, existing_frontmatter, history_context)

    merged_frontmatter = dict(metadata)
    for key, value in source_frontmatter.items():
        if key not in merged_frontmatter:
            merged_frontmatter[key] = value

    return ManagedFile(
        rel_path=item.rel_path,
        source_type=item.source_type,
        source_url=item.source_url,
        content=format_frontmatter(merged_frontmatter, body),
        source_metadata=source_metadata or item.source_metadata,
    )


def annotate_markdown_files(
    managed_files: Sequence[ManagedFile],
    codex_cli_metadata: Dict[str, str],
) -> List[ManagedFile]:
    annotated: List[ManagedFile] = []
    for item in managed_files:
        if item.rel_path.endswith(".md"):
            annotated.append(annotate_markdown_file(item, codex_cli_metadata))
        else:
            annotated.append(item)
    return annotated


def markdown_title(text: str, default: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip() or default
    return default


def capability_name_from_tool_guide_url(url: str) -> str:
    slug = tool_guide_slug(url)
    if slug.startswith("tools-"):
        slug = slug[len("tools-") :]
    return slug.replace("-", "_")


def capability_counts(capabilities: Sequence[Dict[str, object]]) -> Dict[str, object]:
    by_category: Dict[str, int] = {}
    by_maturity: Dict[str, int] = {}
    active = 0
    for item in capabilities:
        category = str(item.get("category", "unknown"))
        by_category[category] = by_category.get(category, 0) + 1
        maturity = str(item.get("maturity", ""))
        if maturity:
            by_maturity[maturity] = by_maturity.get(maturity, 0) + 1
        if item.get("active", True):
            active += 1
    return {
        "total": len(capabilities),
        "active": active,
        "inactive": len(capabilities) - active,
        "by_category": {key: by_category[key] for key in sorted(by_category)},
        "by_maturity": {key: by_maturity[key] for key in sorted(by_maturity)},
    }


def load_existing_capability_inventory() -> Dict[str, object]:
    if not CAPABILITIES_PATH.exists():
        return {}
    try:
        payload = json.loads(CAPABILITIES_PATH.read_text())
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def existing_capabilities_by_id(payload: Dict[str, object]) -> Dict[str, Dict[str, object]]:
    capabilities = payload.get("capabilities", []) if isinstance(payload, dict) else []
    if not isinstance(capabilities, list):
        return {}
    return {
        str(item["id"]): item
        for item in capabilities
        if isinstance(item, dict) and item.get("id")
    }


def cli_release_observation(entry: Dict[str, object]) -> Dict[str, str]:
    """Read the last positive observation, never the inventory's latest environment."""
    observation: Dict[str, str] = {}
    for evidence in entry.get("provenance", []):
        if not isinstance(evidence, dict):
            continue
        if evidence.get("evidence_type") == "installed_cli_observation":
            for key in ("os", "arch", "codex_cli_version"):
                observation[key] = str(evidence.get(key, ""))
        elif evidence.get("evidence_type") == "github_release_metadata":
            observation["source_commit"] = str(evidence.get("source_commit", ""))
            observation["source_ref"] = str(evidence.get("source", ""))
    return observation


def resolve_cli_release_ancestry(
    session: requests.Session, inventory: Dict[str, object], current_commit: str
) -> Dict[str, str]:
    """Resolve immutable commit pairs before transforming capabilities.

    API failures only withhold removal evidence; they cannot imply removal.
    Cache each pair within the transaction, including unknown results.
    """
    result: Dict[str, str] = {}
    for entry in existing_capabilities_by_id(inventory).values():
        if entry.get("source_type") != CLI_SURFACE_SOURCE_TYPE:
            continue
        previous_commit = cli_release_observation(entry).get("source_commit", "")
        if previous_commit in result:
            continue
        result[previous_commit] = "unknown"
        if not all(re.fullmatch(r"[0-9a-f]{40}", value) for value in (previous_commit, current_commit)):
            continue
        if previous_commit == current_commit:
            result[previous_commit] = "ancestor"
            continue
        try:
            comparison = fetch_json(
                session,
                f"{GITHUB_REPOSITORY_API_URL}/compare/{previous_commit}...{current_commit}",
                headers=github_api_headers(),
            )
            status = comparison.get("status")
            if status in {"ahead", "identical"}:
                result[previous_commit] = "ancestor"
            elif status in {"diverged", "behind"}:
                result[previous_commit] = "not_ancestor"
        except (requests.RequestException, ValueError, RuntimeError) as exc:
            LOG.warning("Release ancestry unavailable for %s: %s", previous_commit, exc)
    return result


def cli_absence_reason(
    entry: Dict[str, object], current_environment: Dict[str, str],
    current_version: str, ancestry: Dict[str, str],
) -> str:
    previous = cli_release_observation(entry)
    if any(not previous.get(key) or previous[key] != current_environment.get(key)
           for key in ("os", "arch")):
        return "different_or_unknown_platform"
    previous_version = previous.get("codex_cli_version", "")
    if not all(re.fullmatch(r"\d+\.\d+\.\d+", value)
               for value in (previous_version, current_version)):
        return "unknown_release_order"
    if tuple(map(int, current_version.split("."))) <= tuple(map(int, previous_version.split("."))):
        return "not_newer_release"
    relationship = ancestry.get(previous.get("source_commit", ""), "unknown")
    if relationship == "not_ancestor":
        return "divergent_release_lineage"
    if relationship != "ancestor":
        return "unknown_release_lineage"
    return ""


def model_catalog_coverage(metadata: Dict[str, str]) -> Dict[str, str]:
    return {
        "version": metadata.get("codex_cli_version", ""),
        "source_ref": metadata.get("codex_cli_release_ref", ""),
        "source_commit": metadata.get("codex_cli_source_commit", ""),
        "source_path": model_catalog.SOURCE_PATH,
        "status": "complete",
    }


def build_model_catalog_file(session: requests.Session, metadata: Dict[str, str]) -> ManagedFile:
    commit = metadata.get("codex_cli_source_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Model catalog requires resolved release provenance")
    url = github_raw_url(model_catalog.SOURCE_PATH, commit)
    payload = model_catalog.snapshot(
        fetch_json(session, url), version=metadata.get("codex_cli_version", ""),
        source_ref=metadata.get("codex_cli_release_ref", ""), source_commit=commit,
    )
    return ManagedFile(
        rel_path=MODELS_REL_PATH, source_type=MODEL_SOURCE_TYPE, source_url=url,
        content=json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        source_metadata={**metadata, "source_kind": "release_bundled_model_catalog", "source_area": "models"},
    )


def historical_cli_observations() -> Dict[str, object]:
    """One-time migration: recover each platform's most recent recorded help snapshot."""
    surfaces = {}
    if not (ROOT / ".git").exists():
        return surfaces
    commits = run_local_command([
        "git", "log", "-20", "--format=%H", "--", "docs/codex_cli_surface.json",
    ], cwd=ROOT).splitlines()
    for commit in commits:
        payload = json.loads(run_local_command(["git", "show", f"{commit}:docs/codex_cli_surface.json"], cwd=ROOT))
        if not payload.get("observation_environment"):
            continue
        key = cli_observations.platform_key(payload)
        if key in surfaces:
            continue
        manifest = json.loads(run_local_command(["git", "show", f"{commit}:docs/docs_manifest.json"], cwd=ROOT))
        provenance = manifest.get("sources", {}).get(CLI_SURFACE_REL_PATH, {})
        if not provenance.get("codex_cli_source_commit"):
            continue
        payload.update(source_ref=provenance.get("codex_cli_release_ref", ""), source_commit=provenance["codex_cli_source_commit"])
        surfaces[key] = cli_observations.validate(payload)
        if any(key.startswith("linux-") for key in surfaces) and any(key.startswith("macos-") for key in surfaces):
            break
    return surfaces


def prepare_cli_observations(
    files: Sequence[ManagedFile], metadata: Dict[str, str], observations_dir: Path | None = None,
) -> Tuple[List[ManagedFile], Dict[str, Dict[str, str]]]:
    surfaces = {}
    directory = DOCS_DIR / "cli-surface"
    if directory.exists():
        for path in sorted(directory.glob("*.json")):
            payload = cli_observations.validate(json.loads(path.read_text()))
            key = cli_observations.platform_key(payload)
            if path.stem != key:
                raise ValueError("Stored CLI observation filename does not match its platform")
            surfaces[key] = payload
    if not surfaces:
        surfaces.update(historical_cli_observations())
    # Bootstrap repositories without accessible Git history from the current snapshot.
    if not surfaces and CLI_SURFACE_PATH.exists():
        previous = json.loads(CLI_SURFACE_PATH.read_text())
        provenance = load_existing_manifest().get(CLI_SURFACE_REL_PATH, {})
        if previous.get("observation_environment") and provenance.get("codex_cli_source_commit"):
            previous.update(source_ref=provenance.get("codex_cli_release_ref", ""),
                            source_commit=provenance["codex_cli_source_commit"])
            cli_observations.validate(previous)
            surfaces[cli_observations.platform_key(previous)] = previous
    incoming = [json.loads(managed_file_text(item)) for item in files if item.source_type == CLI_SURFACE_SOURCE_TYPE]
    for payload in incoming:
        payload.update(source_ref=metadata["codex_cli_release_ref"], source_commit=metadata["codex_cli_source_commit"])
    if observations_dir is not None:
        for path in sorted(observations_dir.glob("*.json")):
            payload = cli_observations.validate(json.loads(path.read_text()))
            if payload["codex_cli_version"] != metadata["codex_cli_version"]:
                LOG.warning("Ignoring CLI artifact from a different release: %s", path.name)
                continue
            if payload["source_commit"] != metadata["codex_cli_source_commit"]:
                raise ValueError("CLI artifact does not match the resolved release commit")
            incoming.append(payload)
    for payload in incoming:
        cli_observations.validate(payload)
        key = cli_observations.platform_key(payload)
        prior = surfaces.get(key)
        if prior and tuple(map(int, prior["codex_cli_version"].split("."))) > tuple(map(int, payload["codex_cli_version"].split("."))):
            raise ValueError("Refusing to replace a newer platform observation with an older CLI")
        surfaces[key] = payload
    combined = cli_observations.aggregate(surfaces, metadata)
    result = [item for item in files if item.source_type != CLI_SURFACE_SOURCE_TYPE]
    for key, payload in sorted(surfaces.items()):
        result.append(ManagedFile(
            f"cli-surface/{key}.json", CLI_PLATFORM_SOURCE_TYPE, "codex-cli://help",
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            {"codex_cli_version": payload["codex_cli_version"], "codex_cli_release_ref": payload["source_ref"],
             "codex_cli_source_commit": payload["source_commit"], "source_kind": "installed_cli_observation"},
        ))
    result.append(ManagedFile(
        CLI_SURFACE_REL_PATH, CLI_SURFACE_SOURCE_TYPE, "generated://cli-platform-union",
        json.dumps(combined, indent=2, sort_keys=True) + "\n",
        {**metadata, "source_kind": "aggregated_cli_observation"},
    ))
    return result, combined["platform_observations"]


def previous_cli_platforms(entry: Dict[str, object]) -> Dict[str, object]:
    if isinstance(entry.get("platforms"), dict):
        return entry["platforms"]
    observation = cli_release_observation(entry)
    try:
        key = cli_observations.platform_key(observation)
    except ValueError:
        key = "unknown"
    if not entry:
        return {}
    return {key: {"status": "present" if entry.get("active", True) else "absent",
                  "active": entry.get("active", True), "last_seen": observation}}


def resolve_platform_ancestry(session: requests.Session, inventory: Dict[str, object], observations: dict) -> dict:
    result = {}
    for platform, current in observations.items():
        entries = []
        for identifier, entry in existing_capabilities_by_id(inventory).items():
            if entry.get("source_type") != CLI_SURFACE_SOURCE_TYPE:
                continue
            previous = previous_cli_platforms(entry).get(platform, {}).get("last_seen", {})
            if previous:
                entries.append({"id": identifier, "source_type": CLI_SURFACE_SOURCE_TYPE, "provenance": [
                    {"evidence_type": "github_release_metadata", "source_commit": previous.get("source_commit", "")},
                ]})
        resolved = resolve_cli_release_ancestry(session, {"capabilities": entries}, current["source_commit"])
        result.update({f"{commit}...{current['source_commit']}": status for commit, status in resolved.items()})
    return result


def build_capability_inventory_file(
    codex_cli_files: Sequence[ManagedFile],
    platform_tool_guide_files: Sequence[ManagedFile],
    referenced_platform_tool_guides_by_url: Dict[str, List[str]],
    codex_cli_metadata: Dict[str, str],
    documentation_files: Sequence[ManagedFile] = (),
    release_ancestry: Dict[str, str] | None = None,
    feature_snapshot_payload: Dict[str, object] | None = None,
    platform_ancestry: Dict[str, str] | None = None,
) -> ManagedFile:
    capabilities: List[Dict[str, object]] = []
    codex_cli_version = codex_cli_metadata.get("codex_cli_version", "")
    codex_cli_version_raw = codex_cli_metadata.get("codex_cli_version_raw", "")
    previous_inventory = load_existing_capability_inventory()
    previous_capabilities = existing_capabilities_by_id(previous_inventory)
    current_cli_observation: Dict[str, str] = {}
    platform_observations: Dict[str, object] = {}
    cli_present_on: Dict[str, object] = {}
    for item in codex_cli_files:
        if item.source_type != CLI_SURFACE_SOURCE_TYPE:
            continue
        try:
            surface_payload = json.loads(managed_file_text(item))
        except json.JSONDecodeError:
            continue
        platform_observations = surface_payload.get("platform_observations", {})
        observation_environment = surface_payload.get("observation_environment", {})
        if isinstance(observation_environment, dict):
            current_cli_observation = {
                key: str(observation_environment[key])
                for key in ("os", "arch")
                if observation_environment.get(key)
            }
        break

    def cli_provenance(command: str) -> List[Dict[str, str]]:
        provenance = [
            {
                "evidence_type": "installed_cli_observation",
                "source": command,
                "codex_cli_version": codex_cli_version,
                **current_cli_observation,
            }
        ]
        source_commit = codex_cli_metadata.get("codex_cli_source_commit", "")
        source_ref = codex_cli_metadata.get("codex_cli_release_ref", "")
        if source_commit and source_ref:
            provenance.append(
                {
                    "evidence_type": "github_release_metadata",
                    "source": source_ref,
                    "source_commit": source_commit,
                }
            )
        return provenance

    def docs_provenance(item: ManagedFile) -> List[Dict[str, str]]:
        return [
            {
                "evidence_type": "official_documentation",
                "source_url": item.source_url,
                "mirrored_path": item.rel_path,
            }
        ]

    def add_source_area(entry: Dict[str, object], item: ManagedFile) -> None:
        if item.source_metadata and item.source_metadata.get("source_area"):
            entry["source_area"] = item.source_metadata["source_area"]

    def preserve_source_last_modified_when_etag_matches(entry: Dict[str, object]) -> None:
        previous_entry = previous_capabilities.get(str(entry.get("id", "")), {})
        if not previous_entry:
            return
        if not entry.get("source_etag") or previous_entry.get("source_etag") != entry.get("source_etag"):
            return
        if previous_entry.get("source_last_modified"):
            entry["source_last_modified"] = previous_entry["source_last_modified"]

    def add_version_history(entry: Dict[str, object]) -> None:
        history = codex_cli_version_history_metadata(
            previous_capabilities.get(str(entry.get("id", "")), {}),
            codex_cli_metadata,
        )
        entry.update(history)

    for item in sorted(codex_cli_files, key=lambda entry: entry.rel_path):
        if item.source_type != "codex_cli_system_skill" or not item.rel_path.endswith("/SKILL.md"):
            continue
        skill_rel = item.rel_path.removeprefix(SYSTEM_SKILL_OUTPUT_PREFIX)
        skill_dir = skill_rel.rsplit("/", 1)[0]
        metadata = parse_simple_frontmatter(managed_file_text(item))
        name = metadata.get("name") or Path(skill_dir).name
        entry: Dict[str, object] = {
            "id": f"system_skill:{name}",
            "name": name,
            "category": "system_skill",
            "source_type": item.source_type,
            "source_url": item.source_url,
            "mirrored_path": item.rel_path,
            "first_seen_path": item.rel_path,
            "provenance": cli_provenance("codex debug prompt-input"),
        }
        add_source_area(entry, item)
        if metadata.get("description"):
            entry["description"] = metadata["description"]
        if codex_cli_version:
            entry["codex_cli_version"] = codex_cli_version
        if codex_cli_version_raw:
            entry["codex_cli_version_raw"] = codex_cli_version_raw
        add_version_history(entry)
        capabilities.append(entry)

    for item in sorted(codex_cli_files, key=lambda entry: entry.rel_path):
        if item.source_type != "codex_cli_prompt_input":
            continue
        roles: List[str] = []
        message_count = 0
        try:
            payload = json.loads(managed_file_text(item))
            if isinstance(payload, list):
                message_count = len(payload)
                roles = sorted({str(entry.get("role")) for entry in payload if isinstance(entry, dict) and entry.get("role")})
        except json.JSONDecodeError:
            roles = []
        entry = {
            "id": "system_prompt:prompt-input",
            "name": "prompt-input",
            "category": "system_prompt_snapshot",
            "source_type": item.source_type,
            "source_url": item.source_url,
            "mirrored_path": item.rel_path,
            "first_seen_path": item.rel_path,
            "message_count": message_count,
            "roles": roles,
            "provenance": cli_provenance("codex debug prompt-input"),
        }
        add_source_area(entry, item)
        if codex_cli_version:
            entry["codex_cli_version"] = codex_cli_version
        if codex_cli_version_raw:
            entry["codex_cli_version_raw"] = codex_cli_version_raw
        add_version_history(entry)
        capabilities.append(entry)

    for item in sorted(platform_tool_guide_files, key=lambda entry: entry.rel_path):
        name = capability_name_from_tool_guide_url(item.source_url)
        referenced_from = referenced_platform_tool_guides_by_url.get(item.source_url, [])
        entry = {
            "id": f"tool_guide:{name}",
            "name": name,
            "title": markdown_title(managed_file_text(item), default=name.replace("_", " ").title()),
            "category": "linked_tool_guide",
            "source_type": item.source_type,
            "source_url": item.source_url,
            "mirrored_path": item.rel_path,
            "first_seen_path": referenced_from[0] if referenced_from else item.rel_path,
            "referenced_from": referenced_from,
            "provenance": docs_provenance(item),
        }
        add_source_area(entry, item)
        for key in ("source_last_modified", "source_etag"):
            if item.source_metadata and item.source_metadata.get(key):
                entry[key] = item.source_metadata[key]
        preserve_source_last_modified_when_etag_matches(entry)
        if codex_cli_version:
            entry["codex_cli_version"] = codex_cli_version
        if codex_cli_version_raw:
            entry["codex_cli_version_raw"] = codex_cli_version_raw
        add_version_history(entry)
        capabilities.append(entry)

    for item in sorted(codex_cli_files, key=lambda entry: entry.rel_path):
        if item.source_type != CLI_SURFACE_SOURCE_TYPE:
            continue
        try:
            surface = json.loads(managed_file_text(item))
        except json.JSONDecodeError:
            continue
        if not isinstance(surface, dict):
            continue

        def add_cli_option(option: Dict[str, object], command: str) -> None:
            primary_flag = str(option.get("primary_flag", ""))
            if not primary_flag:
                return
            identifier_scope = command.replace(" ", ":")
            option_entry: Dict[str, object] = {
                "id": f"cli_option:{identifier_scope}:{primary_flag}",
                "name": primary_flag,
                "category": "cli_option",
                "cli_command": command,
                "cli_flags": option.get("flags", []),
                "synopsis": str(option.get("synopsis", "")),
                "description": str(option.get("description", "")),
                "source_type": item.source_type,
                "source_url": item.source_url,
                "mirrored_path": item.rel_path,
                "provenance": cli_provenance(f"{command} --help"),
            }
            cli_present_on[option_entry["id"]] = option.get("observed_on", {})
            config_keys = CLI_OPTION_CONFIG_KEYS.get(primary_flag, [])
            if config_keys:
                option_entry["config_keys"] = config_keys
            add_version_history(option_entry)
            capabilities.append(option_entry)

        for option in surface.get("global_options", []):
            if isinstance(option, dict):
                add_cli_option(option, "codex")

        for command in surface.get("commands", []):
            if not isinstance(command, dict) or not command.get("name"):
                continue
            command_name = str(command["name"])
            command_entry: Dict[str, object] = {
                "id": f"cli_command:{command_name}",
                "name": command_name,
                "category": "cli_command",
                "cli_command": f"codex {command_name}",
                "description": str(command.get("description", "")),
                "usage": command.get("usage", []),
                "source_type": item.source_type,
                "source_url": item.source_url,
                "mirrored_path": item.rel_path,
                "provenance": cli_provenance(f"codex {command_name} --help"),
            }
            cli_present_on[command_entry["id"]] = command.get("observed_on", {})
            add_version_history(command_entry)
            capabilities.append(command_entry)
            for option in command.get("options", []):
                if isinstance(option, dict):
                    add_cli_option(option, f"codex {command_name}")
            for subcommand in command.get("subcommands", []):
                if not isinstance(subcommand, dict) or not subcommand.get("name"):
                    continue
                subcommand_name = str(subcommand["name"])
                subcommand_entry: Dict[str, object] = {
                    "id": f"cli_command:{command_name}:{subcommand_name}",
                    "name": subcommand_name,
                    "category": "cli_command",
                    "cli_command": f"codex {command_name} {subcommand_name}",
                    "parent_cli_command": f"codex {command_name}",
                    "description": str(subcommand.get("description", "")),
                    "source_type": item.source_type,
                    "source_url": item.source_url,
                    "mirrored_path": item.rel_path,
                    "provenance": cli_provenance(
                        f"codex {command_name} --help"
                    ),
                }
                cli_present_on[subcommand_entry["id"]] = subcommand.get("observed_on", {})
                add_version_history(subcommand_entry)
                capabilities.append(subcommand_entry)

    config_reference = next(
        (
            item
            for item in documentation_files
            if item.source_url
            == "https://learn.chatgpt.com/docs/config-file/config-reference"
        ),
        None,
    )
    if config_reference:
        config_keys = sorted(
            set(
                re.findall(
                    r'^\s*key:\s*["\x27]([^"\x27]+)["\x27]\s*,?$',
                    managed_file_text(config_reference),
                    flags=re.MULTILINE,
                )
            )
        )
        for key in config_keys:
            entry = {
                "id": f"config_key:{key}",
                "name": key,
                "category": "config_key",
                "config_key": key,
                "source_type": config_reference.source_type,
                "source_url": config_reference.source_url,
                "mirrored_path": config_reference.rel_path,
                "provenance": docs_provenance(config_reference),
            }
            feature_match = re.fullmatch(r"features\.([a-z0-9_]+)", key)
            if feature_match:
                entry["feature_flag"] = feature_match.group(1)
            add_version_history(entry)
            capabilities.append(entry)

    if feature_snapshot_payload is not None or FEATURE_LIFECYCLE.exists():
        try:
            feature_snapshot = feature_snapshot_payload if feature_snapshot_payload is not None else json.loads(FEATURE_LIFECYCLE.read_text())
        except json.JSONDecodeError:
            feature_snapshot = {}
        if isinstance(feature_snapshot, dict):
            feature_version = parse_codex_cli_version(
                str(feature_snapshot.get("codex_cli_version", ""))
            )
            feature_source_urls = feature_snapshot.get("source_urls", {})
            if not isinstance(feature_source_urls, dict):
                feature_source_urls = {}
            documented_keys = set(feature_snapshot.get("docs_feature_keys", []))
            for feature in feature_snapshot.get("cli_features", []):
                if not isinstance(feature, dict) or not feature.get("key"):
                    continue
                key = str(feature["key"])
                stage = str(feature.get("stage", "unknown"))
                provenance: List[Dict[str, str]] = [
                    {
                        "evidence_type": "installed_cli_observation",
                        "source": "codex features list",
                        "codex_cli_version": feature_version,
                        **feature_snapshot.get("observation_environment", {}),
                    }
                ]
                features_source_url = str(feature_source_urls.get("features_rs", ""))
                if features_source_url:
                    provenance.append(
                        {
                            "evidence_type": "upstream_repository_source",
                            "source_url": features_source_url,
                            "source_commit": str(
                                feature_snapshot.get("source_commit", "")
                            ),
                        }
                    )
                entry = {
                    "id": f"feature_flag:{key}",
                    "name": key,
                    "category": "feature_flag",
                    "feature_flag": key,
                    "maturity": stage,
                    "enabled_by_default": bool(feature.get("enabled")),
                    "config_keys": [f"features.{key}"],
                    "documented_officially": key in documented_keys,
                    "source_type": "feature_flag_snapshot",
                    "source_url": "generated://feature-flags/lifecycle",
                    "mirrored_path": "feature-flags/lifecycle.json",
                    "source_ref": str(feature_snapshot.get("source_ref", "")),
                    "source_commit": str(feature_snapshot.get("source_commit", "")),
                    "provenance": provenance,
                }
                add_version_history(entry)
                capabilities.append(entry)

    capability_ids = [str(entry["id"]) for entry in capabilities]
    duplicate_ids = sorted(
        identifier
        for identifier in set(capability_ids)
        if capability_ids.count(identifier) > 1
    )
    if duplicate_ids:
        raise RuntimeError(
            "Capability inventory contains duplicate IDs: " + ", ".join(duplicate_ids)
        )

    current_ids = set(capability_ids)
    for entry in capabilities:
        previous_entry = previous_capabilities.get(str(entry["id"]), {})
        previous_lifecycle = previous_entry.get("lifecycle", {})
        if not isinstance(previous_lifecycle, dict):
            previous_lifecycle = {}
        versions = metadata_values(entry.get("codex_cli_versions"))
        first_seen = str(previous_lifecycle.get("first_seen_version", ""))
        if not first_seen and versions:
            first_seen = versions[0]
        entry["active"] = entry.get("maturity") != "removed"
        entry["lifecycle"] = {
            "status": str(entry.get("maturity", "active")),
            "first_seen_version": first_seen or codex_cli_version,
            "last_seen_version": codex_cli_version,
        }

    for identifier, previous_entry in sorted(previous_capabilities.items()):
        if identifier in current_ids:
            continue
        historical = dict(previous_entry)
        previous_lifecycle = historical.get("lifecycle", {})
        if not isinstance(previous_lifecycle, dict):
            previous_lifecycle = {}
        if historical.get("source_type") == CLI_SURFACE_SOURCE_TYPE:
            # A missing observation must not resurrect an already removed capability.
            if historical.get("active") is False:
                capabilities.append(historical)
                continue
            reason = cli_absence_reason(
                historical, current_cli_observation, codex_cli_version, release_ancestry or {}
            )
            if reason:
                historical["active"] = True
                historical["lifecycle"] = {
                    **previous_lifecycle,
                    "status": "not_observed_on_current_platform" if reason == "different_or_unknown_platform"
                              else "not_observed_on_current_release",
                    "absence_reason": reason,
                    "not_observed_in_version": codex_cli_version,
                    "observation_environment": current_cli_observation,
                }
                capabilities.append(historical)
                continue
        historical["active"] = False
        historical["lifecycle"] = {
            **previous_lifecycle,
            "status": "removed_from_inventory",
            "removed_in_version": codex_cli_version,
        }
        capabilities.append(historical)

    if platform_observations:
        for entry in capabilities:
            if entry.get("source_type") != CLI_SURFACE_SOURCE_TYPE:
                continue
            identifier = str(entry["id"])
            states = cli_observations.platform_states(
                previous_cli_platforms(previous_capabilities.get(identifier, {})),
                cli_present_on.get(identifier, {}), platform_observations, platform_ancestry or {},
            )
            entry["platforms"] = states
            entry["active"] = any(state.get("active", True) for state in states.values())
            history = codex_cli_version_history_metadata(previous_capabilities.get(identifier, {}), {})
            for observation in cli_present_on.get(identifier, {}).values():
                version = observation["codex_cli_version"]
                history = codex_cli_version_history_metadata(history, {
                    "codex_cli_version": version, "codex_cli_version_raw": f"codex-cli {version}",
                })
            entry.pop("codex_cli_versions", None)
            entry.pop("codex_cli_versions_raw", None)
            entry.update(history)
            lifecycle = dict(entry.get("lifecycle", {}))
            seen_versions = [state.get("last_seen", {}).get("codex_cli_version", "") for state in states.values()]
            seen_versions = sorted((version for version in seen_versions if re.fullmatch(r"\d+\.\d+\.\d+", version)),
                                   key=lambda version: tuple(map(int, version.split("."))))
            if seen_versions:
                lifecycle["last_seen_version"] = seen_versions[-1]
                lifecycle["first_seen_version"] = previous_capabilities.get(identifier, {}).get("lifecycle", {}).get("first_seen_version", seen_versions[0])
            lifecycle.pop("absence_reason", None)
            lifecycle.pop("observation_environment", None)
            lifecycle.pop("not_observed_in_version", None)
            if entry["active"]:
                lifecycle.pop("removed_in_version", None)
                lifecycle["status"] = "active" if cli_present_on.get(identifier) else "not_observed_on_current_release"
            else:
                lifecycle["status"] = "removed_from_inventory"
                lifecycle.setdefault("removed_in_version", codex_cli_version)
            entry["lifecycle"] = lifecycle
            provenance = []
            for platform, state in sorted(states.items()):
                observation = state.get("last_seen")
                if observation:
                    provenance.append({"evidence_type": "installed_cli_observation", "platform": platform,
                                       "source": str(entry.get("cli_command", "codex")) + " --help", **observation})
            entry["provenance"] = provenance

    capabilities = sorted(capabilities, key=lambda item: str(item["id"]))
    payload = {
        "schema_version": 2,
        "source_kind": "generated_capability_inventory",
        "source_area": "capability_inventory",
        "evidence_types": {
            "official_documentation": "Published OpenAI documentation mirrored by this repository.",
            "upstream_repository_source": "Immutable release-matched openai/codex source.",
            "github_release_metadata": "Stable release metadata published by openai/codex.",
            "installed_cli_observation": "Deterministic, platform-scoped output observed from an isolated packaged CLI.",
            "generated_relationship": "A deterministic relationship derived from other recorded evidence.",
        },
        "codex_cli_version": codex_cli_metadata.get("codex_cli_version", ""),
        "codex_cli_version_raw": codex_cli_metadata.get("codex_cli_version_raw", ""),
        "codex_cli_release_ref": codex_cli_metadata.get("codex_cli_release_ref", ""),
        "codex_cli_source_commit": codex_cli_metadata.get("codex_cli_source_commit", ""),
        "cli_observation": current_cli_observation,
        **({"cli_platform_observations": platform_observations} if platform_observations else {}),
        "counts": capability_counts(capabilities),
        "capabilities": capabilities,
    }
    inventory_history = codex_cli_version_history_metadata(previous_inventory, codex_cli_metadata)
    payload.update(inventory_history)
    inventory_metadata = dict(codex_cli_metadata)
    inventory_metadata["source_kind"] = "generated_capability_inventory"
    inventory_metadata["source_area"] = "capability_inventory"
    inventory_metadata.update(inventory_history)
    return ManagedFile(
        rel_path=CAPABILITIES_REL_PATH,
        source_type=CAPABILITY_INVENTORY_SOURCE_TYPE,
        source_url="generated://capability-inventory",
        content=json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        source_metadata=inventory_metadata,
    )


def capability_inventory_counts_from_text(text: str) -> Dict[str, object]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {
            "total": 0,
            "active": 0,
            "inactive": 0,
            "by_category": {},
            "by_maturity": {},
        }
    capabilities = payload.get("capabilities", []) if isinstance(payload, dict) else []
    if not isinstance(capabilities, list):
        return {
            "total": 0,
            "active": 0,
            "inactive": 0,
            "by_category": {},
            "by_maturity": {},
        }
    return capability_counts([item for item in capabilities if isinstance(item, dict)])


def capability_inventory_counts(
    inventory_files: Sequence[ManagedFile],
    preserve_missing_sources: set[str],
) -> Dict[str, object]:
    if inventory_files:
        return capability_inventory_counts_from_text(managed_file_text(inventory_files[0]))
    if CAPABILITY_INVENTORY_SOURCE_TYPE in preserve_missing_sources and CAPABILITIES_PATH.exists():
        return capability_inventory_counts_from_text(CAPABILITIES_PATH.read_text())
    return {
        "total": 0,
        "active": 0,
        "inactive": 0,
        "by_category": {},
        "by_maturity": {},
    }


def help_section_lines(text: str, section: str) -> List[str]:
    lines = text.splitlines()
    header = f"{section}:"
    try:
        start = lines.index(header) + 1
    except ValueError:
        return []
    end = len(lines)
    for index in range(start, len(lines)):
        if re.fullmatch(r"[A-Z][A-Za-z ]+:", lines[index]):
            end = index
            break
    return lines[start:end]


def parse_help_commands(text: str) -> List[Dict[str, str]]:
    commands: List[Dict[str, str]] = []
    current: Dict[str, str] | None = None
    for line in help_section_lines(text, "Commands"):
        match = re.match(r"^  ([a-z0-9][a-z0-9-]*)\s{2,}(.*\S)\s*$", line)
        if match:
            current = {"name": match.group(1), "description": match.group(2)}
            commands.append(current)
            continue
        if current and line.strip():
            current["description"] = f"{current['description']} {line.strip()}"
    return commands


def parse_help_options(text: str) -> List[Dict[str, object]]:
    options: List[Dict[str, object]] = []
    current: Dict[str, object] | None = None
    for line in help_section_lines(text, "Options"):
        flags = re.findall(r"(?<![\w-])-{1,2}[A-Za-z0-9][A-Za-z0-9-]*", line)
        indentation = len(line) - len(line.lstrip(" "))
        if (
            flags
            and 2 <= indentation <= 6
            and re.match(r"^\s+(?:-[A-Za-z0-9]|--)", line)
        ):
            current = {
                "flags": flags,
                "primary_flag": next(
                    (flag for flag in flags if flag.startswith("--")), flags[0]
                ),
                "synopsis": line.strip(),
                "description": "",
            }
            options.append(current)
            continue
        if current and line.strip():
            description = str(current["description"])
            current["description"] = " ".join(
                part for part in (description, line.strip()) if part
            )
    return options


def parse_help_usage(text: str) -> List[str]:
    usage: List[str] = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("Usage:"):
            continue
        first = line.removeprefix("Usage:").strip()
        if first:
            usage.append(first)
        for continuation in lines[index + 1 :]:
            if not continuation.strip():
                break
            usage.append(continuation.strip())
        break
    return usage


def build_cli_surface_snapshot(
    codex_bin: str,
    env: Dict[str, str],
    workspace_path: Path,
    codex_cli_metadata: Dict[str, str],
    observation_environment: Dict[str, str] | None = None,
) -> ManagedFile:
    observation_environment = observation_environment or {
        "os": sys.platform,
        "arch": host_platform.machine().lower(),
    }
    top_help = run_local_command(
        [codex_bin, "--help"], cwd=workspace_path, env=env
    )
    top_commands = parse_help_commands(top_help)
    if not top_commands or not parse_help_options(top_help) or not parse_help_usage(top_help):
        raise SourceContentError("CLI help lacks parseable commands, options, or usage")
    command_surfaces: List[Dict[str, object]] = []
    for command in top_commands:
        name = command["name"]
        command_help = top_help
        if name != "help":
            command_help = run_local_command(
                [codex_bin, name, "--help"], cwd=workspace_path, env=env
            )
        if not parse_help_usage(command_help) or not parse_help_options(command_help):
            raise SourceContentError(f"CLI help for {name} lacks parseable options or usage")
        command_surfaces.append(
            {
                "name": name,
                "description": command["description"],
                "usage": parse_help_usage(command_help),
                "subcommands": parse_help_commands(command_help),
                "options": parse_help_options(command_help),
            }
        )

    payload = {
        "schema_version": 2,
        "source_kind": "installed_cli_help_observation",
        "codex_cli_version": codex_cli_metadata.get("codex_cli_version", ""),
        "codex_cli_version_raw": codex_cli_metadata.get(
            "codex_cli_version_raw", ""
        ),
        "command": "codex --help; codex <command> --help",
        "observation_environment": observation_environment,
        "usage": parse_help_usage(top_help),
        "global_options": parse_help_options(top_help),
        "commands": command_surfaces,
    }
    return ManagedFile(
        rel_path=CLI_SURFACE_REL_PATH,
        source_type=CLI_SURFACE_SOURCE_TYPE,
        source_url="codex-cli://help",
        content=json.dumps(payload, indent=2, sort_keys=True) + "\n",
        source_metadata={
            **codex_cli_metadata,
            "source_kind": "installed_cli_help_observation",
        },
    )


def build_codex_cli_files() -> Tuple[List[ManagedFile], List[Dict[str, str]], Dict[str, str]]:
    codex_bin = shutil.which("codex")
    if not codex_bin:
        raise RuntimeError("codex CLI is not installed or not on PATH")

    version_raw = run_local_command([codex_bin, "--version"], env=codex_subprocess_env()).strip()
    version = parse_codex_cli_version(version_raw)
    metadata = {
        "source_kind": "installed_codex_cli",
        "codex_cli_version": version,
        "codex_cli_version_raw": version_raw,
        "codex_cli_command": "codex --version",
        "codex_prompt_snapshot_command": "codex debug prompt-input",
    }

    managed: List[ManagedFile] = []
    fetch_errors: List[Dict[str, str]] = []

    with tempfile.TemporaryDirectory(prefix="codex-docs-home-") as home_dir, tempfile.TemporaryDirectory(
        prefix="codex-docs-workspace-"
    ) as workspace_dir:
        home_path = Path(home_dir)
        workspace_path = Path(workspace_dir)
        codex_home = home_path / ".codex"
        codex_home.mkdir(parents=True, exist_ok=True)

        env = isolated_codex_subprocess_env()
        env.update(
            {
                "HOME": str(home_path),
                "CODEX_HOME": str(codex_home),
                "NO_COLOR": "1",
                "SHELL": "/bin/bash",
                "TZ": "UTC",
            }
        )

        managed.append(
            build_cli_surface_snapshot(codex_bin, env, workspace_path, metadata)
        )

        prompt_raw = run_local_command([codex_bin, "debug", "prompt-input", ""], cwd=workspace_path, env=env)
        prompt_payload = json.loads(prompt_raw)
        replacement_items = {
            str(codex_home): "$CODEX_HOME",
            str(codex_home.resolve()): "$CODEX_HOME",
            str(home_path): "$HOME",
            str(home_path.resolve()): "$HOME",
            str(workspace_path): "$WORKSPACE",
            str(workspace_path.resolve()): "$WORKSPACE",
        }
        replacements = tuple(sorted(replacement_items.items(), key=lambda item: len(item[0]), reverse=True))
        prompt_payload = sanitize_prompt_payload(prompt_payload, replacements)
        if isinstance(prompt_payload, list):
            for message in prompt_payload:
                if isinstance(message, dict):
                    message.pop("id", None)
        prompt_content = json.dumps(prompt_payload, indent=2, ensure_ascii=False) + "\n"
        managed.append(
            ManagedFile(
                rel_path=f"{SYSTEM_PROMPT_OUTPUT_PREFIX}prompt-input.json",
                source_type="codex_cli_prompt_input",
                source_url="codex-cli://debug/prompt-input",
                content=prompt_content,
                source_metadata=metadata,
            )
        )

        system_skills_source = codex_home / "skills" / ".system"
        if not system_skills_source.is_dir():
            raise RuntimeError("codex debug prompt-input did not materialize system skills")

        for source_path in sorted(path for path in system_skills_source.rglob("*") if path.is_file()):
            rel_path = source_path.relative_to(system_skills_source)
            managed.append(
                ManagedFile(
                    rel_path=system_skill_path_to_rel_path(rel_path),
                    source_type="codex_cli_system_skill",
                    source_url=f"codex-cli://skills/.system/{rel_path.as_posix()}",
                    content=source_path.read_bytes(),
                    source_metadata=metadata,
                )
            )

    return managed, fetch_errors, metadata


def write_manifest(entries: Dict[str, Dict[str, object]]) -> None:
    payload = {
        "schema_version": 1,
        "sources": {key: entries[key] for key in sorted(entries)},
    }
    ensure_parent(MANIFEST_PATH)
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_summary(
    added: List[str],
    updated: List[str],
    removed: List[str],
    total: int,
    failures: List[Dict[str, str]] | None = None,
    source_metadata: Dict[str, object] | None = None,
) -> None:
    failure_items = failures or []
    payload = {
        "generated_at": now_utc_iso(),
        "total_files": total,
        "added": added,
        "updated": updated,
        "removed": removed,
        "failure_count": len(failure_items),
        "failures": failure_items,
    }
    if source_metadata:
        payload["source_metadata"] = source_metadata
    ensure_parent(SUMMARY_PATH)
    SUMMARY_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def semantic_coverage(coverage: Dict[str, object]) -> Dict[str, object]:
    state = {key: value for key, value in coverage.items() if key != "generated_at"}
    if isinstance(state.get("sync"), dict):
        state["sync"] = {key: value for key, value in state["sync"].items()
                         if key not in {"scope", "web_observation"}}
    if isinstance(state.get("web_snapshot"), dict):
        state["web_snapshot"] = {key: value for key, value in state["web_snapshot"].items()
                                 if key != "last_successful_full_sync_at"}
    return state


def write_coverage(coverage: Dict[str, object]) -> None:
    coverage_without_generated_at = semantic_coverage(coverage)
    if COVERAGE_PATH.exists():
        try:
            previous = json.loads(COVERAGE_PATH.read_text())
            if isinstance(previous, dict):
                previous_has_generated_at = "generated_at" in previous
                previous_without_generated_at = semantic_coverage(previous)
                if previous_has_generated_at and previous_without_generated_at == coverage_without_generated_at:
                    return
        except json.JSONDecodeError:
            pass

    ensure_parent(COVERAGE_PATH)
    payload = {**coverage, "generated_at": now_utc_iso()}
    COVERAGE_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def render_sync_event(event: Dict[str, object]) -> str:
    changes = event["changes"]
    added, updated, removed = (changes[key] for key in ("added", "updated", "removed"))
    source_metadata = changes.get("source_metadata", {})
    capability_changes = changes.get("capability_changes", {})
    event_id, observed_at = event["id"], event["observed_at"]
    lines = [
        f"### Transaction {event_id[:12]}",
        "",
        f"Observed at: {observed_at}",
        "",
        f"- Added: {len(added)}",
        f"- Updated: {len(updated)}",
        f"- Removed: {len(removed)}",
        "",
    ]

    if source_metadata:
        lines.append("### Source Snapshot")
        lines.append("")
        for key in SOURCE_METADATA_KEYS:
            value = source_metadata.get(key)
            if value:
                lines.append(f"- `{key}`: `{value}`")
        lines.append("")

    lines.append("### Category Summary")
    lines.append("")
    lines.extend(render_category_summary("Added", added))
    lines.extend(render_category_summary("Updated", updated))
    lines.extend(render_category_summary("Removed", removed))

    if capability_changes:
        lines.append("### Semantic Capability Changes")
        lines.append("")
        lines.extend(render_capability_changes(capability_changes))

    if changes.get("model_changes"):
        lines.extend(["### Model Changes", ""])
        lines.extend(model_catalog.render_changes(changes["model_changes"]))

    if added:
        lines.append("### Added (Raw Paths)")
        lines.extend(f"- `{item}`" for item in added)
        lines.append("")

    if updated:
        lines.append("### Updated (Raw Paths)")
        lines.extend(f"- `{item}`" for item in updated)
        lines.append("")

    if removed:
        lines.append("### Removed (Raw Paths)")
        lines.extend(f"- `{item}`" for item in removed)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_weekly_note(
    added: List[str], updated: List[str], removed: List[str],
    source_metadata: Dict[str, object] | None = None,
    capability_changes: Dict[str, object] | None = None,
    file_changes: Dict[str, object] | None = None,
    model_changes: Dict[str, object] | None = None,
) -> None:
    if not (added or updated or removed):
        return
    date_tag = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    weekly_path = WEEKLY_DIR / f"{date_tag}.md"
    existing_metadata, legacy_report = ({}, "")
    if weekly_path.exists():
        existing_metadata, legacy_report = split_markdown_frontmatter(weekly_path.read_text())
    payload = {
        "added": sorted(added), "updated": sorted(updated), "removed": sorted(removed),
        "source_metadata": source_metadata or {},
        "capability_changes": capability_changes or {},
        "file_changes": file_changes or {},
        "model_changes": model_changes or {},
    }
    ledger = semantic_history.record_event(
        WEEKLY_DIR / "events" / f"{date_tag}.json", payload,
        observed_at=now_utc_iso(), legacy_report=legacy_report,
    )
    sections = [f"# Codex Docs Sync - {date_tag}\n"]
    if ledger.get("legacy_report"):
        sections.extend(["## Earlier report (before event tracking)\n", ledger["legacy_report"]])
    sections.extend(render_sync_event(event) for event in ledger["events"])
    body = "\n".join(sections).rstrip() + "\n"
    metadata = weekly_report_metadata(
        date_tag, body, existing_metadata=existing_metadata, source_metadata=source_metadata,
    )
    write_file_if_changed(weekly_path, format_frontmatter(metadata, body))


def weekly_source_snapshot_metadata(body: str) -> Dict[str, str]:
    metadata: Dict[str, str] = {}
    for key, value in re.findall(r"^- `([^`]+)`: `([^`]+)`$", body, flags=re.MULTILINE):
        metadata[key] = value
    return metadata


def weekly_report_metadata(
    date_tag: str,
    body: str,
    *,
    existing_metadata: Dict[str, object] | None = None,
    source_metadata: Dict[str, object] | None = None,
) -> Dict[str, object]:
    metadata = dict(existing_metadata or {})
    metadata.update(
        {
            "source_type": WEEKLY_REPORT_SOURCE_TYPE,
            "source_area": WEEKLY_REPORT_SOURCE_AREA,
            "source_url": f"generated://weekly/{date_tag}",
            "source_kind": WEEKLY_REPORT_SOURCE_KIND,
            "report_date": date_tag,
        }
    )

    snapshot_metadata = weekly_source_snapshot_metadata(body)
    version_source: Dict[str, str] = {}
    for key in ("codex_cli_version", "codex_cli_version_raw"):
        value = source_metadata.get(key) if source_metadata else None
        if isinstance(value, str) and value:
            version_source[key] = value
        elif snapshot_metadata.get(key):
            version_source[key] = snapshot_metadata[key]
    if version_source:
        metadata.update(codex_cli_version_history_metadata(metadata, version_source))

    return metadata


def ensure_weekly_frontmatter() -> None:
    if not WEEKLY_DIR.exists():
        return

    for weekly_path in sorted(WEEKLY_DIR.glob("*.md")):
        if weekly_path.name == "README.md":
            continue
        text = weekly_path.read_text()
        existing_metadata, body = split_markdown_frontmatter(text)
        metadata = weekly_report_metadata(
            weekly_path.stem,
            body,
            existing_metadata=existing_metadata,
        )
        content = format_frontmatter(metadata, body)
        if content != text:
            weekly_path.write_text(content)


def categorize_path(path: str) -> str:
    for category, prefix in WEEKLY_CATEGORY_RULES:
        if path.startswith(prefix):
            return category
    return "Other"


def render_category_summary(label: str, paths: List[str]) -> List[str]:
    lines: List[str] = [f"### {label}"]
    if not paths:
        lines.append("- None")
        lines.append("")
        return lines

    counts: Dict[str, int] = {}
    for path in paths:
        category = categorize_path(path)
        counts[category] = counts.get(category, 0) + 1

    ordered_categories = [name for name, _ in WEEKLY_CATEGORY_RULES]
    for category in sorted(counts):
        if category not in ordered_categories:
            ordered_categories.append(category)

    for category in ordered_categories:
        count = counts.get(category)
        if count:
            lines.append(f"- {category}: {count}")
    lines.append("")
    return lines


def capability_entries_from_text(text: str) -> Dict[str, Dict[str, object]]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {}
    entries = payload.get("capabilities", []) if isinstance(payload, dict) else []
    if not isinstance(entries, list):
        return {}
    return {
        str(entry["id"]): entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("id")
    }


def semantic_capability_changes(
    previous_text: str, current_text: str
) -> Dict[str, object]:
    previous = capability_entries_from_text(previous_text)
    current = capability_entries_from_text(current_text)
    previous_active = {
        identifier: entry
        for identifier, entry in previous.items()
        if entry.get("active", True)
    }
    current_active = {
        identifier: entry
        for identifier, entry in current.items()
        if entry.get("active", True)
    }
    added = sorted(set(current_active) - set(previous_active))
    removed = sorted(set(previous_active) - set(current_active))
    transitions: List[Dict[str, str]] = []
    for identifier in sorted(set(previous_active) & set(current_active)):
        before = str(previous_active[identifier].get("maturity", ""))
        after = str(current_active[identifier].get("maturity", ""))
        if before != after and (before or after):
            transitions.append(
                {"id": identifier, "from": before or "unspecified", "to": after or "unspecified"}
            )

    def group(identifiers: Sequence[str], entries: Dict[str, Dict[str, object]]):
        grouped: Dict[str, List[str]] = {}
        for identifier in identifiers:
            category = str(entries.get(identifier, {}).get("category", "unknown"))
            grouped.setdefault(category, []).append(identifier)
        return {key: grouped[key] for key in sorted(grouped)}

    return {
        "added": added,
        "removed": removed,
        "lifecycle_transitions": transitions,
        "added_by_category": group(added, current_active),
        "removed_by_category": group(removed, previous_active),
    }


def render_capability_changes(changes: Dict[str, object]) -> List[str]:
    lines: List[str] = []
    for label, key in (("Added", "added_by_category"), ("Removed", "removed_by_category")):
        grouped = changes.get(key, {})
        if not isinstance(grouped, dict) or not grouped:
            lines.append(f"- {label}: none")
            continue
        total = sum(len(values) for values in grouped.values() if isinstance(values, list))
        lines.append(f"- {label}: {total}")
        for category, values in sorted(grouped.items()):
            if not isinstance(values, list):
                continue
            preview = ", ".join(f"`{value}`" for value in values[:10])
            suffix = f" (and {len(values) - 10} more)" if len(values) > 10 else ""
            lines.append(f"  - {category}: {preview}{suffix}")
    transitions = changes.get("lifecycle_transitions", [])
    if isinstance(transitions, list) and transitions:
        lines.append(f"- Lifecycle transitions: {len(transitions)}")
        for transition in transitions[:20]:
            if isinstance(transition, dict):
                lines.append(
                    f"  - `{transition.get('id')}`: `{transition.get('from')}` -> `{transition.get('to')}`"
                )
        if len(transitions) > 20:
            lines.append(f"  - and {len(transitions) - 20} more")
    else:
        lines.append("- Lifecycle transitions: none")
    lines.append("")
    return lines


def apply_sync(
    managed_files: Iterable[ManagedFile],
    failures: List[Dict[str, str]] | None = None,
    preserve_missing_sources: Sequence[str] = (),
    source_metadata: Dict[str, object] | None = None,
) -> Tuple[List[str], List[str], List[str]]:
    previous = load_existing_manifest()
    capability_changes: Dict[str, object] | None = None
    model_changes: Dict[str, object] = {}

    next_entries: Dict[str, Dict[str, object]] = {}
    rel_to_file: Dict[str, ManagedFile] = {}

    for item in managed_files:
        rel_to_file[item.rel_path] = item
        next_entry = {
            "sha256": sha256_content(item.content),
            "source_type": item.source_type,
            "source_url": item.source_url,
        }
        if item.source_metadata:
            previous_meta = previous.get(item.rel_path, {})
            previous_same_hash = previous_meta.get("sha256") == next_entry["sha256"]
            preserved_metadata = {
                key: previous_meta[key]
                for key in PRESERVED_MANIFEST_SOURCE_KEYS
                if previous_same_hash and previous_meta.get(key)
            }
            next_entry.update(item.source_metadata)
            next_entry.update(preserved_metadata)
            if item.source_metadata.get("source_kind"):
                next_entry["source_kind"] = item.source_metadata["source_kind"]
        next_entries[item.rel_path] = next_entry
        if item.rel_path == MODELS_REL_PATH:
            model_path = output_path_for_rel_path(MODELS_REL_PATH)
            previous_models = json.loads(model_path.read_text()) if model_path.exists() else {}
            model_changes = model_catalog.changes(previous_models, json.loads(managed_file_text(item)))
        if item.rel_path == CAPABILITIES_REL_PATH:
            previous_text = CAPABILITIES_PATH.read_text() if CAPABILITIES_PATH.exists() else "{}"
            capability_changes = semantic_capability_changes(
                previous_text, managed_file_text(item)
            )

    previous_paths = set(previous)
    next_paths = set(next_entries)

    added = sorted(next_paths - previous_paths)
    preserve_sources = set(preserve_missing_sources)
    removed_candidates = sorted(previous_paths - next_paths)
    removed: List[str] = []
    for path in removed_candidates:
        previous_source_type = previous.get(path, {}).get("source_type", "")
        if previous_source_type in preserve_sources:
            next_entries[path] = previous[path]
            continue
        removed.append(path)

    updated = sorted(
        path
        for path in (next_paths & previous_paths)
        if previous[path].get("sha256") != next_entries[path].get("sha256")
    )

    touched = set(added) | set(updated)
    for rel_path in sorted(touched):
        abs_path = output_path_for_rel_path(rel_path)
        write_file_if_changed(abs_path, rel_to_file[rel_path].content)

    for rel_path in removed:
        abs_path = output_path_for_rel_path(rel_path)
        if abs_path.exists():
            abs_path.unlink()

    remove_empty_directories(DEVELOPERS_ROOT)
    remove_empty_directories(LEARN_ROOT)
    remove_empty_directories(GITHUB_ROOT)
    remove_empty_directories(PLATFORM_ROOT)
    remove_empty_directories(ROOT / "dot_codex")
    remove_empty_directories(ROOT / "system_prompts")

    write_manifest(next_entries)
    has_changes = bool(added or updated or removed)
    summary_schema_stale = False
    summary_had_failures = False
    if SUMMARY_PATH.exists():
        try:
            summary_payload = json.loads(SUMMARY_PATH.read_text())
            summary_schema_stale = not (
                isinstance(summary_payload, dict)
                and "failure_count" in summary_payload
                and "failures" in summary_payload
            )
            if isinstance(summary_payload, dict):
                try:
                    summary_had_failures = int(summary_payload.get("failure_count", 0)) > 0
                except (TypeError, ValueError):
                    summary_had_failures = bool(summary_payload.get("failure_count"))
                summary_had_failures = summary_had_failures or bool(summary_payload.get("failures"))
        except json.JSONDecodeError:
            summary_schema_stale = True
    if has_changes or not SUMMARY_PATH.exists() or bool(failures) or summary_schema_stale or summary_had_failures:
        write_summary(added, updated, removed, len(next_entries), failures=failures, source_metadata=source_metadata)
    write_weekly_note(
        added,
        updated,
        removed,
        source_metadata=source_metadata,
        capability_changes=capability_changes,
        model_changes=model_changes,
        file_changes={path: {
            "before": previous.get(path, {}).get("sha256"),
            "after": next_entries.get(path, {}).get("sha256"),
        } for path in sorted(set(added + updated + removed))},
    )
    ensure_weekly_frontmatter()

    return added, updated, removed


def load_cached_source_files(source_types: set[str], *, allow_empty: bool = False) -> List[ManagedFile]:
    """Replay complete committed source families without claiming a fresh web fetch."""
    files = []
    for path, metadata in load_existing_manifest().items():
        if metadata.get("source_type") not in source_types:
            continue
        content = output_path_for_rel_path(path).read_bytes()
        if sha256_content(content) != metadata.get("sha256"):
            raise ValueError(f"Cached source does not match the manifest: {path}")
        files.append(ManagedFile(
            path, metadata["source_type"], metadata["source_url"], content,
            {key: value for key, value in metadata.items() if key not in {"sha256", "source_type", "source_url"}},
        ))
    if not files and not allow_empty:
        raise ValueError("Release-only sync requires a complete existing web mirror")
    return files


def main(*, release_only: bool = False, observations_dir: Path | None = None) -> int:
    logging.Formatter.converter = time.gmtime
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    failures: List[Dict[str, str]] = []
    preserve_missing_sources: set[str] = set()
    developers_files: List[ManagedFile] = []
    learn_files: List[ManagedFile] = []
    github_files: List[ManagedFile] = []
    platform_tool_guide_files: List[ManagedFile] = []
    codex_cli_files: List[ManagedFile] = []
    capability_inventory_files: List[ManagedFile] = []
    model_files: List[ManagedFile] = []
    feature_files: List[ManagedFile] = []
    developers_fetch_errors: List[Dict[str, str]] = []
    learn_fetch_errors: List[Dict[str, str]] = []
    github_fetch_errors: List[Dict[str, str]] = []
    platform_tool_guide_fetch_errors: List[Dict[str, str]] = []
    platform_tool_guide_references_by_url: Dict[str, List[str]] = {}
    codex_cli_fetch_errors: List[Dict[str, str]] = []
    codex_cli_metadata: Dict[str, str] = {}
    collected_platforms: Dict[str, object] = {}
    coverage: Dict[str, object] = {
        "generated_at": now_utc_iso(),
        "source_state_semantics": SOURCE_STATE_SEMANTICS,
    }

    try:
        if release_only:
            coverage = json.loads(COVERAGE_PATH.read_text())
            previous_sync = coverage.get("sync", {})
            if previous_sync.get("failure_count") or previous_sync.get("status", "complete") != "complete":
                raise SourceContentError("Release-only sync cannot reuse a partial web mirror")
            if "web_snapshot" not in coverage:
                coverage["web_snapshot"] = (
                    {"status": "complete", "last_successful_full_sync_at": coverage.get("generated_at", "")}
                    if previous_sync.get("scope", "full") == "full" else {"status": "unknown"}
                )
            developers_files = load_cached_source_files({"developers"})
        else:
            developers_files, coverage, developers_fetch_errors = build_developers_files(session)
        developers_files = add_source_area_metadata(developers_files)
        failures.extend(developers_fetch_errors)
        if developers_fetch_errors:
            preserve_missing_sources.add("developers")
    except Exception as exc:
        LOG.warning("Developers source failed; continuing with remaining sources: %s", exc)
        failure = {
            "source": "developers",
            "stage": "source_build",
            "state": "source_unavailable",
            "url": "https://developers.openai.com",
            "error": str(exc),
        }
        failures.append(failure)
        preserve_missing_sources.add("developers")
        coverage["developers"] = {
            "error": str(exc),
            "counts": {
                "codex_related_urls": 0,
                "mirrored_urls": 0,
                "sitemap_urls": 0,
                "skipped_codex_related_urls": 0,
                "sitemap_fetch_errors": 0,
                "page_fetch_errors": 0,
            },
        }

    try:
        if release_only:
            learn_files = load_cached_source_files({LEARN_SOURCE_TYPE})
            learn_coverage = coverage.get("learn", {})
        else:
            learn_files, learn_coverage, learn_fetch_errors = build_learn_files(session)
        learn_files = add_source_area_metadata(learn_files)
        coverage["learn"] = learn_coverage
        failures.extend(learn_fetch_errors)
        if learn_fetch_errors:
            preserve_missing_sources.add(LEARN_SOURCE_TYPE)
    except Exception as exc:
        LOG.warning("Learn source failed; continuing with remaining sources: %s", exc)
        failure = {
            "source": LEARN_SOURCE_TYPE,
            "stage": "source_build",
            "state": "source_unavailable",
            "url": "https://learn.chatgpt.com/docs",
            "error": str(exc),
        }
        failures.append(failure)
        preserve_missing_sources.add(LEARN_SOURCE_TYPE)
        coverage["learn"] = {
            "sitemap_index_url": LEARN_SITEMAP_INDEX_URL,
            "error": str(exc),
            "counts": {
                "sitemap_urls": 0,
                "discovered_urls": 0,
                "mirrored_urls": 0,
                "markdown_pages": 0,
                "html_fallback_pages": 0,
                "sitemap_fetch_errors": 0,
                "page_fetch_errors": 0,
            },
        }

    try:
        codex_cli_files, codex_cli_fetch_errors, codex_cli_metadata = build_codex_cli_files()
        codex_cli_files, codex_cli_metadata = add_cli_release_provenance(
            session, codex_cli_files, codex_cli_metadata
        )
        codex_cli_files, collected_platforms = prepare_cli_observations(codex_cli_files, codex_cli_metadata, observations_dir)
        codex_cli_files = add_source_area_metadata(codex_cli_files)
        failures.extend(codex_cli_fetch_errors)
        if codex_cli_fetch_errors:
            preserve_missing_sources.update(
                item["source"] for item in codex_cli_fetch_errors if item["source"] in CODEX_CLI_SOURCE_TYPES
            )
    except Exception as exc:
        LOG.warning("Codex CLI source failed; continuing with remaining sources: %s", exc)
        failure = {
            "source": "codex_cli",
            "stage": "source_build",
            "state": "source_unavailable",
            "url": "codex-cli://installed",
            "error": str(exc),
        }
        failures.append(failure)
        preserve_missing_sources.update(CODEX_CLI_SOURCE_TYPES)

    try:
        source_ref = codex_cli_metadata.get("codex_cli_release_ref", "")
        source_commit = codex_cli_metadata.get("codex_cli_source_commit", "")
        if not source_ref or not source_commit:
            raise RuntimeError(
                "Release-matched GitHub source requires Codex CLI release provenance"
            )
        github_files, github_fetch_errors = build_github_files(
            session,
            source_ref=source_ref,
            source_commit=source_commit,
        )
        github_files = add_source_area_metadata(github_files)
        failures.extend(github_fetch_errors)
        if github_fetch_errors:
            preserve_missing_sources.add("github")
    except Exception as exc:
        LOG.warning("GitHub source failed; continuing with remaining sources: %s", exc)
        failure = {
            "source": "github",
            "stage": "source_build",
            "state": "source_unavailable",
            "url": "https://github.com/openai/codex",
            "error": str(exc),
        }
        failures.append(failure)
        preserve_missing_sources.add("github")

    try:
        model_files = [build_model_catalog_file(session, codex_cli_metadata)]
        coverage["model_catalog"] = model_catalog_coverage(codex_cli_metadata)
    except Exception as exc:
        failures.append({"source": MODEL_SOURCE_TYPE, "stage": "source_build",
                         "state": "source_unavailable", "error": str(exc)})
        preserve_missing_sources.add(MODEL_SOURCE_TYPE)
        coverage["model_catalog"] = {"status": "degraded", "error": str(exc)}

    try:
        if release_only:
            platform_tool_guide_files = load_cached_source_files({PLATFORM_TOOL_GUIDE_SOURCE_TYPE}, allow_empty=True)
            platform_tool_guide_references_by_url = coverage.get("platform_tool_guides", {}).get("references_by_url", {})
        else:
            platform_tool_guide_files, platform_tool_guide_fetch_errors, platform_tool_guide_references_by_url = (
                build_platform_tool_guide_files(session, developers_files + learn_files + github_files + codex_cli_files)
            )
        platform_tool_guide_files = add_source_area_metadata(platform_tool_guide_files)
        failures.extend(platform_tool_guide_fetch_errors)
        if platform_tool_guide_fetch_errors:
            preserve_missing_sources.add(PLATFORM_TOOL_GUIDE_SOURCE_TYPE)
        if ({"developers", LEARN_SOURCE_TYPE, "github"} | CODEX_CLI_SOURCE_TYPES) & preserve_missing_sources:
            preserve_missing_sources.add(PLATFORM_TOOL_GUIDE_SOURCE_TYPE)
    except Exception as exc:
        LOG.warning("Platform tool guide source failed; continuing with remaining sources: %s", exc)
        failure = {
            "source": PLATFORM_TOOL_GUIDE_SOURCE_TYPE,
            "stage": "source_build",
            "state": "source_unavailable",
            "url": "https://platform.openai.com/docs/guides",
            "error": str(exc),
        }
        failures.append(failure)
        preserve_missing_sources.add(PLATFORM_TOOL_GUIDE_SOURCE_TYPE)

    try:
        feature_payload, feature_markdown = snapshot_feature_flags.build_snapshot()
        if (feature_payload.get("source_commit") != codex_cli_metadata.get("codex_cli_source_commit")
                or feature_payload.get("source_ref") != codex_cli_metadata.get("codex_cli_release_ref")):
            raise ValueError("Feature snapshot does not match the release transaction")
        feature_files = [
            ManagedFile("feature-flags/lifecycle.json", "feature_flags", "generated://feature-lifecycle",
                        json.dumps(feature_payload, indent=2, sort_keys=True) + "\n"),
            ManagedFile("feature-flags/lifecycle.md", "feature_flags", "generated://feature-lifecycle", feature_markdown),
        ]
    except Exception as exc:
        failures.append({"source": "feature_flags", "stage": "source_build", "state": "source_unavailable", "error": str(exc)})
        preserve_missing_sources.add("feature_flags")

    if preserve_missing_sources:
        preserve_missing_sources.add(CAPABILITY_INVENTORY_SOURCE_TYPE)
    else:
        capability_inventory_files = [
            build_capability_inventory_file(
                codex_cli_files,
                platform_tool_guide_files,
                platform_tool_guide_references_by_url,
                codex_cli_metadata,
                documentation_files=developers_files + learn_files + github_files,
                feature_snapshot_payload=feature_payload,
                platform_ancestry=resolve_platform_ancestry(session, load_existing_capability_inventory(), collected_platforms),
                release_ancestry=resolve_cli_release_ancestry(
                    session, load_existing_capability_inventory(),
                    codex_cli_metadata.get("codex_cli_source_commit", ""),
                ) if not collected_platforms else {},
            )
        ]

    learn_source_errors = [
        item for item in failures if item["source"] == LEARN_SOURCE_TYPE and item["stage"] == "source_build"
    ]
    learn_mirrored_paths = coverage_paths_for_source(learn_files, LEARN_SOURCE_TYPE, preserve_missing_sources)
    learn_section = coverage.get("learn", {})
    if isinstance(learn_section, dict):
        learn_section["mirrored_paths_count"] = len(learn_mirrored_paths)
        learn_section["mirrored_paths"] = learn_mirrored_paths
        learn_section["source_errors"] = learn_source_errors
        counts = learn_section.get("counts", {})
        if not isinstance(counts, dict):
            counts = {}
            learn_section["counts"] = counts
        counts["mirrored_paths_count"] = len(learn_mirrored_paths)
        counts["source_errors"] = len(learn_source_errors)

    github_source_errors = [item for item in failures if item["source"] == "github" and item["stage"] == "source_build"]
    github_mirrored_paths = coverage_paths_for_source(github_files, "github", preserve_missing_sources)
    coverage["github"] = {
        "repo": "openai/codex",
        "source_ref": codex_cli_metadata.get("codex_cli_release_ref", ""),
        "source_commit": codex_cli_metadata.get("codex_cli_source_commit", ""),
        "mirrored_paths_count": len(github_mirrored_paths),
        "mirrored_paths": github_mirrored_paths,
        "page_fetch_errors": github_fetch_errors,
        "source_errors": github_source_errors,
        "counts": {
            "mirrored_paths_count": len(github_mirrored_paths),
            "page_fetch_errors": len(github_fetch_errors),
            "source_errors": len(github_source_errors),
        },
    }
    platform_tool_guide_source_errors = [
        item
        for item in failures
        if item["source"] == PLATFORM_TOOL_GUIDE_SOURCE_TYPE and item["stage"] == "source_build"
    ]
    platform_tool_guide_mirrored_paths = coverage_paths_for_source(
        platform_tool_guide_files,
        PLATFORM_TOOL_GUIDE_SOURCE_TYPE,
        preserve_missing_sources,
    )
    coverage["platform_tool_guides"] = {
        "source_type": PLATFORM_TOOL_GUIDE_SOURCE_TYPE,
        "candidate_urls": list(PLATFORM_TOOL_GUIDE_URLS),
        "referenced_urls": sorted(platform_tool_guide_references_by_url),
        "references_by_url": platform_tool_guide_references_by_url,
        "mirrored_paths_count": len(platform_tool_guide_mirrored_paths),
        "mirrored_paths": platform_tool_guide_mirrored_paths,
        "page_fetch_errors": platform_tool_guide_fetch_errors,
        "source_errors": platform_tool_guide_source_errors,
        "counts": {
            "candidate_urls": len(PLATFORM_TOOL_GUIDE_URLS),
            "referenced_urls": len(platform_tool_guide_references_by_url),
            "mirrored_paths_count": len(platform_tool_guide_mirrored_paths),
            "page_fetch_errors": len(platform_tool_guide_fetch_errors),
            "source_errors": len(platform_tool_guide_source_errors),
        },
    }
    capability_inventory_mirrored_paths = coverage_paths_for_source(
        capability_inventory_files,
        CAPABILITY_INVENTORY_SOURCE_TYPE,
        preserve_missing_sources,
    )
    coverage["capability_inventory"] = {
        "source_type": CAPABILITY_INVENTORY_SOURCE_TYPE,
        "output_path": CAPABILITIES_REL_PATH,
        "mirrored_paths_count": len(capability_inventory_mirrored_paths),
        "mirrored_paths": capability_inventory_mirrored_paths,
        "counts": capability_inventory_counts(capability_inventory_files, preserve_missing_sources),
    }
    system_skill_files = [item for item in codex_cli_files if item.source_type == "codex_cli_system_skill"]
    prompt_input_files = [item for item in codex_cli_files if item.source_type == "codex_cli_prompt_input"]
    cli_surface_files = [
        item for item in codex_cli_files if item.source_type == CLI_SURFACE_SOURCE_TYPE
    ]
    cli_surface_paths = coverage_paths_for_source(
        cli_surface_files, CLI_SURFACE_SOURCE_TYPE, preserve_missing_sources
    )
    codex_cli_source_errors = [item for item in failures if item["source"] == "codex_cli" and item["stage"] == "source_build"]
    coverage["codex_cli"] = {
        "source_kind": "installed_codex_cli",
        "version": codex_cli_metadata.get("codex_cli_version", ""),
        "version_raw": codex_cli_metadata.get("codex_cli_version_raw", ""),
        "platform_observations": collected_platforms,
        "system_skill_output_prefix": SYSTEM_SKILL_OUTPUT_PREFIX,
        "prompt_output_prefix": SYSTEM_PROMPT_OUTPUT_PREFIX,
        "prompt_snapshot_command": codex_cli_metadata.get("codex_prompt_snapshot_command", "codex debug prompt-input"),
        "system_skill_paths": sorted(item.rel_path for item in system_skill_files),
        "prompt_snapshot_paths": sorted(item.rel_path for item in prompt_input_files),
        "cli_surface_paths": cli_surface_paths,
        "source_errors": codex_cli_source_errors,
        "counts": {
            "system_skill_paths": len(system_skill_files),
            "prompt_snapshot_paths": len(prompt_input_files),
            "cli_surface_paths": len(cli_surface_paths),
            "source_errors": len(codex_cli_source_errors),
        },
    }
    coverage["system_skills"] = {
        "source_kind": "installed_codex_cli",
        "output_prefix": SYSTEM_SKILL_OUTPUT_PREFIX,
        "mirrored_paths_count": len(system_skill_files),
        "mirrored_paths": sorted(item.rel_path for item in system_skill_files),
        "page_fetch_errors": [],
        "counts": {
            "mirrored_paths_count": len(system_skill_files),
            "page_fetch_errors": 0,
        },
    }
    coverage["system_prompts"] = {
        "source_kind": "installed_codex_cli",
        "output_prefix": SYSTEM_PROMPT_OUTPUT_PREFIX,
        "mirrored_paths_count": len(prompt_input_files),
        "mirrored_paths": sorted(item.rel_path for item in prompt_input_files),
        "page_fetch_errors": [],
        "counts": {
            "mirrored_paths_count": len(prompt_input_files),
            "page_fetch_errors": 0,
        },
    }
    coverage["sync"] = {
        "preserve_missing_sources": sorted(preserve_missing_sources),
        "failure_count": len(failures),
        "status": "partial" if failures else "complete",
        "scope": "release" if release_only else "full",
        "web_observation": "last_known_good" if release_only else "current",
    }
    if failures and STRICT_SYNC_MODE:
        for failure in failures:
            LOG.error("Source transaction failed: %s", json.dumps(failure, sort_keys=True))
        LOG.error("Strict sync rejected the transaction; canonical outputs remain unchanged.")
        return 1
    if not release_only and not failures:
        coverage["web_snapshot"] = {"status": "complete", "last_successful_full_sync_at": now_utc_iso()}
    write_coverage(coverage)

    web_files = developers_files + learn_files + platform_tool_guide_files
    managed_files = annotate_markdown_files(
        github_files + codex_cli_files + capability_inventory_files + model_files
        + ([] if release_only else web_files),
        codex_cli_metadata,
    )
    if release_only:
        managed_files.extend(web_files)
    managed_files.extend(feature_files)
    if not managed_files:
        LOG.error("No source files were fetched successfully.")
        write_summary([], [], [], 0, failures=failures)
        return 1

    try:
        added, updated, removed = apply_sync(
            managed_files,
            failures=failures,
            preserve_missing_sources=sorted(preserve_missing_sources),
            source_metadata={**codex_cli_metadata, "sync_scope": "release" if release_only else "full"},
        )
    except Exception as exc:  # pragma: no cover - guardrail for sync bugs
        LOG.exception("Sync failed while writing output: %s", exc)
        return 1

    LOG.info("Managed files: %d", len(managed_files))
    LOG.info("Added: %d", len(added))
    LOG.info("Updated: %d", len(updated))
    LOG.info("Removed: %d", len(removed))

    if failures:
        LOG.warning("Sync completed with %d failure(s).", len(failures))
        for item in failures[:25]:
            LOG.warning(
                "failure source=%s stage=%s url=%s error=%s",
                item.get("source"),
                item.get("stage"),
                item.get("url"),
                item.get("error"),
            )
        if STRICT_SYNC_MODE:
            LOG.error("Strict sync mode is enabled and failures were detected.")
            return 1

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-only", action="store_true", help="Advance release-derived state using the last complete web mirror")
    parser.add_argument("--cli-observations-dir", type=Path)
    args = parser.parse_args()
    sys.exit(main(release_only=args.release_only, observations_dir=args.cli_observations_dir))
