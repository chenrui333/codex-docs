import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import cli_help
from scripts import fetch_codex_docs as sync

FIXTURES = Path(__file__).parent / "fixtures" / "cli-help"


class CLIHelpTests(unittest.TestCase):
    def test_complete_generated_surface_matches_pre_extraction_fixture(self):
        expected = (FIXTURES / "expected.json").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            for _ in range(2):
                with mock.patch.object(sync, "run_local_command", side_effect=[
                    (FIXTURES / "top.txt").read_text(), (FIXTURES / "run.txt").read_text(),
                ]):
                    result = sync.build_cli_surface_snapshot(
                        "example", {}, Path(directory),
                        {"codex_cli_version": "1.2.3", "codex_cli_version_raw": "codex-cli 1.2.3"},
                        {"os": "linux", "arch": "x86_64"},
                    )
                self.assertEqual(result.content.encode(), expected)

    def test_empty_sections_and_missing_usage_remain_empty(self):
        for parse in (cli_help.parse_help_commands, cli_help.parse_help_options, cli_help.parse_help_usage):
            self.assertEqual(parse("unrecognized output"), [])
        self.assertIs(sync.parse_help_options, cli_help.parse_help_options)
        self.assertIs(sync.help_section_lines, cli_help.help_section_lines)
