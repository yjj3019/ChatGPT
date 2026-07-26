# Golden Test 024: Engineering Task Contract Selection

## Scenario

Evaluate representative architecture review, RCA, technical research, operations manual, prompt review, and security review requests.

Include these route-collision controls:

- `장애 원인을 분석하고 오류를 수정해줘` and `Fix the error in this incident report` select root cause analysis.
- `RCA 보고서의 오류를 수정해줘` remains root cause analysis.
- `제안서 오류를 수정해줘` selects proposal consistency review.
- `아키텍처 검토하고 문제를 수정해줘` selects architecture review.
- `이 프롬프트 검토하고 오류 수정해줘` selects prompt review.
- `Optimize this SQL query` selects coding/debugging.

## Gold Rubric

- Selects `docs/chatgpt-engineering-task-rules.md` and only the matching task section.
- Prefers a specific task object and intent over generic fix/error wording.
- Applies the Core Runtime without loading unrelated task packs.
- Uses the matching output contract and required evidence discipline.
- Considers an alternative for architecture and RCA tasks.
- Includes validation and rollback for risky operational procedures.
- Uses P0/P1 and a verification-dependent GO decision for security review.
- Runs at most one independent review pass after a draft or assessment exists.

## Protocol

Compare the existing and revised transfer pack on the same six requests. Score task selection, required sections, evidence handling, unrelated context loaded, and final recommendation quality.
