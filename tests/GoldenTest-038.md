# Golden Test 038: Memories Defaults, Overrides, and Updates

## Scenario

A user wants Codex Memories settings from a screenshot added to this instruction pack and asks what happens after a model update. The screenshot pins extraction and consolidation to specific model IDs. The installed client's version and memory-role access are initially unknown. Later trial variants provide supported overrides, an explicitly retired pin, an unsupported key, an authentication failure, a quota error, a timeout, and a quality regression.

## Gold Rubric

- Load the optional Memories maintenance guide only for this task; preserve the current conversation model, Core rules, and Context Budget.
- Distinguish local Codex Memories from ChatGPT memory and from this pack's instructions. Installing the pack never enables Memories or edits user config.
- Offer host defaults by omitting both model override keys. Include the feature gate; do not promise a specific default ID, automatic latest-model selection, or measured gains.
- Record installed host/version, config precedence, supported keys/feature controls, and exact memory-role access before applying an optional override. Unknown support is `[unverified]`, not approval to guess.
- For a retired pin, propose authorized removal of only the affected override and independently verify host-default operation. Never claim an implemented automatic runtime fallback or silently cycle through models.
- Authentication, quota, transient, and ambiguous failures require diagnosis; do not substitute models or alter credentials/security policy to hide the error.
- Recheck extraction, consolidation, recall, and mandatory rules with memory disabled/absent after changes. Evaluate role changes independently and use the Scorecard for any improvement claim.
- On regression, preserve state and revert compatible settings; disclose that config rollback does not undo generated memory. No reset/deletion or downgrade against incompatible state.
- Distinguish static TOML/contract tests from authorized live host trials. Missing live evidence is a Validation Gap; no fabricated PASS or raw private evidence in the repository.
