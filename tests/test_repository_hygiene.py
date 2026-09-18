import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from scripts import check_repository as check


class RepositoryHygieneTests(unittest.TestCase):
    def test_relative_root_encoded_reference_and_html_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a file.md").write_text("target")
            doc = root / "README.md"
            doc.write_text('[a](a%20file.md#anchor)\n[b](/a%20file.md)\n[c](<a file.md>)\n[x]: a%20file.md "title"\n<img src="a%20file.md">\n[web](https://example.test/no-network)\n[anchor](#hello)')
            self.assertEqual(check.local_link_errors(root, doc), [])
            doc.write_text('[bad](missing.md)\n[escape](../outside.md)\n[x]: absent.md\n<img src="image.png">')
            self.assertEqual(len(check.local_link_errors(root, doc)), 4)

    def test_fenced_examples_and_mirrored_markdown_are_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/mirrored.md").write_text('[not ours](nonexistent.md)')
            doc = root / "README.md"
            doc.write_text('```markdown\n[example](nonexistent.md)\n```\n')
            self.assertEqual(check.local_link_errors(root, doc), [])
            self.assertEqual(check.authored_markdown(root), [doc])

    def test_duplicate_or_invalid_config_and_version_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "VERSION").write_text('0.1.0\n')
            for content in ['{', '[]', '{"extends":{}}', '{"extends":[],"extends":[]}']:
                (root / "renovate.json").write_text(content)
                self.assertEqual(len(check.config_errors(root)), 1)
            (root / "renovate.json").write_text('{"extends":["config:best-practices"]}')
            self.assertEqual(check.config_errors(root), [])
            (root / "VERSION").write_text('0.1.0-rc1\n')
            self.assertEqual(check.config_errors(root), ['VERSION: expected x.y.z'])

    def test_missing_configs_and_cli_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(len(check.config_errors(root)), 2)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(check.main(root), 1)
            (root / "renovate.json").write_text('{"extends":[]}')
            (root / "VERSION").write_text('1.0.0\n')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(check.main(root), 0)
