#!/usr/bin/env python3
"""Estimate required context load (bytes and rough tokens) per Task Loading Map row."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "CHATGPT.md"
PATH_RE = re.compile(r"`((?:docs|prompts)/[^`]+\.md)`")

# Files that are never part of required Autoload for normal tasks (optional / one-shot only).
HEAVY_OPTIONAL = {
    "docs/chatgpt-transfer-instructions.md",
    "docs/chatgpt-5.5-all-in-one-instructions.md",
    "docs/fable5-pattern-bank-for-chatgpt.md",
}


def file_bytes(rel: str) -> int:
    path = ROOT / rel
    if not path.is_file():
        return 0
    return path.stat().st_size


def rough_tokens(nbytes: int) -> int:
    return max(0, (nbytes + 3) // 4)


def parse_task_map() -> list[tuple[str, str, str]]:
    text = ENTRY.read_text(encoding="utf-8-sig")
    if "## Task Loading Map" not in text:
        raise SystemExit("CHATGPT.md: missing Task Loading Map")
    table = text.split("## Task Loading Map", 1)[1].split("\n## ", 1)[0]
    rows: list[tuple[str, str, str]] = []
    for line in table.splitlines():
        if not line.startswith("|") or "---" in line or "Task Type" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 3:
            continue
        rows.append((cells[0], cells[1], cells[2]))
    return rows


def required_paths(required_cell: str) -> list[str]:
    if "Core Runtime only" in required_cell:
        # Inlined Core is already in CHATGPT.md; count the two canonical sources once.
        return [
            "docs/chatgpt-5.5-project-instructions.md",
            "docs/chatgpt-operational-integrity-rules.md",
        ]
    paths = PATH_RE.findall(required_cell)
    # Deduplicate while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def main() -> int:
    core_paths = [
        "docs/chatgpt-5.5-project-instructions.md",
        "docs/chatgpt-operational-integrity-rules.md",
    ]
    # For non-Core-only tasks, Core is always applied (inlined), so include Core bytes.
    core_nbytes = sum(file_bytes(p) for p in core_paths)

    print("ChatGPT transfer-pack load estimate (required files; tokens ≈ bytes/4)")
    print(f"{'Task Type':<52} {'bytes':>8} {'~tokens':>8}  files")
    print("-" * 100)

    for task, required_cell, _optional in parse_task_map():
        paths = required_paths(required_cell)
        if "Core Runtime only" in required_cell:
            nbytes = core_nbytes
            label_paths = ["Core Runtime (canonical docs)"]
        else:
            nbytes = core_nbytes + sum(file_bytes(p) for p in paths)
            label_paths = ["Core"] + paths
        # Note domain pack "matching section only" — full file size is an upper bound.
        note = ""
        if any("domain-packs" in p for p in paths):
            note = " [domain: matching section only; full-file size is upper bound]"
        print(f"{task:<52} {nbytes:>8} {rough_tokens(nbytes):>8}  {', '.join(label_paths)}{note}")

    print()
    print("Heavy optional / one-shot (do not autoload):")
    for rel in sorted(HEAVY_OPTIONAL):
        n = file_bytes(rel)
        print(f"  {rel}: {n} bytes (~{rough_tokens(n)} tokens)")

    entry_n = ENTRY.stat().st_size if ENTRY.is_file() else 0
    agents = ROOT / "AGENTS.md"
    agents_n = agents.stat().st_size if agents.is_file() else 0
    print()
    print(f"Entry sizes: CHATGPT.md={entry_n} bytes, AGENTS.md={agents_n} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
