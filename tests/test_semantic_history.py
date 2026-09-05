import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import fetch_codex_docs as sync
from scripts import semantic_history as history


class SemanticHistoryTests(unittest.TestCase):
    def test_identity_ignores_time_but_preserves_repeated_transitions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.json"
            first = history.record_event(path, {"visibility": "list"}, observed_at="09:00")
            content = path.read_bytes()
            retry = history.record_event(path, {"visibility": "list"}, observed_at="12:00")
            self.assertEqual(first, retry)
            self.assertEqual(content, path.read_bytes())
            history.record_event(path, {"visibility": "hide"}, observed_at="13:00")
            final = history.record_event(path, {"visibility": "list"}, observed_at="15:00")
            self.assertEqual(len({event["id"] for event in final["events"]}), 3)
            self.assertEqual(final["events"][0], first["events"][0])

    def test_daily_rollup_retains_both_events_and_legacy_report(self):
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(sync, "WEEKLY_DIR", Path(directory)):
            date = sync.datetime.now(sync.timezone.utc).strftime("%Y-%m-%d")
            report = Path(directory) / f"{date}.md"
            report.write_text("# Earlier meaningful event\n")
            sync.write_weekly_note(["models.json"], [], [], capability_changes={"added": ["gpt-6-astra"]})
            first = report.read_bytes()
            sync.write_weekly_note([], [], [])
            self.assertEqual(first, report.read_bytes())
            sync.write_weekly_note([], ["feature-flags/lifecycle.json"], [], capability_changes={
                "lifecycle_transitions": [{"id": "feature_flag:sample", "from": "experimental", "to": "stable"}],
            })
            final = report.read_text()
            self.assertIn("Earlier meaningful event", final)
            self.assertIn("models.json", final)
            self.assertIn("feature_flag:sample", final)
            ledger_path = Path(directory) / "events" / f"{date}.json"
            ledger = json.loads(ledger_path.read_text())
            self.assertEqual(len(ledger["events"]), 2)
            self.assertEqual(ledger["events"][0]["changes"]["capability_changes"]["added"], ["gpt-6-astra"])
            before = ledger_path.read_bytes()
            sync.write_weekly_note([], ["feature-flags/lifecycle.json"], [], capability_changes={
                "lifecycle_transitions": [{"id": "feature_flag:sample", "from": "experimental", "to": "stable"}],
            })
            self.assertEqual(before, ledger_path.read_bytes())
            self.assertEqual(final, report.read_text())

    def test_corrupt_ledger_fails_without_overwriting_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.json"
            path.write_text('{"schema_version": 9, "events": []}')
            with self.assertRaises(ValueError):
                history.record_event(path, {}, observed_at="now")
            self.assertEqual(path.read_text(), '{"schema_version": 9, "events": []}')
