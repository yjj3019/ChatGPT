"""Unit tests for scripts/install_pack.py (detect_targets, dry-run, temp-home install)."""
from __future__ import annotations

import importlib.util
import hashlib
import io
import json
import stat
import os
import subprocess
import sys
import tempfile
import unittest
import warnings
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "install_pack.py"


def load_install_pack():
    spec = importlib.util.spec_from_file_location("install_pack_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


install_pack = load_install_pack()


class SkillMetadataTests(unittest.TestCase):
    def test_generated_skill_has_metadata_and_relative_minimal_entry(self):
        content = install_pack.skill_hint()
        install_pack.validate_skill_metadata(content)
        metadata = dict(line.split(": ", 1) for line in content.splitlines()[1:3])
        self.assertEqual(json.loads(metadata["name"]), install_pack.PACK_NAME)
        self.assertLess(len(json.loads(metadata["description"])), 200)
        self.assertIn("Read [AGENTS.md](AGENTS.md) relative to this SKILL.md directory", content)
        self.assertIn("Not for unrelated", json.loads(metadata["description"]))
        self.assertIn("explicit skill invocation", content)
        self.assertLess(len(content.encode("utf-8")), 1300)

    def test_native_name_validation_preserves_legacy_defaults(self):
        self.assertEqual(install_pack.PACK_NAME, "chatgpt-transfer")
        renamed = install_pack.skill_hint().replace('name: "chatgpt-transfer"', 'name: "taskforge"')
        install_pack.validate_skill_metadata(renamed, expected_name="taskforge")
        with self.assertRaises(ValueError):
            install_pack.validate_skill_metadata(renamed)

    def test_invalid_generated_metadata_is_rejected(self):
        valid = install_pack.skill_hint()
        cases = (
            valid.split("---", 2)[-1],
            valid.replace('name: "chatgpt-transfer"', 'name: "wrong-pack"'),
            valid.replace('name: "chatgpt-transfer"', 'name: null'),
            valid.replace('name: "chatgpt-transfer"', 'description: "duplicate"'),
            valid.replace('name: "chatgpt-transfer"', 'name: [broken'),
        )
        for content in cases:
            with self.subTest(content=content[:70]), self.assertRaises(ValueError):
                install_pack.validate_skill_metadata(content)
        lines = valid.splitlines()
        for description in (None, True, [], "", " ", "x" * 1025, "a\nb"):
            lines[2] = "description: " + json.dumps(description)
            with self.subTest(description=description), self.assertRaises(ValueError):
                install_pack.validate_skill_metadata("\n".join(lines))


class DestinationArgumentTests(unittest.TestCase):
    def test_auto_and_dest_conflict_before_any_target_access(self):
        for mode in ([], ["--check"], ["--dry-run"], ["--force"]):
            for targets in (["--auto", "--dest", "unused"], ["--dest", "unused", "--auto"]):
                with self.subTest(mode=mode, targets=targets), \
                        patch.object(install_pack, "detect_targets") as detect, \
                        patch.object(install_pack, "destination_root") as destination, \
                        patch.object(install_pack, "install_pack") as install, \
                        patch.object(install_pack, "verify_install") as verify, \
                        redirect_stderr(io.StringIO()) as error:
                    with self.assertRaises(SystemExit) as raised:
                        install_pack.main(targets + mode)
                    self.assertEqual(raised.exception.code, 2)
                    self.assertIn("not allowed with argument", error.getvalue())
                    detect.assert_not_called()
                    destination.assert_not_called()
                    install.assert_not_called()
                    verify.assert_not_called()


class DetectTargetsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def test_detects_each_host(self):
        cases = (
            (".claude", ".claude/skills"),
            (".codex", ".agents/skills"),
            (".grok", ".grok/skills"),
            (".agents", ".agents/skills"),
            (".cursor", ".cursor/skills"),
        )
        for marker, expected in cases:
            with self.subTest(marker=marker):
                home = Path(tempfile.mkdtemp(dir=self.home))
                (home / marker).mkdir()
                with patch.dict(os.environ, {}, clear=True):
                    targets = install_pack.detect_targets(home)
                self.assertEqual([p for _, p in targets], [home / expected])

    def test_detects_nothing_on_bare_home(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(install_pack.detect_targets(self.home), [])

    def test_env_ai_pack_dir(self):
        pack = self.home / "custom-packs"
        pack.mkdir()
        with patch.dict(os.environ, {"AI_PACK_DIR": str(pack)}, clear=True):
            targets = install_pack.detect_targets(self.home)
        self.assertEqual([p for _, p in targets], [pack.absolute()])

    def test_env_codex_home(self):
        codex = self.home / "codex-home"
        codex.mkdir()
        with patch.dict(os.environ, {"CODEX_HOME": str(codex)}, clear=True):
            targets = install_pack.detect_targets(self.home)
        self.assertEqual([p for _, p in targets], [(codex / "skills").absolute()])

    def test_dedupes_codex_and_agents_marker(self):
        (self.home / ".codex").mkdir()
        (self.home / ".agents").mkdir()
        with patch.dict(os.environ, {}, clear=True):
            targets = install_pack.detect_targets(self.home)
        paths = [p for _, p in targets]
        self.assertEqual(paths, [(self.home / ".agents/skills").absolute()])


    def test_detect_preserves_symlink_path_so_install_can_refuse_it(self):
        target = self.home / "real-skills"
        target.mkdir()
        link = self.home / "linked-skills"
        try:
            link.symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlinks unavailable: {exc}")
        with patch.dict(os.environ, {"AI_PACK_DIR": str(link)}, clear=True):
            targets = install_pack.detect_targets(self.home)
        self.assertEqual([p for _, p in targets], [link.absolute()])
        with self.assertRaisesRegex(SystemExit, "Symlink|junction"):
            install_pack.install_pack(targets[0][1])
        self.assertEqual(list(target.iterdir()), [])


class InstallPackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def _run(self, *args: str, home: Path | None = None, env_extra: dict | None = None):
        env = {
            k: v
            for k, v in os.environ.items()
            if k
            not in {
                "AI_PACK_DIR",
                "AI_SKILLS_DIR",
                "CURSOR_PACK_DIR",
                "CURSOR_SKILLS_DIR",
                "CODEX_HOME",
            }
        }
        env["HOME"] = env["USERPROFILE"] = str(home or self.home)
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(ROOT),
            env=env,
        )

    def test_dry_run_auto_does_not_create_files(self):
        (self.home / ".claude").mkdir()
        proc = self._run("--auto", "--dry-run")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("Would install", proc.stdout)
        self.assertFalse((self.home / ".claude/skills/chatgpt-transfer").exists())

    def test_auto_installs_into_temp_home_hosts(self):
        (self.home / ".claude").mkdir()
        (self.home / ".grok").mkdir()
        proc = self._run("--auto")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        for host in (".claude/skills", ".grok/skills"):
            pack = self.home / host / "chatgpt-transfer"
            self.assertTrue((pack / "CHATGPT.md").is_file(), pack)
            self.assertTrue((pack / "AGENTS.md").is_file())
            self.assertTrue((pack / "docs").is_dir())
            self.assertTrue((pack / "prompts").is_dir())
            self.assertTrue((pack / "scripts" / "validate_framework.py").is_file())
            self.assertTrue((pack / "scripts" / "install_pack.py").is_file())
            self.assertTrue((pack / "SKILL.md").is_file())
            self.assertTrue((pack / "INSTALL_NOTE.md").is_file())
            self.assertFalse((pack / "tests").exists())

    def test_auto_fallback_when_no_host(self):
        proc = self._run("--auto")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("No AI host detected", proc.stdout)
        pack = self.home / ".agents/skills/chatgpt-transfer"
        self.assertTrue((pack / "CHATGPT.md").is_file())

    def test_auto_install_preserves_codex_settings_and_memory_state(self):
        codex = self.home / ".codex"
        (codex / "memories").mkdir(parents=True)
        config = codex / "config.toml"
        memory = codex / "memories" / "MEMORY.md"
        config.write_text('model = "recipient-model-fixture"\nmodel_reasoning_effort = "low"\n'
                          '[features]\nmulti_agent = false\n[memories]\nuse_memories = false\n',
                          encoding="utf-8")
        memory.write_text("Benign synthetic memory fixture.\n", encoding="utf-8")
        (codex / "agents").mkdir()
        existing_role = codex / "agents/recipient-role.toml"
        existing_role.write_text('name = "recipient_role"\ndescription = "Fixture"\n'
                                 'developer_instructions = "Preserve this recipient role."\n',
                                 encoding="utf-8")
        before = {path: path.read_bytes() for path in (config, memory, existing_role)}
        proc = self._run("--auto")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual({path: path.read_bytes() for path in before}, before)
        pack = self.home / ".agents/skills/chatgpt-transfer"
        self.assertEqual((pack / "docs/codex-memories-maintenance.md").read_bytes(),
                         (ROOT / "docs/codex-memories-maintenance.md").read_bytes())
        self.assertFalse((pack / "config.toml").exists())
        self.assertFalse((pack / "memories").exists())
        for filename in ("luna-explorer.toml", "luna-runner.toml", "astra-reviewer.toml", "AGENTS.snippet.md",
                         "AGENTS.auto.snippet.md", "notion-recorder.toml"):
            relative = Path("docs/examples/codex-three-models") / filename
            self.assertEqual((pack / relative).read_bytes(), (ROOT / relative).read_bytes())
        self.assertFalse((pack / ".codex").exists())
        self.assertFalse((codex / "agents/notion-recorder.toml").exists())
        for filename in ("codex-notion-recording.md", "host-verification-2026-10-16.md",
                         "host-verification-2026-10-18.md"):
            relative = Path("docs") / filename
            self.assertEqual((pack / relative).read_bytes(), (ROOT / relative).read_bytes())
        for filename in ("pack-explorer.toml", "pack-runner.toml", "pack-reviewer.toml", "AGENTS.snippet.md"):
            relative = Path("docs/examples/codex-standard-agents") / filename
            self.assertEqual((pack / relative).read_bytes(), (ROOT / relative).read_bytes())
        self.assertEqual(list((codex / "agents").iterdir()), [existing_role])

    def test_with_tests_copies_tests_dir(self):
        dest = self.home / "skills"
        proc = self._run("--dest", str(dest), "--with-tests")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue((dest / "chatgpt-transfer" / "tests" / "Scorecard.md").is_file())
        pack = dest / "chatgpt-transfer"
        manifest = json.loads((pack / install_pack.MANIFEST_FILE).read_text(encoding="utf-8"))
        for name in ("README.md", "skill-invocation-cases.json"):
            relative = Path("tests/evals") / name
            self.assertEqual((pack / relative).read_bytes(), (ROOT / relative).read_bytes())
            self.assertIn(relative.as_posix(), manifest["files"])

    def test_identical_install_preserves_user_files(self):
        dest = self.home / "skills"
        first = self._run("--dest", str(dest))
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        marker = dest / "chatgpt-transfer" / "USER_NOTES.txt"
        marker.write_text("stale", encoding="utf-8")
        second = self._run("--dest", str(dest))
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(marker.read_text(encoding="utf-8"), "stale")
        self.assertIn("Unchanged", second.stdout)
        self.assertTrue((dest / "chatgpt-transfer" / "CHATGPT.md").is_file())

    def test_installed_pack_contains_both_languages_and_compatibility_entry(self):
        dest = self.home / "skills"
        proc = self._run("--dest", str(dest))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        pack = dest / "chatgpt-transfer"
        manifest = json.loads((pack / install_pack.MANIFEST_FILE).read_text(encoding="utf-8"))
        for name in ("README.md", "README.en.md", "README.ko.md"):
            self.assertEqual((pack / name).read_bytes(), (ROOT / name).read_bytes())
            self.assertIn(name, manifest["files"])
        self.assertIn("](README.en.md)", (pack / "README.md").read_text(encoding="utf-8"))
        self.assertIn("](README.md)", (pack / "README.en.md").read_text(encoding="utf-8"))
        (pack / "README.en.md").unlink()
        self.assertTrue(install_pack.verify_install(pack))

    def test_print_chatgpt_mentions_entry(self):
        proc = self._run("--print-chatgpt")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("CHATGPT.md", proc.stdout)
        self.assertIn("Project Instructions", proc.stdout)

    def test_license_is_distributed_and_integrity_checked(self):
        dest = self.home / "skills"
        proc = self._run("--dest", str(dest))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        pack = dest / "chatgpt-transfer"
        license_file = pack / "LICENSE"
        self.assertEqual(license_file.read_bytes(), (ROOT / "LICENSE").read_bytes())
        self.assertIn("MIT License", license_file.read_text(encoding="utf-8"))
        self.assertEqual(install_pack.verify_install(pack), [])
        license_file.unlink()
        self.assertTrue(install_pack.verify_install(pack))

    def test_check_source_tree(self):
        proc = self._run("--check")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("validate OK", proc.stdout)

    def test_check_installed_pack(self):
        dest = self.home / "skills"
        install = self._run("--dest", str(dest))
        self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
        proc = self._run("--check", "--dest", str(dest))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("files OK", proc.stdout)
        self.assertIn("validate skipped", proc.stdout)

    def test_check_installed_pack_with_tests_runs_validate(self):
        dest = self.home / "skills"
        install = self._run("--dest", str(dest), "--with-tests")
        self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
        proc = self._run("--check", "--dest", str(dest))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("files OK", proc.stdout)
        self.assertIn("validate OK", proc.stdout)

    def test_installed_script_checks_its_own_integrity_without_destination_config(self):
        dest = self.home / "skills"
        pack = dest / install_pack.PACK_NAME
        installed_script = pack / "scripts" / "install_pack.py"
        for scenario in ("clean", "tampered", "missing_manifest", "missing_manifest_and_note"):
            with self.subTest(scenario=scenario):
                installed = self._run("--dest", str(dest), "--force")
                self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
                if scenario == "tampered":
                    (pack / "docs" / "chatgpt-coding-rules.md").write_text("tampered", encoding="utf-8")
                elif scenario.startswith("missing_manifest"):
                    (pack / install_pack.MANIFEST_FILE).unlink()
                    if scenario == "missing_manifest_and_note":
                        (pack / "INSTALL_NOTE.md").unlink()
                env = {k: v for k, v in os.environ.items()
                       if k not in {"AI_PACK_DIR", "AI_SKILLS_DIR", "CURSOR_PACK_DIR",
                                    "CURSOR_SKILLS_DIR", "CODEX_HOME"}}
                env["HOME"] = env["USERPROFILE"] = str(self.home)
                proc = subprocess.run(
                    [sys.executable, "-X", "utf8", str(installed_script), "--check"],
                    cwd=pack, env=env, capture_output=True, text=True, encoding="utf-8",
                    errors="replace",
                )
                if scenario == "clean":
                    self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                    self.assertIn("files OK", proc.stdout)
                else:
                    self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                    self.assertIn("FAIL", proc.stdout)
                    self.assertNotIn("files OK", proc.stdout)

    def test_list_targets(self):
        (self.home / ".cursor").mkdir()
        proc = self._run("--list-targets")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(str(Path(".cursor") / "skills"), proc.stdout)
        self.assertFalse((self.home / ".cursor/skills").exists())

    def test_destination_root_requires_config(self):
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(SystemExit):
            install_pack.destination_root(None)

    def test_destination_root_explicit_wins(self):
        with patch.dict(os.environ, {"AI_PACK_DIR": "ignored"}, clear=True):
            self.assertEqual(
                install_pack.destination_root(str(self.home / "x")),
                self.home / "x",
            )

    def test_verify_reports_gutted_install(self):
        dest_root = self.home / "skills"
        pack = install_pack.install_pack(dest_root)
        self.assertEqual(install_pack.verify_install(pack), [])
        (pack / "scripts" / "validate_framework.py").unlink()
        problems = install_pack.verify_install(pack)
        self.assertTrue(any("validate_framework.py" in p for p in problems))


class SafeInstallTests(unittest.TestCase):
    """Small source fixtures isolate safety behavior from repository contents."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.source = self.base / "source"
        self.source.mkdir()
        for name in install_pack.REQUIRED_FILES:
            (self.source / name).write_text(name + " original", encoding="utf-8")
        for name in (*install_pack.REQUIRED_DIRS, "tests"):
            (self.source / name).mkdir()
        for name in ("install_pack.py", "sync_runtime.py", "validate_framework.py"):
            (self.source / "scripts" / name).write_text("# fixture\n", encoding="utf-8")
        (self.source / "docs" / "guide.md").write_text("guide", encoding="utf-8")
        (self.source / "prompts" / "task.md").write_text("prompt", encoding="utf-8")
        (self.source / "tests" / "Scorecard.md").write_text("scorecard", encoding="utf-8")
        self.root = self.base / "skills"
        self.pack = self.root / install_pack.PACK_NAME
        self.addCleanup(patch.stopall)
        patch.object(install_pack, "REPO_ROOT", self.source).start()
        self.out, self.err = io.StringIO(), io.StringIO()
        self.stdout = redirect_stdout(self.out)
        self.stderr = redirect_stderr(self.err)
        self.stdout.__enter__()
        self.stderr.__enter__()
        self.addCleanup(self.stdout.__exit__, None, None, None)
        self.addCleanup(self.stderr.__exit__, None, None, None)

    def install(self, **kwargs):
        return install_pack.install_pack(self.root, **kwargs)

    def snapshot(self):
        return {p.relative_to(self.pack).as_posix(): p.read_bytes()
                for p in self.pack.rglob("*") if p.is_file()}

    def write_manifest(self, data):
        (self.pack / install_pack.MANIFEST_FILE).write_text(json.dumps(data), encoding="utf-8")

    def read_manifest(self):
        return json.loads((self.pack / install_pack.MANIFEST_FILE).read_text(encoding="utf-8"))

    def symlink(self, link, target, *, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlinks unavailable: {exc}")

    def test_installed_skill_metadata_is_in_manifest_and_integrity_checked(self):
        self.install()
        skill = self.pack / "SKILL.md"
        manifest = self.read_manifest()
        self.assertEqual(manifest["files"]["SKILL.md"], hashlib.sha256(skill.read_bytes()).hexdigest())
        install_pack.validate_skill_metadata(skill.read_text(encoding="utf-8"))
        skill.write_text("# Missing metadata\n", encoding="utf-8")
        # Even self-consistent checksums cannot make malformed metadata valid.
        manifest["files"]["SKILL.md"] = hashlib.sha256(skill.read_bytes()).hexdigest()
        self.write_manifest(manifest)
        self.assertTrue(any("SKILL.md" in problem for problem in install_pack.verify_install(self.pack)))
        with patch.object(install_pack, "run_validate") as validate:
            self.assertEqual(install_pack.main(["--check", "--dest", str(self.root)]), 1)
        validate.assert_not_called()

    def test_invalid_generated_skill_refuses_before_replacing_pack(self):
        self.install()
        before = self.snapshot()
        with patch.object(install_pack, "skill_hint", return_value="# No metadata\n"):
            with self.assertRaisesRegex(SystemExit, "SKILL.md"):
                self.install(force=True)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(list(self.root.iterdir()), [self.pack])

    def test_invalid_generated_skill_dry_run_creates_nothing(self):
        with patch.object(install_pack, "skill_hint", return_value="# No metadata\n"):
            with self.assertRaisesRegex(SystemExit, "SKILL.md"):
                self.install(dry_run=True)
        self.assertFalse(self.root.exists())

    def test_identical_install_skips_copy_and_preserves_user_content(self):
        self.install()
        (self.pack / "user.txt").write_text("keep", encoding="utf-8")
        before = self.snapshot()
        with patch.object(install_pack.shutil, "copytree") as copytree:
            self.assertEqual(self.install(), self.pack)
        copytree.assert_not_called()
        self.assertEqual(before, self.snapshot())
        self.assertIn("Unchanged", self.out.getvalue())

    def test_modified_or_missing_shipped_file_refuses_without_writes(self):
        for missing in (False, True):
            with self.subTest(missing=missing):
                self.install(force=True)
                target = self.pack / "docs" / "guide.md"
                if missing:
                    target.unlink()
                else:
                    target.write_text("local edits", encoding="utf-8")
                before = self.snapshot()
                with self.assertRaisesRegex(SystemExit, "Refusing.*--force"):
                    self.install()
                self.assertEqual(before, self.snapshot())

    def test_added_changed_or_removed_source_file_requires_force(self):
        target = self.source / "docs" / "guide.md"
        for change in ("added", "changed", "removed"):
            with self.subTest(change=change):
                target.write_text("guide", encoding="utf-8")
                extra = self.source / "docs" / "new.md"
                extra.unlink(missing_ok=True)
                self.install(force=True)
                before = self.snapshot()
                if change == "added":
                    extra.write_text("new", encoding="utf-8")
                elif change == "changed":
                    target.write_text("updated", encoding="utf-8")
                else:
                    target.unlink()
                with self.assertRaisesRegex(SystemExit, "Refusing"):
                    self.install()
                self.assertEqual(before, self.snapshot())

    def test_missing_required_source_refuses_even_with_force(self):
        self.install()
        before = self.snapshot()
        (self.source / "CHATGPT.md").unlink()
        with self.assertRaisesRegex(SystemExit, "Missing required"):
            self.install(force=True)
        self.assertEqual(before, self.snapshot())

    def test_force_warns_and_replaces_all_contents(self):
        self.install()
        (self.pack / "user.txt").write_text("local", encoding="utf-8")
        (self.source / "CHATGPT.md").write_text("new", encoding="utf-8")
        self.install(force=True)
        self.assertFalse((self.pack / "user.txt").exists())
        self.assertEqual((self.pack / "CHATGPT.md").read_text(encoding="utf-8"), "new")
        self.assertIn("WARNING", self.err.getvalue())
        self.assertIn("user files", self.err.getvalue())
        self.assertEqual(install_pack.verify_install(self.pack), [])

    def test_dry_run_does_not_create_parent(self):
        self.assertEqual(self.install(dry_run=True), self.pack)
        self.assertFalse(self.root.exists())

    def test_dry_run_refuses_conflict_and_force_leaves_everything_unchanged(self):
        self.install()
        (self.pack / "CHATGPT.md").write_text("local", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaisesRegex(SystemExit, "Refusing"):
            self.install(dry_run=True)
        self.install(dry_run=True, force=True)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(list(self.root.iterdir()), [self.pack])

    def test_missing_or_corrupt_manifest_refuses_and_check_fails(self):
        for content in (None, "{broken", "[]", "{}"):
            with self.subTest(content=content):
                self.install(force=True)
                manifest = self.pack / install_pack.MANIFEST_FILE
                if content is None:
                    manifest.unlink()
                else:
                    manifest.write_text(content, encoding="utf-8")
                before = self.snapshot()
                self.assertTrue(install_pack.verify_install(self.pack))
                with self.assertRaisesRegex(SystemExit, "Refusing"):
                    self.install()
                with patch.object(install_pack, "run_validate") as validate:
                    self.assertEqual(install_pack.main(["--check", "--dest", str(self.root)]), 1)
                validate.assert_not_called()
                self.assertEqual(before, self.snapshot())

    def test_manifest_rejects_unsafe_paths_before_hashing(self):
        self.install()
        original = self.read_manifest()
        for name in ("../outside", "/absolute", "C:/absolute", r"docs\guide.md",
                     "docs/../outside", "./README.md", "docs//guide.md", "docs/", "",
                     "docs/CON", "docs/nul.txt", "docs/guide.", "docs/guide "):
            with self.subTest(name=name):
                data = dict(original, files=dict(original["files"]))
                data["files"][name] = "0" * 64
                self.write_manifest(data)
                with patch.object(install_pack, "_hash") as hash_file:
                    self.assertTrue(install_pack.verify_install(self.pack))
                hash_file.assert_not_called()

    def test_install_and_verify_do_not_use_deprecated_path_apis(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            self.install()
            self.assertEqual(install_pack.verify_install(self.pack), [])

    def test_manifest_rejects_invalid_checksums_and_missing_required_entries(self):
        self.install()
        original = self.read_manifest()
        for checksum in ("0" * 63, "G" * 64, None, 123):
            with self.subTest(checksum=checksum):
                data = dict(original, files=dict(original["files"]))
                data["files"]["README.md"] = checksum
                self.write_manifest(data)
                self.assertTrue(install_pack.verify_install(self.pack))
        data = dict(original, files=dict(original["files"]))
        del data["files"]["scripts/validate_framework.py"]
        self.write_manifest(data)
        self.assertTrue(install_pack.verify_install(self.pack))

    def test_destination_symlink_refused_even_with_force(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.root.mkdir()
        self.symlink(self.pack, outside, directory=True)
        for force in (False, True):
            with self.subTest(force=force), self.assertRaisesRegex(SystemExit, "Symlink|junction"):
                self.install(force=force)
        self.assertEqual(list(outside.iterdir()), [])

    def test_destination_parent_symlink_refused(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.symlink(self.root, outside, directory=True)
        with self.assertRaisesRegex(SystemExit, "Symlink|junction"):
            self.install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_source_root_symlink_refused(self):
        link = self.base / "linked-source"
        self.symlink(link, self.source, directory=True)
        with patch.object(install_pack, "REPO_ROOT", link):
            with self.assertRaisesRegex(SystemExit, "Symlink|junction"):
                self.install()
        self.assertFalse(self.root.exists())

    def test_source_file_and_nested_directory_symlinks_refused(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "secret.txt").write_text("secret", encoding="utf-8")
        for is_dir in (False, True):
            with self.subTest(directory=is_dir):
                link = self.source / "docs" / "link"
                self.symlink(link, outside if is_dir else outside / "secret.txt", directory=is_dir)
                try:
                    with self.assertRaisesRegex(SystemExit, "Symlink|junction"):
                        self.install()
                    self.assertFalse(self.root.exists())
                finally:
                    link.unlink()

    def test_reparse_point_attribute_is_rejected(self):
        original = Path.lstat
        def lstat(path, *args, **kwargs):
            if path == self.source / "docs":
                return SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400)
            return original(path, *args, **kwargs)
        with patch.object(Path, "lstat", lstat):
            with self.assertRaisesRegex(SystemExit, "junction"):
                self.install()
        self.assertFalse(self.root.exists())

    @unittest.skipUnless(os.name == "nt", "Actual junction creation requires Windows")
    def test_actual_windows_junction_destination_and_parent_are_refused(self):
        target = self.base / "junction target"
        target.mkdir()
        marker = target / "user.txt"
        marker.write_text("preserve target", encoding="utf-8")
        for location in ("parent", "destination"):
            with self.subTest(location=location):
                root = self.base / f"junction {location} skills"
                if location == "destination":
                    root.mkdir()
                link = root if location == "parent" else root / install_pack.PACK_NAME
                proc = subprocess.run(
                    ["cmd", "/c", "mklink", "/J", str(link), str(target)],
                    capture_output=True, text=True, errors="replace",
                )
                if proc.returncode != 0:
                    self.skipTest(f"Cannot create Windows junction: {proc.stdout} {proc.stderr}")
                try:
                    for force in (False, True):
                        with self.subTest(force=force):
                            with self.assertRaisesRegex(SystemExit, "Symlink|junction"):
                                install_pack.install_pack(root, force=force)
                    self.assertEqual(marker.read_text(encoding="utf-8"), "preserve target")
                    self.assertEqual(list(target.iterdir()), [marker])
                finally:
                    # Remove only the junction entry, never recurse into its target.
                    os.rmdir(link)

    def test_overlap_rejected_in_both_directions(self):
        with self.assertRaisesRegex(SystemExit, "overlap"):
            install_pack.install_pack(self.source / "skills")
        self.assertFalse((self.source / "skills").exists())
        outer = self.base / "outer"
        nested_source = outer / install_pack.PACK_NAME / "source"
        nested_source.mkdir(parents=True)
        with patch.object(install_pack, "REPO_ROOT", nested_source):
            with self.assertRaisesRegex(SystemExit, "overlap"):
                install_pack.install_pack(outer, force=True)
        self.assertTrue(nested_source.is_dir())

    def test_copy_failure_keeps_old_pack_and_cleans_staging(self):
        self.install()
        before = self.snapshot()
        with patch.object(install_pack.shutil, "copytree", side_effect=OSError("copy failed")):
            with self.assertRaisesRegex(SystemExit, "copy failed"):
                self.install(force=True)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(list(self.root.iterdir()), [self.pack])

    def test_publish_rename_failure_restores_old_pack(self):
        self.install()
        before = self.snapshot()
        original = Path.rename
        def rename(path, target):
            if path.name == "new" and Path(target) == self.pack:
                raise OSError("publish failed")
            return original(path, target)
        with patch.object(Path, "rename", rename):
            with self.assertRaisesRegex(SystemExit, "publish failed"):
                self.install(force=True)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(list(self.root.iterdir()), [self.pack])

    def test_failed_publish_and_rollback_retains_recoverable_old_pack(self):
        self.install()
        (self.pack / "user.txt").write_text("irreplaceable", encoding="utf-8")
        before = self.snapshot()
        original = Path.rename
        def rename(path, target):
            if path.name in {"new", "old"} and Path(target) == self.pack:
                raise OSError("rename blocked")
            return original(path, target)
        with patch.object(Path, "rename", rename):
            with self.assertRaisesRegex(SystemExit, "rename blocked"):
                self.install(force=True)
        self.assertFalse(self.pack.exists())
        recoveries = list(self.root.glob(".chatgpt-transfer-*/old"))
        self.assertEqual(len(recoveries), 1)
        backup = recoveries[0]
        recovered = {p.relative_to(backup).as_posix(): p.read_bytes()
                     for p in backup.rglob("*") if p.is_file()}
        self.assertEqual(before, recovered)
        self.assertIn(str(backup), self.err.getvalue())
        self.assertIn("Recovery required", self.err.getvalue())

    def test_corrupt_staged_copy_never_replaces_old_pack(self):
        self.install()
        before = self.snapshot()
        copy2 = install_pack.shutil.copy2
        def corrupt_copy(source, target, *args, **kwargs):
            result = copy2(source, target, *args, **kwargs)
            if Path(source).name == "CHATGPT.md":
                Path(target).write_text("corrupted during copy", encoding="utf-8")
            return result
        with patch.object(install_pack.shutil, "copy2", corrupt_copy):
            with self.assertRaisesRegex(SystemExit, "Staged content differs"):
                self.install(force=True)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(list(self.root.iterdir()), [self.pack])

    def test_unexpected_file_in_staged_copy_preserves_old_pack(self):
        self.install()
        before = self.snapshot()
        copytree = install_pack.shutil.copytree
        def inject_extra(source, target, *args, **kwargs):
            result = copytree(source, target, *args, **kwargs)
            if Path(source).name == "docs":
                (Path(target) / "unexpected.md").write_text("late file", encoding="utf-8")
            return result
        with patch.object(install_pack.shutil, "copytree", inject_extra):
            with self.assertRaisesRegex(SystemExit, "Staged content differs"):
                self.install(force=True)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(list(self.root.iterdir()), [self.pack])

    def test_boolean_manifest_version_is_invalid(self):
        self.install()
        data = self.read_manifest()
        data["version"] = True
        self.write_manifest(data)
        self.assertTrue(install_pack.verify_install(self.pack))

    def test_switching_test_selection_requires_force_in_both_directions(self):
        self.install()
        for with_tests in (True, False):
            with self.subTest(with_tests=with_tests):
                before = self.snapshot()
                with self.assertRaisesRegex(SystemExit, "Refusing"):
                    self.install(with_tests=with_tests)
                self.assertEqual(before, self.snapshot())
                self.install(with_tests=with_tests, force=True)
                self.assertEqual((self.pack / "tests").exists(), with_tests)
                self.assertEqual(install_pack.verify_install(self.pack), [])

    def test_check_tampering_never_executes_validation(self):
        self.install(with_tests=True)
        (self.pack / "scripts" / "validate_framework.py").write_text("raise RuntimeError('tampered')", encoding="utf-8")
        with patch.object(install_pack.subprocess, "run") as run:
            self.assertEqual(install_pack.main(["--check", "--dest", str(self.root)]), 1)
        run.assert_not_called()
        self.assertIn("modified file: scripts/validate_framework.py", self.out.getvalue())

    def test_check_missing_file_never_executes_validation(self):
        self.install(with_tests=True)
        (self.pack / "docs" / "guide.md").unlink()
        with patch.object(install_pack.subprocess, "run") as run:
            self.assertEqual(install_pack.main(["--check", "--dest", str(self.root)]), 1)
        run.assert_not_called()

    def test_check_symlinked_shipped_file_fails_without_execution(self):
        self.install(with_tests=True)
        shipped = self.pack / "README.md"
        shipped.unlink()
        self.symlink(shipped, self.source / "README.md")
        with patch.object(install_pack.subprocess, "run") as run:
            self.assertEqual(install_pack.main(["--check", "--dest", str(self.root)]), 1)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
