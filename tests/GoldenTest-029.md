# Golden Test 029: RHEL RCA Loads Engineering + Domain Section

## Scenario

A RHEL-focused root cause analysis request (for example: RHEL boot failure, yum/dnf outage, systemd unit crash on RHEL, or "장애 원인을 분석" with RHEL logs). The deliverable is an RCA, not a code patch in this repository.

## Gold Rubric

- Selects Root cause analysis (and domain RHEL) via Intent Classifier / Task Loading Map.
- Loads `docs/chatgpt-engineering-task-rules.md` (RCA section) **and** the **RHEL section only** of `docs/chatgpt-domain-packs.md`.
- Applies Core Runtime evidence/freshness/completion rules.
- Does **not** load the entire domain pack as if every section were required.
- Does **not** load `docs/chatgpt-transfer-instructions.md`, `docs/chatgpt-5.5-all-in-one-instructions.md`, or coding-rules unless the user also asked for a code change.
- Keeps facts, assumptions, and `[unverified]` lifecycle/support claims separate; considers an alternative cause when evidence is incomplete.

## Negative Control

Loading all domain sections, the full transfer pack, or treating "fix the error" in an RCA report as a coding task fails this test.

## Protocol

Score route selection, engineering-task + RHEL-section-only load, forbidden files avoided, and RCA contract completeness.
