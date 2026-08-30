import hashlib
import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from subprocess import TimeoutExpired
from unittest import mock

from scripts import fetch_codex_docs as sync


class FetchCodexDocsTests(unittest.TestCase):
    def test_canonicalize_url_removes_query_fragment_and_trailing_slash(self):
        self.assertEqual(
            sync.canonicalize_url("https://developers.openai.com/codex/cli/?q=1#top"),
            "https://developers.openai.com/codex/cli",
        )

    def test_chatgpt_plugin_url_has_an_explicit_classification(self):
        detail = sync.developers_skipped_url_detail(
            "https://developers.openai.com/learn/developers-codex-plugin"
        )

        self.assertIsNotNone(detail)
        self.assertEqual(detail["classification"], "chatgpt_plugin_page")

    def test_local_command_timeout_is_reported(self):
        with mock.patch.object(
            sync.subprocess,
            "run",
            side_effect=TimeoutExpired(["codex", "--version"], 120),
        ):
            with self.assertRaisesRegex(RuntimeError, "timed out after"):
                sync.run_local_command(["codex", "--version"])

    def test_output_path_rejects_absolute_and_parent_paths(self):
        with self.assertRaisesRegex(ValueError, "Unsafe managed output path"):
            sync.output_path_for_rel_path("../README.md")
        with self.assertRaisesRegex(ValueError, "Unsafe managed output path"):
            sync.output_path_for_rel_path("/tmp/output.md")

    def test_frontmatter_round_trip_and_version_history(self):
        content = sync.format_frontmatter(
            {
                "source_type": "github",
                "source_url": "https://example.test/doc",
                "codex_cli_versions": ["0.145.0", "0.146.0"],
            },
            "# Title\n",
        )
        metadata, body = sync.split_markdown_frontmatter(content)

        self.assertEqual(metadata["codex_cli_versions"], ["0.145.0", "0.146.0"])
        self.assertEqual(body, "# Title\n")

        history = sync.codex_cli_version_history_metadata(
            metadata,
            {
                "codex_cli_version": "0.146.0",
                "codex_cli_version_raw": "codex-cli 0.146.0",
            },
        )
        self.assertEqual(history["codex_cli_versions"], ["0.145.0", "0.146.0"])

    def test_apply_sync_is_idempotent_and_preserves_failed_source(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with self._isolated_outputs(root):
                managed = sync.ManagedFile(
                    rel_path="github.openai.com/openai/codex/docs/example.md",
                    source_type="github",
                    source_url="https://example.test/example.md",
                    content="# Example\n",
                )

                first = sync.apply_sync([managed])
                snapshot_after_first = self._tree_snapshot(root)
                second = sync.apply_sync([managed])
                snapshot_after_second = self._tree_snapshot(root)

                self.assertEqual(first, ([managed.rel_path], [], []))
                self.assertEqual(second, ([], [], []))
                self.assertEqual(snapshot_after_first, snapshot_after_second)

                preserved = sync.apply_sync([], preserve_missing_sources=["github"])
                self.assertEqual(preserved, ([], [], []))
                self.assertTrue((root / "docs" / managed.rel_path).exists())
                manifest = json.loads((root / "docs" / "docs_manifest.json").read_text())
                self.assertIn(managed.rel_path, manifest["sources"])

    @staticmethod
    def _tree_snapshot(root: Path) -> dict[str, str]:
        return {
            str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    @staticmethod
    def _isolated_outputs(root: Path):
        docs = root / "docs"
        patches = {
            "ROOT": root,
            "DOCS_DIR": docs,
            "WEEKLY_DIR": root / "weekly",
            "MANIFEST_PATH": docs / "docs_manifest.json",
            "SUMMARY_PATH": docs / "sync_summary.json",
            "COVERAGE_PATH": docs / "source_coverage.json",
            "CAPABILITIES_PATH": docs / "codex_capabilities.json",
            "CLI_SURFACE_PATH": docs / "codex_cli_surface.json",
            "FEATURE_LIFECYCLE": docs / "feature-flags" / "lifecycle.json",
            "DEVELOPERS_ROOT": docs / "developers.openai.com",
            "LEARN_ROOT": docs / "learn.chatgpt.com",
            "GITHUB_ROOT": docs / "github.openai.com" / "openai" / "codex",
            "PLATFORM_ROOT": docs / "platform.openai.com",
            "SYSTEM_SKILLS_ROOT": root / "dot_codex" / "skills" / "dot_system",
            "SYSTEM_PROMPTS_ROOT": root / "system_prompts" / "codex-cli",
        }
        stack = ExitStack()
        for name, value in patches.items():
            stack.enter_context(mock.patch.object(sync, name, value))
        return stack


if __name__ == "__main__":
    unittest.main()
