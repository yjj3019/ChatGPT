"""Static contracts for optional live trials; never invoke Codex or a model."""
import json
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/evals/skill-invocation-cases.json"


class SkillInvocationCasesTests(unittest.TestCase):
    def test_cases_are_complete_and_targets_stay_inside_pack(self):
        data = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertEqual(set(data), {"version", "skill", "cases"})
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["skill"], "chatgpt-transfer")
        categories = {name: 0 for name in ("explicit", "implicit", "contextual", "negative")}
        identifiers = set()
        for case in data["cases"]:
            with self.subTest(case=case.get("id")):
                self.assertEqual(set(case), {"id", "category", "prompt", "expected_invocation", "expected_guides"})
                self.assertIsInstance(case["id"], str)
                self.assertTrue(case["id"].strip())
                self.assertNotIn(case["id"], identifiers)
                identifiers.add(case["id"])
                self.assertIn(case["category"], categories)
                categories[case["category"]] += 1
                self.assertIsInstance(case["prompt"], str)
                self.assertTrue(case["prompt"].strip())
                self.assertIs(type(case["expected_invocation"]), bool)
                self.assertEqual(case["expected_invocation"], case["category"] != "negative")
                self.assertIsInstance(case["expected_guides"], list)
                if case["category"] == "explicit":
                    self.assertIn("$chatgpt-transfer", case["prompt"])
                elif case["category"] in {"implicit", "contextual"}:
                    self.assertNotIn("$chatgpt-transfer", case["prompt"])
                if not case["expected_invocation"]:
                    self.assertEqual(case["expected_guides"], [])
                for guide in case["expected_guides"]:
                    self.assertIsInstance(guide, str)
                    path = PurePosixPath(guide)
                    self.assertNotIn("\\", guide)
                    self.assertFalse(path.is_absolute())
                    self.assertNotIn("..", path.parts)
                    self.assertEqual(path.parts[0], "docs")
                    self.assertEqual(path.suffix, ".md")
                    self.assertTrue((ROOT / guide).is_file(), guide)
        self.assertEqual(categories, dict.fromkeys(categories, 2))

    def test_simulation_policy_preserves_host_selection(self):
        text = (ROOT / "tests/Scorecard.md").read_text(encoding="utf-8")
        protocol = text.split("## Simulation Protocol", 1)[1].split("## Skill Invocation Trials", 1)[0]
        self.assertIn("preservation of the host-selected model/effort", protocol)
        self.assertIn("justified, supported, authorized change", protocol)
        self.assertNotIn("expected model tier", protocol)
        self.assertNotIn("weak-model escalation", protocol)
        self.assertIn("(evals/README.md)", text)


if __name__ == "__main__":
    unittest.main()
