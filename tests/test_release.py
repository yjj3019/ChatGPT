"""Check release version gating against disposable Git repositories."""
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_check", ROOT / "scripts/check_release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseCheckTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.git("init", "-q")
        self.git("symbolic-ref", "HEAD", "refs/heads/fixture-main")
        self.write("plugin.json", json.dumps({"version": "2.2.1"}))
        self.write("docs/policy.md", "original\n")
        self.commit("fixture")
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, capture_output=True,
                              text=True, encoding="utf-8", check=True).stdout

    def write(self, name, text):
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def commit(self, message):
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-qm", message)

    def check(self, expected, base=None):
        with patch.object(release, "ROOT", self.repo), redirect_stdout(io.StringIO()) as output:
            result = release.main(["--base", base or self.base])
        self.assertEqual(result, expected, output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())
        return output.getvalue()

    def test_unchanged_or_workflow_only_pass_without_bump(self):
        self.check(0)
        self.write(".github/workflows/check.yml", "name: CI\n")
        self.check(0)

    def test_unstaged_staged_and_untracked_payload_require_bump(self):
        self.write("docs/policy.md", "changed\n")
        self.assertIn("without a higher", self.check(1))
        self.git("add", "docs/policy.md")
        self.check(1)
        self.git("reset", "--quiet", self.base, "--", "docs/policy.md")
        self.write("docs/policy.md", "original\n")
        self.write("skills/new/SKILL.md", "new payload\n")
        self.check(1)

    def test_numeric_version_increase_passes_and_records_revision(self):
        self.write("docs/policy.md", "changed\n")
        self.write("plugin.json", json.dumps({"version": "2.3.0"}))
        output = self.check(0)
        self.assertIn("version=2.3.0", output)
        self.assertIn(f"HEAD={self.base}", output)
        self.assertIn(f"base={self.base}", output)

    def test_same_lower_and_malformed_versions_fail(self):
        for value in ("2.2.1", "2.2.0", "2.1.99", "02.3.0", "2.3", None):
            with self.subTest(value=value):
                self.write("plugin.json", json.dumps({"version": value}))
                self.write("docs/policy.md", "changed\n")
                self.check(1)
        self.write("plugin.json", "[]")
        self.check(1)

    def test_deleted_payload_requires_bump(self):
        (self.repo / "docs/policy.md").unlink()
        self.check(1)

    def test_invalid_base_fails_and_initial_push_passes(self):
        self.check(1, "missing-ref")
        self.assertIn("base=initial", self.check(0, "0" * 40))

    def test_new_branch_checks_payload_before_workflow_only_tip(self):
        self.git("branch", "baseline")
        self.write("docs/policy.md", "changed\n")
        self.commit("payload without version bump")
        self.write(".github/workflows/check.yml", "name: CI\n")
        self.commit("workflow only")
        self.assertIn("explicit --base", self.check(1, "0" * 40))
        self.assertIn("without a higher", self.check(1, "refs/heads/baseline"))

    def test_new_branch_version_bump_before_final_payload_passes(self):
        self.git("branch", "baseline")
        self.write("plugin.json", json.dumps({"version": "2.3.0"}))
        self.commit("version bump")
        self.write("docs/policy.md", "changed\n")
        self.commit("final payload")
        self.assertIn(f"base={self.base}", self.check(0, "refs/heads/baseline"))

    def test_branch_version_must_exceed_current_baseline_not_only_merge_base(self):
        self.write("plugin.json", json.dumps({"version": "2.4.0"}))
        self.commit("advance baseline version")
        self.git("branch", "baseline")
        self.git("checkout", "-qb", "feature", self.base)
        self.write("plugin.json", json.dumps({"version": "2.3.0"}))
        self.write("docs/policy.md", "feature\n")
        self.commit("feature version above ancestor but below baseline")
        self.assertIn("base=2.4.0", self.check(1, "refs/heads/baseline"))


@unittest.skipIf((ROOT / ".chatgpt-transfer-manifest.json").is_file(),
                 "CI workflow applies to the repository, not legacy skill copies")
class WorkflowBaseTests(unittest.TestCase):
    def test_workflow_selects_explicit_base_without_shell_interpolation(self):
        workflow = (ROOT / ".github/workflows/validate-framework.yml").read_text(encoding="utf-8")
        step = workflow.split("      - name: Require a version bump for distributed changes\n", 1)[1]
        self.assertIn("        shell: python\n", step)
        code = textwrap.dedent(step.split("        run: |\n", 1)[1])
        for base, branch, ref, expected in (
            ("a" * 40, "main", "refs/heads/main", "a" * 40),
            ("b" * 40, "main", "refs/pull/1/merge", "b" * 40),
            ("0" * 40, "main", "refs/heads/feature", "refs/remotes/origin/main"),
            ("0" * 40, "main", "refs/heads/main", "0" * 40),
            ("0" * 40, "branch'$(literal)", "refs/heads/feature", "refs/remotes/origin/branch'$(literal)"),
        ):
            with self.subTest(ref=ref, branch=branch), patch.dict(os.environ, {
                "RELEASE_BASE": base, "RELEASE_DEFAULT_BRANCH": branch, "RELEASE_REF": ref,
            }, clear=True), patch.object(subprocess, "run") as run:
                exec(compile(code, str(ROOT / ".github/workflows/validate-framework.yml"), "exec"), {})
                run.assert_called_once_with(
                    [sys.executable, "-X", "utf8", "scripts/check_release.py", "--base", expected], check=True)


if __name__ == "__main__":
    unittest.main()
