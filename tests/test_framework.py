"""Exercise the real maintenance commands against disposable repository copies."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FrameworkCommandsTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="chatgpt-test-", dir=ROOT.parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "pack"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def run_script(self, script, *arguments):
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(self.root / "scripts" / script), *arguments],
            cwd=self.temporary.name, capture_output=True, text=True, encoding="utf-8", timeout=20,
        )

    def rewrite(self, relative, old, new):
        path = self.root / relative
        text = path.read_text(encoding="utf-8-sig")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def assert_failure(self, result, message):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(message, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_repository_passes_from_another_directory(self):
        result = self.run_script("validate_framework.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_runtime_growth_exceeding_budget_fails(self):
        entry = self.root / "CHATGPT.md"
        entry.write_text("x" * 8000 + "\n" + entry.read_text(encoding="utf-8"), encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "character budget exceeded")

    def test_codex_growth_exceeding_budget_fails(self):
        entry = self.root / "AGENTS.md"
        entry.write_text("x" * 4001, encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "AGENTS.md: character budget exceeded")

    def test_missing_core_file_is_reported_without_traceback(self):
        (self.root / "docs/chatgpt-5.5-project-instructions.md").unlink()
        self.assert_failure(self.run_script("validate_framework.py"), "missing required file")

    def test_sync_check_detects_drift_without_writing(self):
        core = self.root / "docs/chatgpt-5.5-project-instructions.md"
        core.write_text(core.read_text(encoding="utf-8") + "\nChanged rule.\n", encoding="utf-8")
        entry = self.root / "CHATGPT.md"
        before = entry.read_bytes()
        result = self.run_script("sync_runtime.py", "--check")
        self.assertEqual(entry.read_bytes(), before)
        self.assert_failure(result, "out of sync")

    def test_sync_check_does_not_touch_clean_files(self):
        entry = self.root / "CHATGPT.md"
        before = (entry.read_bytes(), entry.stat().st_mtime_ns)
        result = self.run_script("sync_runtime.py", "--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((entry.read_bytes(), entry.stat().st_mtime_ns), before)

    def test_sync_is_idempotent_and_preserves_surrounding_text(self):
        entry = self.root / "CHATGPT.md"
        entry.write_text("before\n" + entry.read_text(encoding="utf-8") + "\nafter\n", encoding="utf-8")
        self.assertEqual(self.run_script("sync_runtime.py").returncode, 0)
        once = entry.read_bytes()
        self.assertEqual(self.run_script("sync_runtime.py").returncode, 0)
        self.assertEqual(entry.read_bytes(), once)
        self.assertTrue(once.startswith(b"before\n"))
        self.assertTrue(once.endswith(b"\nafter\n"))

    def test_invalid_markers_fail_without_writing(self):
        self.rewrite("CHATGPT.md", "<!-- END INLINED CORE RUNTIME -->", "")
        entry = self.root / "CHATGPT.md"
        before = entry.read_bytes()
        self.assert_failure(self.run_script("sync_runtime.py"), "marker pair")
        self.assertEqual(entry.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
