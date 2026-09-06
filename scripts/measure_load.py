#!/usr/bin/env python3
"""Estimate required context load (bytes and rough tokens) per Task Loading Map row.

Reports full-file upper bounds and, when feasible, section-scoped estimates for
multi-section packs (engineering-task-rules, domain-packs).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "CHATGPT.md"
PATH_RE = re.compile(r"`((?:docs|prompts)/[^`]+\.md)`")

HEAVY_OPTIONAL = {
    "docs/chatgpt-transfer-instructions.md",
    "docs/chatgpt-5.5-all-in-one-instructions.md",
    "docs/fable5-pattern-bank-for-chatgpt.md",
}

# Representative section titles for section-aware estimates (must match ## headers).
ENGINEERING_SECTION_BY_TASK = {
    "Architecture review": "Architecture Review",
    "Root cause analysis": "Root Cause Analysis",
    "Technical research": "Technical Research",
    "Operations manual or SOP": "Operations Manual or SOP",
    "Prompt review": "Prompt Review",
    "Security review": "Security Review",
}

# Sample domain sections shown in the section-aware appendix.
SAMPLE_DOMAIN_SECTIONS = ("RHEL", "Kubernetes", "OpenShift")


def file_bytes(rel: str) -> int:
    path = ROOT / rel
    if not path.is_file():
        return 0
    return path.stat().st_size


def rough_tokens(nbytes: int) -> int:
    return max(0, (nbytes + 3) // 4)


def parse_sections(rel: str) -> dict[str, int]:
    """Return {section_title: byte_size} for each ## section (incl. leading intro before first ##)."""
    path = ROOT / rel
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8-sig")
    parts = re.split(r"(?m)^## ", text)
    sizes: dict[str, int] = {}
    if parts:
        intro = parts[0]
        sizes["__intro__"] = len(intro.encode("utf-8"))
    for chunk in parts[1:]:
        line, _, body = chunk.partition("\n")
        title = line.strip()
        # Section content = "## " + title line + rest until next section
        section_text = "## " + chunk
        sizes[title] = len(section_text.encode("utf-8"))
    return sizes


def section_load_bytes(rel: str, section_title: str, *, include_intro: bool = True) -> int:
    sizes = parse_sections(rel)
    if not sizes:
        return file_bytes(rel)
    total = sizes.get(section_title, 0)
    if include_intro:
        total += sizes.get("__intro__", 0)
    # Engineering tasks also commonly need Execution Shape for multi-context guidance
    if rel.endswith("chatgpt-engineering-task-rules.md") and section_title != "Execution Shape":
        total += sizes.get("Execution Shape", 0)
    return total


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
        return [
            "docs/chatgpt-5.5-project-instructions.md",
            "docs/chatgpt-operational-integrity-rules.md",
        ]
    paths = PATH_RE.findall(required_cell)
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
        notes: list[str] = []
        if any("domain-packs" in p for p in paths):
            notes.append("domain: matching section only; full-file upper bound")
        if any("engineering-task-rules" in p for p in paths):
            notes.append("engineering: matching section only; full-file upper bound")
        note = (" [" + "; ".join(notes) + "]") if notes else ""
        print(f"{task:<52} {nbytes:>8} {rough_tokens(nbytes):>8}  {', '.join(label_paths)}{note}")

    print()
    print("Section-aware estimates (intro + matching section[+ Execution Shape for engineering]):")
    eng_rel = "docs/chatgpt-engineering-task-rules.md"
    for task, section in ENGINEERING_SECTION_BY_TASK.items():
        n = core_nbytes + section_load_bytes(eng_rel, section)
        print(f"  {task:<50} {n:>8} bytes (~{rough_tokens(n)} tokens)  section={section!r}")

    dom_rel = "docs/chatgpt-domain-packs.md"
    for section in SAMPLE_DOMAIN_SECTIONS:
        n = core_nbytes + section_load_bytes(dom_rel, section)
        print(f"  Domain-only ({section}):{' ' * (38 - len(section))} {n:>8} bytes (~{rough_tokens(n)} tokens)")

    # Combined sample: RHEL RCA
    rca = section_load_bytes(eng_rel, "Root Cause Analysis")
    rhel = section_load_bytes(dom_rel, "RHEL")
    combined = core_nbytes + rca + rhel
    print(
        f"  RHEL RCA (eng RCA section + RHEL section):     {combined:>8} bytes "
        f"(~{rough_tokens(combined)} tokens)  [vs full-file upper bound "
        f"{core_nbytes + file_bytes(eng_rel) + file_bytes(dom_rel)}]"
    )

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
