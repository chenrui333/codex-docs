import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from scripts import check_codex_freshness as freshness


def cli_fixture():
    return {"codex_cli_version": "1.2.3", "source_ref": "rust-v1.2.3", "source_commit": "a" * 40,
            "platform_observations": {"linux-x86_64": {
                "os": "linux", "arch": "x86_64", "codex_cli_version": "1.2.3",
                "source_ref": "rust-v1.2.3", "source_commit": "a" * 40,
            }}}


class CheckCodexFreshnessTests(unittest.TestCase):
    def test_parse_version_accepts_release_tag_prefix(self):
        self.assertEqual(freshness.parse_version("rust-v0.151.0"), "0.151.0")
        self.assertGreater(
            freshness.version_tuple("0.10.0"),
            freshness.version_tuple("0.9.9"),
        )

    def test_latest_release_rejects_prerelease(self):
        with self.assertRaisesRegex(freshness.FreshnessError, "non-stable"):
            freshness.latest_stable_release(
                lambda _url: {
                    "tag_name": "rust-v1.2.3-alpha.1",
                    "prerelease": True,
                    "draft": False,
                }
            )

    def test_annotated_tag_resolves_to_immutable_commit(self):
        tag_object_url = f"{freshness.REPOSITORY_API}/git/tags/{'b' * 40}"
        responses = {
            f"{freshness.REPOSITORY_API}/git/ref/tags/rust-v1.2.3": {
                "object": {"type": "tag", "url": tag_object_url}
            },
            tag_object_url: {"object": {"type": "commit", "sha": "c" * 40}},
        }

        self.assertEqual(
            freshness.resolve_tag_commit(
                "rust-v1.2.3", fetch_json_fn=responses.__getitem__
            ),
            "c" * 40,
        )

    def test_report_is_fresh_and_deterministic_when_versions_match(self):
        release = {
            "version": "1.2.3",
            "tag": "rust-v1.2.3",
            "published_at": "2026-08-29T10:00:00Z",
            "source_commit": "a" * 40,
            "url": "https://example.test/release",
            "provenance": "github_release_metadata",
        }
        arguments = {
            "latest_release": release,
            "installed_cli": {"version": "1.2.3", "version_raw": "codex-cli 1.2.3"},
            "summary": {
                "generated_at": "2026-08-29T11:00:00+00:00",
                "source_metadata": {
                    "codex_cli_version": "1.2.3",
                    "codex_cli_release_ref": "rust-v1.2.3",
                    "codex_cli_source_commit": "a" * 40,
                },
            },
            "coverage": {
                "codex_cli": {"version": "1.2.3"},
                "github": {
                    "source_ref": "rust-v1.2.3",
                    "source_commit": "a" * 40,
                },
            },
            "cli_surface": cli_fixture(),
            "model_snapshot": {
                "codex_cli_version": "1.2.3", "source_ref": "rust-v1.2.3",
                "source_commit": "a" * 40, "source_path": "codex-rs/models-manager/models.json",
            },
            "feature_snapshot": {
                "codex_cli_version": "codex-cli 1.2.3",
                "source_ref": "rust-v1.2.3",
                "source_commit": "a" * 40,
            },
            "now": datetime(2026, 8, 29, 23, tzinfo=timezone.utc),
            "grace_hours": 12,
            "resolve_tag_commit_fn": lambda _tag: "a" * 40,
        }

        first = freshness.build_report(**arguments)
        second = freshness.build_report(**arguments)

        self.assertEqual(first, second)
        self.assertEqual(first["status"], "fresh")
        self.assertEqual(
            first["canonical_mirror"]["last_successful_full_sync_at"],
            "2026-08-29T11:00:00+00:00",
        )

        old_linux = arguments["cli_surface"]["platform_observations"]["linux-x86_64"]
        old_linux.update(codex_cli_version="1.2.2", source_ref="rust-v1.2.2", source_commit="b" * 40)
        arguments["resolve_tag_commit_fn"] = lambda tag: ("b" if tag == "rust-v1.2.2" else "a") * 40
        report = freshness.build_report(**arguments)
        self.assertEqual(report["status"], "fresh")
        self.assertFalse(report["cli_surface"]["platform_observations"]["linux-x86_64"]["matches_latest_stable"])
        old_linux["source_commit"] = "c" * 40
        report = freshness.build_report(**arguments)
        self.assertEqual(report["status"], "stale")

    def test_model_provenance_failure_is_not_subject_to_release_grace(self):
        release = {"version": "1.2.3", "published_at": "2026-08-29T10:00:00Z"}
        model = {"codex_cli_version": "1.2.3", "source_ref": "rust-v1.2.3",
                 "source_commit": "a" * 40, "source_path": "codex-rs/models-manager/models.json"}
        for key, value, check in (
            ("source_commit", "b" * 40, "model_catalog_commit_matches_release_tag"),
            ("source_ref", "rust-v1.2.2", "model_catalog_release_ref_matches_version"),
            ("source_path", "wrong.json", "model_catalog_source_path"),
        ):
            with self.subTest(key=key):
                report = freshness.build_report(
                    latest_release=release, installed_cli={"version": "1.2.3"},
                    summary={"source_metadata": {"codex_cli_version": "1.2.3",
                        "codex_cli_release_ref": "rust-v1.2.3", "codex_cli_source_commit": "a" * 40}},
                    coverage={"codex_cli": {"version": "1.2.3"}, "github": {
                        "source_ref": "rust-v1.2.3", "source_commit": "a" * 40}},
                    feature_snapshot=model, model_snapshot={**model, key: value}, cli_surface=cli_fixture(),
                    now=datetime(2026, 8, 29, 11, tzinfo=timezone.utc), grace_hours=12,
                    resolve_tag_commit_fn=lambda _tag: "a" * 40,
                )
                self.assertEqual(report["status"], "stale")
                self.assertEqual(next(c for c in report["checks"] if c["name"] == check)["status"], "fail")

    def test_stable_release_gap_warns_then_fails_after_grace(self):
        base = {
            "latest_release": {
                "version": "1.2.4",
                "tag": "rust-v1.2.4",
                "published_at": "2026-08-29T10:00:00Z",
                "source_commit": "b" * 40,
            },
            "installed_cli": {"version": "1.2.3", "version_raw": "codex-cli 1.2.3"},
            "summary": {
                "generated_at": "2026-08-28T10:00:00+00:00",
                "source_metadata": {
                    "codex_cli_version": "1.2.3",
                    "codex_cli_release_ref": "rust-v1.2.3",
                    "codex_cli_source_commit": "a" * 40,
                },
            },
            "coverage": {
                "codex_cli": {"version": "1.2.3"},
                "github": {
                    "source_ref": "rust-v1.2.3",
                    "source_commit": "a" * 40,
                },
            },
            "cli_surface": cli_fixture(),
            "model_snapshot": {
                "codex_cli_version": "1.2.3", "source_ref": "rust-v1.2.3",
                "source_commit": "a" * 40, "source_path": "codex-rs/models-manager/models.json",
            },
            "feature_snapshot": {
                "codex_cli_version": "codex-cli 1.2.3",
                "source_ref": "rust-v1.2.3",
                "source_commit": "a" * 40,
            },
            "grace_hours": 12,
            "resolve_tag_commit_fn": lambda _tag: "a" * 40,
        }

        warning = freshness.build_report(
            **base, now=datetime(2026, 8, 29, 11, tzinfo=timezone.utc)
        )
        stale = freshness.build_report(
            **base, now=datetime(2026, 8, 30, 0, tzinfo=timezone.utc)
        )

        self.assertEqual(warning["status"], "warning")
        self.assertEqual(stale["status"], "stale")

    def test_mismatched_release_provenance_can_never_report_fresh(self):
        base = {
            "latest_release": {
                "version": "1.2.3",
                "tag": "rust-v1.2.3",
                "published_at": "2026-08-29T10:00:00Z",
                "source_commit": "a" * 40,
            },
            "installed_cli": {"version": "1.2.3", "version_raw": "codex-cli 1.2.3"},
            "summary": {
                "generated_at": "2026-08-29T11:00:00+00:00",
                "source_metadata": {
                    "codex_cli_version": "1.2.3",
                    "codex_cli_release_ref": "rust-v1.2.3",
                    "codex_cli_source_commit": "b" * 40,
                },
            },
            "coverage": {
                "codex_cli": {"version": "1.2.3"},
                "github": {
                    "source_ref": "rust-v1.2.3",
                    "source_commit": "a" * 40,
                },
            },
            "cli_surface": cli_fixture(),
            "model_snapshot": {
                "codex_cli_version": "1.2.3", "source_ref": "rust-v1.2.3",
                "source_commit": "a" * 40, "source_path": "codex-rs/models-manager/models.json",
            },
            "feature_snapshot": {
                "codex_cli_version": "codex-cli 1.2.3",
                "source_ref": "rust-v1.2.3",
                "source_commit": "a" * 40,
            },
            "now": datetime(2026, 8, 29, 11, tzinfo=timezone.utc),
            "grace_hours": 12,
            "resolve_tag_commit_fn": lambda _tag: "a" * 40,
        }

        report = freshness.build_report(**base)

        self.assertEqual(report["status"], "stale")
        checks = {check["name"]: check for check in report["checks"]}
        self.assertEqual(
            checks["canonical_mirror_commit_matches_release_tag"]["status"],
            "fail",
        )

        base["summary"]["source_metadata"]["codex_cli_source_commit"] = "a" * 40
        base["coverage"]["github"]["source_ref"] = "rust-v1.2.2"
        report = freshness.build_report(**base)
        self.assertEqual(report["status"], "stale")
        checks = {check["name"]: check for check in report["checks"]}
        self.assertEqual(
            checks["source_coverage_release_ref_matches_version"]["status"],
            "fail",
        )

    def test_main_strict_fails_for_materially_stale_mirror(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "freshness.json"
            with (
                mock.patch.object(freshness, "latest_stable_release", return_value={}),
                mock.patch.object(freshness, "installed_cli_version", return_value={}),
                mock.patch.object(freshness, "load_json", return_value={}),
                mock.patch.object(
                    freshness,
                    "build_report",
                    return_value={
                        "status": "stale",
                        "canonical_mirror": {"version": "1.2.3"},
                        "latest_stable_release": {"version": "1.2.4"},
                    },
                ),
            ):
                self.assertEqual(
                    freshness.main(["--strict", "--output", str(output)]), 1
                )

    def test_api_failure_writes_unhealthy_report_and_fails(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "freshness.json"
            with mock.patch.object(
                freshness,
                "latest_stable_release",
                side_effect=freshness.FreshnessError("GitHub unavailable"),
            ):
                self.assertEqual(freshness.main(["--output", str(output)]), 1)

            report = freshness.load_json(output)
            self.assertEqual(report["status"], "unhealthy")
            self.assertIn("GitHub unavailable", report["error"])


if __name__ == "__main__":
    unittest.main()
