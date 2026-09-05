import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import cli_observations as cli
from scripts import collect_cli_surface as collector
from scripts import fetch_codex_docs as sync
from test_fetch_codex_docs_extended import isolated_outputs


def surface(os_name, commands=(), version="1.2.3", commit="a"):
    return {"codex_cli_version": version, "source_ref": f"rust-v{version}", "source_commit": commit * 40,
            "observation_environment": {"os": os_name, "arch": "arm64" if os_name == "darwin" else "x86_64"},
            "commands": [{"name": name, "options": [], "subcommands": []} for name in commands], "global_options": []}


METADATA = {"codex_cli_version": "1.2.4", "codex_cli_release_ref": "rust-v1.2.4", "codex_cli_source_commit": "b" * 40}


class CliObservationsTests(unittest.TestCase):
    def test_platform_union_preserves_positive_provenance(self):
        linux, mac = surface("linux", ["linux-only", "common"]), surface("darwin", ["app", "common"])
        result = cli.aggregate({"linux-x86_64": linux, "macos-arm64": mac}, METADATA)
        commands = {item["name"]: item for item in result["commands"]}
        self.assertEqual(set(commands["app"]["observed_on"]), {"macos-arm64"})
        self.assertEqual(set(commands["linux-only"]["observed_on"]), {"linux-x86_64"})
        self.assertEqual(len(commands["common"]["observed_on"]), 2)
        self.assertEqual(cli.aggregate({"macos-arm64": mac, "linux-x86_64": linux}, METADATA), result)

    def test_union_lifecycle_uses_each_platforms_lineage(self):
        before = {"linux-x86_64": {"active": True, "status": "present", "last_seen": cli.observation_metadata(surface("linux"))}}
        current = {"linux-x86_64": cli.observation_metadata(surface("linux", version="1.2.4", commit="b"))}
        for relationship, expected in (("ancestor", False), ("not_ancestor", True), ("unknown", True)):
            with self.subTest(relationship=relationship):
                states = cli.platform_states(before, {}, current, {f"{'a' * 40}...{'b' * 40}": relationship})
                self.assertEqual(states["linux-x86_64"]["active"], expected)
                self.assertEqual(cli.platform_states(states, {}, current, {f"{'a' * 40}...{'b' * 40}": relationship}), states)
        same = cli.platform_states(before, {}, {"linux-x86_64": before["linux-x86_64"]["last_seen"]}, {})
        self.assertTrue(same["linux-x86_64"]["active"])
        self.assertEqual(same["linux-x86_64"]["absence_reason"], "not_newer_release")
        current["macos-arm64"] = cli.observation_metadata(surface("darwin", version="1.2.4", commit="b"))
        moved = cli.platform_states(before, {"macos-arm64": current["macos-arm64"]}, current,
                                    {f"{'a' * 40}...{'b' * 40}": "ancestor"})
        self.assertFalse(moved["linux-x86_64"]["active"])
        self.assertTrue(moved["macos-arm64"]["active"])
        restored = cli.platform_states(moved, current, current, {})
        self.assertTrue(restored["linux-x86_64"]["active"])
        self.assertNotIn("removed_in_version", restored["linux-x86_64"])

    def test_inventory_stays_active_for_macos_only_command(self):
        linux = surface("linux", version="1.2.4", commit="b")
        mac = surface("darwin", ["app"])
        combined = cli.aggregate({"linux-x86_64": linux, "macos-arm64": mac}, METADATA)
        item = sync.ManagedFile(sync.CLI_SURFACE_REL_PATH, sync.CLI_SURFACE_SOURCE_TYPE, "generated://union", json.dumps(combined))
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            first = sync.build_capability_inventory_file([item], [], {}, METADATA)
            entry = json.loads(first.content)["capabilities"][0]
            self.assertTrue(entry["active"])
            self.assertFalse(entry["platforms"]["linux-x86_64"]["active"])
            self.assertEqual(entry["lifecycle"]["last_seen_version"], "1.2.3")
            self.assertEqual(entry["codex_cli_versions"], ["1.2.3"])
            sync.CAPABILITIES_PATH.parent.mkdir(parents=True)
            sync.CAPABILITIES_PATH.write_text(first.content)
            second = sync.build_capability_inventory_file([item], [], {}, METADATA)
            self.assertEqual(first.content, second.content)
            self.assertEqual(sync.semantic_capability_changes(first.content, second.content)["removed"], [])

    def test_failed_platform_collection_retains_its_last_good_raw_snapshot(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            mac = surface("darwin", ["app"])
            path = sync.DOCS_DIR / "cli-surface" / "macos-arm64.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(mac, indent=2, sort_keys=True) + "\n")
            linux = surface("linux", ["linux-only"], "1.2.4", "b")
            native = sync.ManagedFile(sync.CLI_SURFACE_REL_PATH, sync.CLI_SURFACE_SOURCE_TYPE, "codex-cli://help", json.dumps(linux))
            files, observations = sync.prepare_cli_observations([native], METADATA, Path(directory) / "missing-runner-artifacts")
            retained = next(item for item in files if item.rel_path == "cli-surface/macos-arm64.json")
            self.assertEqual(retained.content, path.read_text())
            self.assertEqual(observations["macos-arm64"]["codex_cli_version"], "1.2.3")
            self.assertEqual(observations["linux-x86_64"]["codex_cli_version"], "1.2.4")

    def test_malformed_platform_provenance_is_rejected(self):
        for field, value in (("source_ref", "main"), ("source_commit", "main"), ("commands", None)):
            with self.subTest(field=field), self.assertRaises(ValueError):
                cli.validate({**surface("linux"), field: value})
        with self.assertRaises(ValueError):
            cli.aggregate({"macos-arm64": surface("linux")}, METADATA)
        with self.assertRaises(ValueError):
            cli.aggregate({"linux-x86_64": surface("linux", ["duplicate", "duplicate"])}, METADATA)
        self.assertEqual(cli.platform_key(surface("windows")), "windows-x86_64")

    def test_collector_does_not_inherit_tokens_or_real_home(self):
        payload = surface("linux")
        item = sync.ManagedFile(sync.CLI_SURFACE_REL_PATH, sync.CLI_SURFACE_SOURCE_TYPE, "codex-cli://help", json.dumps(payload))
        with mock.patch.dict("os.environ", {"GH_TOKEN": "do-not-inherit", "GITHUB_TOKEN": "do-not-inherit", "OPENAI_API_KEY": "do-not-inherit"}), \
             mock.patch.object(collector.shutil, "which", return_value="fake-cli"), \
             mock.patch.object(sync, "run_local_command", return_value="codex-cli 1.2.3") as run, \
             mock.patch.object(sync, "build_cli_surface_snapshot", return_value=item), \
             mock.patch.object(sync, "add_cli_release_provenance", return_value=([], {
                 "codex_cli_release_ref": "rust-v1.2.3", "codex_cli_source_commit": "a" * 40,
             })):
            self.assertEqual(collector.collect()["source_commit"], "a" * 40)
            for call in run.call_args_list:
                env = call.kwargs["env"]
                self.assertFalse({"GH_TOKEN", "GITHUB_TOKEN", "OPENAI_API_KEY"} & env.keys())
                self.assertIn("cli-observation-", env["CODEX_HOME"])

    def test_removal_requires_descendants_on_every_previously_observed_platform(self):
        old_meta = {"codex_cli_version": "1.2.3", "codex_cli_release_ref": "rust-v1.2.3", "codex_cli_source_commit": "a" * 40}
        old = cli.aggregate({"linux-x86_64": surface("linux", ["common"]),
                             "macos-arm64": surface("darwin", ["common"], "1.2.2", "c")}, old_meta)
        current = cli.aggregate({"linux-x86_64": surface("linux", [], "1.2.4", "b"),
                                 "macos-arm64": surface("darwin", [], "1.2.4", "b")}, METADATA)
        for relationship in ("ancestor", "not_ancestor", "unknown"):
            with self.subTest(relationship=relationship), tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
                before = sync.build_capability_inventory_file([sync.ManagedFile(sync.CLI_SURFACE_REL_PATH, sync.CLI_SURFACE_SOURCE_TYPE,
                    "generated://union", json.dumps(old))], [], {}, old_meta)
                sync.CAPABILITIES_PATH.parent.mkdir(parents=True)
                sync.CAPABILITIES_PATH.write_text(before.content)
                item = sync.ManagedFile(sync.CLI_SURFACE_REL_PATH, sync.CLI_SURFACE_SOURCE_TYPE, "generated://union", json.dumps(current))
                ancestry = {f"{'a' * 40}...{'b' * 40}": "ancestor", f"{'c' * 40}...{'b' * 40}": relationship}
                after = sync.build_capability_inventory_file([item], [], {}, METADATA, platform_ancestry=ancestry)
                self.assertEqual(json.loads(after.content)["capabilities"][0]["active"], relationship != "ancestor")
                self.assertEqual(sync.semantic_capability_changes(before.content, after.content)["removed"],
                                 ["cli_command:common"] if relationship == "ancestor" else [])
                sync.CAPABILITIES_PATH.write_text(after.content)
                self.assertEqual(sync.build_capability_inventory_file([item], [], {}, METADATA, platform_ancestry=ancestry).content, after.content)

    def test_migration_recovers_last_recorded_platforms_with_their_own_provenance(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            (Path(directory) / ".git").mkdir()
            mac, linux = surface("darwin", ["app"]), surface("linux", [], "1.2.2", "c")
            def manifest(payload):
                return json.dumps({"sources": {sync.CLI_SURFACE_REL_PATH: {
                    "codex_cli_release_ref": payload["source_ref"], "codex_cli_source_commit": payload["source_commit"],
                }}})
            with mock.patch.object(sync, "run_local_command", side_effect=["head\nolder", json.dumps(mac), manifest(mac), json.dumps(linux), manifest(linux)]):
                recovered = sync.historical_cli_observations()
            self.assertEqual(recovered["linux-x86_64"]["source_commit"], "c" * 40)
            self.assertEqual(recovered["macos-arm64"]["source_commit"], "a" * 40)

    def test_unparseable_help_cannot_be_published_as_absence_evidence(self):
        with mock.patch.object(sync, "run_local_command", return_value="new or truncated help format"):
            with self.assertRaises(sync.SourceContentError):
                sync.build_cli_surface_snapshot("fake-cli", {}, Path("/tmp"), {"codex_cli_version": "1.2.3"})
