# ChatGPT Task Prompts

## 1. Proposal Consistency Check

```text
Use the ChatGPT 5.5 Project Instructions.
Task: perform a proposal consistency check.

Input:
[paste proposal/RFP/deck text]

Check:
- requirement coverage
- contradictions
- unsupported claims
- lifecycle/version/date accuracy
- terminology consistency
- compliance/certification claims
- structure completeness

Output:
Executive Summary, Critical, Major, Minor, Open Evidence Gaps, Recommended Next Edits.
Mark unsupported factual claims as [unverified].
```

## 2. Coding Debug Task

```text
Use the ChatGPT 5.5 Project Instructions.
Task: debug and propose the smallest correct fix.

Bug report:
[paste bug report]

Relevant files:
[paste files or summaries]

Rules:
- find shared root cause, not just symptom
- scan sibling callers conceptually from provided code
- avoid new abstractions
- propose smallest diff
- include one verification command or minimal test
- state if anything cannot be verified

Output: Root cause, Change, Verification, Caller scan, Risks.
```

## 3. Technical Blog Draft

```text
Use the ChatGPT 5.5 Project Instructions.
Task: draft a technical blog post.

Topic:
[paste topic]

Audience:
[paste audience]

Facts/sources available:
[paste facts or links]

Style:
- calm practitioner tone
- structured sections
- no unsupported claims
- practical takeaways

Output: title options, outline, draft, evidence gaps.
```

## 4. Fable-style Self Check

```text
Before finalizing, check your answer against these rules:
- Did you separate facts, assumptions, and open questions?
- Did you mark unsupported factual claims as [unverified]?
- Did you catch contradictions instead of hiding them?
- For code, did you target the shared root cause and sibling callers?
- Is the answer smaller than a framework but complete enough to use?

Revise only if one of these checks fails.
```
