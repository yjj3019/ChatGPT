#!/usr/bin/env python3
"""Validate the ChatGPT transfer-pack structure."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "CHATGPT.md"
PATH_RE = re.compile(r"`((?:(?:docs|prompts|tests)/[^`]+|(?:CHATGPT|AGENTS|README))\.md)`")
TEST_RE = re.compile(r"^# Golden Test (\d{3}):", re.MULTILINE)
REQUIRED = [
    "CHATGPT.md",
    "docs/chatgpt-5.5-project-instructions.md",
    "docs/chatgpt-operational-integrity-rules.md",
    "docs/chatgpt-coding-rules.md",
]


def main() -> int:
    errors = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    for source in [*ROOT.glob("*.md"), *(ROOT / "docs").glob("*.md"), *(ROOT / "prompts").glob("*.md"), *(ROOT / "tests").glob("*.md")]:
        text = source.read_text(encoding="utf-8-sig")
        for line_number, line in enumerate(text.splitlines(), 1):
            for rel in PATH_RE.findall(line):
                exists = any(ROOT.glob(rel)) if any(char in rel for char in "*?[") else (ROOT / rel).is_file()
                if not exists:
                    errors.append(f"{source.relative_to(ROOT)}:{line_number} references missing file: {rel}")

    seen = {}
    for path in sorted((ROOT / "tests").glob("GoldenTest-*.md")):
        match = TEST_RE.search(path.read_text(encoding="utf-8-sig"))
        if not match:
            errors.append(f"missing Golden Test ID header: {path.relative_to(ROOT)}")
            continue
        test_id = match.group(1)
        if path.stem != f"GoldenTest-{test_id}":
            errors.append(f"Golden Test filename/header mismatch: {path.relative_to(ROOT)}")
        if test_id in seen:
            errors.append(f"duplicate Golden Test ID {test_id}: {seen[test_id]}, {path.relative_to(ROOT)}")
        seen[test_id] = path.relative_to(ROOT)

    runtime = ENTRY.read_text(encoding="utf-8") if ENTRY.is_file() else ""
    for term in ["Fable5 Enhanced", "Fable5 Distilled Patterns"]:
        if term in runtime:
            errors.append(f"prohibited model-specific Runtime term in CHATGPT.md: {term}")

    if errors:
        print("ChatGPT transfer-pack validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ChatGPT transfer-pack validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
