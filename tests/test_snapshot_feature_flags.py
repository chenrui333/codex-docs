import unittest
from subprocess import TimeoutExpired
from unittest import mock

from scripts import snapshot_feature_flags as snapshot


class SnapshotFeatureFlagsTests(unittest.TestCase):
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

    def test_release_tag_response_must_contain_an_object(self):
        with self.assertRaisesRegex(snapshot.SnapshotError, "object target"):
            snapshot.resolve_feature_source(
                "codex-cli 0.146.0", fetch_json_fn=lambda _url: {}
            )

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


if __name__ == "__main__":
    unittest.main()
