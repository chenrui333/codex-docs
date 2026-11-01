"""Isolated environments for Codex CLI subprocesses.

Every generator that executes the installed CLI uses this boundary, so user
configuration, credentials, and local paths cannot influence or leak into
generated artifacts.
"""

from __future__ import annotations

import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator, Mapping, NamedTuple

SAFE_CODEX_ENV_KEYS = frozenset({
    "COMSPEC",
    "LANG",
    "LC_ALL",
    "PATH",
    "PATHEXT",
    "SSL_CERT_DIR",
    "SSL_CERT_FILE",
    "SYSTEMROOT",
    "TMPDIR",
})


class CodexRuntime(NamedTuple):
    env: Dict[str, str]
    home: Path
    codex_home: Path
    workspace: Path


def isolated_codex_subprocess_env(base: Mapping[str, str] | None = None) -> Dict[str, str]:
    source = os.environ if base is None else base
    return {key: value for key, value in source.items() if key in SAFE_CODEX_ENV_KEYS}


@contextmanager
def isolated_codex_runtime(prefix: str, **overrides: str) -> Iterator[CodexRuntime]:
    """Yield an allowlisted environment with temporary home and workspace."""
    with tempfile.TemporaryDirectory(prefix=prefix) as directory:
        root = Path(directory)
        home, workspace = root / "home", root / "workspace"
        codex_home = home / ".codex"
        codex_home.mkdir(parents=True)
        workspace.mkdir()
        env = isolated_codex_subprocess_env()
        env.update(HOME=str(home), CODEX_HOME=str(codex_home), NO_COLOR="1", TZ="UTC")
        env.update(overrides)
        yield CodexRuntime(env, home, codex_home, workspace)
