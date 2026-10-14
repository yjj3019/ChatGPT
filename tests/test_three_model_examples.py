"""Validate the opt-in preset's public TOML contract without invoking a host."""
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "docs/examples/codex-three-models"


class ThreeModelExamplesTest(unittest.TestCase):
    def test_role_examples_have_only_supported_fields_and_selected_settings(self):
        cases = {
            "luna-explorer.toml": ("luna_explorer", "gpt-6-luna", "high"),
            "luna-runner.toml": ("luna_runner", "gpt-6-luna", "low"),
            "astra-reviewer.toml": ("astra_reviewer", "gpt-6-astra", "low"),
        }
        for filename, expected in cases.items():
            with self.subTest(filename=filename):
                config = tomllib.loads((EXAMPLES / filename).read_text(encoding="utf-8-sig"))
                self.assertEqual(set(config), {
                    "name", "description", "model", "model_reasoning_effort", "developer_instructions",
                })
                self.assertEqual(tuple(config[key] for key in (
                    "name", "model", "model_reasoning_effort",
                )), expected)
                self.assertIsInstance(config["description"], str)
                self.assertTrue(config["description"].strip())
                self.assertIsInstance(config["developer_instructions"], str)
                self.assertTrue(config["developer_instructions"].strip())

    def test_optional_policy_has_one_ordered_marker_pair(self):
        policy = (EXAMPLES / "AGENTS.snippet.md").read_text(encoding="utf-8-sig")
        begin = "<!-- BEGIN CODEX THREE MODEL DELEGATION -->"
        end = "<!-- END CODEX THREE MODEL DELEGATION -->"
        self.assertEqual(policy.count(begin), 1)
        self.assertEqual(policy.count(end), 1)
        self.assertLess(policy.index(begin), policy.index(end))


if __name__ == "__main__":
    unittest.main()
