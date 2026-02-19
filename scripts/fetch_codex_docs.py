#!/usr/bin/env python3
"""Sync Codex-focused docs from developers.openai.com and openai/codex."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple
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
DEVELOPERS_ROOT = DOCS_DIR / "developers.openai.com"
GITHUB_ROOT = DOCS_DIR / "github.openai.com" / "openai" / "codex"

SITEMAP_INDEX_URL = "https://developers.openai.com/sitemap-index.xml"
GITHUB_TREE_URL = "https://api.github.com/repos/openai/codex/git/trees/main?recursive=1"
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
    ("Developers Codex", "developers.openai.com/codex/"),
    ("Developers Cookbook", "developers.openai.com/cookbook/"),
    ("Developers Resources", "developers.openai.com/resources/"),
    ("GitHub Core Docs", "github.openai.com/openai/codex/docs/"),
    ("GitHub Other Docs", "github.openai.com/openai/codex/"),
)


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
STRICT_SYNC_MODE = os.environ.get("CODEX_DOCS_STRICT_SYNC", "0") == "1"


@dataclass(frozen=True)
class ManagedFile:
    rel_path: str
    source_type: str
    source_url: str
    content: str


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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

    if path == "/cookbook/examples/gpt-5/codex_prompting_guide":
        return True

    return False


def is_codex_related_developers_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc != "developers.openai.com":
        return False
    path = parsed.path.rstrip("/")
    if not path:
        return False
    return "codex" in path.lower()


def fetch_text(session: requests.Session, url: str) -> str:
    last_error: Exception | None = None
    for attempt in range(1, REQUEST_MAX_RETRIES + 1):
        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            return response.text
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

    previous_coverage = load_existing_coverage()
    previous_developers = previous_coverage.get("developers", {})
    previous_codex_related = set()
    previous_mirrored = set()
    if isinstance(previous_developers, dict):
        previous_codex_related = set(previous_developers.get("codex_related_urls", []))
        previous_mirrored = set(previous_developers.get("mirrored_urls", []))

    new_codex_related = sorted(set(codex_related_sorted) - previous_codex_related)
    new_mirrored = sorted(set(mirrored_sorted) - previous_mirrored)

    LOG.info(
        "Coverage watchdog: codex-related=%d mirrored=%d skipped=%d",
        len(codex_related_sorted),
        len(mirrored_sorted),
        len(skipped_codex_related),
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
    if strict_coverage and new_codex_related and not new_mirrored:
        raise RuntimeError(
            "Strict coverage mode failed: new codex-related URLs were discovered but none were mirrored."
        )

    coverage = {
        "generated_at": now_utc_iso(),
        "developers": {
            "sitemap_index_url": SITEMAP_INDEX_URL,
            "sitemap_urls": sitemap_urls,
            "codex_related_urls": codex_related_sorted,
            "mirrored_urls": mirrored_sorted,
            "skipped_codex_related_urls": skipped_codex_related,
            "new_codex_related_urls_since_last_run": new_codex_related,
            "new_mirrored_urls_since_last_run": new_mirrored,
            "counts": {
                "sitemap_urls": len(sitemap_urls),
                "codex_related_urls": len(codex_related_sorted),
                "mirrored_urls": len(mirrored_sorted),
                "skipped_codex_related_urls": len(skipped_codex_related),
                "sitemap_fetch_errors": len(sitemap_fetch_errors),
            },
            "sitemap_fetch_errors": sitemap_fetch_errors,
        },
    }

    return mirrored_sorted, coverage


def developers_url_to_rel_path(url: str) -> str:
    parsed = urlparse(url)
    segments = [segment for segment in parsed.path.split("/") if segment]
    if not segments:
        segments = ["root"]
    path = DEVELOPERS_ROOT.joinpath(*segments, "index.md")
    return str(path.relative_to(DOCS_DIR))


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
    response = session.get(GITHUB_TREE_URL, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    payload = response.json()
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


def load_existing_manifest() -> Dict[str, Dict[str, str]]:
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

    parsed: Dict[str, Dict[str, str]] = {}
    for rel_path, meta in sources.items():
        if isinstance(meta, dict):
            parsed[rel_path] = {
                "sha256": str(meta.get("sha256", "")),
                "source_url": str(meta.get("source_url", "")),
                "source_type": str(meta.get("source_type", "")),
            }
    return parsed


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_file_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text() == content:
        return False

    ensure_parent(path)
    path.write_text(content)
    return True


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
            html = fetch_text(session, url)
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


def build_github_files(session: requests.Session) -> Tuple[List[ManagedFile], List[Dict[str, str]]]:
    managed: List[ManagedFile] = []
    fetch_errors: List[Dict[str, str]] = []

    for path in discover_github_paths(session):
        raw_url = f"https://raw.githubusercontent.com/openai/codex/main/{path}"
        try:
            raw_text = fetch_text(session, raw_url)
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
            )
        )

    return managed, fetch_errors


def write_manifest(entries: Dict[str, Dict[str, str]]) -> None:
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


def write_weekly_note(added: List[str], updated: List[str], removed: List[str]) -> None:
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

    weekly_path.write_text("\n".join(lines).rstrip() + "\n")


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
) -> Tuple[List[str], List[str], List[str]]:
    previous = load_existing_manifest()

    next_entries: Dict[str, Dict[str, str]] = {}
    rel_to_file: Dict[str, ManagedFile] = {}

    for item in managed_files:
        rel_to_file[item.rel_path] = item
        next_entries[item.rel_path] = {
            "sha256": sha256_text(item.content),
            "source_type": item.source_type,
            "source_url": item.source_url,
        }

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
        abs_path = DOCS_DIR / rel_path
        write_file_if_changed(abs_path, rel_to_file[rel_path].content)

    for rel_path in removed:
        abs_path = DOCS_DIR / rel_path
        if abs_path.exists():
            abs_path.unlink()

    remove_empty_directories(DEVELOPERS_ROOT)
    remove_empty_directories(GITHUB_ROOT)

    write_manifest(next_entries)
    has_changes = bool(added or updated or removed)
    summary_schema_stale = False
    if SUMMARY_PATH.exists():
        try:
            summary_payload = json.loads(SUMMARY_PATH.read_text())
            summary_schema_stale = not (
                isinstance(summary_payload, dict)
                and "failure_count" in summary_payload
                and "failures" in summary_payload
            )
        except json.JSONDecodeError:
            summary_schema_stale = True
    if has_changes or not SUMMARY_PATH.exists() or bool(failures) or summary_schema_stale:
        write_summary(added, updated, removed, len(next_entries), failures=failures)
    write_weekly_note(added, updated, removed)

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
    github_files: List[ManagedFile] = []
    developers_fetch_errors: List[Dict[str, str]] = []
    github_fetch_errors: List[Dict[str, str]] = []
    coverage: Dict[str, object] = {"generated_at": now_utc_iso()}

    try:
        developers_files, coverage, developers_fetch_errors = build_developers_files(session)
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
        github_files, github_fetch_errors = build_github_files(session)
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

    github_source_errors = [item for item in failures if item["source"] == "github" and item["stage"] == "source_build"]
    coverage["github"] = {
        "repo": "openai/codex",
        "mirrored_paths_count": len(github_files),
        "mirrored_paths": sorted(item.rel_path for item in github_files),
        "page_fetch_errors": github_fetch_errors,
        "source_errors": github_source_errors,
        "counts": {
            "mirrored_paths_count": len(github_files),
            "page_fetch_errors": len(github_fetch_errors),
            "source_errors": len(github_source_errors),
        },
    }
    coverage["sync"] = {
        "strict_sync_mode": STRICT_SYNC_MODE,
        "preserve_missing_sources": sorted(preserve_missing_sources),
        "failure_count": len(failures),
    }
    write_coverage(coverage)

    managed_files = developers_files + github_files
    if not managed_files:
        LOG.error("No source files were fetched successfully.")
        write_summary([], [], [], 0, failures=failures)
        return 1

    try:
        added, updated, removed = apply_sync(
            managed_files,
            failures=failures,
            preserve_missing_sources=sorted(preserve_missing_sources),
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
