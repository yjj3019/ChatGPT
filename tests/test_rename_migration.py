"""Keep old skill installations and user files intact during the ID transition."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rename_installer", ROOT / "scripts/install_pack.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
NEW_ID = "taskforge-for-chatgpt"


class RenameMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def old_skill(self, name):
        old = self.root / name
        old.mkdir()
        content = installer.skill_hint().replace(
            "name: " + json.dumps(installer.PACK_NAME), "name: " + json.dumps(name), 1)
        (old / "SKILL.md").write_text(content, encoding="utf-8")
        (old / "USER_NOTES.txt").write_bytes(b"keep these exact user bytes\x00")
        return old

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.root.rglob("*") if p.is_file()}

    def test_old_skill_blocks_before_writes_even_with_force_or_dry_run(self):
        for name in installer.LEGACY_PACK_NAMES:
            with self.subTest(name=name):
                self.old_skill(name)
                before = self.snapshot()
                for options in ({}, {"force": True}, {"dry_run": True}):
                    with patch.object(installer, "PACK_NAME", NEW_ID), patch.object(
                            installer, "_source_files") as source:
                        with self.assertRaisesRegex(SystemExit, "Legacy pack detected"):
                            installer.install_pack(self.root, **options)
                        source.assert_not_called()
                    self.assertEqual(self.snapshot(), before)
                    self.assertFalse((self.root / NEW_ID).exists())

    def test_unrelated_old_named_directory_is_not_an_installation(self):
        for name in installer.LEGACY_PACK_NAMES:
            directory = self.root / name
            directory.mkdir()
            (directory / "USER_NOTES.txt").write_text("unrelated", encoding="utf-8")
        with patch.object(installer, "PACK_NAME", NEW_ID):
            installer._reject_legacy_install(self.root)

    def test_different_skill_in_old_named_directory_is_not_blocked(self):
        old = self.root / "taskforge"
        old.mkdir()
        (old / "SKILL.md").write_text(
            '---\nname: "unrelated"\ndescription: "Another skill"\n---\n# Other\n',
            encoding="utf-8")
        with patch.object(installer, "PACK_NAME", NEW_ID):
            installer._reject_legacy_install(self.root)

    def test_corrupt_legacy_manifest_fails_closed_without_writes(self):
        old = self.root / "chatgpt-transfer"
        old.mkdir()
        (old / installer.LEGACY_MANIFEST_FILE).write_text("{broken", encoding="utf-8")
        before = self.snapshot()
        with patch.object(installer, "PACK_NAME", NEW_ID):
            with self.assertRaises(SystemExit):
                installer.install_pack(self.root)
        self.assertEqual(self.snapshot(), before)

    def test_new_and_old_manifests_cannot_both_be_accepted(self):
        old = self.root / "pack"
        old.mkdir()
        new_manifest = ".taskforge-for-chatgpt-manifest.json"
        (old / new_manifest).write_text("{}", encoding="utf-8")
        (old / installer.LEGACY_MANIFEST_FILE).write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Conflicting old and new"):
            installer._read_manifest(old, manifest_file=new_manifest)

    def test_auto_preflights_all_targets_before_installing_any(self):
        first, second = self.root / "first", self.root / "second"
        second.mkdir()
        old = second / "chatgpt-transfer"
        old.mkdir()
        (old / "SKILL.md").write_text(
            '---\nname: "chatgpt-transfer"\ndescription: "Old pack"\n---\n# Old\n',
            encoding="utf-8")
        before = self.snapshot()
        with patch.object(installer, "PACK_NAME", NEW_ID), patch.object(
                installer, "detect_targets", return_value=[("first", first), ("second", second)]), patch.object(
                installer, "install_pack") as install:
            with self.assertRaisesRegex(SystemExit, "Legacy pack detected"):
                installer.main(["--auto"])
            install.assert_not_called()
        self.assertFalse(first.exists())
        self.assertEqual(self.snapshot(), before)

    def test_legacy_manifest_without_skill_is_still_detected(self):
        old = self.root / "chatgpt-transfer"
        old.mkdir()
        required = (*installer.REQUIRED_FILES, *installer.GENERATED_FILES,
                    "scripts/install_pack.py", "scripts/sync_runtime.py", "scripts/validate_framework.py")
        manifest = {"version": 1, "with_tests": False, "files": {name: "0" * 64 for name in required}}
        (old / installer.LEGACY_MANIFEST_FILE).write_text(json.dumps(manifest), encoding="utf-8")
        with patch.object(installer, "PACK_NAME", NEW_ID):
            with self.assertRaisesRegex(ValueError, "Legacy pack detected"):
                installer._reject_legacy_install(self.root)

    def test_edited_legacy_metadata_still_blocks_without_writes(self):
        old = self.old_skill("taskforge")
        for identity in ('"taskforge"', "'taskforge'", "taskforge # user comment"):
            with self.subTest(identity=identity):
                (old / "SKILL.md").write_text(
                    '---\ndescription: |\n  Edited description\nname: ' + identity
                    + '\nuser_field: preserved\n---\n# Old\n', encoding="utf-8")
                before = self.snapshot()
                with self.assertRaisesRegex(SystemExit, "Legacy pack detected"):
                    installer.install_pack(self.root, force=True)
                self.assertEqual(self.snapshot(), before)
                self.assertFalse((self.root / NEW_ID).exists())

    def test_unsafe_legacy_skill_path_is_not_treated_as_unrelated(self):
        old = self.old_skill("taskforge")
        safe = installer._safe_path

        def reject_entry(path):
            if path == old / "SKILL.md":
                raise ValueError("unsafe legacy skill path")
            safe(path)

        with patch.object(installer, "PACK_NAME", NEW_ID), patch.object(
                installer, "_safe_path", side_effect=reject_entry):
            with self.assertRaisesRegex(ValueError, "unsafe legacy skill path"):
                installer._reject_legacy_install(self.root)


if __name__ == "__main__":
    unittest.main()
