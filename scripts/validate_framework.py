#!/usr/bin/env python3
"""Validate the ChatGPT transfer-pack structure and context-budget gates."""
import re
import sys
from pathlib import Path

from sync_runtime import synchronized_text

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "CHATGPT.md"
AGENTS = ROOT / "AGENTS.md"
PATH_RE = re.compile(r"`((?:(?:docs|prompts|tests)/[^`]+|(?:CHATGPT|AGENTS|README))\.md)`")
TEST_RE = re.compile(r"^# Golden Test (\d{3}):", re.MULTILINE)

# Context-budget entry size caps (bytes). Adjust slightly after intentional slim/expand;
# keep CHATGPT lean enough for Project Instructions and AGENTS lean for Codex cold start.
CHATGPT_MAX_BYTES = 14000
AGENTS_MAX_BYTES = 4500

# Never required by Autoload Protocol itself; only via explicit Task Loading Map rows
# (optional / one-shot). Autoload must not mandate these for every task.
HEAVY_NEVER_AUTOLOAD = (
    "docs/chatgpt-transfer-instructions.md",
    "docs/chatgpt-5.5-all-in-one-instructions.md",
    "docs/fable5-pattern-bank-for-chatgpt.md",
)

REQUIRED = [
    "CHATGPT.md",
    "AGENTS.md",
    "docs/chatgpt-5.5-project-instructions.md",
    "docs/chatgpt-operational-integrity-rules.md",
    "docs/chatgpt-coding-rules.md",
    "docs/chatgpt-engineering-task-rules.md",
]
EXPECTED_TASKS = {
    "Coding/debugging",
    "Proposal consistency review",
    "Technical blog post",
    "Architecture review",
    "Root cause analysis",
    "Technical research",
    "Operations manual or SOP",
    "Prompt review",
    "Security review",
    "Meeting notes, presentation, or executive summary",
    "RHEL/OpenShift/Kubernetes/Linux/Ansible/Satellite/Enterprise Architecture/AI infrastructure/EV topic",
    "General answer calibration",
    "One-shot copy/paste setup",
}

# Golden tests 015–029 (inclusive) expected present after context-budget suite.
EXPECTED_GOLDEN_MIN = 15
EXPECTED_GOLDEN_MAX = 29


def validate_inlined_runtime(errors: list[str]) -> None:
    if not ENTRY.is_file():
        return
    text = ENTRY.read_text(encoding="utf-8-sig")
    try:
        expected = synchronized_text(text)
    except ValueError as error:
        errors.append(str(error))
        return
    if text != expected:
        errors.append("CHATGPT.md inlined Core Runtime is out of sync; run python3 scripts/sync_runtime.py")


def validate_task_loading_map(errors: list[str]) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    if not ENTRY.is_file():
        return rows
    text = ENTRY.read_text(encoding="utf-8-sig")
    if "## Task Loading Map" not in text:
        errors.append("CHATGPT.md: missing Task Loading Map section")
        return rows
    table = text.split("## Task Loading Map", 1)[1].split("\n## ", 1)[0]
    tasks = []
    for line in table.splitlines():
        if not line.startswith("|") or "---" in line or "Task Type" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 3:
            errors.append(f"CHATGPT.md: invalid task-map row with {len(cells)} columns: {line}")
            continue
        tasks.append(cells[0])
        rows.append((cells[0], cells[1], cells[2]))
    duplicates = sorted({task for task in tasks if tasks.count(task) > 1})
    if duplicates:
        errors.append(f"CHATGPT.md: duplicate task-map rows: {', '.join(duplicates)}")
    missing = sorted(EXPECTED_TASKS - set(tasks))
    extra = sorted(set(tasks) - EXPECTED_TASKS)
    if missing:
        errors.append(f"CHATGPT.md: missing task-map rows: {', '.join(missing)}")
    if extra:
        errors.append(f"CHATGPT.md: unexpected task-map rows: {', '.join(extra)}")
    return rows


def validate_budget_caps(errors: list[str]) -> None:
    if ENTRY.is_file():
        size = ENTRY.stat().st_size
        if size > CHATGPT_MAX_BYTES:
            errors.append(
                f"CHATGPT.md exceeds context budget: {size} bytes > {CHATGPT_MAX_BYTES} "
                f"(trim Autoload/Map/Classifier prose or Core canonical sources)"
            )
    if AGENTS.is_file():
        size = AGENTS.stat().st_size
        if size > AGENTS_MAX_BYTES:
            errors.append(
                f"AGENTS.md exceeds context budget: {size} bytes > {AGENTS_MAX_BYTES} "
                f"(keep pointers; move long prose into docs/)"
            )


