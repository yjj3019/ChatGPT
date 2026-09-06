#!/usr/bin/env python3
"""Synchronize the generated Core Runtime block in CHATGPT.md."""
import argparse
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without writing files")
    args = parser.parse_args()
    try:
        current = ENTRY.read_text(encoding="utf-8-sig")
        expected = synchronized_text(current)
        if args.check:
            if current != expected:
                print("CHATGPT.md is out of sync; run python scripts/sync_runtime.py")
                return 1
            print("Generated runtime is in sync.")
            return 0
        encoded = expected.encode("utf-8")
        if ENTRY.read_bytes() != encoded:
            ENTRY.write_bytes(encoded)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Runtime synchronization failed: {error}")
        return 1
    print("Synchronized CHATGPT.md inlined Core Runtime.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
