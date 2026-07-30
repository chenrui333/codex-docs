#!/usr/bin/env python3
"""Sync Codex-focused docs from official OpenAI documentation sources."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Collection, Dict, Iterable, List, Sequence, Tuple
from urllib.parse import ParseResult, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as to_markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
WEEKLY_DIR = ROOT / "weekly"
MANIFEST_PATH = DOCS_DIR / "docs_manifest.json"
SUMMARY_PATH = DOCS_DIR / "sync_summary.json"
COVERAGE_PATH = DOCS_DIR / "source_coverage.json"
CAPABILITIES_PATH = DOCS_DIR / "codex_capabilities.json"
CAPABILITIES_REL_PATH = str(CAPABILITIES_PATH.relative_to(DOCS_DIR))
DEVELOPERS_ROOT = DOCS_DIR / "developers.openai.com"
LEARN_ROOT = DOCS_DIR / "learn.chatgpt.com"
GITHUB_ROOT = DOCS_DIR / "github.openai.com" / "openai" / "codex"
PLATFORM_ROOT = DOCS_DIR / "platform.openai.com"
SYSTEM_SKILLS_ROOT = ROOT / "dot_codex" / "skills" / "dot_system"
SYSTEM_PROMPTS_ROOT = ROOT / "system_prompts" / "codex-cli"

SYSTEM_SKILL_OUTPUT_PREFIX = "dot_codex/skills/dot_system/"
SYSTEM_PROMPT_OUTPUT_PREFIX = "system_prompts/codex-cli/"
ROOT_OUTPUT_PREFIXES = ("dot_codex/", "system_prompts/")
CODEX_CLI_SOURCE_TYPES = {"codex_cli_system_skill", "codex_cli_prompt_input"}
PLATFORM_TOOL_GUIDE_SOURCE_TYPE = "platform_tool_guide"
LEARN_SOURCE_TYPE = "learn"
CAPABILITY_INVENTORY_SOURCE_TYPE = "capability_inventory"
WEEKLY_REPORT_SOURCE_TYPE = "weekly_sync_report"
WEEKLY_REPORT_SOURCE_AREA = "weekly"
WEEKLY_REPORT_SOURCE_KIND = "generated_weekly_report"
SOURCE_METADATA_KEYS = (
    "source_area",
    "source_kind",
    "source_last_modified",
    "source_etag",
    "codex_cli_versions",
    "codex_cli_versions_raw",
    "codex_cli_version",
    "codex_cli_version_raw",
    "codex_cli_command",
    "codex_prompt_snapshot_command",
)

SITEMAP_INDEX_URL = "https://developers.openai.com/sitemap-index.xml"
LEARN_SITEMAP_INDEX_URL = "https://learn.chatgpt.com/sitemap-index.xml"
GITHUB_TREE_URL = "https://api.github.com/repos/openai/codex/git/trees/main?recursive=1"
GITHUB_RAW_URL_TEMPLATE = "https://raw.githubusercontent.com/openai/codex/main/{path}"
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


def parse_loc_tags(xml_text: str) -> List[str]:
    return re.findall(r"<loc>([^<]+)</loc>", xml_text)


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

    if path.startswith("/blog/"):
        return {
            "url": url,
            "classification": "blog_post",
            "reason": "Blog posts are intentionally excluded from the docs mirror.",
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


def github_raw_url(path: str) -> str:
    return GITHUB_RAW_URL_TEMPLATE.format(path=path)


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
    marker = "/openai/codex/main/"
    path = parsed.path.split(marker, 1)[1] if marker in parsed.path else parsed.path.lstrip("/")
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
        return {key: sanitize_prompt_payload(item, replacements) for key, item in value.items()}
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
    sitemap_urls = parse_loc_tags(index_xml)
    mirrored_urls: set[str] = set()
    codex_related_urls: set[str] = set()
    sitemap_fetch_errors: List[Dict[str, str]] = []

    for sitemap_url in sitemap_urls:
        try:
            sitemap_xml = fetch_text(session, sitemap_url)
        except requests.RequestException as exc:
            LOG.warning("Skipping sitemap %s due to error: %s", sitemap_url, exc)
            sitemap_fetch_errors.append(
                {
                    "source": "developers",
                    "stage": "sitemap_fetch",
                    "url": sitemap_url,
                    "error": str(exc),
                }
            )
            continue

        for raw_url in parse_loc_tags(sitemap_xml):
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
    sitemap_urls = sorted({canonicalize_url(url) for url in parse_loc_tags(index_xml)})
    if not sitemap_urls:
        raise RuntimeError("Learn sitemap index did not contain any sitemap URLs")

    discovered_urls: set[str] = set()
    sitemap_fetch_errors: List[Dict[str, str]] = []
    for sitemap_url in sitemap_urls:
        try:
            sitemap_xml = fetch_text(session, sitemap_url)
        except requests.RequestException as exc:
            LOG.warning("Skipping Learn sitemap %s due to error: %s", sitemap_url, exc)
            sitemap_fetch_errors.append(
                {
                    "source": LEARN_SOURCE_TYPE,
                    "stage": "sitemap_fetch",
                    "url": sitemap_url,
                    "error": str(exc),
                }
            )
            continue

        for raw_url in parse_loc_tags(sitemap_xml):
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
    return f"{heading}\n\n{source_line}\n\n{markdown_body}\n"


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


def discover_github_paths(session: requests.Session) -> List[str]:
    LOG.info("Discovering markdown files from openai/codex GitHub tree")
    payload = fetch_json(session, GITHUB_TREE_URL, headers=github_api_headers())
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
    developers_urls, coverage = discover_developers_urls(session)
    for url in developers_urls:
        try:
            html, source_metadata = fetch_text_with_source_metadata(session, url)
            content = html_to_markdown(url, html)
        except requests.RequestException as exc:
            LOG.warning("Skipping developers URL %s due to error: %s", url, exc)
            fetch_errors.append(
                {
                    "source": "developers",
                    "stage": "page_fetch",
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
        counts = developers_section.get("counts", {})
        if isinstance(counts, dict):
            counts["page_fetch_errors"] = len(fetch_errors)
        else:
            developers_section["counts"] = {"page_fetch_errors": len(fetch_errors)}

    return managed, coverage, fetch_errors


def fetch_learn_page(
    session: requests.Session,
    url: str,
) -> Tuple[str, Dict[str, object], str]:
    markdown_url = f"{url}.md"
    markdown_response = fetch_response(session, markdown_url, allowed_statuses=(404,))
    content_type = markdown_response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
    if markdown_response.status_code != 404 and content_type in {"text/markdown", "text/plain"}:
        metadata: Dict[str, object] = response_source_metadata(markdown_response)
        metadata["source_kind"] = "learn_markdown"
        content = markdown_with_source(url, markdown_response.text, default_title="ChatGPT Learn Docs")
        return content, metadata, "markdown"

    if markdown_response.status_code != 404:
        LOG.info("Learn Markdown endpoint returned %s for %s; using HTML fallback", content_type or "unknown", url)

    html_response = fetch_response(session, url)
    metadata = response_source_metadata(html_response)
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

    for url in learn_urls:
        try:
            content, source_metadata, fetch_mode = fetch_learn_page(session, url)
        except requests.RequestException as exc:
            LOG.warning("Skipping Learn URL %s due to error: %s", url, exc)
            failure = {
                "source": LEARN_SOURCE_TYPE,
                "stage": "page_fetch",
                "url": url,
                "error": str(exc),
            }
            page_fetch_errors.append(failure)
            fetch_errors.append(failure)
            continue

        mirrored_urls.append(url)
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
        }
    )
    return managed, coverage, fetch_errors


def build_github_files(session: requests.Session) -> Tuple[List[ManagedFile], List[Dict[str, str]]]:
    managed: List[ManagedFile] = []
    fetch_errors: List[Dict[str, str]] = []

    for path in discover_github_paths(session):
        raw_url = github_raw_url(path)
        try:
            raw_text, source_metadata = fetch_text_with_source_metadata(session, raw_url)
        except requests.RequestException as exc:
            LOG.warning("Skipping GitHub path %s due to error: %s", path, exc)
            fetch_errors.append(
                {
                    "source": "github",
                    "stage": "page_fetch",
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
                source_metadata=source_metadata,
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
    "codex_cli_versions",
    "codex_cli_versions_raw",
    "report_date",
    "name",
    "description",
)
PRESERVED_FRONTMATTER_SOURCE_KEYS = ("source_last_modified", "source_etag")


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
    for key in ("source_area", "source_kind", "source_last_modified", "source_etag"):
        if source_metadata.get(key):
            frontmatter[key] = source_metadata[key]

    for key in ("source_area", "source_kind", "source_last_modified", "source_etag"):
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

    apply_codex_version_history(metadata, source_metadata, existing_frontmatter, codex_cli_metadata)

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
    for item in capabilities:
        category = str(item.get("category", "unknown"))
        by_category[category] = by_category.get(category, 0) + 1
    return {
        "total": len(capabilities),
        "by_category": {key: by_category[key] for key in sorted(by_category)},
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


def build_capability_inventory_file(
    codex_cli_files: Sequence[ManagedFile],
    platform_tool_guide_files: Sequence[ManagedFile],
    referenced_platform_tool_guides_by_url: Dict[str, List[str]],
    codex_cli_metadata: Dict[str, str],
) -> ManagedFile:
    capabilities: List[Dict[str, object]] = []
    codex_cli_version = codex_cli_metadata.get("codex_cli_version", "")
    codex_cli_version_raw = codex_cli_metadata.get("codex_cli_version_raw", "")
    previous_inventory = load_existing_capability_inventory()
    previous_capabilities = existing_capabilities_by_id(previous_inventory)

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

    capabilities = sorted(capabilities, key=lambda item: str(item["id"]))
    payload = {
        "schema_version": 1,
        "source_kind": "generated_capability_inventory",
        "source_area": "capability_inventory",
        "codex_cli_version": codex_cli_metadata.get("codex_cli_version", ""),
        "codex_cli_version_raw": codex_cli_metadata.get("codex_cli_version_raw", ""),
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
        return {"total": 0, "by_category": {}}
    capabilities = payload.get("capabilities", []) if isinstance(payload, dict) else []
    if not isinstance(capabilities, list):
        return {"total": 0, "by_category": {}}
    return capability_counts([item for item in capabilities if isinstance(item, dict)])


def capability_inventory_counts(
    inventory_files: Sequence[ManagedFile],
    preserve_missing_sources: set[str],
) -> Dict[str, object]:
    if inventory_files:
        return capability_inventory_counts_from_text(managed_file_text(inventory_files[0]))
    if CAPABILITY_INVENTORY_SOURCE_TYPE in preserve_missing_sources and CAPABILITIES_PATH.exists():
        return capability_inventory_counts_from_text(CAPABILITIES_PATH.read_text())
    return {"total": 0, "by_category": {}}


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

        env = codex_subprocess_env()
        env.update(
            {
                "HOME": str(home_path),
                "CODEX_HOME": str(codex_home),
                "NO_COLOR": "1",
                "SHELL": "/bin/bash",
                "TZ": "UTC",
            }
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


def write_coverage(coverage: Dict[str, object]) -> None:
    coverage_without_generated_at = {k: v for k, v in coverage.items() if k != "generated_at"}
    if COVERAGE_PATH.exists():
        try:
            previous = json.loads(COVERAGE_PATH.read_text())
            if isinstance(previous, dict):
                previous_has_generated_at = "generated_at" in previous
                previous_without_generated_at = {k: v for k, v in previous.items() if k != "generated_at"}
                if previous_has_generated_at and previous_without_generated_at == coverage_without_generated_at:
                    return
        except json.JSONDecodeError:
            pass

    ensure_parent(COVERAGE_PATH)
    COVERAGE_PATH.write_text(json.dumps(coverage, indent=2, sort_keys=True) + "\n")


def write_weekly_note(
    added: List[str],
    updated: List[str],
    removed: List[str],
    source_metadata: Dict[str, object] | None = None,
) -> None:
    if not (added or updated or removed):
        return

    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    date_tag = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    weekly_path = WEEKLY_DIR / f"{date_tag}.md"

    lines = [
        f"# Codex Docs Sync - {date_tag}",
        "",
        f"Generated at: {now_utc_iso()}",
        "",
        f"- Added: {len(added)}",
        f"- Updated: {len(updated)}",
        f"- Removed: {len(removed)}",
        "",
    ]

    if source_metadata:
        lines.append("## Source Snapshot")
        lines.append("")
        for key in SOURCE_METADATA_KEYS:
            value = source_metadata.get(key)
            if value:
                lines.append(f"- `{key}`: `{value}`")
        lines.append("")

    lines.append("## Category Summary")
    lines.append("")
    lines.extend(render_category_summary("Added", added))
    lines.extend(render_category_summary("Updated", updated))
    lines.extend(render_category_summary("Removed", removed))

    if added:
        lines.append("## Added (Raw Paths)")
        lines.extend(f"- `{item}`" for item in added)
        lines.append("")

    if updated:
        lines.append("## Updated (Raw Paths)")
        lines.extend(f"- `{item}`" for item in updated)
        lines.append("")

    if removed:
        lines.append("## Removed (Raw Paths)")
        lines.extend(f"- `{item}`" for item in removed)
        lines.append("")

    body = "\n".join(lines).rstrip() + "\n"
    existing_metadata: Dict[str, object] = {}
    if weekly_path.exists():
        existing_metadata, _ = split_markdown_frontmatter(weekly_path.read_text())
    metadata = weekly_report_metadata(
        date_tag,
        body,
        existing_metadata=existing_metadata,
        source_metadata=source_metadata,
    )
    weekly_path.write_text(format_frontmatter(metadata, body))


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


def apply_sync(
    managed_files: Iterable[ManagedFile],
    failures: List[Dict[str, str]] | None = None,
    preserve_missing_sources: Sequence[str] = (),
    source_metadata: Dict[str, object] | None = None,
) -> Tuple[List[str], List[str], List[str]]:
    previous = load_existing_manifest()

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
                for key in SOURCE_METADATA_KEYS
                if key != "source_kind" and previous_same_hash and previous_meta.get(key)
            }
            next_entry.update(item.source_metadata)
            next_entry.update(preserved_metadata)
            if item.source_metadata.get("source_kind"):
                next_entry["source_kind"] = item.source_metadata["source_kind"]
        next_entries[item.rel_path] = next_entry

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
    write_weekly_note(added, updated, removed, source_metadata=source_metadata)
    ensure_weekly_frontmatter()

    return added, updated, removed


def main() -> int:
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
    developers_fetch_errors: List[Dict[str, str]] = []
    learn_fetch_errors: List[Dict[str, str]] = []
    github_fetch_errors: List[Dict[str, str]] = []
    platform_tool_guide_fetch_errors: List[Dict[str, str]] = []
    platform_tool_guide_references_by_url: Dict[str, List[str]] = {}
    codex_cli_fetch_errors: List[Dict[str, str]] = []
    codex_cli_metadata: Dict[str, str] = {}
    coverage: Dict[str, object] = {"generated_at": now_utc_iso()}

    try:
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
        github_files, github_fetch_errors = build_github_files(session)
        github_files = add_source_area_metadata(github_files)
        failures.extend(github_fetch_errors)
        if github_fetch_errors:
            preserve_missing_sources.add("github")
    except Exception as exc:
        LOG.warning("GitHub source failed; continuing with remaining sources: %s", exc)
        failure = {
            "source": "github",
            "stage": "source_build",
            "url": "https://github.com/openai/codex",
            "error": str(exc),
        }
        failures.append(failure)
        preserve_missing_sources.add("github")

    try:
        codex_cli_files, codex_cli_fetch_errors, codex_cli_metadata = build_codex_cli_files()
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
            "url": "codex-cli://installed",
            "error": str(exc),
        }
        failures.append(failure)
        preserve_missing_sources.update(CODEX_CLI_SOURCE_TYPES)

    try:
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
            "url": "https://platform.openai.com/docs/guides",
            "error": str(exc),
        }
        failures.append(failure)
        preserve_missing_sources.add(PLATFORM_TOOL_GUIDE_SOURCE_TYPE)

    if preserve_missing_sources:
        preserve_missing_sources.add(CAPABILITY_INVENTORY_SOURCE_TYPE)
    else:
        capability_inventory_files = [
            build_capability_inventory_file(
                codex_cli_files,
                platform_tool_guide_files,
                platform_tool_guide_references_by_url,
                codex_cli_metadata,
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
    codex_cli_source_errors = [item for item in failures if item["source"] == "codex_cli" and item["stage"] == "source_build"]
    coverage["codex_cli"] = {
        "source_kind": "installed_codex_cli",
        "version": codex_cli_metadata.get("codex_cli_version", ""),
        "version_raw": codex_cli_metadata.get("codex_cli_version_raw", ""),
        "system_skill_output_prefix": SYSTEM_SKILL_OUTPUT_PREFIX,
        "prompt_output_prefix": SYSTEM_PROMPT_OUTPUT_PREFIX,
        "prompt_snapshot_command": codex_cli_metadata.get("codex_prompt_snapshot_command", "codex debug prompt-input"),
        "system_skill_paths": sorted(item.rel_path for item in system_skill_files),
        "prompt_snapshot_paths": sorted(item.rel_path for item in prompt_input_files),
        "source_errors": codex_cli_source_errors,
        "counts": {
            "system_skill_paths": len(system_skill_files),
            "prompt_snapshot_paths": len(prompt_input_files),
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
    }
    write_coverage(coverage)

    managed_files = annotate_markdown_files(
        developers_files
        + learn_files
        + github_files
        + platform_tool_guide_files
        + codex_cli_files
        + capability_inventory_files,
        codex_cli_metadata,
    )
    if not managed_files:
        LOG.error("No source files were fetched successfully.")
        write_summary([], [], [], 0, failures=failures)
        return 1

    try:
        added, updated, removed = apply_sync(
            managed_files,
            failures=failures,
            preserve_missing_sources=sorted(preserve_missing_sources),
            source_metadata=codex_cli_metadata,
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
    sys.exit(main())
