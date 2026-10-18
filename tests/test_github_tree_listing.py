import unittest
from unittest import mock

from scripts import fetch_codex_docs as sync

COMPLETE = {
    "truncated": False,
    "tree": [
        {"type": "blob", "path": "README.md"},
        {"type": "blob", "path": "src/main.rs"},
    ],
}


class GitHubTreeListingTests(unittest.TestCase):
    """The tree listing decides removals, so it must be complete before it is trusted."""

    def test_complete_listing_is_used(self):
        with mock.patch.object(sync, "fetch_json", return_value=COMPLETE):
            self.assertEqual(sync.discover_github_paths(mock.Mock(), "a" * 40), ["README.md"])

    def test_incomplete_or_malformed_listing_blocks_the_family(self):
        payloads = {
            "truncated": {**COMPLETE, "truncated": True},
            # fetch_json turns a non-object response into {}.
            "non-object response": {},
            "tree not a list": {"truncated": False, "tree": {"README.md": "blob"}},
            "entry not an object": {"truncated": False, "tree": ["README.md"]},
        }
        for name, payload in payloads.items():
            with self.subTest(name), mock.patch.object(sync, "fetch_json", return_value=payload):
                with self.assertRaises(sync.SourceContentError):
                    sync.discover_github_paths(mock.Mock(), "a" * 40)

    def test_builder_propagates_incomplete_listing_instead_of_returning_no_files(self):
        with mock.patch.object(sync, "fetch_json", return_value={**COMPLETE, "truncated": True}):
            with self.assertRaises(sync.SourceContentError):
                sync.build_github_files(mock.Mock(), source_ref="rust-v1.2.3", source_commit="a" * 40)


if __name__ == "__main__":
    unittest.main()
