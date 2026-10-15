"""Validate the native marketplace package without changing user configuration."""
import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipIf((ROOT / ".chatgpt-transfer-manifest.json").is_file(),
                 "Native marketplace checks apply to the repository, not legacy skill copies")
class PluginDistributionTests(unittest.TestCase):
    def test_marketplace_resolves_complete_plugin_inside_repository(self):
        catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["name"], "yjj3019")
        self.assertEqual(len(catalog["plugins"]), 1)
        entry = catalog["plugins"][0]
        self.assertEqual(entry["source"]["source"], "local")
        self.assertTrue(entry["source"]["path"].startswith("./"))
        plugin_root = (ROOT / entry["source"]["path"]).resolve()
        self.assertTrue(plugin_root.is_relative_to(ROOT.resolve()))
        manifest = json.loads((plugin_root / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "taskforge")
        self.assertEqual(manifest["name"], entry["name"])
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(manifest["license"], "MIT")
        self.assertTrue((plugin_root / "LICENSE").is_file())
        self.assertEqual(entry["policy"], {"installation": "AVAILABLE", "authentication": "ON_INSTALL"})
        self.assertEqual(entry["category"], manifest["extensions"]["com.openai"]["interface"]["category"])

    def test_skill_metadata_and_references_resolve_from_installed_layout(self):
        skill = ROOT / "skills/taskforge/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        spec = importlib.util.spec_from_file_location("plugin_installer", ROOT / "scripts/install_pack.py")
        installer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(installer)
        installer.validate_skill_metadata(text, expected_name="taskforge")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            path = (skill.parent / target).resolve()
            self.assertTrue(path.is_relative_to(ROOT.resolve()), target)
            self.assertTrue(path.is_file(), target)
        self.assertEqual((skill.parent / "../..").resolve(), ROOT.resolve())

    def test_plugin_has_no_configuration_or_execution_side_effects(self):
        manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["extensions"]["com.openai"]), {"interface"})
        for relative in ("mcp.json", ".mcp.json", ".app.json", "hooks/hooks.json", ".codex/config.toml"):
            self.assertFalse((ROOT / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
