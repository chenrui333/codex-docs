import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

from scripts import fetch_codex_docs as sync
from scripts import snapshot_feature_flags as snapshot
from test_fetch_codex_docs_extended import isolated_outputs

FIXTURES = Path(__file__).parent / "fixtures"
BASIC_REL = snapshot.CONFIG_BASIC_DOC.relative_to(snapshot.DOCS_ROOT).as_posix()
REFERENCE_REL = snapshot.CONFIG_REFERENCE_DOC.relative_to(snapshot.DOCS_ROOT).as_posix()
METADATA = {
    "codex_cli_version": "1.2.4",
    "codex_cli_version_raw": "codex-cli 1.2.4",
    "codex_cli_release_ref": "rust-v1.2.4",
    "codex_cli_source_commit": "b" * 40,
}
FEATURES_SOURCE = 'FeatureSpec { key: "apps", stage: Stage::Stable, default_enabled: true, }'
CLIENT_SOURCE = (
    "(_, true) => Some(ResponsesWebsocketVersion::V2)\n"
    "(true, false) => Some(ResponsesWebsocketVersion::V1)\n"
    "(false, false) => None"
)
BASIC_V1 = (FIXTURES / "config-basic-current.md").read_text()
REFERENCE_V1 = (FIXTURES / "config-reference-current.md").read_text()
BASIC_V2 = BASIC_V1 + "\nUpdated upstream guidance.\n"
REFERENCE_V2 = REFERENCE_V1 + '\n    key: "features.transaction_probe",\n'


def fake_codex(argv, env=None, cwd=None):
    if argv[1:] == ["--version"]:
        return "codex-cli 1.2.4"
    return "apps  stable  true\ntransaction_probe  experimental  false"


def learn_family(*documents):
    files = [
        sync.ManagedFile(rel_path, sync.LEARN_SOURCE_TYPE, f"https://learn.example.test/{rel_path}", text)
        for rel_path, text in documents
    ]
    return files, {"counts": {}}, []


