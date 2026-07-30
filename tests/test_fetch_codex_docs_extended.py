import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock

import requests

from scripts import fetch_codex_docs as sync


class FakeResponse:
    def __init__(
        self,
        *,
        text="",
        content=b"",
        status_code=200,
        headers=None,
        error=None,
    ):
        self.text = text
        self.content = content or text.encode()
        self.status_code = status_code
        self.headers = headers or {}
        self.error = error

    def raise_for_status(self):
        if self.error:
            raise self.error


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []
        self.headers = {}

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.responses.pop(0)


class FetchHelpersTests(unittest.TestCase):
    def test_environment_parsers_accept_values_and_fall_back(self):
        with mock.patch.dict(
            sync.os.environ,
            {"COUNT": "7", "RATE": "2.5"},
            clear=False,
        ):
            self.assertEqual(sync._env_int("COUNT", 3), 7)
            self.assertEqual(sync._env_float("RATE", 1.0), 2.5)

        with mock.patch.dict(
            sync.os.environ,
            {"COUNT": "bad", "RATE": "bad"},
            clear=False,
        ):
            self.assertEqual(sync._env_int("COUNT", 3), 3)
            self.assertEqual(sync._env_float("RATE", 1.0), 1.0)

    def test_url_filters_and_classifications_cover_expected_groups(self):
        self.assertEqual(
            sync.parse_loc_tags("<loc>https://example.test/a</loc><loc>b</loc>"),
            ["https://example.test/a", "b"],
        )
        self.assertTrue(sync.keep_developers_url("https://developers.openai.com/codex/cli"))
        self.assertTrue(
            sync.keep_developers_url(
                "https://developers.openai.com/cookbook/articles/codex_exec_plans"
            )
        )
        self.assertFalse(sync.keep_developers_url("https://example.test/codex"))
        self.assertFalse(sync.keep_developers_url("https://developers.openai.com/"))
        self.assertTrue(
            sync.is_codex_related_developers_url(
                "https://developers.openai.com/blog/a-codex-post"
            )
        )
        self.assertFalse(sync.is_codex_related_developers_url("https://example.test/codex"))

        classifications = [
            sync.developers_skipped_url_detail(url)["classification"]
            for url in (
                "https://developers.openai.com/blog/topic/codex",
                "https://developers.openai.com/blog/codex-release",
                "https://developers.openai.com/community/codex",
                "https://developers.openai.com/learn/codex",
                "https://developers.openai.com/showcase/codex",
            )
        ]
        self.assertEqual(
            sync.count_details_by_classification(
                [{"classification": item} for item in classifications]
            ),
            {
                "blog_index": 1,
                "blog_post": 1,
                "community_page": 1,
                "learn_index": 1,
                "showcase_page": 1,
            },
        )
        self.assertIsNone(
            sync.developers_skipped_url_detail(
                "https://developers.openai.com/unknown/codex"
            )
        )

    def test_fetch_helpers_retry_and_extract_metadata(self):
        failure = requests.ConnectionError("temporary")
        session = FakeSession(
            [
                FakeResponse(error=failure),
                FakeResponse(
                    text='{"ok": true}',
                    content=b"payload",
                    headers={
                        "Last-Modified": "Tue, 15 Nov 1994 12:45:26 GMT",
                        "ETag": '"abc"',
                    },
                ),
            ]
        )
        with (
            mock.patch.object(sync, "REQUEST_MAX_RETRIES", 2),
            mock.patch.object(sync, "REQUEST_BACKOFF_SECONDS", 0),
        ):
            response = sync.fetch_response(session, "https://example.test")

        self.assertEqual(response.text, '{"ok": true}')
        self.assertEqual(len(session.calls), 2)
        self.assertEqual(
            sync.response_source_metadata(response),
            {
                "source_last_modified": "1994-11-15T12:45:26Z",
                "source_etag": '"abc"',
            },
        )
        self.assertEqual(sync.normalize_http_datetime("not-a-date"), "not-a-date")

        allowed = FakeSession([FakeResponse(status_code=404, error=requests.HTTPError())])
        self.assertEqual(
            sync.fetch_response(
                allowed, "https://example.test/missing", allowed_statuses=(404,)
            ).status_code,
            404,
        )

    def test_fetch_helpers_raise_after_retry_exhaustion(self):
        error = requests.ConnectionError("offline")
        session = FakeSession([FakeResponse(error=error), FakeResponse(error=error)])
        with (
            mock.patch.object(sync, "REQUEST_MAX_RETRIES", 2),
            mock.patch.object(sync, "REQUEST_BACKOFF_SECONDS", 0),
        ):
            with self.assertRaisesRegex(requests.ConnectionError, "offline"):
                sync.fetch_response(session, "https://example.test")

    def test_fetch_text_bytes_json_and_github_headers(self):
        session = FakeSession(
            [
                FakeResponse(text="hello"),
                FakeResponse(content=b"bytes"),
                FakeResponse(text='{"value": 3}'),
                FakeResponse(text="[]"),
            ]
        )
        self.assertEqual(sync.fetch_text(session, "https://example.test/text"), "hello")
        self.assertEqual(sync.fetch_bytes(session, "https://example.test/bytes"), b"bytes")
        self.assertEqual(sync.fetch_json(session, "https://example.test/json"), {"value": 3})
        self.assertEqual(sync.fetch_json(session, "https://example.test/list"), {})

        with mock.patch.dict(sync.os.environ, {"GH_TOKEN": "token"}, clear=True):
            self.assertEqual(sync.github_api_token(), "token")
            self.assertEqual(sync.github_api_headers()["Authorization"], "Bearer token")
        with mock.patch.dict(sync.os.environ, {}, clear=True):
            self.assertNotIn("Authorization", sync.github_api_headers())

    def test_local_command_version_and_path_helpers(self):
        completed = mock.Mock(returncode=0, stdout="codex-cli 1.2.3\n", stderr="")
        with mock.patch.object(sync.subprocess, "run", return_value=completed):
            self.assertEqual(sync.run_local_command(["tool", "--version"]), "codex-cli 1.2.3\n")

        failed = mock.Mock(returncode=2, stdout="", stderr="bad")
        with mock.patch.object(sync.subprocess, "run", return_value=failed):
            with self.assertRaisesRegex(RuntimeError, "exit code 2"):
                sync.run_local_command(["tool"])

        self.assertEqual(sync.parse_codex_cli_version("codex-cli 1.2.3"), "1.2.3")
        self.assertEqual(sync.parse_codex_cli_version("development"), "development")
        self.assertEqual(sync.encode_dot_path(Path(".system/.hidden/file")), "dot_system/dot_hidden/file")
        self.assertEqual(sync.source_area_slug("Tools & Guides"), "tools_guides")

    def test_source_area_metadata_covers_source_types(self):
        cases = [
            ("developers", "https://developers.openai.com/codex/cli", "codex_cli_docs"),
            (sync.LEARN_SOURCE_TYPE, "https://learn.chatgpt.com/docs/config-file", "learn_config_file"),
            ("github", sync.github_raw_url("docs/example.md"), "github_docs"),
            (
                sync.PLATFORM_TOOL_GUIDE_SOURCE_TYPE,
                "https://platform.openai.com/docs/guides/tools-web-search",
                "tool_guide_web_search",
            ),
            ("codex_cli_system_skill", "codex-cli://skills", "system_skill_alpha"),
            ("codex_cli_prompt_input", "codex-cli://prompt", "system_prompt"),
            (sync.CAPABILITY_INVENTORY_SOURCE_TYPE, "generated://capabilities", "capability_inventory"),
        ]
        items = [
            sync.ManagedFile(
                rel_path=(
                    f"{sync.SYSTEM_SKILL_OUTPUT_PREFIX}alpha/SKILL.md"
                    if source_type == "codex_cli_system_skill"
                    else f"{index}.md"
                ),
                source_type=source_type,
                source_url=url,
                content="# Test\n",
            )
            for index, (source_type, url, _area) in enumerate(cases)
        ]
        enriched = sync.add_source_area_metadata(items)
        self.assertEqual(
            [item.source_metadata["source_area"] for item in enriched],
            [area for _source_type, _url, area in cases],
        )

    def test_prompt_sanitization_is_recursive(self):
        payload = {
            "message": "at /private/user <current_date>today</current_date>",
            "nested": ["<shell>fish</shell>", "<timezone>local</timezone>"],
        }
        sanitized = sync.sanitize_prompt_payload(payload, [("/private/user", "$HOME")])
        self.assertEqual(
            sanitized,
            {
                "message": "at $HOME <current_date>YYYY-MM-DD</current_date>",
                "nested": ["<shell>bash</shell>", "<timezone>Etc/UTC</timezone>"],
            },
        )
        self.assertEqual(sync.sanitize_prompt_payload(4, []), 4)

    def test_discover_developers_urls_reports_coverage_and_fetch_errors(self):
        index = "<loc>https://example.test/one.xml</loc><loc>https://example.test/two.xml</loc>"
        sitemap = "".join(
            [
                "<loc>https://developers.openai.com/codex/cli/</loc>",
                "<loc>https://developers.openai.com/blog/topic/codex</loc>",
                "<loc>https://developers.openai.com/new-codex-page</loc>",
            ]
        )
        responses = [index, sitemap, requests.ConnectionError("broken sitemap")]

        def fake_fetch(_session, _url, headers=None):
            result = responses.pop(0)
            if isinstance(result, Exception):
                raise result
            return result

        with (
            mock.patch.object(sync, "fetch_text", side_effect=fake_fetch),
            mock.patch.object(sync, "load_existing_coverage", return_value={}),
            mock.patch.object(sync, "now_utc_iso", return_value="2026-01-01T00:00:00+00:00"),
        ):
            urls, coverage = sync.discover_developers_urls(mock.Mock())

        self.assertEqual(urls, ["https://developers.openai.com/codex/cli"])
        developers = coverage["developers"]
        self.assertEqual(developers["counts"]["sitemap_fetch_errors"], 1)
        self.assertEqual(
            developers["unclassified_skipped_codex_related_urls"],
            ["https://developers.openai.com/new-codex-page"],
        )

    def test_discover_learn_urls_filters_and_reports_new_pages(self):
        responses = [
            "<loc>https://learn.chatgpt.com/sitemap-1.xml/</loc>",
            "".join(
                [
                    "<loc>https://learn.chatgpt.com/docs/config-file/</loc>",
                    "<loc>https://learn.chatgpt.com/not-docs</loc>",
                ]
            ),
        ]
        with (
            mock.patch.object(sync, "fetch_text", side_effect=lambda *_args, **_kwargs: responses.pop(0)),
            mock.patch.object(sync, "load_existing_coverage", return_value={}),
        ):
            urls, coverage, errors = sync.discover_learn_urls(mock.Mock())

        self.assertEqual(urls, ["https://learn.chatgpt.com/docs/config-file"])
        self.assertEqual(coverage["counts"]["discovered_urls"], 1)
        self.assertEqual(errors, [])

        with mock.patch.object(sync, "fetch_text", return_value="<xml />"):
            with self.assertRaisesRegex(RuntimeError, "did not contain"):
                sync.discover_learn_urls(mock.Mock())

    def test_path_and_tool_guide_helpers(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            with isolated_outputs(Path(temporary_directory)):
                self.assertEqual(
                    sync.developers_url_to_rel_path(
                        "https://developers.openai.com/codex/cli"
                    ),
                    "developers.openai.com/codex/cli/index.md",
                )
                self.assertEqual(
                    sync.learn_url_to_rel_path("https://learn.chatgpt.com/docs/config"),
                    "learn.chatgpt.com/docs/config/index.md",
                )
                self.assertEqual(
                    sync.platform_url_to_rel_path(
                        "https://platform.openai.com/docs/guides/tools-web-search"
                    ),
                    "platform.openai.com/docs/guides/tools-web-search/index.md",
                )
                self.assertEqual(sync.github_path_to_rel_path("docs/a.md"), "github.openai.com/openai/codex/docs/a.md")

        url = "https://platform.openai.com/docs/guides/tools-web-search"
        self.assertEqual(sync.platform_markdown_url(url + "/"), url + ".md")
        self.assertEqual(sync.tool_guide_slug(url), "tools-web-search")
        self.assertIn("https://developers.openai.com/api/docs/guides/tools-web-search.md", sync.tool_guide_aliases(url))

    def test_markdown_and_html_conversion_remove_noise(self):
        raw = "import Thing from 'pkg';\n\n# Guide\n\nBody\nBody\n"
        rendered = sync.markdown_with_source("https://example.test/guide", raw, "Default")
        self.assertNotIn("import Thing", rendered)
        self.assertEqual(rendered.count("Body"), 1)
        self.assertTrue(rendered.startswith("# Guide\n\nSource:"))

        html = """
        <html><head><meta property="og:title" content="Example"></head>
        <body><nav>Noise</nav><main><h1>Example</h1><p>Useful text</p><script>bad()</script></main></body></html>
        """
        converted = sync.html_to_markdown("https://example.test/page", html)
        self.assertIn("# Example", converted)
        self.assertIn("Useful text", converted)
        self.assertNotIn("Noise", converted)
        self.assertNotIn("bad()", converted)

    def test_github_discovery_and_manifest_preservation(self):
        payload = {
            "tree": [
                {"type": "blob", "path": "README.md"},
                {"type": "blob", "path": "docs/guide.md"},
                {"type": "tree", "path": "docs"},
                {"type": "blob", "path": "src/main.rs"},
            ]
        }
        with mock.patch.object(sync, "fetch_json", return_value=payload):
            self.assertEqual(sync.discover_github_paths(mock.Mock()), ["README.md", "docs/guide.md"])

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with isolated_outputs(root):
                sync.MANIFEST_PATH.parent.mkdir(parents=True)
                sync.MANIFEST_PATH.write_text(
                    json.dumps(
                        {
                            "sources": {
                                "a.md": {"source_type": "github"},
                                "b.md": {"source_type": "developers"},
                            }
                        }
                    )
                )
                current = sync.ManagedFile("c.md", "github", "u", "c")
                self.assertEqual(
                    sync.coverage_paths_for_source([current], "github", {"github"}),
                    ["a.md", "c.md"],
                )

    def test_source_builders_keep_successes_and_record_failures(self):
        developer_urls = ["https://developers.openai.com/codex/a", "https://developers.openai.com/codex/b"]
        developer_coverage = {"developers": {"counts": {}}}
        with (
            mock.patch.object(sync, "discover_developers_urls", return_value=(developer_urls, developer_coverage)),
            mock.patch.object(
                sync,
                "fetch_text_with_source_metadata",
                side_effect=[("<main><h1>A</h1></main>", {}), requests.ConnectionError("bad")],
            ),
        ):
            files, coverage, failures = sync.build_developers_files(mock.Mock())
        self.assertEqual(len(files), 1)
        self.assertEqual(len(failures), 1)
        self.assertEqual(coverage["developers"]["counts"]["page_fetch_errors"], 1)

        learn_coverage = {"counts": {}}
        with (
            mock.patch.object(sync, "discover_learn_urls", return_value=(developer_urls, learn_coverage, [])),
            mock.patch.object(
                sync,
                "fetch_learn_page",
                side_effect=[("# A\n", {}, "markdown"), requests.ConnectionError("bad")],
            ),
        ):
            files, coverage, failures = sync.build_learn_files(mock.Mock())
        self.assertEqual(len(files), 1)
        self.assertEqual(coverage["counts"]["markdown_pages"], 1)
        self.assertEqual(len(failures), 1)

    def test_learn_page_prefers_markdown_and_falls_back_to_html(self):
        markdown = FakeSession(
            [FakeResponse(text="# Learn\n", headers={"Content-Type": "text/markdown"})]
        )
        content, metadata, mode = sync.fetch_learn_page(markdown, "https://learn.chatgpt.com/docs/a")
        self.assertEqual(mode, "markdown")
        self.assertEqual(metadata["source_kind"], "learn_markdown")
        self.assertIn("# Learn", content)

        fallback = FakeSession(
            [
                FakeResponse(status_code=404),
                FakeResponse(text="<main><h1>Learn</h1><p>HTML</p></main>"),
            ]
        )
        content, metadata, mode = sync.fetch_learn_page(fallback, "https://learn.chatgpt.com/docs/a")
        self.assertEqual(mode, "html_fallback")
        self.assertEqual(metadata["source_kind"], "learn_html_fallback")
        self.assertIn("HTML", content)

    def test_annotation_and_capability_helpers(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with isolated_outputs(root):
                item = sync.ManagedFile(
                    "guide.md",
                    "github",
                    "https://example.test/guide",
                    "# Guide\n",
                    {"source_area": "github_docs", "source_etag": '"new"'},
                )
                annotated = sync.annotate_markdown_file(
                    item,
                    {
                        "codex_cli_version": "1.2.3",
                        "codex_cli_version_raw": "codex-cli 1.2.3",
                    },
                )
                metadata, body = sync.split_markdown_frontmatter(annotated.content)
                self.assertEqual(metadata["source_area"], "github_docs")
                self.assertEqual(metadata["codex_cli_versions"], ["1.2.3"])
                self.assertEqual(body, "# Guide\n")

        self.assertEqual(sync.markdown_title("text\n# Name\n", "Default"), "Name")
        self.assertEqual(sync.markdown_title("text", "Default"), "Default")
        self.assertEqual(
            sync.capability_counts(
                [{"category": "tool"}, {"category": "skill"}, {"category": "tool"}]
            ),
            {"total": 3, "by_category": {"skill": 1, "tool": 2}},
        )

    def test_main_success_and_strict_partial_failure(self):
        developer = sync.ManagedFile("developers/a.md", "developers", "https://example.test/a", "# A\n")
        learn = sync.ManagedFile("learn/a.md", sync.LEARN_SOURCE_TYPE, "https://example.test/l", "# L\n")
        github = sync.ManagedFile("github/a.md", "github", "https://example.test/g", "# G\n")
        cli = sync.ManagedFile("cli/a.md", "codex_cli_prompt_input", "codex-cli://prompt", "# C\n")
        capability = sync.ManagedFile(sync.CAPABILITIES_REL_PATH, sync.CAPABILITY_INVENTORY_SOURCE_TYPE, "generated://capabilities", "{}\n")

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with (
                isolated_outputs(root),
                mock.patch.object(sync, "build_developers_files", return_value=([developer], {"developers": {"counts": {}}}, [])),
                mock.patch.object(sync, "build_learn_files", return_value=([learn], {"counts": {}}, [])),
                mock.patch.object(sync, "build_github_files", return_value=([github], [])),
                mock.patch.object(sync, "build_codex_cli_files", return_value=([cli], [], {"codex_cli_version": "1.2.3"})),
                mock.patch.object(sync, "build_platform_tool_guide_files", return_value=([], [], {})),
                mock.patch.object(sync, "build_capability_inventory_file", return_value=capability),
                mock.patch.object(sync, "write_coverage") as write_coverage,
                mock.patch.object(sync, "apply_sync", return_value=([], [], [])) as apply_sync,
            ):
                self.assertEqual(sync.main(), 0)
                self.assertTrue(write_coverage.called)
                self.assertTrue(apply_sync.called)

            failure = {"source": "developers", "stage": "page_fetch", "url": "u", "error": "bad"}
            with (
                isolated_outputs(root),
                mock.patch.object(sync, "build_developers_files", return_value=([developer], {"developers": {"counts": {}}}, [failure])),
                mock.patch.object(sync, "build_learn_files", return_value=([], {"counts": {}}, [])),
                mock.patch.object(sync, "build_github_files", return_value=([], [])),
                mock.patch.object(sync, "build_codex_cli_files", return_value=([], [], {})),
                mock.patch.object(sync, "build_platform_tool_guide_files", return_value=([], [], {})),
                mock.patch.object(sync, "write_coverage"),
                mock.patch.object(sync, "apply_sync", return_value=([], [], [])),
                mock.patch.object(sync, "STRICT_SYNC_MODE", True),
            ):
                self.assertEqual(sync.main(), 1)

    def test_main_isolates_source_build_failures(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            error = RuntimeError("offline")
            with (
                isolated_outputs(root),
                mock.patch.object(sync, "build_developers_files", side_effect=error),
                mock.patch.object(sync, "build_learn_files", side_effect=error),
                mock.patch.object(sync, "build_github_files", side_effect=error),
                mock.patch.object(sync, "build_codex_cli_files", side_effect=error),
                mock.patch.object(sync, "build_platform_tool_guide_files", side_effect=error),
                mock.patch.object(sync, "write_coverage"),
                mock.patch.object(sync, "write_summary") as write_summary,
            ):
                self.assertEqual(sync.main(), 1)
                self.assertTrue(write_summary.called)


def isolated_outputs(root: Path):
    docs = root / "docs"
    patches = {
        "ROOT": root,
        "DOCS_DIR": docs,
        "WEEKLY_DIR": root / "weekly",
        "MANIFEST_PATH": docs / "docs_manifest.json",
        "SUMMARY_PATH": docs / "sync_summary.json",
        "COVERAGE_PATH": docs / "source_coverage.json",
        "CAPABILITIES_PATH": docs / "codex_capabilities.json",
        "DEVELOPERS_ROOT": docs / "developers.openai.com",
        "LEARN_ROOT": docs / "learn.chatgpt.com",
        "GITHUB_ROOT": docs / "github.openai.com" / "openai" / "codex",
        "PLATFORM_ROOT": docs / "platform.openai.com",
        "SYSTEM_SKILLS_ROOT": root / "dot_codex" / "skills" / "dot_system",
        "SYSTEM_PROMPTS_ROOT": root / "system_prompts" / "codex-cli",
    }
    stack = ExitStack()
    for name, value in patches.items():
        stack.enter_context(mock.patch.object(sync, name, value))
    return stack


if __name__ == "__main__":
    unittest.main()
