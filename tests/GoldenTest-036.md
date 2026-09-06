# Golden Test 036: Fence-Aware Section Parsing

## Scenario

A supporting guide (for example `docs/chatgpt-blog-rules.md`) contains an outline example inside a fenced code block. The outline lists lines that begin with `##` such as `## Why this matters now`. A maintainer runs section-scoped load measurement or validation that extracts `##` sections.

## Gold Rubric

- Real top-level sections outside fences remain the only section boundaries (for blog rules: Style, Outline, Review Checklist).
- `##` headings that appear only inside ``` / ~~~ fences do not create extra sections or truncate the enclosing section.
- `scripts/measure_load.py` and `scripts/validate_framework.py` share the same fence-aware helper rather than a naive `^## ` split.
- Failing to ignore fenced headings is a structural defect even if Task Loading Map routes are otherwise correct.
