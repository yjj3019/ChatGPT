# ChatGPT Proposal Review Rules

Use for proposal, RFP, sales deck, public-sector document, and consistency review tasks.

## Checkpoints

- Requirement coverage
- Internal contradictions
- Unsupported claims
- Lifecycle/version/date accuracy
- Terminology consistency
- Compliance/certification claims
- Structure completeness
- Customer-specific assumptions

## Severity

- Critical: false, non-compliant, misleading, or likely to fail evaluation.
- Major: materially weakens credibility, coverage, or scoring.
- Minor: local wording or structure issue.
- Note: optional improvement.

## Output

```text
Executive Summary
- ...

Critical
- [C1] ...

Major
- [M1] ...

Minor
- [m1] ...

Open Evidence Gaps
- ...

Recommended Next Edits
1. ...
```

## Guardrails

- Do not rewrite the whole proposal unless asked.
- Do not invent certifications, public-sector requirements, product dates, or support periods.
- Keep evidence gaps separate from wording improvements.
