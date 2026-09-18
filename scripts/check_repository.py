#!/usr/bin/env python3
"""Offline checks for authored Markdown links and repository configuration."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


def authored_markdown(root: Path) -> list[Path]:
    return sorted({*root.glob("*.md"), *(root / "audits").rglob("*.md"), *(root / ".github").rglob("*.md")})


def local_link_errors(root: Path, document: Path) -> list[str]:
    text = document.read_text()
    # Examples in fenced code are not rendered links. Preserve line numbers.
    text = re.sub(r"(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$", lambda match: "\n" * match[0].count("\n"), text)
    patterns = [
        r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+[^)]+)?\)",
        r"(?m)^\s*\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)",
        r'''(?:href|src)=["']([^"']+)["']''',
    ]
    errors = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            target = match[1].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = unquote(parsed.path)
            resolved = ((root / path.lstrip("/")) if path.startswith("/") else document.parent / path).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                line = text[:match.start()].count("\n") + 1
                errors.append(f"{document.relative_to(root)}:{line}: missing or outside-repository link: {target}")
    return errors


def unique_json_object(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def config_errors(root: Path) -> list[str]:
    errors = []
    try:
        config = json.loads((root / "renovate.json").read_text(), object_pairs_hook=unique_json_object)
        if not isinstance(config, dict):
            raise ValueError("expected a JSON object")
        if not isinstance(config.get("extends"), list) or not all(isinstance(item, str) for item in config["extends"]):
            raise ValueError("extends must be a list of preset names")
    except (OSError, ValueError) as error:
        errors.append(f"renovate.json: {error}")
    try:
        if not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\n?", (root / "VERSION").read_text()):
            errors.append("VERSION: expected x.y.z")
    except OSError as error:
        errors.append(f"VERSION: {error}")
    return errors


def main(root: Path) -> int:
    errors = config_errors(root)
    for document in authored_markdown(root):
        errors.extend(local_link_errors(root, document))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Authored Markdown paths, Renovate JSON, and VERSION passed offline checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(__file__).resolve().parent.parent))
