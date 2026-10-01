import json
import tempfile
import unittest
from pathlib import Path
from subprocess import TimeoutExpired
from unittest import mock

from scripts import snapshot_feature_flags as snapshot


class SnapshotFeatureFlagsTests(unittest.TestCase):
    FIXTURES = Path(__file__).parent / "fixtures"

    def test_command_timeout_and_failures(self):
        with mock.patch.dict(snapshot.os.environ, {}, clear=True):
            self.assertEqual(snapshot.command_timeout_seconds(), 120.0)
        with mock.patch.dict(
            snapshot.os.environ,
            {"CODEX_DOCS_COMMAND_TIMEOUT_SECONDS": "0"},
            clear=True,
        ):
            self.assertEqual(snapshot.command_timeout_seconds(), 0.1)
        with mock.patch.dict(
            snapshot.os.environ,
            {"CODEX_DOCS_COMMAND_TIMEOUT_SECONDS": "bad"},
            clear=True,
        ):
            with self.assertRaisesRegex(snapshot.SnapshotError, "must be a number"):
                snapshot.command_timeout_seconds()

        failed = mock.Mock(returncode=2, stdout="out", stderr="err")
        with mock.patch.object(snapshot.subprocess, "run", return_value=failed):
            with self.assertRaisesRegex(snapshot.SnapshotError, "Command failed"):
                snapshot.run_command(["codex", "features", "list"])

    def test_parse_features_list(self):
        rows = snapshot.parse_features_list(
            "stable_flag  stable  true\nexperimental_flag  experimental  false\n"
        )

        self.assertEqual(
            rows,
            [
                {"key": "stable_flag", "stage": "stable", "enabled": True},
                {"key": "experimental_flag", "stage": "experimental", "enabled": False},
            ],
        )

    def test_parse_features_list_rejects_changed_cli_shape(self):
        with self.assertRaisesRegex(snapshot.SnapshotError, "Unexpected"):
            snapshot.parse_features_list("flag stable true extra")

    def test_codex_subprocess_env_removes_github_tokens(self):
        environment = snapshot.codex_subprocess_env(
            {"GH_TOKEN": "secret", "GITHUB_TOKEN": "secret", "PATH": "/bin"}
        )

        self.assertEqual(environment, {"PATH": "/bin"})

    def test_command_timeout_is_reported(self):
        with mock.patch.object(
            snapshot.subprocess,
            "run",
            side_effect=TimeoutExpired(["codex", "--version"], 120),
        ):
            with self.assertRaisesRegex(snapshot.SnapshotError, "timed out after"):
                snapshot.run_command(["codex", "--version"])

    def test_resolve_lightweight_release_tag(self):
        commit = "a" * 40

        source_ref, source_commit = snapshot.resolve_feature_source(
            "codex-cli 0.146.0",
            fetch_json_fn=lambda _url: {
                "object": {"type": "commit", "sha": commit}
            },
        )

        self.assertEqual(source_ref, "rust-v0.146.0")
        self.assertEqual(source_commit, commit)

    def test_resolve_annotated_release_tag(self):
        tag_url = f"{snapshot.OSS_REPOSITORY_API_URL}/git/tags/{'b' * 40}"
        responses = {
            f"{snapshot.OSS_REPOSITORY_API_URL}/git/ref/tags/rust-v0.146.0": {
                "object": {"type": "tag", "url": tag_url}
            },
            tag_url: {"object": {"type": "commit", "sha": "c" * 40}},
        }

        source_ref, source_commit = snapshot.resolve_feature_source(
            "codex-cli 0.146.0", fetch_json_fn=responses.__getitem__
        )

        self.assertEqual(source_ref, "rust-v0.146.0")
        self.assertEqual(source_commit, "c" * 40)

    def test_source_override_must_be_a_full_commit(self):
        with self.assertRaisesRegex(snapshot.SnapshotError, "40-character"):
            snapshot.resolve_feature_source("codex-cli 0.146.0", "abc123")

    def test_source_override_must_match_release_tag(self):
        commit = "a" * 40
        source_ref, source_commit = snapshot.resolve_feature_source(
            "codex-cli 0.146.0",
            commit,
            fetch_json_fn=lambda _url: {
                "object": {"type": "commit", "sha": commit}
            },
        )
        self.assertEqual(source_ref, "rust-v0.146.0")
        self.assertEqual(source_commit, commit)

        with self.assertRaisesRegex(snapshot.SnapshotError, "does not match"):
            snapshot.resolve_feature_source(
                "codex-cli 0.146.0",
                "b" * 40,
                fetch_json_fn=lambda _url: {
                    "object": {"type": "commit", "sha": commit}
                },
            )

    def test_release_tag_response_must_contain_an_object(self):
        with self.assertRaisesRegex(snapshot.SnapshotError, "object target"):
            snapshot.resolve_feature_source(
                "codex-cli 0.146.0", fetch_json_fn=lambda _url: {}
            )

    def test_tag_resolution_and_version_validation_fail_closed(self):
        with self.assertRaisesRegex(snapshot.SnapshotError, "derive"):
            snapshot.feature_source_ref("development")
        with self.assertRaisesRegex(snapshot.SnapshotError, "unsupported"):
            snapshot.resolve_tag_commit(
                "rust-v1.2.3",
                fetch_json_fn=lambda _url: {"object": {"type": "tree"}},
            )
        with self.assertRaisesRegex(snapshot.SnapshotError, "invalid tag object URL"):
            snapshot.resolve_tag_commit(
                "rust-v1.2.3",
                fetch_json_fn=lambda _url: {
                    "object": {"type": "tag", "url": "https://example.test/tag"}
                },
            )

    def test_frontmatter_source_and_default_parsers(self):
        content = snapshot.format_frontmatter(
            {
                "source_type": "snapshot",
                "codex_cli_versions": ["1.2.3"],
                "description": "deterministic snapshot",
            },
            "# Body\n",
        )
        metadata, body = snapshot.split_markdown_frontmatter(content)
        self.assertEqual(metadata["codex_cli_versions"], ["1.2.3"])
        self.assertEqual(metadata["description"], "deterministic snapshot")
        self.assertEqual(body, "# Body\n")

        source = """
        FeatureSpec {
            key: "alpha",
            stage: Stage::Stable,
            default_enabled: true,
        }
        FeatureSpec {
            key: "beta",
            stage: if cfg!(target_os = "macos") { Stage::Experimental } else { Stage::Removed },
            default_enabled: cfg!(target_os = "macos"),
        }
        FeatureSpec { stage: Stage::Deprecated, default_enabled: false, }
        """
        parsed = snapshot.parse_feature_defaults_from_source(source)
        self.assertEqual(parsed["alpha"]["stage_from_source"], "stable")
        self.assertIn("platform-dependent", parsed["beta"]["stage_from_source"])
        self.assertEqual(parsed["beta"]["default_enabled_expr"], 'cfg!(target_os = "macos")')

    def test_current_config_parsers_handle_mirrored_fixture_shapes(self):
        basic = self.FIXTURES / "config-basic-current.md"
        reference = self.FIXTURES / "config-reference-current.md"
        self.assertEqual(
            snapshot.parse_config_basic_feature_keys(basic), ["apps", "memories"]
        )
        self.assertEqual(
            snapshot.parse_config_basic_feature_metadata(basic),
            {"apps": "stable", "memories": "experimental"},
        )
        self.assertEqual(
            snapshot.parse_config_reference_feature_keys(reference),
            ["apps", "memories"],
        )
        metadata = snapshot.documentation_source_metadata(basic, ["apps", "memories"])
        self.assertEqual(metadata["parsed_feature_key_count"], 2)
        self.assertEqual(len(metadata["sha256"]), 64)

    def test_config_parsers_fail_closed_on_missing_or_changed_inputs(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with self.assertRaisesRegex(snapshot.SnapshotError, "missing"):
                snapshot.parse_config_basic_feature_keys(root / "missing.md")

            basic = root / "basic.md"
            basic.write_text("### Former section\n\n| `alpha` | true |\n")
            with self.assertRaisesRegex(snapshot.SnapshotError, "Common feature flags"):
                snapshot.parse_config_basic_feature_keys(basic)

            basic.write_text(
                "### Common feature flags\n\n"
                "| Key | Default | Description |\n"
                "| --- | --- | --- |\n"
                "| `alpha` | true | Enable alpha |\n"
            )
            with self.assertRaisesRegex(snapshot.SnapshotError, "Key and Maturity"):
                snapshot.parse_config_basic_feature_metadata(basic)

            basic.write_text(
                "### Common feature flags\n\n"
                "| Key | Maturity | Default |\n"
                "| --- | invalid | --- |\n"
                "| `alpha` | Stable | true |\n"
            )
            with self.assertRaisesRegex(snapshot.SnapshotError, "invalid separator"):
                snapshot.parse_config_basic_feature_metadata(basic)

            reference = root / "reference.md"
            reference.write_text('key: "features.alpha.enabled"\n')
            with self.assertRaisesRegex(snapshot.SnapshotError, "zero feature keys"):
                snapshot.parse_config_reference_feature_keys(reference)

    def test_config_basic_parser_locates_reordered_maturity_column(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            basic = Path(temporary_directory) / "basic.md"
            basic.write_text(
                "### Common feature flags\n\n"
                "| Key | Maturity | Default | Description |\n"
                "| --- | --- | --- | --- |\n"
                "| `alpha` | Experimental | false | Enable alpha |\n"
                "| `beta` | Stable | true | Enable beta |\n"
            )

            self.assertEqual(
                snapshot.parse_config_basic_feature_metadata(basic),
                {"alpha": "experimental", "beta": "stable"},
            )

    def test_main_writes_snapshot_and_reports_errors(self):
        features_source = 'FeatureSpec { key: "alpha", stage: Stage::Stable, default_enabled: true, }'
        client_source = "(_, true) => Some(ResponsesWebsocketVersion::V2)\n(true, false) => Some(ResponsesWebsocketVersion::V1)\n(false, false) => None"
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output_dir = root / "feature-flags"
            output_json = output_dir / "lifecycle.json"
            output_md = output_dir / "lifecycle.md"
            command_outputs = [
                "codex-cli 1.2.3",
                "alpha  stable  true\nbeta  experimental  false",
            ]
            with (
                mock.patch.object(snapshot, "ROOT", root),
                mock.patch.object(snapshot, "OUTPUT_DIR", output_dir),
                mock.patch.object(snapshot, "OUTPUT_JSON", output_json),
                mock.patch.object(snapshot, "OUTPUT_MD", output_md),
                mock.patch.object(snapshot, "run_command", side_effect=command_outputs),
                mock.patch.object(snapshot, "resolve_feature_source", return_value=("rust-v1.2.3", "a" * 40)),
                mock.patch.object(
                    snapshot,
                    "parse_config_basic_feature_metadata",
                    return_value={"alpha": "stable"},
                ),
                mock.patch.object(snapshot, "parse_config_reference_feature_keys", return_value=[]),
                mock.patch.object(snapshot, "fetch_text", side_effect=[features_source, client_source]),
            ):
                self.assertEqual(snapshot.main(), 0)

            payload = json.loads(output_json.read_text())
            self.assertEqual(payload["schema_version"], 3)
            self.assertEqual(payload["source_commit"], "a" * 40)
            self.assertEqual(payload["coverage"]["actionable_missing_in_docs"], ["beta"])
            self.assertEqual(
                payload["coverage"]["documentation_stage_mismatches"], []
            )
            self.assertEqual(
                payload["documentation_sources"]["config_basic"][
                    "parsed_feature_key_count"
                ],
                1,
            )
            self.assertIn("Feature Flag Lifecycle Snapshot", output_md.read_text())

        with mock.patch.object(
            snapshot, "run_command", side_effect=snapshot.SnapshotError("offline")
        ):
            self.assertEqual(snapshot.main(), 1)

    def test_missing_docs_are_grouped_by_lifecycle(self):
        features = [
            {"key": "stable_missing", "stage": "stable", "enabled": True},
            {"key": "experimental_missing", "stage": "experimental", "enabled": False},
            {"key": "removed_missing", "stage": "removed", "enabled": False},
            {"key": "documented", "stage": "stable", "enabled": True},
        ]

        missing, actionable, grouped = snapshot.group_missing_in_docs(
            features, ["documented"]
        )

        self.assertEqual(
            missing,
            ["experimental_missing", "removed_missing", "stable_missing"],
        )
        self.assertEqual(actionable, ["experimental_missing", "stable_missing"])
        self.assertEqual(
            grouped,
            {
                "experimental": ["experimental_missing"],
                "removed": ["removed_missing"],
                "stable": ["stable_missing"],
            },
        )

    def test_documentation_stage_mismatches_are_reported(self):
        mismatches = snapshot.find_documentation_stage_mismatches(
            [
                {"key": "memories", "stage": "stable", "enabled": True},
                {"key": "apps", "stage": "stable", "enabled": True},
            ],
            {"apps": "stable", "memories": "experimental"},
        )

        self.assertEqual(
            mismatches,
            [
                {
                    "key": "memories",
                    "cli_stage": "stable",
                    "documentation_stage": "experimental",
                }
            ],
        )

    def test_rendered_markdown_separates_actionable_and_informational_gaps(self):
        arguments = {
            "codex_version": "codex-cli 0.146.0",
            "source_ref": "rust-v0.146.0",
            "source_commit": "d" * 40,
            "cli_features": [
                {"key": "stable_missing", "stage": "stable", "enabled": True},
                {"key": "removed_missing", "stage": "removed", "enabled": False},
            ],
            "docs_keys": [],
            "source_defaults": {},
            "missing_in_docs": ["removed_missing", "stable_missing"],
            "actionable_missing_in_docs": ["stable_missing"],
            "missing_in_docs_by_stage": {
                "removed": ["removed_missing"],
                "stable": ["stable_missing"],
            },
            "stale_in_docs": [],
            "ws_precedence": {
                "detected": False,
                "openai_beta_headers": {},
            },
            "source_hashes": {
                "features_rs_sha256": "e" * 64,
                "client_rs_sha256": "f" * 64,
            },
        }

        rendered = snapshot.render_markdown(**arguments)

        self.assertEqual(rendered, snapshot.render_markdown(**arguments))
        self.assertIn("Actionable missing in docs (`stable`, `experimental`): `1`", rendered)
        self.assertIn("- Informational missing in docs:", rendered)
        self.assertIn(f"- Source commit: `{'d' * 40}`", rendered)

    def test_websocket_precedence_detection(self):
        source = "\n".join(
            [
                "(_, true) => Some(ResponsesWebsocketVersion::V2)",
                "(true, false) => Some(ResponsesWebsocketVersion::V1)",
                "(false, false) => None",
                'OPENAI_BETA_RESPONSES_WEBSOCKETS: &str = "responses_websockets=v1";',
                'RESPONSES_WEBSOCKETS_V2_BETA_HEADER_VALUE: &str = "responses_websockets=v2";',
            ]
        )

        semantics = snapshot.derive_websocket_precedence(source)

        self.assertTrue(semantics["detected"])
        self.assertEqual(
            semantics["openai_beta_headers"]["responses_websockets_v2"],
            "responses_websockets=v2",
        )


    def test_compatibility_defaults_do_not_imply_effective_behavior(self):
        source = """
        enum Feature {
            /// Steer feature flag - when enabled, Enter submits immediately instead of queuing.
            /// Kept for config backward compatibility; behavior is always steer-enabled.
            Steer,
            /// Removed compatibility flag retained as a no-op so old configs can parse.
            Undo,
            /// Removed compatibility flag; replacement is selected by the model.
            Legacy,
        }
        FeatureSpec { id: Feature::Steer, key: "steer", stage: Stage::Removed, default_enabled: true, }
        FeatureSpec { id: Feature::Undo, key: "undo", stage: Stage::Removed, default_enabled: false, }
        FeatureSpec { id: Feature::Legacy, key: "legacy", stage: Stage::Removed, default_enabled: true, }
        FeatureSpec { key: "old", stage: Stage::Deprecated, default_enabled: false, }
        FeatureSpec { key: "platform", stage: Stage::Stable, default_enabled: cfg!(target_os = "macos"), }
        FeatureSpec { key: "public", stage: Stage::Experimental, default_enabled: false, }
        """
        parsed = snapshot.parse_feature_defaults_from_source(source)
        self.assertEqual(parsed["steer"]["effective_behavior"], "always_on")
        self.assertTrue(parsed["steer"]["default_enabled"])
        self.assertFalse(parsed["steer"]["configurable"])
        self.assertTrue(parsed["steer"]["compatibility_flag"])
        self.assertIn("always steer-enabled", parsed["steer"]["behavior_evidence"])
        self.assertEqual(parsed["undo"]["effective_behavior"], "no_op")
        self.assertEqual(parsed["legacy"]["effective_behavior"], "unknown")
        self.assertTrue(parsed["old"]["configurable"])
        self.assertEqual(parsed["old"]["stage_from_source"], "deprecated")
        self.assertEqual(parsed["platform"]["effective_behavior"], "platform_dependent")
        self.assertIsNone(parsed["platform"]["default_enabled"])
        self.assertEqual(parsed["public"]["effective_behavior"], "feature_gated")
        self.assertTrue(parsed["public"]["configurable"])

    def test_conditional_source_comments_do_not_establish_always_on(self):
        behavior = snapshot.feature_behavior("removed", "true", "Always enabled when the server supports it.")
        self.assertEqual(behavior["effective_behavior"], "unknown")
        self.assertIsNone(snapshot.feature_behavior("unknown", "unknown", "")["configurable"])


if __name__ == "__main__":
    unittest.main()
