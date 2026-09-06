#!/usr/bin/env python3
"""Synchronize the generated Core Runtime block in CHATGPT.md."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "CHATGPT.md"
CORE_FILES = [
    ROOT / "docs" / "chatgpt-5.5-project-instructions.md",
    ROOT / "docs" / "chatgpt-operational-integrity-rules.md",
]
BEGIN = "<!-- BEGIN INLINED CORE RUNTIME (generated from docs/ — do not edit here) -->"
END = "<!-- END INLINED CORE RUNTIME -->"


def normalize(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()).rstrip()


def rendered_runtime() -> str:
    return "\n\n".join(normalize(path.read_text(encoding="utf-8-sig")) for path in CORE_FILES)


def synchronized_text(text: str) -> str:
    if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(BEGIN) >= text.index(END):
        raise ValueError("CHATGPT.md must contain exactly one ordered inlined Core Runtime marker pair")
    before, remainder = text.split(BEGIN, 1)
    _, after = remainder.split(END, 1)
    return f"{before}{BEGIN}\n{rendered_runtime()}\n{END}{after}"


def main() -> int:
    ENTRY.write_text(synchronized_text(ENTRY.read_text(encoding="utf-8-sig")), encoding="utf-8")
    print("Synchronized CHATGPT.md inlined Core Runtime.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
