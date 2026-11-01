"""Regression tests for safety invariants that previously survived mutation testing.

Each test names the audit mutation (audits/2026-10-18.md) it is designed to kill.
"""

import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

import requests
import test_learn_evidence as learn_tests
import test_release_transaction as release_tests
from test_cli_observations import METADATA, surface
from test_fetch_codex_docs_extended import isolated_outputs

from scripts import check_codex_freshness as freshness
from scripts import fetch_codex_docs as sync

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
PUSH_COMMAND = "git push origin HEAD:main"
STALE_GUARD = "steps.writer_base.outputs.stale == 'false'"


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def http_response(url, status=200, body="", content_type="text/html", final_url=None):
    response = requests.Response()
    response.status_code = status
    response.url = final_url or url
    response._content = body.encode()
    response.headers["Content-Type"] = content_type
    response.request = requests.Request("GET", url).prepare()
    return response


class FakeSession:
    def __init__(self, responses):
        self.responses = responses
        self.requested = []

    def get(self, url, timeout=None, headers=None):
        self.requested.append(url)
        return self.responses[url]


class DocumentRetentionTests(unittest.TestCase):
    """M3b/M3c: a confirmed tombstone removes the file, its manifest entry, and reports it."""

    def test_confirmed_learn_tombstone_deletes_file_manifest_entry_and_reports_removal(self):
        shared = learn_tests.DOCS + "shared"
        rel_path = sync.learn_url_to_rel_path(shared)

        def tombstoned(_session, url):
            if url == shared:
                raise sync.SourceTombstone(url, 404, (404, 404))
            return f"# {url.rsplit('/', 1)[-1]}\n", {"source_kind": "learn_markdown"}, "markdown"

        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            path = sync.output_path_for_rel_path(rel_path)
            with learn_tests.LearnEvidenceTests().builders():
                self.assertEqual(sync.main(), 0)
            self.assertTrue(path.is_file())
            self.assertIn(rel_path, sync.load_existing_manifest())

            with learn_tests.LearnEvidenceTests().builders(), \
                    mock.patch.object(sync, "fetch_learn_page", side_effect=tombstoned):
                self.assertEqual(sync.main(), 0)
                self.assertFalse(path.exists())
                self.assertNotIn(rel_path, sync.load_existing_manifest())
                self.assertEqual(json.loads(sync.SUMMARY_PATH.read_text())["removed"], [rel_path])
                tombstones = json.loads(sync.COVERAGE_PATH.read_text())["learn"]["tombstoned_urls"]
                self.assertEqual([item["url"] for item in tombstones], [shared])

                before = snapshot(Path(directory))
                with mock.patch.object(sync, "now_utc_iso", return_value="2099-01-01T00:00:00+00:00"):
                    self.assertEqual(sync.main(), 0)
                self.assertEqual(before, snapshot(Path(directory)))


