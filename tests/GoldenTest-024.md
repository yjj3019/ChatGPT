# Golden Test 024: Engineering Task Contract Selection

## Scenario

Evaluate representative architecture review, RCA, technical research, operations manual, prompt review, and security review requests.

## Gold Rubric

- Selects `docs/chatgpt-engineering-task-rules.md` and only the matching task section.
- Applies the Core Runtime without loading unrelated task packs.
- Uses the matching output contract and required evidence discipline.
- Considers an alternative for architecture and RCA tasks.
- Includes validation and rollback for risky operational procedures.
- Uses P0/P1 and a verification-dependent GO decision for security review.
- Runs at most one independent review pass after a draft or assessment exists.

## Protocol

Compare the existing and revised transfer pack on the same six requests. Score task selection, required sections, evidence handling, unrelated context loaded, and final recommendation quality.
