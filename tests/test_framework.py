"""Exercise the real maintenance commands against disposable repository copies."""
import importlib.util
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

    def test_fallback_drift_is_detected(self):
        self.rewrite("docs/chatgpt-5.5-all-in-one-instructions.md", "# ChatGPT", "# Modified ChatGPT")
        self.assert_failure(self.run_script("validate_framework.py"), "out of sync")

    def test_full_guide_drift_is_detected(self):
        self.rewrite("docs/chatgpt-transfer-instructions.md", "# ChatGPT", "# Modified ChatGPT")
        self.assert_failure(self.run_script("sync_runtime.py", "--check"), "out of sync")

    def test_changed_rule_reaches_all_generated_documents(self):
        rule = "Unique regression rule for canonical ownership."
        source = self.root / "docs/chatgpt-5.5-project-instructions.md"
        source.write_text(source.read_text(encoding="utf-8") + "\n" + rule + "\n", encoding="utf-8")
        self.assertEqual(self.run_script("sync_runtime.py").returncode, 0)
        for relative in ("CHATGPT.md", "docs/chatgpt-5.5-all-in-one-instructions.md", "docs/chatgpt-transfer-instructions.md"):
            self.assertEqual((self.root / relative).read_text(encoding="utf-8").count(rule), 1)

    def test_missing_source_does_not_partially_write_generated_documents(self):
        (self.root / "docs/chatgpt-blog-rules.md").unlink()
        paths = [self.root / relative for relative in (
            "CHATGPT.md", "docs/chatgpt-5.5-all-in-one-instructions.md", "docs/chatgpt-transfer-instructions.md",
        )]
        before = [path.read_bytes() for path in paths]
        self.assert_failure(self.run_script("sync_runtime.py"), "synchronization failed")
        self.assertEqual([path.read_bytes() for path in paths], before)

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

    def test_required_route_cannot_be_empty_or_wrong(self):
        for required in ("None", "`docs/chatgpt-blog-rules.md`"):
            with self.subTest(required=required):
                entry = self.root / "CHATGPT.md"
                original = entry.read_text(encoding="utf-8")
                self.rewrite("CHATGPT.md", "| Coding/debugging | `docs/chatgpt-coding-rules.md` |",
                             f"| Coding/debugging | {required} |")
                self.assert_failure(self.run_script("validate_framework.py"), "incorrect required route")
                entry.write_text(original, encoding="utf-8")

    def test_duplicate_route_is_rejected(self):
        entry = self.root / "CHATGPT.md"
        text = entry.read_text(encoding="utf-8")
        row = next(line for line in text.splitlines() if line.startswith("| Coding/debugging |"))
        self.rewrite("CHATGPT.md", row, row + "\n" + row)
        self.assert_failure(self.run_script("validate_framework.py"), "duplicate task-map rows")

    def test_missing_route_is_rejected(self):
        entry = self.root / "CHATGPT.md"
        row = next(line for line in entry.read_text(encoding="utf-8").splitlines() if line.startswith("| Coding/debugging |"))
        self.rewrite("CHATGPT.md", row, "")
        self.assert_failure(self.run_script("validate_framework.py"), "missing task-map rows")

    def test_missing_golden_test_is_rejected(self):
        (self.root / "tests/GoldenTest-016.md").unlink()
        self.assert_failure(self.run_script("validate_framework.py"), "missing required Golden Test 016")

    def test_empty_golden_rubric_is_rejected(self):
        path = self.root / "tests/GoldenTest-015.md"
        prefix = path.read_text(encoding="utf-8-sig").split("## Gold Rubric", 1)[0]
        path.write_text(prefix + "## Gold Rubric\n", encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "missing or empty Gold Rubric")

    def test_empty_golden_scenario_is_rejected(self):
        path = self.root / "tests/GoldenTest-015.md"
        path.write_text("# Golden Test 015: Example\n\n## Scenario\n\n## Gold Rubric\n- Evidence\n", encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "missing or empty Scenario")

    def test_multiple_golden_headers_are_rejected(self):
        path = self.root / "tests/GoldenTest-015.md"
        path.write_text(path.read_text(encoding="utf-8-sig") + "\n# Golden Test 099: Duplicate\n", encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "expected one Golden Test ID header")

    def test_golden_filename_must_match_header(self):
        self.rewrite("tests/GoldenTest-015.md", "# Golden Test 015:", "# Golden Test 099:")
        self.assert_failure(self.run_script("validate_framework.py"), "filename/header mismatch")

    def test_missing_inline_reference_is_rejected(self):
        path = self.root / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n`scripts/missing.py`\n", encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "references missing file: scripts/missing.py")

    def test_missing_markdown_link_is_rejected(self):
        path = self.root / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n[Missing](docs/missing.md)\n", encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "references missing file: docs/missing.md")

    def test_relative_markdown_link_is_supported(self):
        (self.root / "docs/link-check.md").write_text("[Entry](../CHATGPT.md#core-runtime)\n", encoding="utf-8")
        result = self.run_script("validate_framework.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_malformed_url_is_reported_without_traceback(self):
        (self.root / "docs/link-check.md").write_text("[Bad](https://[broken)\n", encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "invalid link")

    def test_invalid_local_path_is_reported_without_traceback(self):
        (self.root / "docs/link-check.md").write_text("[Bad](missing\x00file.md)\n", encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "invalid file reference")

    def test_reference_cannot_leave_repository(self):
        (self.root / "docs/link-check.md").write_text("[Outside](../../outside.md)\n", encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "reference leaves repository")

    def test_invalid_utf8_is_reported_without_traceback(self):
        (self.root / "README.md").write_bytes(bytes([0xFF]))
        self.assert_failure(self.run_script("validate_framework.py"), "cannot read document")

    def test_bom_and_crlf_sources_do_not_create_drift(self):
        path = self.root / "docs/chatgpt-5.5-project-instructions.md"
        text = path.read_text(encoding="utf-8-sig")
        path.write_bytes(bytes([0xEF, 0xBB, 0xBF]) + text.replace("\n", "\r\n").encode("utf-8"))
        result = self.run_script("sync_runtime.py", "--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_duplicate_and_reversed_markers_are_rejected(self):
        entry = self.root / "CHATGPT.md"
        original = entry.read_text(encoding="utf-8")
        begin = next(line for line in original.splitlines() if line.startswith("<!-- BEGIN INLINED"))
        end = "<!-- END INLINED CORE RUNTIME -->"
        for text in (original + "\n" + begin, original.replace(begin, "TEMP").replace(end, begin).replace("TEMP", end)):
            with self.subTest(text=text[:30]):
                entry.write_text(text, encoding="utf-8")
                self.assert_failure(self.run_script("sync_runtime.py", "--check"), "marker pair")

    def test_missing_entry_is_reported_without_traceback(self):
        (self.root / "CHATGPT.md").unlink()
        self.assert_failure(self.run_script("validate_framework.py"), "missing required file: CHATGPT.md")

    def test_missing_context_budget_is_rejected(self):
        self.rewrite("AGENTS.md", "## Context Budget", "## Unrecognized Heading")
        self.assert_failure(self.run_script("validate_framework.py"), "missing or empty Context Budget")

    def test_missing_intent_classifier_is_rejected(self):
        self.rewrite("CHATGPT.md", "## Intent Classifier", "## Unrecognized Heading")
        self.assert_failure(self.run_script("validate_framework.py"), "missing or empty Intent Classifier")

    def test_forced_heavy_autoload_is_rejected(self):
        self.rewrite("CHATGPT.md", "## Autoload Protocol", "## Autoload Protocol\n\nAlways load `docs/chatgpt-transfer-instructions.md` for every task.")
        self.assert_failure(self.run_script("validate_framework.py"), "heavy guide must not always load")

    def test_measurement_does_not_double_count_standalone_core(self):
        result = self.run_script("measure_load.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        row = next(line for line in result.stdout.splitlines() if line.startswith("One-shot copy/paste setup"))
        size = len((self.root / "docs/chatgpt-5.5-all-in-one-instructions.md").read_text(encoding="utf-8-sig").encode("utf-8"))
        self.assertEqual(int(row.split()[3]), size)
        self.assertIn("not actual usage", result.stdout)

    def test_measurement_missing_input_fails(self):
        (self.root / "docs/chatgpt-coding-rules.md").unlink()
        self.assert_failure(self.run_script("measure_load.py"), "Load estimate failed")

    def test_measurement_missing_section_fails(self):
        self.rewrite("docs/chatgpt-engineering-task-rules.md", "## Root Cause Analysis", "## Unknown Section")
        self.assert_failure(self.run_script("measure_load.py"), "missing section")

    def test_measurement_uses_normalized_bytes(self):
        before = self.run_script("measure_load.py")
        path = self.root / "docs/chatgpt-5.5-project-instructions.md"
        text = path.read_text(encoding="utf-8-sig")
        path.write_bytes(bytes([0xEF, 0xBB, 0xBF]) + text.replace("\n", "\r\n").encode("utf-8"))
        after = self.run_script("measure_load.py")
        self.assertEqual(after.returncode, 0, after.stdout + after.stderr)
        self.assertEqual(before.stdout, after.stdout)


    def _load_markdown_sections(self):
        module_path = self.root / "scripts" / "markdown_sections.py"
        spec = importlib.util.spec_from_file_location("markdown_sections_under_test", module_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module

    def test_fence_aware_section_parse_ignores_headings_in_fences(self):
        ms = self._load_markdown_sections()
        sample = (
            "# Title\n\n## Real One\n\nBody\n\n"
            "```text\n## Fake Inside\n## Also Fake\n```\n\n"
            "## Real Two\n\nMore\n"
        )
        titles = [t for t in ms.parse_sections(sample) if t != "__intro__"]
        self.assertEqual(titles, ["Real One", "Real Two"])
        self.assertIn("## Fake Inside", ms.section_body(sample, "Real One"))
        blog = (self.root / "docs/chatgpt-blog-rules.md").read_text(encoding="utf-8-sig")
        blog_titles = sorted(t for t in ms.parse_sections(blog) if t != "__intro__")
        self.assertEqual(blog_titles, ["Outline", "Review Checklist", "Style"])

    def test_meta_phrase_inside_inlined_core_fails(self):
        entry = self.root / "CHATGPT.md"
        text = entry.read_text(encoding="utf-8")
        begin = "<!-- BEGIN INLINED CORE RUNTIME (generated from docs/ — do not edit here) -->"
        self.assertIn(begin, text)
        poisoned = text.replace(begin, begin + "\nsync_runtime maintainer note\n", 1)
        entry.write_text(poisoned, encoding="utf-8")
        self.assert_failure(self.run_script("validate_framework.py"), "maintainer/meta phrase inside inlined Core")

    def test_invariant_coverage_detects_missing_unverified_marker(self):
        # Strip the invariant needle from Core sources and AGENTS without removing required headings.
        self.rewrite("docs/chatgpt-operational-integrity-rules.md", "[unverified]", "[not-verified-marker]")
        self.rewrite("AGENTS.md", "[unverified]", "[not-verified-marker]")
        self.assertEqual(self.run_script("sync_runtime.py").returncode, 0)
        self.assert_failure(self.run_script("validate_framework.py"), "invariant coverage failed: unverified_marker")

    def test_measurement_blog_outline_not_split_by_fence(self):
        result = self.run_script("measure_load.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        ms = self._load_markdown_sections()
        blog = (self.root / "docs/chatgpt-blog-rules.md").read_text(encoding="utf-8-sig")
        sizes = {title: len(body.encode("utf-8")) for title, body in ms.parse_sections(blog).items()}
        self.assertIn("Outline", sizes)
        self.assertNotIn("Why this matters now", sizes)

if __name__ == "__main__":
    unittest.main()
