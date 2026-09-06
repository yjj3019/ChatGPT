#!/usr/bin/env python3
"""Validate runtime synchronization, routing, references, budgets, and scenario contracts."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from sync_runtime import generated_documents

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "CHATGPT.md"
PATH_RE = re.compile(r"`((?:(?:docs|prompts|tests|scripts|\.github)/[^`\n]+|(?:CHATGPT|AGENTS|README)\.md))`")
LINK_RE = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^\s)]+)\)")
TEST_RE = re.compile(r"^# Golden Test (\d{3}):", re.MULTILINE)
# Repository maintenance budgets, not model token or product limits.
RUNTIME_CHARACTER_BUDGETS = {
    "CHATGPT.md": 8000, "AGENTS.md": 4000,
    "docs/chatgpt-5.5-all-in-one-instructions.md": 8000,
}
REQUIRED = [
    "CHATGPT.md", "AGENTS.md", "README.md", "tests/Scorecard.md",
    "docs/chatgpt-5.5-project-instructions.md",
    "docs/chatgpt-operational-integrity-rules.md",
    "docs/chatgpt-coding-rules.md",
    "docs/chatgpt-engineering-task-rules.md",
]
EXPECTED_TASKS = {
    "Coding/debugging": "docs/chatgpt-coding-rules.md",
    "Proposal consistency review": "docs/chatgpt-proposal-review-rules.md",
    "Technical blog post": "docs/chatgpt-blog-rules.md",
    "Architecture review": "docs/chatgpt-engineering-task-rules.md",
    "Root cause analysis": "docs/chatgpt-engineering-task-rules.md",
    "Technical research": "docs/chatgpt-engineering-task-rules.md",
    "Operations manual or SOP": "docs/chatgpt-engineering-task-rules.md",
    "Prompt review": "docs/chatgpt-engineering-task-rules.md",
    "Security review": "docs/chatgpt-engineering-task-rules.md",
    "Meeting notes, presentation, or executive summary": "docs/chatgpt-knowledge-work-rules.md",
    "RHEL/OpenShift/Kubernetes/Linux/Ansible/Satellite/Enterprise Architecture/AI infrastructure/EV topic": "docs/chatgpt-domain-packs.md",
    "Model selection / routing advice": "docs/chatgpt-codex-model-routing.md",
    "General answer calibration": None,
    "One-shot copy/paste setup": "docs/chatgpt-5.5-all-in-one-instructions.md",
}
EXPECTED_TEST_IDS = {f"{number:03d}" for number in range(15, 36)}
HEAVY_FILES = (
    "docs/chatgpt-transfer-instructions.md",
    "docs/chatgpt-5.5-all-in-one-instructions.md",
    "docs/fable5-pattern-bank-for-chatgpt.md",
)


def read_document(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        errors.append(f"{path.relative_to(ROOT)}: cannot read document: {error}")
        return ""


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def validate_inlined_runtime(errors: list[str]) -> None:
    if not ENTRY.is_file():
        return
    try:
        for path, expected in generated_documents().items():
            if not path.is_file() or read_document(path, errors) != expected:
                errors.append(f"{path.relative_to(ROOT)} is out of sync; run python scripts/sync_runtime.py")
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(f"generated runtime: {error}")


def validate_task_loading_map(text: str, errors: list[str]) -> None:
    table = section(text, "Task Loading Map")
    if not table:
        errors.append("CHATGPT.md: missing Task Loading Map section")
        return
    tasks = []
    for line in table.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] == "Task Type" or all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        if len(cells) != 3 or not all(cells):
            errors.append(f"CHATGPT.md: invalid task-map row: {line}")
            continue
        task = cells[0]
        tasks.append(task)
        if task in EXPECTED_TASKS:
            required = EXPECTED_TASKS[task]
            actual = set(PATH_RE.findall(cells[1]))
            if (required is None and cells[1] != "Core Runtime only") or (required is not None and actual != {required}):
                errors.append(f"CHATGPT.md: incorrect required route for {task}")
    duplicates = sorted({task for task in tasks if tasks.count(task) > 1})
    if duplicates:
        errors.append(f"CHATGPT.md: duplicate task-map rows: {', '.join(duplicates)}")
    missing = sorted(set(EXPECTED_TASKS) - set(tasks))
    extra = sorted(set(tasks) - set(EXPECTED_TASKS))
    if missing:
        errors.append(f"CHATGPT.md: missing task-map rows: {', '.join(missing)}")
    if extra:
        errors.append(f"CHATGPT.md: unexpected task-map rows: {', '.join(extra)}")


def validate_references(source: Path, text: str, errors: list[str]) -> None:
    for line_number, line in enumerate(text.splitlines(), 1):
        references = [(ROOT, rel) for rel in PATH_RE.findall(line) if Path(rel).suffix in {".md", ".py", ".yml", ".yaml"}]
        for target in LINK_RE.findall(line):
            try:
                url = urlsplit(target)
            except ValueError as error:
                errors.append(f"{source.relative_to(ROOT)}:{line_number}: invalid link: {error}")
                continue
            if url.scheme or url.netloc or not url.path:
                continue
            relative = unquote(url.path)
            references.append((ROOT if relative.startswith("/") else source.parent, relative.lstrip("/")))
        for base, relative in references:
            try:
                if "\x00" in relative:
                    raise ValueError("NUL byte in file reference")
                candidate = base / relative
                if not candidate.resolve().is_relative_to(ROOT):
                    errors.append(f"{source.relative_to(ROOT)}:{line_number}: reference leaves repository: {relative}")
                    continue
                exists = any(path.is_file() for path in base.glob(relative)) if any(char in relative for char in "*?[") else candidate.is_file()
            except (OSError, ValueError, RuntimeError) as error:
                errors.append(f"{source.relative_to(ROOT)}:{line_number}: invalid file reference: {error}")
                continue
            if not exists:
                errors.append(f"{source.relative_to(ROOT)}:{line_number} references missing file: {relative}")


def validate_loading_policy(documents: dict[Path, str], errors: list[str]) -> None:
    for relative, headings in {
        "CHATGPT.md": ("Autoload Protocol", "Context Budget", "Intent Classifier"),
        "AGENTS.md": ("Context Budget",),
    }.items():
        text = documents.get(ROOT / relative, "")
        for heading in headings:
            if not section(text, heading):
                errors.append(f"{relative}: missing or empty {heading}")
        policy = section(text, "Autoload Protocol") + "\n" + section(text, "Context Budget")
        for path in HEAVY_FILES:
            if re.search(rf"(?is)always\s+(?:read|load|apply).{{0,80}}{re.escape(path)}", policy):
                errors.append(f"{relative}: heavy guide must not always load: {path}")


def validate_golden_tests(documents: dict[Path, str], errors: list[str]) -> None:
    seen = set()
    for path in sorted((ROOT / "tests").glob("GoldenTest-*.md")):
        text = documents.get(path, "")
        matches = TEST_RE.findall(text)
        if len(matches) != 1:
            errors.append(f"expected one Golden Test ID header: {path.relative_to(ROOT)}")
            continue
        test_id = matches[0]
        if path.stem != f"GoldenTest-{test_id}":
            errors.append(f"Golden Test filename/header mismatch: {path.relative_to(ROOT)}")
        if test_id in seen:
            errors.append(f"duplicate Golden Test ID {test_id}: {path.relative_to(ROOT)}")
        seen.add(test_id)
        # Test 025 predates the standard Scenario / Gold Rubric layout.
        headings = ("Triggers and Expected Routes", "Forbidden Behavior") if test_id == "025" else ("Scenario", "Gold Rubric")
        for heading in headings:
            if not section(text, heading):
                errors.append(f"{path.relative_to(ROOT)}: missing or empty {heading}")
    for test_id in sorted(EXPECTED_TEST_IDS - seen):
        errors.append(f"missing required Golden Test {test_id}")


def main() -> int:
    errors = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    sources = sorted([*ROOT.glob("*.md"), *(ROOT / "docs").glob("*.md"),
                      *(ROOT / "prompts").glob("*.md"), *(ROOT / "tests").glob("*.md")])
    documents = {path: read_document(path, errors) for path in sources}
    runtime = documents.get(ENTRY, "")
    validate_inlined_runtime(errors)
    if ENTRY.is_file():
        validate_task_loading_map(runtime, errors)
    validate_loading_policy(documents, errors)
    for relative, budget in RUNTIME_CHARACTER_BUDGETS.items():
        size = len(documents.get(ROOT / relative, ""))
        if size > budget:
            errors.append(f"{relative}: character budget exceeded ({size} > {budget})")
    for source, text in documents.items():
        validate_references(source, text, errors)
    validate_golden_tests(documents, errors)
    for term in ["Fable5 Enhanced", "Fable5 Distilled Patterns"]:
        if term in runtime:
            errors.append(f"prohibited model-specific Runtime term in CHATGPT.md: {term}")

    if errors:
        print("ChatGPT transfer-pack validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"ChatGPT transfer-pack validation passed ({len(EXPECTED_TASKS)} routes, {len(EXPECTED_TEST_IDS)} required scenarios).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