class FeatureSnapshotTransactionTests(unittest.TestCase):
    """A full sync must describe the Learn config docs it writes, not the previous mirror."""

    def transaction(self, root: Path) -> ExitStack:
        docs = root / "docs"
        surface = sync.ManagedFile(sync.CLI_SURFACE_REL_PATH, sync.CLI_SURFACE_SOURCE_TYPE, "codex-cli://help", json.dumps({
            "codex_cli_version": "1.2.4",
            "observation_environment": {"os": "linux", "arch": "x86_64"}, "commands": [], "global_options": [],
        }))
        model = sync.ManagedFile(sync.MODELS_REL_PATH, sync.MODEL_SOURCE_TYPE, "https://example.test/models", json.dumps({
            "models": [{"slug": "gpt-6-astra", "visibility": "list", "priority": 1}],
            "source_commit": "b" * 40,
        }))
        stack = ExitStack()
        stack.enter_context(isolated_outputs(root))
        for name, value in {
            "ROOT": root,
            "DOCS_ROOT": docs,
            "CONFIG_BASIC_DOC": docs / BASIC_REL,
            "CONFIG_REFERENCE_DOC": docs / REFERENCE_REL,
            "OUTPUT_DIR": docs / "feature-flags",
            "OUTPUT_JSON": docs / "feature-flags" / "lifecycle.json",
            "OUTPUT_MD": docs / "feature-flags" / "lifecycle.md",
        }.items():
            stack.enter_context(mock.patch.object(snapshot, name, value))
        stack.enter_context(mock.patch.object(snapshot, "run_command", side_effect=fake_codex))
        stack.enter_context(mock.patch.object(snapshot, "resolve_feature_source", return_value=("rust-v1.2.4", "b" * 40)))
        stack.enter_context(mock.patch.object(
            snapshot, "fetch_text", side_effect=lambda url: CLIENT_SOURCE if url.endswith("client.rs") else FEATURES_SOURCE))
        stack.enter_context(mock.patch.object(sync, "STRICT_SYNC_MODE", True))
        stack.enter_context(mock.patch.object(sync, "build_codex_cli_files", return_value=([surface], [], dict(METADATA))))
        stack.enter_context(mock.patch.object(sync, "add_cli_release_provenance", side_effect=lambda _s, files, meta: (files, meta)))
        stack.enter_context(mock.patch.object(sync, "build_github_files", return_value=([
            sync.ManagedFile("github/release.md", "github", "https://example.test/release", "# Release\n")], [])))
        stack.enter_context(mock.patch.object(sync, "build_model_catalog_file", return_value=model))
        stack.enter_context(mock.patch.object(sync, "build_platform_tool_guide_files", return_value=([], [], {})))
        developers = sync.ManagedFile("developers.openai.com/codex/index.md", "developers",
                                      "https://developers.example.test/codex", "# Codex\n")
        stack.enter_context(mock.patch.object(
            sync, "build_developers_files", return_value=([developers], {"developers": {"counts": {}}}, [])))
        stack.enter_context(mock.patch.object(sync, "resolve_cli_release_ancestry", return_value={}))
        return stack

    @staticmethod
    def tree(root: Path) -> dict:
        return {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}

    @staticmethod
    def lifecycle(root: Path) -> dict:
        return json.loads((root / "docs" / "feature-flags" / "lifecycle.json").read_text())

    def assert_snapshot_describes_mirror(self, root: Path) -> None:
        sources = self.lifecycle(root)["documentation_sources"]
        for name, rel_path in (("config_basic", BASIC_REL), ("config_reference", REFERENCE_REL)):
            written = (root / "docs" / rel_path).read_text()
            self.assertEqual(sources[name]["sha256"], snapshot.sha256_text(written), name)

    def test_changed_config_docs_are_snapshotted_in_the_same_transaction(self):
        with tempfile.TemporaryDirectory() as directory, self.transaction(Path(directory)):
            root = Path(directory)
            with mock.patch.object(sync, "build_learn_files", return_value=learn_family(
                    (BASIC_REL, BASIC_V1), (REFERENCE_REL, REFERENCE_V1))):
                self.assertEqual(sync.main(), 0)
            self.assert_snapshot_describes_mirror(root)
            self.assertNotIn("transaction_probe", self.lifecycle(root)["docs_feature_keys"])

            with mock.patch.object(sync, "build_learn_files", return_value=learn_family(
                    (BASIC_REL, BASIC_V2), (REFERENCE_REL, REFERENCE_V2))):
                self.assertEqual(sync.main(), 0)
                self.assert_snapshot_describes_mirror(root)
                payload = self.lifecycle(root)
                self.assertIn("transaction_probe", payload["docs_feature_keys"])
                self.assertEqual(payload["documentation_sources"]["config_reference"]["parsed_feature_key_count"], 3)

                # A standalone regeneration from the committed mirror agrees with the sync.
                standalone, _ = snapshot.build_snapshot()
                self.assertEqual(standalone["documentation_sources"], payload["documentation_sources"])

                before = self.tree(root)
                self.assertEqual(sync.main(), 0)
                self.assertEqual(before, self.tree(root))

    def test_learn_failure_does_not_promote_a_snapshot(self):
        with tempfile.TemporaryDirectory() as directory, self.transaction(Path(directory)):
            root = Path(directory)
            with mock.patch.object(sync, "build_learn_files", return_value=learn_family(
                    (BASIC_REL, BASIC_V1), (REFERENCE_REL, REFERENCE_V1))):
                self.assertEqual(sync.main(), 0)
            before = self.tree(root)
            with mock.patch.object(sync, "build_learn_files", side_effect=TimeoutError("sitemap timeout")):
                self.assertEqual(sync.main(), 1)
            self.assertEqual(before, self.tree(root))

    def test_removed_config_doc_is_not_described_from_the_stale_mirror(self):
        with tempfile.TemporaryDirectory() as directory, self.transaction(Path(directory)):
            root = Path(directory)
            with mock.patch.object(sync, "build_learn_files", return_value=learn_family(
                    (BASIC_REL, BASIC_V1), (REFERENCE_REL, REFERENCE_V1))):
                self.assertEqual(sync.main(), 0)
            before = self.tree(root)
            with mock.patch.object(sync, "build_learn_files", return_value=learn_family((BASIC_REL, BASIC_V2))):
                self.assertEqual(sync.main(), 1)
            self.assertEqual(before, self.tree(root))

    def test_release_only_snapshot_matches_committed_docs(self):
        with tempfile.TemporaryDirectory() as directory, self.transaction(Path(directory)):
            root = Path(directory)
            with mock.patch.object(sync, "build_learn_files", return_value=learn_family(
                    (BASIC_REL, BASIC_V2), (REFERENCE_REL, REFERENCE_V2))):
                self.assertEqual(sync.main(), 0)
            with mock.patch.object(sync, "build_learn_files", side_effect=AssertionError("release-only fetched Learn")):
                self.assertEqual(sync.main(release_only=True), 0)
                self.assert_snapshot_describes_mirror(root)
                before = self.tree(root)
                self.assertEqual(sync.main(release_only=True), 0)
                self.assertEqual(before, self.tree(root))

    def test_transaction_documents_cover_removal_and_retained_learn(self):
        files = [sync.ManagedFile(BASIC_REL, sync.LEARN_SOURCE_TYPE, "https://learn.example.test/basic", BASIC_V1)]
        complete = sync.transaction_feature_documents(files, METADATA, annotate=False, learn_retained=False)
        self.assertEqual(complete, {snapshot.CONFIG_BASIC_DOC: BASIC_V1, snapshot.CONFIG_REFERENCE_DOC: None})
        retained = sync.transaction_feature_documents(files, METADATA, annotate=False, learn_retained=True)
        self.assertEqual(retained, {snapshot.CONFIG_BASIC_DOC: BASIC_V1})

    def test_in_memory_documents_hash_like_the_written_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.md"
            path.write_bytes(b"line one\r\nline two\r")
            self.assertEqual(snapshot.read_config_document(path, {path: "line one\r\nline two\r"}), path.read_text())
            with self.assertRaisesRegex(snapshot.SnapshotError, "missing"):
                snapshot.read_config_document(path, {path: None})


if __name__ == "__main__":
    unittest.main()
