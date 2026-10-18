import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

from scripts import fetch_codex_docs as sync
from test_fetch_codex_docs_extended import isolated_outputs


def capabilities(*identifiers):
    entries = [{"id": identifier, "category": "cli", "active": True} for identifier in identifiers]
    return json.dumps({"capabilities": entries}, indent=2) + "\n"


def managed(rel_path, content, source_type="github"):
    return sync.ManagedFile(rel_path, source_type, f"https://example.test/{rel_path}", content)


V1 = [
    managed(sync.CAPABILITIES_REL_PATH, capabilities("alpha"), sync.CAPABILITY_INVENTORY_SOURCE_TYPE),
    managed("github.openai.com/openai/codex/a.md", "# A v1\n"),
    managed("github.openai.com/openai/codex/b.md", "# B\n"),
    managed("github.openai.com/openai/codex/old.md", "# Old\n"),
]
# V2 updates the capabilities and a.md, keeps b.md, adds c.md, and removes old.md.
V2 = [
    managed(sync.CAPABILITIES_REL_PATH, capabilities("alpha", "beta"), sync.CAPABILITY_INVENTORY_SOURCE_TYPE),
    managed("github.openai.com/openai/codex/a.md", "# A v2\n"),
    managed("github.openai.com/openai/codex/b.md", "# B\n"),
    managed("github.openai.com/openai/codex/c.md", "# C\n"),
]
V2_RESULT = (["github.openai.com/openai/codex/c.md"], [sync.CAPABILITIES_REL_PATH, "github.openai.com/openai/codex/a.md"], ["github.openai.com/openai/codex/old.md"])
SOURCE_BUILDERS = (
    "build_developers_files", "build_learn_files", "build_codex_cli_files",
    "build_github_files", "build_model_catalog_file", "build_platform_tool_guide_files",
)


class SyncRecoveryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        stack = isolated_outputs(self.root)
        stack.__enter__()
        self.addCleanup(stack.close)

    def tree(self):
        return {str(path.relative_to(self.root)): path.read_bytes()
                for path in sorted(self.root.rglob("*")) if path.is_file()}

    def canonical(self):
        return {path.name: path.read_bytes() if path.exists() else None
                for path in (sync.MANIFEST_PATH, sync.SUMMARY_PATH, sync.COVERAGE_PATH)}

    def events(self):
        return [event for path in sorted((sync.WEEKLY_DIR / "events").glob("*.json"))
                for event in json.loads(path.read_text())["events"]]

    def assert_manifest_matches_disk(self):
        sources = json.loads(sync.MANIFEST_PATH.read_text())["sources"]
        self.assertTrue(sources)
        for rel_path, entry in sources.items():
            path = sync.output_path_for_rel_path(rel_path)
            self.assertTrue(path.exists(), rel_path)
            self.assertEqual(sync.sha256_content(path.read_bytes()), entry["sha256"], rel_path)

    def commit_v1(self, source_metadata=None):
        sync.apply_sync(V1, source_metadata=source_metadata)
        sync.write_coverage({"sync": {"status": "complete", "failure_count": 0}})

    def assert_v2_recovered(self, events_before):
        self.assertEqual(sync.apply_sync(V2), V2_RESULT)
        self.assert_manifest_matches_disk()
        self.assertFalse(sync.output_path_for_rel_path("github.openai.com/openai/codex/old.md").exists())
        new_events = self.events()[events_before:]
        self.assertEqual(len(new_events), 1)
        self.assertEqual(sorted(new_events[0]["changes"]["file_changes"]),
                         sorted(V2_RESULT[0] + V2_RESULT[1] + V2_RESULT[2]))
        self.assertEqual(new_events[0]["changes"]["capability_changes"]["added"], ["beta"])
        settled = self.tree()
        self.assertEqual(sync.apply_sync(V2), ([], [], []))
        self.assertEqual(settled, self.tree())

    # Manifest loading fails closed.

    def test_corrupt_manifest_json_fails_closed_everywhere(self):
        self.commit_v1()
        sync.MANIFEST_PATH.write_text('{"sources": {')
        before = self.tree()
        with self.assertRaisesRegex(sync.ManifestError, "git checkout -- docs/docs_manifest.json"):
            sync.load_existing_manifest()
        with self.assertRaises(sync.ManifestError):
            sync.manifest_paths_for_source_type("github")
        with self.assertRaises(sync.ManifestError):
            sync.load_cached_source_files({"github"})
        with self.assertRaises(sync.ManifestError):
            sync.apply_sync(V2)
        self.assertEqual(before, self.tree())

    def test_invalid_manifest_structures_fail_closed(self):
        self.commit_v1()
        entry = {"source_type": "github", "source_url": "https://example.test/a", "sha256": "a" * 64}
        payloads = (
            [],
            {"schema_version": 1, "sources": []},
            {"schema_version": 1, "sources": {"github.openai.com/openai/codex/a.md": "x"}},
            {"sources": {"github.openai.com/openai/codex/a.md": entry}},
            {"schema_version": 2, "sources": {"github.openai.com/openai/codex/a.md": entry}},
            # Partial entries would be skipped by release-only replay and then pruned.
            {"schema_version": 1, "sources": {"github.openai.com/openai/codex/a.md": {}}},
            {"schema_version": 1, "sources": {"github.openai.com/openai/codex/a.md": {**entry, "sha256": "not-a-digest"}}},
            {"schema_version": 1, "sources": {"github.openai.com/openai/codex/a.md": {**entry, "source_type": ""}}},
            {"schema_version": 1, "sources": {"github.openai.com/openai/codex/a.md": {**entry, "source_url": None}}},
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                sync.MANIFEST_PATH.write_text(json.dumps(payload))
                before = self.tree()
                with self.assertRaises(sync.ManifestError):
                    sync.load_existing_manifest()
                with self.assertRaises(sync.ManifestError):
                    sync.apply_sync(V2)
                self.assertEqual(before, self.tree())

    def test_invalid_manifest_paths_fail_before_fetching_or_publishing_history(self):
        self.commit_v1()
        committed = json.loads(sync.MANIFEST_PATH.read_text())
        entry = committed["sources"]["github.openai.com/openai/codex/a.md"]
        maintained_paths = ("README.md", "feature-flags/README.md", "dot_codex/config.toml")
        for rel_path in maintained_paths:
            path = sync.output_path_for_rel_path(rel_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("maintained source\n")
        for invalid_path in ("", ".", "../outside.md", "/outside.md", "github", *maintained_paths):
            with self.subTest(path=invalid_path):
                payload = {"schema_version": 1, "sources": {invalid_path: entry}}
                sync.MANIFEST_PATH.write_text(json.dumps(payload))
                before = self.tree()
                with ExitStack() as stack:
                    fetches = [
                        stack.enter_context(mock.patch.object(sync, name, side_effect=RuntimeError("synthetic offline")))
                        for name in SOURCE_BUILDERS
                    ]
                    stack.enter_context(mock.patch.object(sync, "STRICT_SYNC_MODE", True))
                    stack.enter_context(mock.patch.object(
                        sync.snapshot_feature_flags, "build_snapshot", side_effect=RuntimeError("synthetic offline")))
                    self.assertEqual(sync.main(), 1)
                for fetch in fetches:
                    fetch.assert_not_called()
                self.assertEqual(before, self.tree())

    def test_addition_orphaned_by_interrupted_transaction_is_removed(self):
        kept = managed(sync.github_path_to_rel_path("README.md"), "# Readme\n")
        added = managed(sync.github_path_to_rel_path("docs/new.md"), "# New\n")
        sync.apply_sync([kept])
        sync.write_coverage({"sync": {"status": "complete", "failure_count": 0}})
        with mock.patch.object(sync, "write_manifest", side_effect=OSError("synthetic")):
            with self.assertRaises(OSError):
                sync.apply_sync([kept, added])
        orphan = sync.output_path_for_rel_path(added.rel_path)
        self.assertTrue(orphan.exists())

        # Upstream dropped the page before the retry, so the plan no longer mentions it.
        self.assertEqual(sync.apply_sync([kept]), ([], [], []))
        self.assertFalse(orphan.exists())
        self.assertFalse(orphan.parent.exists())
        self.assert_manifest_matches_disk()
        on_disk = sorted(str(path.relative_to(sync.DOCS_DIR)) for path in sync.GITHUB_ROOT.rglob("*") if path.is_file())
        self.assertEqual(on_disk, [kept.rel_path])

    def test_cleanup_preserves_files_outside_documented_generated_subtrees(self):
        kept = managed(sync.github_path_to_rel_path("README.md"), "# Readme\n")
        sync.apply_sync([kept])
        maintained = (
            sync.ROOT / "dot_codex" / "config.toml",
            sync.ROOT / "dot_codex" / "skills" / "manual" / "SKILL.md",
            sync.ROOT / "system_prompts" / "maintained.txt",
            sync.DOCS_DIR / "feature-flags" / "README.md",
        )
        for path in maintained:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("maintained source, not generated\n")

        self.assertEqual(sync.apply_sync([kept]), ([], [], []))
        for path in maintained:
            self.assertTrue(path.exists(), str(path.relative_to(sync.ROOT)))
            self.assertEqual(path.read_text(), "maintained source, not generated\n")

    def test_orphaned_cli_and_feature_outputs_are_removed_on_changed_retry(self):
        kept = managed(sync.github_path_to_rel_path("README.md"), "# Readme\n")
        sync.apply_sync([kept])
        sync.write_coverage({"sync": {"status": "complete", "failure_count": 0}})
        additions = (
            managed("cli-surface/orphan.json", '{"commands": []}\n', "codex_cli_platform_observation"),
            managed("feature-flags/lifecycle.json", '{"features": []}\n', "feature_flags"),
        )
        with mock.patch.object(sync, "write_manifest", side_effect=OSError("synthetic")):
            with self.assertRaises(OSError):
                sync.apply_sync([kept, *additions])
        for item in additions:
            self.assertTrue(sync.output_path_for_rel_path(item.rel_path).exists())

        self.assertEqual(sync.apply_sync([kept]), ([], [], []))
        for item in additions:
            self.assertFalse(sync.output_path_for_rel_path(item.rel_path).exists(), item.rel_path)
        self.assert_manifest_matches_disk()

    def test_orphaned_top_level_generated_files_are_removed(self):
        kept = managed(sync.github_path_to_rel_path("README.md"), "# Readme\n")
        sync.apply_sync([kept])
        orphan_paths = (
            sync.CAPABILITIES_PATH,
            sync.CLI_SURFACE_PATH,
            sync.DOCS_DIR / sync.MODELS_REL_PATH,
        )
        for path in orphan_paths:
            path.write_text("{}\n")

        self.assertEqual(sync.apply_sync([kept]), ([], [], []))
        for path in orphan_paths:
            self.assertFalse(path.exists(), path.name)
        self.assert_manifest_matches_disk()


    def test_main_refuses_unusable_manifest_before_fetching_or_writing(self):
        self.commit_v1()
        valid_manifest = sync.MANIFEST_PATH.read_bytes()
        for label, corrupt in (("invalid", lambda: sync.MANIFEST_PATH.write_text("[]")),
                               ("missing", sync.MANIFEST_PATH.unlink)):
            with self.subTest(label), ExitStack() as stack:
                sync.MANIFEST_PATH.write_bytes(valid_manifest)
                corrupt()
                before = self.tree()
                builders = [stack.enter_context(mock.patch.object(sync, name)) for name in SOURCE_BUILDERS]
                features = stack.enter_context(mock.patch.object(sync.snapshot_feature_flags, "build_snapshot"))
                with self.assertLogs(sync.LOG, "ERROR") as logs:
                    self.assertEqual(sync.main(), 1)
                self.assertIn("Refusing to sync", "\n".join(logs.output))
                for builder in [*builders, features]:
                    builder.assert_not_called()
                self.assertEqual(before, self.tree())

    def test_missing_manifest_with_existing_coverage_fails_closed(self):
        self.commit_v1()
        sync.MANIFEST_PATH.unlink()
        before = self.tree()
        with self.assertRaisesRegex(sync.ManifestError, "bootstrap"):
            sync.load_existing_manifest()
        with self.assertRaises(sync.ManifestError):
            sync.apply_sync(V2)
        self.assertEqual(before, self.tree())

    def test_true_bootstrap_without_manifest_or_coverage_succeeds(self):
        self.assertEqual(sync.load_existing_manifest(), {})
        self.assertEqual(sync.apply_sync(V1), (sorted(item.rel_path for item in V1), [], []))
        self.assert_manifest_matches_disk()

    def test_unsafe_target_paths_fail_before_any_write(self):
        self.commit_v1()
        committed = sync.MANIFEST_PATH.read_bytes()
        manifest = json.loads(committed)
        manifest["sources"]["zz/../../outside.md"] = {"sha256": "0" * 64, "source_type": "github", "source_url": "u"}
        cases = (
            ("unsafe write", committed, [*V2, managed("zz/../../outside.md", "# Escape\n")]),
            ("unsafe removal", json.dumps(manifest).encode(), V2),
        )
        for label, manifest_bytes, files in cases:
            with self.subTest(label):
                sync.MANIFEST_PATH.write_bytes(manifest_bytes)
                before = self.tree()
                with self.assertRaises(ValueError):
                    sync.apply_sync(files)
                self.assertEqual(before, self.tree())

    # Every planned file is reconciled, not only manifest-hash changes.

    def test_missing_generated_file_with_unchanged_hash_is_repaired(self):
        self.commit_v1()
        manifest = sync.MANIFEST_PATH.read_bytes()
        sync.output_path_for_rel_path("github.openai.com/openai/codex/b.md").unlink()
        with self.assertLogs(sync.LOG, "WARNING"):
            self.assertEqual(sync.apply_sync(V1), ([], [], []))
        self.assert_manifest_matches_disk()
        self.assertEqual(manifest, sync.MANIFEST_PATH.read_bytes())

    def test_corrupted_generated_files_with_unchanged_hash_are_repaired(self):
        self.commit_v1()
        events_before = len(self.events())
        for rel_path in ("github.openai.com/openai/codex/a.md", sync.CAPABILITIES_REL_PATH):
            sync.output_path_for_rel_path(rel_path).write_bytes(b"\xff\xfe truncated")
        with self.assertLogs(sync.LOG, "WARNING"):
            self.assertEqual(sync.apply_sync(V1), ([], [], []))
        self.assert_manifest_matches_disk()
        self.assertEqual(events_before, len(self.events()))

    # Interrupted transactions keep canonical metadata and are recoverable.

    def test_failed_output_write_keeps_canonical_state_and_rerun_recovers(self):
        self.commit_v1()
        baseline = self.canonical()
        events_before = len(self.events())
        write = sync.write_file_if_changed
        calls = []

        def fail_third_write(path, content):
            calls.append(path)
            if len(calls) == 3:
                raise OSError("synthetic disk full")
            return write(path, content)

        with mock.patch.object(sync, "write_file_if_changed", side_effect=fail_third_write):
            with self.assertRaisesRegex(OSError, "synthetic"):
                sync.apply_sync(V2)
        self.assertEqual(baseline, self.canonical())
        written = sync.output_path_for_rel_path(sync.CAPABILITIES_REL_PATH).read_bytes()
        self.assertEqual(written, V2[0].content.encode())  # the disk is genuinely partial
        self.assert_v2_recovered(events_before)

    def test_failure_before_manifest_replacement_keeps_old_manifest(self):
        self.commit_v1()
        baseline = self.canonical()
        events_before = len(self.events())
        with mock.patch.object(sync, "remove_empty_directories", side_effect=OSError("synthetic")):
            with self.assertRaises(OSError):
                sync.apply_sync(V2)
        self.assertEqual(baseline, self.canonical())
        self.assertFalse(sync.output_path_for_rel_path("github.openai.com/openai/codex/old.md").exists())
        self.assert_v2_recovered(events_before)

    def test_failure_during_manifest_replacement_keeps_old_bytes_and_no_temp_files(self):
        self.commit_v1()
        baseline = self.canonical()
        events_before = len(self.events())
        with mock.patch.object(sync.os, "replace", side_effect=OSError("synthetic rename failure")):
            with self.assertRaisesRegex(OSError, "synthetic"):
                sync.apply_sync(V2)
        self.assertEqual(baseline, self.canonical())
        self.assertEqual([], [path for path in self.root.rglob("*") if path.name.endswith(".tmp")])
        self.assert_v2_recovered(events_before)

    def test_summary_interrupted_after_manifest_is_rewritten_by_next_run(self):
        self.commit_v1(source_metadata={"codex_cli_version": "1.0.0", "sync_scope": "full"})
        current = {"codex_cli_version": "2.0.0", "sync_scope": "full"}
        with mock.patch.object(sync, "write_summary", side_effect=OSError("synthetic")):
            with self.assertRaises(OSError):
                sync.apply_sync(V2, source_metadata=current)
        self.assertEqual("1.0.0", json.loads(sync.SUMMARY_PATH.read_text())["source_metadata"]["codex_cli_version"])

        self.assertEqual(sync.apply_sync(V2, source_metadata=current), ([], [], []))
        summary = json.loads(sync.SUMMARY_PATH.read_text())
        self.assertEqual(summary["source_metadata"], current)
        self.assertEqual(summary["total_files"], len(json.loads(sync.MANIFEST_PATH.read_text())["sources"]))
        # A no-op scope switch must not rewrite the success timestamp.
        before = sync.SUMMARY_PATH.read_bytes()
        sync.apply_sync(V2, source_metadata={**current, "sync_scope": "release"})
        self.assertEqual(before, sync.SUMMARY_PATH.read_bytes())

    def test_summary_interrupted_after_content_only_change_is_rewritten(self):
        # Same file count and release metadata: only the manifest digest tells the summaries apart.
        self.commit_v1(source_metadata={"codex_cli_version": "1.0.0", "sync_scope": "full"})
        content_only = [managed(item.rel_path, item.content.replace("v1", "v1.1"), item.source_type) for item in V1]
        with mock.patch.object(sync, "write_summary", side_effect=OSError("synthetic")):
            with self.assertRaises(OSError):
                sync.apply_sync(content_only, source_metadata={"codex_cli_version": "1.0.0", "sync_scope": "full"})
        stale = json.loads(sync.SUMMARY_PATH.read_text())

        self.assertEqual(sync.apply_sync(content_only, source_metadata={"codex_cli_version": "1.0.0", "sync_scope": "full"}),
                         ([], [], []))
        summary = json.loads(sync.SUMMARY_PATH.read_text())
        self.assertNotEqual(stale["manifest_sha256"], summary["manifest_sha256"])
        self.assertEqual(summary["manifest_sha256"], sync.sha256_content(sync.MANIFEST_PATH.read_bytes()))

    def test_retained_family_must_still_match_its_files(self):
        self.commit_v1()
        without_github = [item for item in V1 if item.source_type != "github"]
        for name, damage in (
            ("rewritten", lambda path: path.write_text("# half-written by an interrupted run\n")),
            ("removed", lambda path: path.unlink()),
        ):
            with self.subTest(name):
                retained = sync.output_path_for_rel_path("github.openai.com/openai/codex/b.md")
                damage(retained)
                before = self.tree()
                with self.assertRaisesRegex(sync.ManifestError, "github.openai.com/openai/codex/b.md"):
                    sync.apply_sync(without_github, failures=[{"source": "github"}], preserve_missing_sources=["github"])
                self.assertEqual(before, self.tree())
                retained.write_text("# B\n")

        # With intact files the unavailable family is retained as before.
        sync.apply_sync(without_github, failures=[{"source": "github"}], preserve_missing_sources=["github"])
        self.assert_manifest_matches_disk()
        self.assertIn("github.openai.com/openai/codex/b.md", json.loads(sync.MANIFEST_PATH.read_text())["sources"])

    # main() advances coverage only after a committed apply_sync.

    def full_sync_sources(self, version):
        metadata = {"codex_cli_version": version, "codex_cli_version_raw": f"codex-cli {version}",
                    "codex_cli_release_ref": f"rust-v{version}", "codex_cli_source_commit": "b" * 40}
        surface = sync.ManagedFile(sync.CLI_SURFACE_REL_PATH, sync.CLI_SURFACE_SOURCE_TYPE, "codex-cli://help",
                                   json.dumps({"codex_cli_version": version, "commands": [], "global_options": []}))
        model = sync.ManagedFile(sync.MODELS_REL_PATH, sync.MODEL_SOURCE_TYPE, "https://example.test/models",
                                 json.dumps({"models": [{"slug": "gpt-6-astra", "visibility": "list", "priority": 1}],
                                             "source_commit": "b" * 40}))
        returns = {
            "build_developers_files": ([managed("developers.openai.com/codex/a.md", "# D\n", "developers")], {"developers": {"counts": {}}}, []),
            "build_learn_files": ([managed("learn.chatgpt.com/docs/a/index.md", "# L\n", sync.LEARN_SOURCE_TYPE)], {"counts": {}}, []),
            "build_codex_cli_files": ([surface], [], metadata),
            "add_cli_release_provenance": ([surface], metadata),
            "prepare_cli_observations": ([surface], {}),
            "build_github_files": ([managed("github.openai.com/openai/codex/a.md", f"# G {version}\n")], []),
            "build_model_catalog_file": model,
            "build_platform_tool_guide_files": ([], [], {}),
            "build_capability_inventory_file": V1[0],
            "resolve_platform_ancestry": {},
            "resolve_cli_release_ancestry": {},
        }
        stack = ExitStack()
        stack.enter_context(mock.patch.object(sync, "STRICT_SYNC_MODE", True))
        for name, value in returns.items():
            stack.enter_context(mock.patch.object(sync, name, return_value=value))
        stack.enter_context(mock.patch.object(sync.snapshot_feature_flags, "build_snapshot", return_value=(
            {"source_ref": f"rust-v{version}", "source_commit": "b" * 40, "cli_features": []}, "# Features\n")))
        return stack

    def test_no_sources_built_preserves_committed_summary_and_coverage(self):
        self.commit_v1()
        before = self.tree()
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(sync, "STRICT_SYNC_MODE", False))
            for name in SOURCE_BUILDERS:
                stack.enter_context(mock.patch.object(sync, name, side_effect=RuntimeError("synthetic offline")))
            stack.enter_context(mock.patch.object(
                sync.snapshot_feature_flags, "build_snapshot", side_effect=RuntimeError("synthetic offline")))
            self.assertEqual(sync.main(), 1)
        self.assertEqual(before, self.tree())

    def test_failed_main_write_does_not_advance_coverage_or_summary(self):
        with self.full_sync_sources("1.2.4"):
            self.assertEqual(sync.main(), 0)
        baseline = self.canonical()
        for failure in (mock.patch.object(sync, "write_manifest", side_effect=OSError("synthetic")),
                        mock.patch.object(sync, "annotate_markdown_files", side_effect=RuntimeError("synthetic"))):
            with self.subTest(failure.attribute), self.full_sync_sources("1.2.5"), failure:
                self.assertEqual(sync.main(), 1)
                self.assertEqual(baseline, self.canonical())
        coverage = json.loads(sync.COVERAGE_PATH.read_text())
        self.assertEqual(coverage["codex_cli"]["version"], "1.2.4")
        self.assertEqual(json.loads(sync.SUMMARY_PATH.read_text())["source_metadata"]["codex_cli_version"], "1.2.4")

        with self.full_sync_sources("1.2.5"):
            self.assertEqual(sync.main(), 0)
        self.assertEqual(json.loads(sync.COVERAGE_PATH.read_text())["codex_cli"]["version"], "1.2.5")
        self.assertEqual(json.loads(sync.SUMMARY_PATH.read_text())["source_metadata"]["codex_cli_version"], "1.2.5")
        self.assertEqual(json.loads(sync.COVERAGE_PATH.read_text())["web_snapshot"]["status"], "complete")
        self.assert_manifest_matches_disk()

    def test_repeated_successful_sync_is_byte_identical(self):
        for version in ("1.2.4", "1.2.5"):
            with self.subTest(version), self.full_sync_sources(version):
                self.assertEqual(sync.main(), 0)
                first = self.tree()
                self.assertEqual(sync.main(), 0)
                self.assertEqual(first, self.tree())
                self.assert_manifest_matches_disk()


class DerivedEventKeyTests(unittest.TestCase):
    def test_derived_keys_are_ignored_only_when_detecting_a_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.json"
            first = {"file_changes": {"a": {"before": "1", "after": "2"}}, "capability_changes": {"added": ["x"]}}
            retry = {**first, "capability_changes": {}}
            sync.semantic_history.record_event(path, first, observed_at="09:00", derived_keys=("capability_changes",))
            content = path.read_bytes()
            sync.semantic_history.record_event(path, retry, observed_at="10:00", derived_keys=("capability_changes",))
            self.assertEqual(content, path.read_bytes())
            later = {**first, "file_changes": {"a": {"before": "2", "after": "3"}}}
            ledger = sync.semantic_history.record_event(path, later, observed_at="11:00", derived_keys=("capability_changes",))
            self.assertEqual([event["changes"] for event in ledger["events"]], [first, later])
            # Without derived keys every payload field still identifies the transaction.
            ledger = sync.semantic_history.record_event(path, {**later, "capability_changes": {}}, observed_at="12:00")
            self.assertEqual(len(ledger["events"]), 3)


if __name__ == "__main__":
    unittest.main()
