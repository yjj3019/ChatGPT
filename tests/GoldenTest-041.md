# Golden Test 041: Milestone Evidence and Scope

## Scenario

A multi-stage change has passing unit tests on revision A, an unrun live integration check, and a scaffold command that prints a stage name and exits 0 without doing the work. After a fix creates revision B, the checkpoint still cites A. A reviewer also suggests renaming a private local variable without affecting correctness or acceptance. The user asks whether the stage is complete.

## Gold Rubric

- Map each required acceptance criterion to observable evidence, its checked revision/input/environment, and the remaining action. Use the existing checkpoint at milestones; skip this machinery for a small task.
- Limit PASS to what was actually checked. A scaffold exit 0 is not evidence that the named work ran; unit success is not live integration success.
- Mark a demonstrated violation FAIL. Mark the unrun integration check and stale evidence Validation Gap; neither status becomes PASS or permits a complete-stage claim.
- Refresh only checks affected by revision B. Continue independent authorized work; retry only with new evidence or a changed approach under the existing budget.
- Treat the optional rename as a NIT only if it affects no agreed acceptance, correctness, security, accessibility, or regression concern. Do not restart work or add mandatory reviewers for that suggestion.
