import unittest

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
