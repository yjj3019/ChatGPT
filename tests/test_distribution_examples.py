"""Check model-inheriting examples without reading a recipient's configuration."""
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "docs/examples/codex-standard-agents"


class DistributionExamplesTest(unittest.TestCase):
    def test_standard_roles_do_not_override_host_settings(self):
        for role in ("explorer", "runner", "reviewer"):
            with self.subTest(role=role):
                config = tomllib.loads((EXAMPLES / f"pack-{role}.toml").read_text(encoding="utf-8-sig"))
                self.assertEqual(set(config), {"name", "description", "developer_instructions"})
                self.assertEqual(config["name"], f"pack_{role}")
                for value in config.values():
                    self.assertIsInstance(value, str)
                    self.assertTrue(value.strip())

    def test_standard_policy_has_one_ordered_marker_pair(self):
        text = (EXAMPLES / "AGENTS.snippet.md").read_text(encoding="utf-8-sig")
        begin = "<!-- BEGIN TRANSFER PACK STANDARD DELEGATION -->"
        end = "<!-- END TRANSFER PACK STANDARD DELEGATION -->"
        self.assertEqual(text.count(begin), 1)
        self.assertEqual(text.count(end), 1)
        self.assertLess(text.index(begin), text.index(end))


if __name__ == "__main__":
    unittest.main()
