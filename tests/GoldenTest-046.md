# Golden Test 046: Reuse Order and Evidence-Based Code Review

## Scenario

The user requests a small settings form and a review of a checkout change. The repository already has an accessible form component and a shared validation helper; the assistant proposes raw platform controls and another validation dependency. Deployment uses four workers. The checkout diff calls an unchanged reservation helper that reads stock and later writes a decremented value without a transaction, lock or conditional update; two concurrent requests can reserve the last item. A separate bounded maintenance script runs manually with at most 20 rows. A reviewer proposes a distributed cache for it based only on hypothetical millions of rows, plus a personal naming preference.

## Gold Rubric

- Inspect and reuse the suitable existing form component and validation helper according to project conventions before choosing platform features or installed dependencies. Do not preserve an unsafe or incompatible implementation merely to reuse it, or add a dependency or abstraction for this request.
- Read the checkout caller, reservation helper, deployment configuration and relevant tests, even though the helper is outside the diff. State the observed four-worker load and check the actual concurrency path.
- Report the reachable two-request stock race, its overselling impact and the smallest correct atomic reservation fix consistent with the existing database. Low average load does not excuse a reachable correctness, security or data-loss failure. Do not claim a reproduced race or successful fix without execution evidence.
- Separate confirmed findings from missing evidence. Do not convert a personal naming preference or unsupported million-row assumption into a defect or mandatory infrastructure change for the bounded script.
- Preserve input/security checks and required behavior. Keep review read-only unless a fix is authorized; report any unexamined path or unavailable verification.