def validate_autoload_heavy_files(errors: list[str]) -> None:
    """Autoload Protocol must not require transfer/all-in-one/fable5 for every task."""
    if not ENTRY.is_file():
        return
    text = ENTRY.read_text(encoding="utf-8-sig")
    if "## Autoload Protocol" not in text:
        errors.append("CHATGPT.md: missing Autoload Protocol section")
        return
    # Slice until Context Budget or Core Runtime (whichever comes first after Autoload).
    after = text.split("## Autoload Protocol", 1)[1]
    for stop in ("## Context Budget", "## Core Runtime", "## Task Loading Map"):
        if stop in after:
            after = after.split(stop, 1)[0]
            break
    autoload = after
    for rel in HEAVY_NEVER_AUTOLOAD:
        # Allow mentioning them as "never autoload" / forbid lists; forbid "required"/"always load".
        if rel not in autoload:
            continue
        # If the path appears, require nearby never/do not/unless language in the same section.
        if not re.search(
            r"(?is)(never\s+autoload|do\s+not\s+autoload|unless\s+the\s+Task\s+Loading\s+Map)",
            autoload,
        ):
            errors.append(
                f"CHATGPT.md Autoload Protocol references {rel} without an explicit never-autoload guard"
            )
        # Must not say these are always/required for each task.
        if re.search(
            rf"(?is)(always\s+(read|load|apply)|required\s+files?).{{0,80}}{re.escape(rel)}",
            autoload,
        ) or re.search(
            rf"(?is){re.escape(rel)}.{{0,80}}(always\s+(read|load|apply)|for\s+each\s+task)",
            autoload,
        ):
            errors.append(
                f"CHATGPT.md Autoload Protocol must not require {rel} for every task"
            )


def validate_map_and_agents_paths(errors: list[str], map_rows: list[tuple[str, str, str]]) -> None:
    """All Task Loading Map and AGENTS.md referenced docs/prompts paths must exist."""
    referenced: list[tuple[str, str]] = []
    for task, required, optional in map_rows:
        for cell in (required, optional):
            for rel in PATH_RE.findall(cell):
                referenced.append((f"Task Loading Map:{task}", rel))
    if AGENTS.is_file():
        for line_number, line in enumerate(AGENTS.read_text(encoding="utf-8-sig").splitlines(), 1):
            for rel in PATH_RE.findall(line):
                referenced.append((f"AGENTS.md:{line_number}", rel))
    for where, rel in referenced:
        if any(char in rel for char in "*?["):
            exists = any(ROOT.glob(rel))
        else:
            exists = (ROOT / rel).is_file()
        if not exists:
            errors.append(f"{where} references missing file: {rel}")


def validate_context_budget_section(errors: list[str]) -> None:
    for path, label in ((ENTRY, "CHATGPT.md"), (AGENTS, "AGENTS.md")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8-sig")
        if "## Context Budget" not in text:
            errors.append(f"{label}: missing Context Budget section")
            continue
        budget = text.split("## Context Budget", 1)[1].split("\n## ", 1)[0]
        for rel in HEAVY_NEVER_AUTOLOAD:
            if rel.split("/")[-1] not in budget and rel not in budget:
                errors.append(f"{label} Context Budget must mention never-autoload file: {rel}")


def validate_golden_range(errors: list[str], seen: dict[str, Path]) -> None:
    ids = sorted(int(i) for i in seen)
    if not ids:
        errors.append("no GoldenTest-*.md files found under tests/")
        return
    expected = set(range(EXPECTED_GOLDEN_MIN, EXPECTED_GOLDEN_MAX + 1))
    present = set(ids)
    missing = sorted(expected - present)
    if missing:
        errors.append(
            f"missing Golden Test IDs in {EXPECTED_GOLDEN_MIN:03d}–{EXPECTED_GOLDEN_MAX:03d}: "
            + ", ".join(f"{i:03d}" for i in missing)
        )
    outside = sorted(i for i in present if i < EXPECTED_GOLDEN_MIN or i > EXPECTED_GOLDEN_MAX)
    if outside:
        # Allow only the documented contiguous suite for now.
        errors.append(
            "unexpected Golden Test IDs outside "
            f"{EXPECTED_GOLDEN_MIN:03d}–{EXPECTED_GOLDEN_MAX:03d}: "
            + ", ".join(f"{i:03d}" for i in outside)
        )


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    validate_inlined_runtime(errors)
    map_rows = validate_task_loading_map(errors)
    validate_budget_caps(errors)
    validate_autoload_heavy_files(errors)
    validate_map_and_agents_paths(errors, map_rows)
    validate_context_budget_section(errors)

    for source in [
        *ROOT.glob("*.md"),
        *(ROOT / "docs").glob("*.md"),
        *(ROOT / "prompts").glob("*.md"),
        *(ROOT / "tests").glob("*.md"),
    ]:
        text = source.read_text(encoding="utf-8-sig")
        for line_number, line in enumerate(text.splitlines(), 1):
            for rel in PATH_RE.findall(line):
                exists = any(ROOT.glob(rel)) if any(char in rel for char in "*?[") else (ROOT / rel).is_file()
                if not exists:
                    errors.append(f"{source.relative_to(ROOT)}:{line_number} references missing file: {rel}")

    seen: dict[str, Path] = {}
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

    validate_golden_range(errors, seen)

    runtime = ENTRY.read_text(encoding="utf-8") if ENTRY.is_file() else ""
    for term in ["Fable5 Enhanced", "Fable5 Distilled Patterns"]:
        if term in runtime:
            errors.append(f"prohibited model-specific Runtime term in CHATGPT.md: {term}")

    if "## Intent Classifier" not in runtime:
        errors.append("CHATGPT.md: missing Intent Classifier section")

    if errors:
        print("ChatGPT transfer-pack validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ChatGPT transfer-pack validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
