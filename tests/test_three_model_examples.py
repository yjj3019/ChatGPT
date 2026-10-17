"""Validate session-policy packaging and role TOML without invoking a host."""
import tomllib
import re
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
            "notion-recorder.toml": ("notion-recorder", "gpt-6-luna", "low"),
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

    def test_native_entry_links_complete_session_policy(self):
        skill = (ROOT / "skills/taskforge/SKILL.md").read_text(encoding="utf-8-sig")
        guide = (ROOT / "docs/codex-three-model-setup.md").read_text(encoding="utf-8-sig")
        self.assertIn("../../docs/codex-three-model-setup.md#session-policy", skill)
        section = guide.split("## Session Policy\n", 1)[1].split("\n## ", 1)[0]
        for event in (
            "New conversation applying TaskForge", "including Sol",
            "compaction", "resuming the same conversation",
            "Explicit request to re-enable", "first request",
        ):
            self.assertIn(event, section)
        for limitation in (
            "not a persisted setting", "active model slug alone",
            "cannot reliably intercept", "does not control app restart",
            "does not change the running main model", "Do not silently install roles",
        ):
            self.assertIn(limitation, section)
        self.assertIn("DEFAULT preserves the current main model and reasoning effort", section)
        for role in ("pack_explorer", "pack_runner", "pack_reviewer"):
            self.assertIn(role, section)
        self.assertNotRegex(section, r"gpt-[a-zA-Z0-9.-]+")
        self.assertIn("explicit preset opt-in", section)
        self.assertIn("Return to DEFAULT; this does not select the fixed-model preset", section)
        self.assertIn("do not carry suspension or the fixed-model opt-in", section)
        self.assertIn("unless a separately approved host-wide PRESET policy applies", skill)
        self.assertIn("A separately approved host-wide preset policy may request PRESET", section)

    def test_optional_policy_has_one_ordered_marker_pair(self):
        policy = (EXAMPLES / "AGENTS.snippet.md").read_text(encoding="utf-8-sig")
        begin = "<!-- BEGIN CODEX THREE MODEL DELEGATION -->"
        end = "<!-- END CODEX THREE MODEL DELEGATION -->"
        self.assertEqual(policy.count(begin), 1)
        self.assertEqual(policy.count(end), 1)
        self.assertLess(policy.index(begin), policy.index(end))

    def test_automatic_policy_has_distinct_markers_and_preserves_manual_override(self):
        policy = (EXAMPLES / "AGENTS.auto.snippet.md").read_text(encoding="utf-8")
        begin = "<!-- BEGIN TASKFORGE AUTOMATIC THREE MODEL -->"
        end = "<!-- END TASKFORGE AUTOMATIC THREE MODEL -->"
        self.assertEqual(policy.count(begin), 1)
        self.assertEqual(policy.count(end), 1)
        self.assertLess(policy.index(begin), policy.index(end))
        self.assertNotIn("BEGIN CODEX THREE MODEL DELEGATION", policy)
        for filename in ("luna-explorer.toml", "luna-runner.toml", "astra-reviewer.toml"):
            role = tomllib.loads((EXAMPLES / filename).read_text(encoding="utf-8"))
            self.assertIn(role["name"], policy)
        self.assertIn("이 대화에서는 선택한 모델만 사용해", policy)
        self.assertIn("스킬 재호출", policy)
        guide = (ROOT / "docs/codex-three-model-setup.md").read_text(encoding="utf-8")
        self.assertIn("Choose one; do not append both", guide)

    def test_recorder_has_no_private_target_and_keeps_write_boundaries(self):
        role = tomllib.loads((EXAMPLES / "notion-recorder.toml").read_text(encoding="utf-8"))
        instructions = role["developer_instructions"]
        for field in ("page_url", "title", "type", "summary", "files", "result", "next"):
            self.assertIn(field, instructions)
        for boundary in ("dry-run", "저장 승인", "재조회", "맹목적으로 재시도하지", "원자성", "blocked"):
            self.assertIn(boundary, instructions)
        for path in (EXAMPLES / "notion-recorder.toml", EXAMPLES / "AGENTS.auto.snippet.md",
                     ROOT / "docs/codex-notion-recording.md", ROOT / "docs/host-verification-2026-10-16.md"):
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(re.search(r"[A-Za-z]:[\\/](?:Users|AI-Codding)[\\/]", text))
                self.assertIsNone(re.search(r"https?://(?:www\.)?(?:notion\.so|app\.notion\.com)/", text))


if __name__ == "__main__":
    unittest.main()
