"""Pure parsing of isolated CLI help observations."""

import re
from typing import Dict, List


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
