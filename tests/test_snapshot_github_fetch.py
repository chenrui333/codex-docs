import re
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from scripts import snapshot_feature_flags as snapshot

ROOT = Path(__file__).resolve().parent.parent
TOKEN = "synthetic-token-for-tests"


class RecordingServer:
    """Loopback HTTP server that records the Authorization header of each request."""

    def __init__(self, routes):
        self.seen = []
        recorder = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                recorder.seen.append((self.path, self.headers.get("Authorization")))
                status, headers, body = routes(self.path)
                self.send_response(status)
                for name, value in headers.items():
                    self.send_header(name, value)
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args):
                pass

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True).start()

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


class SnapshotGitHubFetchTests(unittest.TestCase):
    def setUp(self):
        self.target = RecordingServer(lambda _path: (200, {"Content-Type": "application/json"}, b'{"ok": true}'))
        self.addCleanup(self.target.close)
        target_port = self.target.port

        def origin_routes(path):
            if path == "/same-host":
                return 302, {"Location": "/json"}, b""
            if path == "/cross-host":
                # Different host string than 127.0.0.1, so the credential must not follow.
                return 302, {"Location": f"http://localhost:{target_port}/json"}, b""
            if path.startswith("/limited"):
                return 403, {"Content-Type": "application/json"}, b'{"message": "API rate limit exceeded"}'
            if path == "/array":
                return 200, {"Content-Type": "application/json"}, b"[]"
            return 200, {"Content-Type": "application/json"}, b'{"ok": true}'

        self.origin = RecordingServer(origin_routes)
        self.addCleanup(self.origin.close)
        self.base = f"http://127.0.0.1:{self.origin.port}"
        patches = (
            mock.patch("urllib.request.getproxies", return_value={}),
            mock.patch.dict(snapshot.os.environ, {"GITHUB_TOKEN": TOKEN}),
        )
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)
        snapshot.os.environ.pop("GH_TOKEN", None)

    def test_authenticates_github_api_requests(self):
        self.assertEqual(snapshot.fetch_json(f"{self.base}/json"), {"ok": True})
        self.assertEqual(self.origin.seen, [("/json", f"Bearer {TOKEN}")])

    def test_same_host_redirect_keeps_credentials(self):
        self.assertEqual(snapshot.fetch_json(f"{self.base}/same-host"), {"ok": True})
        self.assertEqual([auth for _path, auth in self.origin.seen], [f"Bearer {TOKEN}"] * 2)

    def test_cross_host_redirect_drops_credentials(self):
        self.assertEqual(snapshot.fetch_json(f"{self.base}/cross-host"), {"ok": True})
        self.assertEqual(self.origin.seen, [("/cross-host", f"Bearer {TOKEN}")])
        self.assertEqual(self.target.seen, [("/json", None)])

    def test_raw_source_fetches_send_no_credentials(self):
        snapshot.fetch_text(f"{self.base}/json")
        self.assertEqual(self.origin.seen, [("/json", None)])

    def test_api_failures_are_snapshot_errors_without_credentials(self):
        for path, pattern in (("/limited", "HTTP 403"), ("/array", "Unexpected JSON object")):
            with self.subTest(path=path):
                with self.assertRaisesRegex(snapshot.SnapshotError, pattern) as raised:
                    snapshot.fetch_json(f"{self.base}{path}")
                self.assertFalse(TOKEN in str(raised.exception), "error message exposed the token")

    def test_rate_limited_tag_lookup_fails_main_cleanly(self):
        with (
            mock.patch.object(snapshot, "OSS_REPOSITORY_API_URL", f"{self.base}/limited"),
            mock.patch.object(snapshot, "run_command", return_value="codex-cli 1.2.3"),
            mock.patch("sys.stderr") as stderr,
        ):
            self.assertEqual(snapshot.main(), 1)
        written = "".join(call.args[0] for call in stderr.write.call_args_list)
        self.assertIn("error: Request failed", written)
        self.assertFalse(TOKEN in written, "stderr exposed the token")


class FeatureFlagWorkflowTokenTests(unittest.TestCase):
    def test_every_snapshot_generation_step_is_authenticated(self):
        workflow = (ROOT / ".github" / "workflows" / "update-feature-flags.yml").read_text()
        steps = re.split(r"\n(?=\s+- name: )", workflow)
        generators = [
            step for step in steps
            if re.search(r"^\s+run: python3 scripts/snapshot_feature_flags\.py$", step, re.MULTILINE)
        ]
        self.assertEqual(len(generators), 2)
        for step in generators:
            self.assertIn("GITHUB_TOKEN: ${{ github.token }}", step)


if __name__ == "__main__":
    unittest.main()
