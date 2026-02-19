#!/usr/bin/env python3
"""Sync Codex-focused docs from developers.openai.com and openai/codex."""

from __future__ import annotations

import hashlib
import json
import logging
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from urllib.parse import ParseResult, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as to_markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
WEEKLY_DIR = ROOT / "weekly"
MANIFEST_PATH = DOCS_DIR / "docs_manifest.json"
SUMMARY_PATH = DOCS_DIR / "sync_summary.json"
DEVELOPERS_ROOT = DOCS_DIR / "developers.openai.com"
GITHUB_ROOT = DOCS_DIR / "github.openai.com" / "openai" / "codex"

SITEMAP_INDEX_URL = "https://developers.openai.com/sitemap-index.xml"
GITHUB_TREE_URL = "https://api.github.com/repos/openai/codex/git/trees/main?recursive=1"
USER_AGENT = "codex-docs-sync/0.1 (+https://github.com/chenrui333/codex-docs)"
REQUEST_TIMEOUT_SECONDS = 30

LOG = logging.getLogger("fetch_codex_docs")


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


def fetch_text(session: requests.Session, url: str) -> str:
    response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.text


def discover_developers_urls(session: requests.Session) -> List[str]:
    LOG.info("Discovering Codex URLs from %s", SITEMAP_INDEX_URL)
    index_xml = fetch_text(session, SITEMAP_INDEX_URL)
    sitemap_urls = parse_loc_tags(index_xml)
    urls: set[str] = set()

    for sitemap_url in sitemap_urls:
        try:
            sitemap_xml = fetch_text(session, sitemap_url)
        except requests.RequestException as exc:
            LOG.warning("Skipping sitemap %s due to error: %s", sitemap_url, exc)
            continue

        for raw_url in parse_loc_tags(sitemap_xml):
            cleaned = canonicalize_url(raw_url)
            if keep_developers_url(cleaned):
                urls.add(cleaned)

    return sorted(urls)


def developers_url_to_rel_path(url: str) -> str:
    parsed = urlparse(url)
    segments = [segment for segment in parsed.path.split("/") if segment]
    if not segments:
        segments = ["root"]
    path = DEVELOPERS_ROOT.joinpath(*segments, "index.md")
    return str(path.relative_to(DOCS_DIR))


def html_to_markdown(url: str, html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg", "canvas"]):
        tag.decompose()

    main = soup.find("main") or soup.find("article") or soup.body
    if main is None:
        main = soup

    title = None
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()

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
        if stripped in {"Copy PageMore page actions", "Copy Page", "More page actions"}:
            continue
        filtered_lines.append(line.rstrip())

    lines = filtered_lines
    normalized = "\n".join(lines)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip() + "\n"


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


def build_developers_files(session: requests.Session) -> List[ManagedFile]:
    managed: List[ManagedFile] = []
    for url in discover_developers_urls(session):
        try:
            html = fetch_text(session, url)
            content = html_to_markdown(url, html)
        except requests.RequestException as exc:
            LOG.warning("Skipping developers URL %s due to error: %s", url, exc)
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

    return managed


def build_github_files(session: requests.Session) -> List[ManagedFile]:
    managed: List[ManagedFile] = []

    for path in discover_github_paths(session):
        raw_url = f"https://raw.githubusercontent.com/openai/codex/main/{path}"
        try:
            raw_text = fetch_text(session, raw_url)
        except requests.RequestException as exc:
            LOG.warning("Skipping GitHub path %s due to error: %s", path, exc)
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

    return managed


def write_manifest(entries: Dict[str, Dict[str, str]]) -> None:
    payload = {
        "schema_version": 1,
        "sources": {key: entries[key] for key in sorted(entries)},
    }
    ensure_parent(MANIFEST_PATH)
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_summary(
    added: List[str], updated: List[str], removed: List[str], total: int
) -> None:
    payload = {
        "generated_at": now_utc_iso(),
        "total_files": total,
        "added": added,
        "updated": updated,
        "removed": removed,
    }
    ensure_parent(SUMMARY_PATH)
    SUMMARY_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


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

    if added:
        lines.append("## Added")
        lines.extend(f"- `{item}`" for item in added)
        lines.append("")

    if updated:
        lines.append("## Updated")
        lines.extend(f"- `{item}`" for item in updated)
        lines.append("")

    if removed:
        lines.append("## Removed")
        lines.extend(f"- `{item}`" for item in removed)
        lines.append("")

    weekly_path.write_text("\n".join(lines).rstrip() + "\n")


def apply_sync(managed_files: Iterable[ManagedFile]) -> Tuple[List[str], List[str], List[str]]:
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
    removed = sorted(previous_paths - next_paths)
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
    if has_changes or not SUMMARY_PATH.exists():
        write_summary(added, updated, removed, len(next_entries))
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

    try:
        developers_files = build_developers_files(session)
        github_files = build_github_files(session)
        managed_files = developers_files + github_files

        added, updated, removed = apply_sync(managed_files)

        LOG.info("Managed files: %d", len(managed_files))
        LOG.info("Added: %d", len(added))
        LOG.info("Updated: %d", len(updated))
        LOG.info("Removed: %d", len(removed))

        return 0
    except Exception as exc:  # pragma: no cover - guardrail for CI
        LOG.exception("Sync failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
