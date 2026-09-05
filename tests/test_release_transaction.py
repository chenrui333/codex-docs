import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

from scripts import fetch_codex_docs as sync
from test_fetch_codex_docs_extended import isolated_outputs


class ReleaseTransactionTests(unittest.TestCase):
    def seed(self):
        entries = {}
        for source in ("developers", "learn", sync.PLATFORM_TOOL_GUIDE_SOURCE_TYPE):
            path = f"{source}/page.md"
            item = sync.annotate_markdown_file(sync.ManagedFile(path, source, "https://example.test/page", "# Cached\n"), {})
            sync.write_file_if_changed(sync.output_path_for_rel_path(path), item.content)
            entries[path] = {"source_type": source, "source_url": item.source_url, "sha256": sync.sha256_content(item.content)}
        sync.write_manifest(entries)
        sync.write_coverage({"developers": {"counts": {}}, "learn": {"counts": {}},
                             "platform_tool_guides": {"references_by_url": {}}})
        return {path: sync.output_path_for_rel_path(path).read_bytes() for path in entries}

    def release_builders(self, *, broken=False):
        metadata = {"codex_cli_version": "1.2.4", "codex_cli_version_raw": "codex-cli 1.2.4",
                    "codex_cli_release_ref": "rust-v1.2.4", "codex_cli_source_commit": "b" * 40}
        surface = sync.ManagedFile(sync.CLI_SURFACE_REL_PATH, sync.CLI_SURFACE_SOURCE_TYPE, "codex-cli://help", json.dumps({
            "observation_environment": {"os": "linux", "arch": "x86_64"}, "commands": [], "global_options": [],
        }))
        model = sync.ManagedFile(sync.MODELS_REL_PATH, sync.MODEL_SOURCE_TYPE, "https://example.test/models", json.dumps({
            "models": [{"slug": "gpt-6-astra", "visibility": "list", "priority": 1}],
            "source_commit": "b" * 40,
        }))
        stack = ExitStack()
        stack.enter_context(mock.patch.object(sync, "STRICT_SYNC_MODE", True))
        stack.enter_context(mock.patch.object(sync, "build_codex_cli_files", return_value=([surface], [], metadata)))
        stack.enter_context(mock.patch.object(sync, "add_cli_release_provenance", return_value=([surface], metadata)))
        stack.enter_context(mock.patch.object(sync, "build_github_files", return_value=([
            sync.ManagedFile("github/release.md", "github", "https://example.test/release", "# Release\n")], [])))
        stack.enter_context(mock.patch.object(sync, "build_model_catalog_file", return_value=model,
                                             side_effect=RuntimeError("catalog timeout") if broken else None))
        stack.enter_context(mock.patch.object(sync.snapshot_feature_flags, "build_snapshot", return_value=({
            "source_ref": "rust-v1.2.4", "source_commit": "b" * 40, "cli_features": [],
        }, "# Features\n")))
        return stack

    def test_release_advances_without_contacting_unavailable_web_sources(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            cached = self.seed()
            with self.release_builders(), mock.patch.object(sync, "build_learn_files", side_effect=TimeoutError) as learn, \
                 mock.patch.object(sync, "build_developers_files", side_effect=TimeoutError) as developers, \
                 mock.patch.object(sync, "build_platform_tool_guide_files", side_effect=TimeoutError) as guides:
                self.assertEqual(sync.main(release_only=True), 0)
                before = {p: p.read_bytes() for p in Path(directory).rglob("*") if p.is_file()}
                self.assertEqual(sync.main(release_only=True), 0)
                self.assertEqual(before, {p: p.read_bytes() for p in Path(directory).rglob("*") if p.is_file()})
                for builder in (learn, developers, guides):
                    builder.assert_not_called()
            self.assertEqual(cached, {p: sync.output_path_for_rel_path(p).read_bytes() for p in cached})
            self.assertEqual(json.loads(sync.COVERAGE_PATH.read_text())["sync"]["web_observation"], "last_known_good")
            self.assertEqual(json.loads(sync.output_path_for_rel_path(sync.MODELS_REL_PATH).read_text())["source_commit"], "b" * 40)

    def test_failed_release_transaction_does_not_write_partial_outputs(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            self.seed()
            before = {p: p.read_bytes() for p in Path(directory).rglob("*") if p.is_file()}
            with self.release_builders(broken=True):
                self.assertEqual(sync.main(release_only=True), 1)
            self.assertEqual(before, {p: p.read_bytes() for p in Path(directory).rglob("*") if p.is_file()})

    def test_cached_family_must_match_its_manifest(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            self.seed()
            sync.output_path_for_rel_path("learn/page.md").write_text("partial content")
            with self.assertRaisesRegex(ValueError, "does not match"):
                sync.load_cached_source_files({"learn"})
