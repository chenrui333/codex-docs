import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import requests
import test_release_transaction as release_tests
from test_fetch_codex_docs_extended import isolated_outputs

from scripts import fetch_codex_docs as sync

FIXTURES = Path(__file__).parent / "fixtures" / "learn"
PRIMARY = "https://learn.chatgpt.com/chatgpt-sitemap-0.xml"
CHILD = "https://learn.chatgpt.com/sitemap-codex-localized.xml"
DOCS = "https://learn.chatgpt.com/docs/"


class LearnEvidenceTests(unittest.TestCase):
    def builders(self, child="localized.xml", *, root_failure=False):
        def fetch(_session, url):
            if url == sync.LEARN_SITEMAP_INDEX_URL:
                if root_failure:
                    raise requests.Timeout("root unavailable")
                return (FIXTURES / "index.xml").read_text()
            if url == PRIMARY:
                return (FIXTURES / "primary.xml").read_text()
            if isinstance(child, Exception):
                raise child
            if child == "recovered":
                return (FIXTURES / "localized.xml").read_text().replace("</urlset>", f"<url><loc>{DOCS}new-after-recovery</loc></url></urlset>")
            return (FIXTURES / child).read_text() if child.endswith(".xml") else child

        stack = ExitStack()
        stack.enter_context(release_tests.ReleaseTransactionTests().release_builders())
        stack.enter_context(mock.patch.object(sync, "build_developers_files", return_value=(
            [sync.ManagedFile("developers/page.md", "developers", "https://developers.openai.com/codex", "# Developer\n")],
            {"developers": {"counts": {}}}, [],
        )))
        stack.enter_context(mock.patch.object(sync, "fetch_text", side_effect=fetch))
        stack.enter_context(mock.patch.object(sync, "fetch_learn_page", side_effect=lambda _session, url: (
            f"# {url.rsplit('/', 1)[-1]}\n", {"source_kind": "learn_markdown"}, "markdown",
        )))
        stack.enter_context(mock.patch.object(sync, "build_platform_tool_guide_files", return_value=([], [], {})))
        return stack

    def snapshot(self, root):
        return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}

    def test_complete_children_record_actual_unique_paths_and_are_idempotent(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            with self.builders():
                self.assertEqual(sync.main(), 0)
                before = self.snapshot(Path(directory))
                with mock.patch.object(sync, "now_utc_iso", return_value="2099-01-01T00:00:00+00:00"):
                    self.assertEqual(sync.main(), 0)
            self.assertEqual(before, self.snapshot(Path(directory)))
            learn = json.loads(sync.COVERAGE_PATH.read_text())["learn"]
            self.assertEqual(learn["discovery_status"], "complete")
            self.assertEqual(learn["sitemap_observations"][CHILD]["unique_discovered_urls"], [DOCS + "child-only"])
            self.assertEqual(learn["sitemap_observations"][PRIMARY]["unique_discovered_urls"], [DOCS + "primary"])
            self.assertEqual(len(learn["discovered_urls"]), 3)

    def test_blocking_failures_keep_complete_snapshot_bytes_and_freshness(self):
        cases = [(requests.Timeout("timeout"), False), ("<urlset>", False), ("localized.xml", True)]
        for child, root_failure in cases:
            with self.subTest(child=child, root=root_failure), tempfile.TemporaryDirectory() as directory, \
                    tempfile.TemporaryDirectory() as diagnostic_dir, isolated_outputs(Path(directory)):
                with self.builders():
                    self.assertEqual(sync.main(), 0)
                before = self.snapshot(Path(directory))
                diagnostics = Path(diagnostic_dir) / "attempt.json"
                with self.builders(child, root_failure=root_failure):
                    for _ in range(2):
                        self.assertEqual(sync.main(diagnostics_path=diagnostics), 1)
                        self.assertEqual(before, self.snapshot(Path(directory)))
                attempt = json.loads(diagnostics.read_text())
                self.assertEqual(attempt["status"], "blocked")
                self.assertTrue(all(f["severity"] == "blocking" for f in attempt["failures"]))
                self.assertEqual(attempt["canonical_baseline"]["coverage_sha256"], sync.sha256_content(sync.COVERAGE_PATH.read_bytes()))
                if not root_failure:
                    learn = attempt["current_observation"]["learn"]
                    self.assertEqual(learn["removed_from_sitemap_urls_since_last_run"], [])
                    self.assertEqual(learn["unconfirmed_removed_urls_due_to_partial_sitemap"], [DOCS + "child-only"])
                    self.assertIsNone(learn["sitemap_observations"][CHILD]["discovered_urls"])
                    self.assertIsNone(learn["sitemap_observations"][PRIMARY]["unique_discovered_urls"])
                with self.builders("recovered"):
                    self.assertEqual(sync.main(), 0)
                recovered = json.loads(sync.COVERAGE_PATH.read_text())
                self.assertIn(DOCS + "new-after-recovery", recovered["learn"]["discovered_urls"])
                self.assertEqual(recovered["learn"]["sitemap_observations"][CHILD]["status"], "complete")
                recovered_bytes = self.snapshot(Path(directory))
                with self.builders("recovered"), mock.patch.object(sync, "now_utc_iso", return_value="2099-01-01T00:00:00+00:00"):
                    self.assertEqual(sync.main(), 0)
                self.assertEqual(recovered_bytes, self.snapshot(Path(directory)))

    def test_nonstrict_partial_discovery_retains_files_and_is_not_release_baseline(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            with self.builders():
                self.assertEqual(sync.main(), 0)
            path = sync.output_path_for_rel_path(sync.learn_url_to_rel_path(DOCS + "child-only"))
            original = path.read_bytes()
            with self.builders(requests.Timeout("timeout")), mock.patch.object(sync, "STRICT_SYNC_MODE", False):
                self.assertEqual(sync.main(), 0)
            self.assertEqual(path.read_bytes(), original)
            coverage = json.loads(sync.COVERAGE_PATH.read_text())
            self.assertEqual(coverage["learn"]["removed_from_sitemap_urls_since_last_run"], [])
            self.assertNotIn("web_snapshot", coverage)
            before = self.snapshot(Path(directory))
            with self.builders():
                self.assertEqual(sync.main(release_only=True), 1)
            self.assertEqual(before, self.snapshot(Path(directory)))

    def test_all_children_unavailable_without_baseline_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            with self.builders(), mock.patch.object(sync, "fetch_text", side_effect=[
                (FIXTURES / "index.xml").read_text(), requests.Timeout("one"), requests.Timeout("two"),
            ]):
                self.assertEqual(sync.main(), 1)
            self.assertFalse(sync.MANIFEST_PATH.exists())
            self.assertFalse(sync.COVERAGE_PATH.exists())

    def test_diagnostics_cannot_replace_canonical_files(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            for path in [sync.COVERAGE_PATH, sync.WEEKLY_DIR / "note.md", sync.ROOT / "dot_codex" / "skills.json"]:
                with self.assertRaisesRegex(ValueError, "outside canonical"):
                    sync.write_attempt_diagnostics(path, {}, [])
