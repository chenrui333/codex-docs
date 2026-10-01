import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import fetch_codex_docs as sync
from scripts import model_catalog as catalog


def model(**overrides):
    return {"slug": "gpt-6-astra", "visibility": "hide", "priority": 1,
            "supported_reasoning_levels": [{"effort": "low"}, {"effort": "ultra"}],
            "input_modalities": ["image", "text"], **overrides}


class ModelCatalogTests(unittest.TestCase):
    def test_projection_excludes_prompts_and_ignores_order(self):
        payload = {"models": [model(model_messages={"instructions_template": "PRIVATE" * 10000})]}
        first = catalog.snapshot(payload, version="1.2.3", source_ref="rust-v1.2.3", source_commit="a" * 40)
        self.assertNotIn("PRIVATE", json.dumps(first))
        payload["models"][0]["supported_reasoning_levels"].reverse()
        payload["models"][0]["input_modalities"].reverse()
        second = catalog.snapshot(payload, version="1.2.3", source_ref="rust-v1.2.3", source_commit="a" * 40)
        self.assertEqual(first, second)
        self.assertEqual(catalog.changes(first, second), {"added": [], "removed": [], "changed": []})

    def test_visibility_change_is_one_structured_model_change(self):
        before = {"models": [model()]}
        after = {"models": [model(visibility="list")]}
        diff = catalog.changes(before, after)
        self.assertEqual(diff, {"added": [], "removed": [], "changed": [{
            "slug": "gpt-6-astra", "fields": {"visibility": {"before": "hide", "after": "list"}},
        }]})
        self.assertIn('`"hide"` -> `"list"`', "\n".join(catalog.render_changes(diff)))

    def test_runtime_fields_and_add_remove_are_semantic(self):
        for field, value in (("priority", 2), ("supported_reasoning_levels", [{"effort": "high"}]),
                             ("minimal_client_version", "1.2.4"), ("context_window", 272000),
                             ("supported_in_api", False), ("tool_mode", "code_mode_only"),
                             ("upgrade", {"model": "replacement"})):
            with self.subTest(field=field):
                diff = catalog.changes({"models": [model()]}, {"models": [model(**{field: value})]})
                self.assertEqual(list(diff["changed"][0]["fields"]), [field])
        diff = catalog.changes({"models": [model()]}, {"models": [model(slug="new")]})
        self.assertEqual(diff["added"], ["new"])
        self.assertEqual(diff["removed"], ["gpt-6-astra"])

    def test_missing_duplicate_or_malformed_models_fail_closed(self):
        for payload in ({}, {"models": []}, {"models": [None]}, {"models": [model(), model()]},
                        {"models": [model(priority=True)]}, {"models": [model(slug="")]}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                catalog.project_models(payload)
        for version, ref, commit in (("1.2.3", "main", "a" * 40),
                                     ("1.2.3", "rust-v1.2.3", "main"),
                                     ("1.2.3-beta", "rust-v1.2.3-beta", "a" * 40)):
            with self.assertRaises(ValueError):
                catalog.snapshot({"models": [model()]}, version=version, source_ref=ref, source_commit=commit)

    def test_builder_fetches_only_the_immutable_source(self):
        with mock.patch.object(sync, "fetch_json", return_value={"models": [model()]}) as fetch:
            item = sync.build_model_catalog_file(mock.sentinel.session, {
                "codex_cli_version": "1.2.3", "codex_cli_release_ref": "rust-v1.2.3",
                "codex_cli_source_commit": "a" * 40,
            })
            self.assertIn("a" * 40, fetch.call_args.args[1])
            self.assertEqual(json.loads(item.content)["source_commit"], "a" * 40)

    def test_model_event_replay_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(sync, "WEEKLY_DIR", Path(directory)):
            diff = catalog.changes({"models": [model()]}, {"models": [model(visibility="list")]})
            sync.write_weekly_note([], ["codex_models.json"], [], model_changes=diff)
            before = {p: p.read_bytes() for p in Path(directory).rglob("*") if p.is_file()}
            sync.write_weekly_note([], ["codex_models.json"], [], model_changes=copy.deepcopy(diff))
            self.assertEqual(before, {p: p.read_bytes() for p in before})
            report = next(Path(directory).glob("*.md")).read_text()
            self.assertEqual(report.count('`"hide"` -> `"list"`'), 1)
