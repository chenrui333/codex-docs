import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from scripts import check_writer_base as writer_base


ROOT = Path(__file__).resolve().parent.parent


class WriterBaseTests(unittest.TestCase):
    def test_detects_fresh_and_stale_heads(self):
        self.assertFalse(writer_base.is_stale("A" * 40, "a" * 40))
        self.assertTrue(writer_base.is_stale("a" * 40, "b" * 40))

    def test_main_emits_outputs_for_fresh_head(self):
        output = io.StringIO()
        with (
            mock.patch.object(writer_base, "fetch_remote_head", return_value="a" * 40),
            redirect_stdout(output),
        ):
            result = writer_base.main(["--expected", "a" * 40])

        self.assertEqual(result, 0)
        self.assertIn("stale=false", output.getvalue())

    def test_main_treats_moved_main_as_successful_skip(self):
        output = io.StringIO()
        errors = io.StringIO()
        with (
            mock.patch.object(writer_base, "fetch_remote_head", return_value="b" * 40),
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            result = writer_base.main(["--expected", "a" * 40])

        self.assertEqual(result, 0)
        self.assertIn("stale=true", output.getvalue())
        self.assertIn("Skipping direct push", errors.getvalue())

    def test_main_fails_closed_when_remote_cannot_be_resolved(self):
        with (
            mock.patch.object(
                writer_base,
                "fetch_remote_head",
                side_effect=RuntimeError("fetch failed"),
            ),
            redirect_stderr(io.StringIO()),
        ):
            self.assertEqual(writer_base.main(["--expected", "a" * 40]), 1)


class WriterWorkflowTests(unittest.TestCase):
    def test_writer_credentials_and_stale_push_guards(self):
        workflow_paths = [
            ROOT / ".github" / "workflows" / "update-docs.yml",
            ROOT / ".github" / "workflows" / "update-feature-flags.yml",
        ]
        workflows = [path.read_text() for path in workflow_paths]

        self.assertIn(
            "GITHUB_TOKEN: ${{ github.token }}",
            workflows[0],
        )

        for content in workflows:
            self.assertIn("persist-credentials: false", content)
            self.assertNotIn("git pull --rebase", content)
            self.assertNotIn("secrets.GITHUB_TOKEN", content)
            self.assertIn("steps.writer_base.outputs.stale == 'false'", content)
            self.assertIn("git push origin HEAD:main", content)

            token_position = content.index("GH_TOKEN: ${{ github.token }}")
            push_step_position = content.index("git push origin HEAD:main")
            self.assertLess(token_position, push_step_position)
            self.assertNotIn("GH_TOKEN:", content[:token_position])


if __name__ == "__main__":
    unittest.main()
