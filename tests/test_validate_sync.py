import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VALIDATE_SCRIPT = ROOT / "scripts" / "validate_sync.sh"


class ValidateSyncScopeTests(unittest.TestCase):
    """Run validate_sync.sh against stub generators in a disposable checkout."""

    def run_validation(self, sync_body: str) -> subprocess.CompletedProcess:
        tmp = Path(tempfile.mkdtemp(prefix="validate-sync-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        repo = tmp / "repo"
        scripts = repo / "scripts"
        scripts.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        shutil.copy2(VALIDATE_SCRIPT, scripts / "validate_sync.sh")

        bin_dir = tmp / "bin"
        bin_dir.mkdir()
        (bin_dir / "python").symlink_to(sys.executable)
        activate = repo / ".venv" / "bin" / "activate"
        activate.parent.mkdir(parents=True)
        activate.write_text(f'export PATH="{bin_dir}:$PATH"\n')

        (scripts / "sync_helper.py").write_text("VALUE = 'stable'\n")
        (scripts / "fetch_codex_docs.py").write_text(textwrap.dedent(sync_body))
        (scripts / "check_codex_freshness.py").write_text("import sync_helper\n")

        # Only what the script needs; inherited credentials never reach the stub generators.
        env = {key: os.environ[key] for key in ("PATH", "TMPDIR", "LANG") if key in os.environ}
        env["HOME"] = str(tmp)
        return subprocess.run(
            ["bash", "scripts/validate_sync.sh"],
            cwd=repo,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )

    def test_generator_imports_do_not_count_as_repository_changes(self):
        result = self.run_validation(
            """
            from pathlib import Path
            import sync_helper

            Path("docs").mkdir(exist_ok=True)
            Path("docs/output.txt").write_text(sync_helper.VALUE)
            """
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Validation passed", result.stdout)
        self.assertNotIn("__pycache__", result.stdout)

    def test_writes_outside_generated_roots_still_fail_scope_check(self):
        result = self.run_validation(
            """
            from pathlib import Path
            import sync_helper

            Path("stray.txt").write_text(sync_helper.VALUE)
            """
        )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Changed-file scope violation", result.stdout)
        self.assertIn("- stray.txt", result.stdout)
        self.assertNotIn("__pycache__", result.stdout)


if __name__ == "__main__":
    unittest.main()