class PlatformObservationTests(unittest.TestCase):
    """M26-M29: stored and incoming CLI platform observations are validated, never silently merged."""

    def store(self, name, payload):
        path = sync.DOCS_DIR / "cli-surface" / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        entries = sync.load_existing_manifest()
        entries[f"cli-surface/{name}.json"] = {
            "sha256": sync.sha256_content(path.read_bytes()),
            "source_type": sync.CLI_PLATFORM_SOURCE_TYPE,
            "source_url": "codex-cli://help",
            "codex_cli_version": payload["codex_cli_version"],
            "codex_cli_release_ref": payload["source_ref"],
            "codex_cli_source_commit": payload["source_commit"],
        }
        sync.write_manifest(entries)
        return path

    def native(self, payload):
        return sync.ManagedFile(sync.CLI_SURFACE_REL_PATH, sync.CLI_SURFACE_SOURCE_TYPE, "codex-cli://help",
                                json.dumps(payload))

    def artifact(self, directory, name, payload):
        directory.mkdir(parents=True, exist_ok=True)
        (directory / f"{name}.json").write_text(json.dumps(payload))

    def test_artifact_commit_mismatch_for_current_release_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            self.store("macos-arm64", surface("darwin", ["app"]))
            artifacts = Path(directory) / "artifacts"
            self.artifact(artifacts, "macos-arm64", surface("darwin", ["app"], "1.2.4", "c"))
            native = self.native(surface("linux", [], "1.2.4", "b"))
            with self.assertRaisesRegex(ValueError, "does not match the resolved release commit"):
                sync.prepare_cli_observations([native], METADATA, artifacts)

    def test_version_skewed_artifact_is_ignored_and_stored_platform_keeps_its_own_provenance(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            stored = self.store("macos-arm64", surface("darwin", ["app"], "1.2.2", "c"))
            artifacts = Path(directory) / "artifacts"
            # Older artifact carrying its own (correct) commit and no commands.
            self.artifact(artifacts, "macos-arm64", surface("darwin", [], "1.2.3", "a"))
            native = self.native(surface("linux", [], "1.2.4", "b"))
            files, observations = sync.prepare_cli_observations([native], METADATA, artifacts)
            self.assertEqual({key: (value["codex_cli_version"], value["source_commit"])
                              for key, value in observations.items()},
                             {"linux-x86_64": ("1.2.4", "b" * 40), "macos-arm64": ("1.2.2", "c" * 40)})
            by_path = {item.rel_path: item for item in files}
            self.assertEqual(by_path["cli-surface/macos-arm64.json"].content, stored.read_text())
            union = json.loads(by_path[sync.CLI_SURFACE_REL_PATH].content)
            commands = {item["name"]: item for item in union["commands"]}
            # The skewed artifact's empty help must not be published as evidence that `app` vanished.
            self.assertEqual(set(commands["app"]["observed_on"]), {"macos-arm64"})

    def test_older_cli_cannot_replace_newer_platform_observation(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            self.store("linux-x86_64", surface("linux", ["future"], "1.2.5", "d"))
            native = self.native(surface("linux", [], "1.2.4", "b"))
            with self.assertRaisesRegex(ValueError, "Refusing to replace a newer"):
                sync.prepare_cli_observations([native], METADATA, None)

    def test_misnamed_stored_observation_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            self.store("linux-x86_64", surface("darwin", ["app"]))
            native = self.native(surface("linux", [], "1.2.4", "b"))
            with self.assertRaisesRegex(ValueError, "filename does not match"):
                sync.prepare_cli_observations([native], METADATA, None)


class ReleaseProvenanceTests(unittest.TestCase):
    """M7, M16, M17, M18: release provenance fails closed."""

    MISMATCHES = (
        {"source_ref": "rust-v1.2.4", "source_commit": "c" * 40, "cli_features": []},
        {"source_ref": "rust-v1.2.3", "source_commit": "b" * 40, "cli_features": []},
    )

    def test_release_only_rejects_feature_snapshot_from_another_release(self):
        for payload in self.MISMATCHES:
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as directory, \
                    isolated_outputs(Path(directory)):
                release_tests.ReleaseTransactionTests().seed()
                before = snapshot(Path(directory))
                with release_tests.ReleaseTransactionTests().release_builders(), \
                        mock.patch.object(sync.snapshot_feature_flags, "build_snapshot",
                                          return_value=(payload, "# Features\n")):
                    self.assertEqual(sync.main(release_only=True), 1)
                self.assertEqual(before, snapshot(Path(directory)))

    def test_full_sync_rejects_feature_snapshot_from_another_release(self):
        for payload in self.MISMATCHES:
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as directory, \
                    isolated_outputs(Path(directory)):
                lifecycle = sync.output_path_for_rel_path("feature-flags/lifecycle.json")
                with learn_tests.LearnEvidenceTests().builders():
                    self.assertEqual(sync.main(), 0)
                    accepted = lifecycle.read_bytes()
                    before = snapshot(Path(directory))
                    with mock.patch.object(sync.snapshot_feature_flags, "build_snapshot",
                                           return_value=(payload, "# Features\n")):
                        self.assertEqual(sync.main(), 1)
                        self.assertEqual(before, snapshot(Path(directory)))
                        with mock.patch.object(sync, "STRICT_SYNC_MODE", False):
                            sync.main()
                self.assertEqual(lifecycle.read_bytes(), accepted)
                self.assertEqual(json.loads(accepted)["source_commit"], "b" * 40)

    def tag_responses(self, tag_target, resolved):
        api = sync.GITHUB_REPOSITORY_API_URL
        return {f"{api}/git/ref/tags/rust-v1.2.4": {"object": tag_target}, **resolved}

    def resolve(self, responses):
        with mock.patch.object(sync, "github_api_headers", return_value={}), \
                mock.patch.object(sync, "fetch_json", side_effect=lambda _s, url, headers=None: responses[url]):
            return sync.resolve_github_tag_commit(object(), "rust-v1.2.4")

    def test_resolve_github_tag_commit_dereferences_only_repository_tag_objects(self):
        api = sync.GITHUB_REPOSITORY_API_URL
        tag_url = f"{api}/git/tags/{'e' * 40}"
        commit = {"object": {"type": "commit", "sha": "C" * 40}}
        self.assertEqual(self.resolve(self.tag_responses({"type": "tag", "url": tag_url}, {tag_url: commit})), "c" * 40)
        foreign = "https://api.github.com/repos/attacker/codex/git/tags/" + "e" * 40
        failures = {
            "foreign tag object": self.tag_responses({"type": "tag", "url": foreign}, {foreign: commit}),
            # A tree that points at a well-formed tag URL must still be refused on its type alone.
            "tree target": self.tag_responses({"type": "tree", "sha": "c" * 40, "url": tag_url}, {tag_url: commit}),
            "symbolic commit": self.tag_responses({"type": "commit", "sha": "main"}, {}),
            "empty object": self.tag_responses({}, {}),
        }
        for name, responses in failures.items():
            with self.subTest(name), self.assertRaises(RuntimeError):
                self.resolve(responses)

    def test_add_cli_release_provenance_rejects_non_release_versions(self):
        for version in ("development", "", "1.2", "rust-v1.2.4", "1.2.4 extra"):
            with self.subTest(version=version), \
                    mock.patch.object(sync, "resolve_github_tag_commit", return_value="a" * 40) as resolve:
                with self.assertRaisesRegex(RuntimeError, "Cannot resolve a release tag"):
                    sync.add_cli_release_provenance(object(), [], {"codex_cli_version": version})
                resolve.assert_not_called()

    def test_freshness_fails_when_feature_commit_disagrees_with_its_release_tag(self):
        arguments = {
            "latest_release": {"version": "1.2.3", "tag": "rust-v1.2.3", "published_at": "2026-08-29T10:00:00Z",
                               "source_commit": "a" * 40},
            "installed_cli": {"version": "1.2.3", "version_raw": "codex-cli 1.2.3"},
            "summary": {"generated_at": "2026-08-29T11:00:00+00:00", "source_metadata": {
                "codex_cli_version": "1.2.3", "codex_cli_release_ref": "rust-v1.2.3",
                "codex_cli_source_commit": "a" * 40}},
            "coverage": {"codex_cli": {"version": "1.2.3"},
                         "github": {"source_ref": "rust-v1.2.3", "source_commit": "a" * 40}},
            "cli_surface": {"codex_cli_version": "1.2.3", "source_ref": "rust-v1.2.3", "source_commit": "a" * 40,
                            "platform_observations": {"linux-x86_64": {
                                "codex_cli_version": "1.2.3", "source_ref": "rust-v1.2.3",
                                "source_commit": "a" * 40}}},
            "model_snapshot": {"codex_cli_version": "1.2.3", "source_ref": "rust-v1.2.3", "source_commit": "a" * 40,
                               "source_path": "codex-rs/models-manager/models.json"},
            "feature_snapshot": {"codex_cli_version": "codex-cli 1.2.3", "source_ref": "rust-v1.2.3",
                                 "source_commit": "a" * 40},
            "now": datetime(2026, 8, 29, 11, tzinfo=timezone.utc),
            "grace_hours": 12,
            "resolve_tag_commit_fn": lambda _tag: "a" * 40,
        }
        self.assertEqual(freshness.build_report(**arguments)["status"], "fresh")
        arguments["feature_snapshot"] = {**arguments["feature_snapshot"], "source_commit": "f" * 40}
        report = freshness.build_report(**arguments)
        self.assertEqual(report["status"], "stale")
        check = next(c for c in report["checks"] if c["name"] == "feature_snapshot_commit_matches_release_tag")
        self.assertEqual((check["status"], check["observed"], check["expected"]), ("fail", "f" * 40, "a" * 40))


class ReleaseManifestIntegrityTests(unittest.TestCase):
    """M8: release-only replay refuses a manifest that lacks the web mirror."""

    def test_release_only_rejects_truncated_manifest_without_writing(self):
        variants = {
            "empty": lambda entries: {},
            "web-less": lambda entries: {path: entry for path, entry in entries.items()
                                         if entry["source_type"] == sync.PLATFORM_TOOL_GUIDE_SOURCE_TYPE},
        }
        for name, truncate in variants.items():
            with self.subTest(name), tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
                release_tests.ReleaseTransactionTests().seed()
                sync.write_manifest(truncate(sync.load_existing_manifest()))
                before = snapshot(Path(directory))
                with release_tests.ReleaseTransactionTests().release_builders():
                    self.assertEqual(sync.main(release_only=True), 1)
                self.assertEqual(before, snapshot(Path(directory)))


def workflow_jobs(text):
    """Split a GitHub Actions workflow into {job: [step_lines]} using its fixed two-space layout."""
    jobs, job, steps, in_jobs, step_indent = {}, None, None, False, None
    for line in text.splitlines():
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if not stripped or stripped.startswith("#"):
            if steps is not None and steps:
                steps[-1].append(line)
            continue
        if indent == 0:
            in_jobs = stripped == "jobs:"
            job = steps = None
            continue
        if in_jobs and indent == 2 and re.fullmatch(r"[A-Za-z0-9_-]+:", stripped):
            job, steps, step_indent = stripped[:-1], None, None
            jobs[job] = []
            continue
        if job is None:
            continue
        if stripped == "steps:" and indent == 4:
            steps = jobs[job]
            continue
        if steps is None:
            continue
        if indent <= 4:
            steps = None
            continue
        if stripped.startswith("- ") and (step_indent is None or indent == step_indent):
            step_indent = indent
            steps.append([" " * (indent + 2) + stripped[2:]])
        else:
            steps[-1].append(line)
    return jobs


def step_field(step, key):
    """Return a top-level scalar field of a step, joining folded/literal continuation lines."""
    field_indent = len(step[0]) - len(step[0].lstrip(" "))
    for index, line in enumerate(step):
        if line.startswith(" " * field_indent + f"{key}:") and not line[field_indent].isspace():
            value = line.split(":", 1)[1].strip()
            if value in {"|", ">", ">-", "|-"}:
                value = " ".join(item.strip() for item in step[index + 1:]
                                 if len(item) - len(item.lstrip(" ")) > field_indent and item.strip())
            return value
    return None


class WorkflowWriterGuardTests(unittest.TestCase):
    """M20: every direct push to main is guarded per step, not merely somewhere in the file."""

    def test_every_push_step_is_gated_by_a_preceding_writer_base_check_in_its_job(self):
        workflows = sorted(WORKFLOWS.glob("*.yml"))
        self.assertTrue(workflows)
        guarded = 0
        for workflow in workflows:
            text = workflow.read_text()
            jobs = workflow_jobs(text)
            push_steps = 0
            for job, steps in jobs.items():
                for index, step in enumerate(steps):
                    if not any(PUSH_COMMAND in line for line in step):
                        continue
                    push_steps += 1
                    with self.subTest(workflow=workflow.name, job=job, step=step_field(step, "name") or index):
                        condition = step_field(step, "if") or ""
                        self.assertIn(STALE_GUARD, condition)
                        self.assertNotIn("||", condition)
                        checks = [prior for prior in steps[:index] if step_field(prior, "id") == "writer_base"]
                        self.assertEqual(len(checks), 1)
                        self.assertIn("scripts/check_writer_base.py", " ".join(checks[0]))
            # The splitter must account for every push occurrence, so it can never pass vacuously.
            self.assertEqual(push_steps, text.count(PUSH_COMMAND), workflow.name)
            guarded += push_steps
        self.assertGreaterEqual(guarded, 3)

    def test_splitter_attributes_guards_to_their_own_step(self):
        text = "\n".join([
            "jobs:",
            "  one:",
            "    steps:",
            "      - name: Check writer base",
            "        id: writer_base",
            "        run: python3 scripts/check_writer_base.py",
            "      - name: Push",
            f"        if: {STALE_GUARD}",
            "        run: |",
            f"          {PUSH_COMMAND}",
            "  two:",
            "    steps:",
            "      - name: Push unguarded",
            "        run: |",
            f"          {PUSH_COMMAND}",
        ])
        jobs = workflow_jobs(text)
        self.assertEqual([len(jobs["one"]), len(jobs["two"])], [2, 1])
        self.assertEqual(step_field(jobs["one"][0], "id"), "writer_base")
        self.assertEqual(step_field(jobs["one"][1], "if"), STALE_GUARD)
        self.assertIsNone(step_field(jobs["two"][0], "if"))


class SourceStateTests(unittest.TestCase):
    """M13/M14: current redirect recording and permanent-missing handling for developers pages."""

    URL = "https://developers.openai.com/codex/page"
    HTML = "<html><head><title>Codex page</title></head><body><main><h1>Codex page</h1>" \
           "<p>Body text for the page.</p></main></body></html>"

    def build(self, response):
        session = FakeSession({self.URL: response})
        with mock.patch.object(sync, "discover_developers_urls",
                               return_value=([self.URL], {"developers": {"counts": {}}})), \
                mock.patch.object(sync, "REQUEST_BACKOFF_SECONDS", 0):
            return sync.build_developers_files(session)

    def test_developers_redirect_is_recorded_in_metadata_coverage_and_manifest(self):
        final = "https://developers.openai.com/codex/moved"
        managed, coverage, errors = self.build(http_response(self.URL, body=self.HTML, final_url=final))
        self.assertEqual(errors, [])
        self.assertEqual(managed[0].source_metadata["source_redirect_url"], final)
        self.assertEqual(coverage["developers"]["redirected_urls"],
                         [{"url": self.URL, "redirect_url": final, "state": "redirected"}])
        self.assertEqual(coverage["developers"]["counts"]["redirected_urls"], 1)
        with tempfile.TemporaryDirectory() as directory, isolated_outputs(Path(directory)):
            sync.apply_sync(managed)
            self.assertEqual(sync.load_existing_manifest()[managed[0].rel_path]["source_redirect_url"], final)

    def test_learn_markdown_redirect_is_recorded(self):
        url = "https://learn.chatgpt.com/docs/page"
        final = "https://learn.chatgpt.com/docs/renamed.md"
        session = FakeSession({f"{url}.md": http_response(f"{url}.md", body="# Page\n", content_type="text/markdown",
                                                          final_url=final)})
        _content, metadata, mode = sync.fetch_learn_page(session, url)
        self.assertEqual((mode, metadata["source_redirect_url"]), ("markdown", final))

    def test_unredirected_page_records_no_redirect(self):
        managed, coverage, _errors = self.build(http_response(self.URL, body=self.HTML))
        self.assertNotIn("source_redirect_url", managed[0].source_metadata)
        self.assertEqual(coverage["developers"]["redirected_urls"], [])

    def test_developers_permanent_missing_is_tombstoned_not_mirrored_or_failed(self):
        for status in sync.PERMANENT_MISSING_HTTP_STATUSES:
            with self.subTest(status=status):
                managed, coverage, errors = self.build(http_response(self.URL, status, self.HTML))
                self.assertEqual((managed, errors), ([], []))
                tombstones = coverage["developers"]["tombstoned_urls"]
                self.assertEqual([(item["url"], item["status_code"]) for item in tombstones], [(self.URL, status)])
                self.assertEqual(coverage["developers"]["counts"]["tombstoned_urls"], 1)

    def test_developers_transient_status_is_a_failure_not_a_tombstone(self):
        with self.assertLogs(sync.LOG, "WARNING"):
            managed, coverage, errors = self.build(http_response(self.URL, 503, self.HTML))
        self.assertEqual(managed, [])
        self.assertEqual([(item["url"], item["state"]) for item in errors], [(self.URL, "transient_page_failure")])
        self.assertEqual(coverage["developers"]["tombstoned_urls"], [])


FAKE_CODEX = """#!/bin/sh
set -eu
case "$1" in
  --version) echo "codex-cli 1.2.3" ;;
  debug)
    workspace="$(pwd -P)"
    home="$(cd "$HOME" && pwd -P)"
    codex_home="$(cd "$CODEX_HOME" && pwd -P)"
    mkdir -p "$CODEX_HOME/skills/.system/demo"
    printf '# Demo\\n' > "$CODEX_HOME/skills/.system/demo/SKILL.md"
    printf '[{"id":"x","role":"user","content":"cwd=%s home=%s codex=%s raw=%s"}]\\n' \\
      "$workspace" "$home" "$codex_home" "$CODEX_HOME"
    ;;
  *) exit 2 ;;
esac
"""


@unittest.skipIf(sys.platform.startswith("win"), "POSIX shell fake CLI")
class CodexCliPathSanitizationTests(unittest.TestCase):
    """M30: prompt snapshots replace both literal and symlink-resolved runtime paths (macOS /private/var)."""

    def test_resolved_runtime_paths_are_replaced_in_prompt_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_bin, real_tmp = root / "bin", root / "real-tmp"
            fake_bin.mkdir()
            real_tmp.mkdir()
            linked_tmp = root / "linked-tmp"
            linked_tmp.symlink_to(real_tmp, target_is_directory=True)
            codex = fake_bin / "codex"
            codex.write_text(FAKE_CODEX)
            codex.chmod(0o755)
            surface_file = sync.ManagedFile(sync.CLI_SURFACE_REL_PATH, sync.CLI_SURFACE_SOURCE_TYPE, "codex-cli://help", "{}")
            synthetic_env = {"PATH": os.pathsep.join([str(fake_bin), "/usr/bin", "/bin"])}
            with mock.patch.dict(os.environ, synthetic_env, clear=True), \
                    mock.patch.object(tempfile, "tempdir", str(linked_tmp)), \
                    mock.patch.object(sync, "build_cli_surface_snapshot", return_value=surface_file):
                self.assertEqual(shutil.which("codex"), str(codex))
                files, errors, metadata = sync.build_codex_cli_files()
        self.assertEqual((errors, metadata["codex_cli_version"]), ([], "1.2.3"))
        prompt = next(item for item in files if item.source_type == "codex_cli_prompt_input")
        message = json.loads(prompt.content)[0]
        self.assertNotIn("id", message)
        self.assertEqual(message["content"],
                         "cwd=$WORKSPACE home=$HOME codex=$CODEX_HOME raw=$CODEX_HOME")
        self.assertNotIn(str(root), prompt.content, "temporary runtime path leaked into prompt snapshot")
        self.assertNotIn(str(real_tmp.resolve()), prompt.content, "resolved runtime path leaked into prompt snapshot")
        skills = [item.rel_path for item in files if item.source_type == "codex_cli_system_skill"]
        self.assertEqual(len(skills), 1)


if __name__ == "__main__":
    unittest.main()
