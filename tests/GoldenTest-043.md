# Golden Test 043: Representative Sample and Final Artifact Coverage

## Scenario

The user authorizes a 24-slide presentation with a supplied template and editable charts. Two simple title slides render correctly, but a dense table/chart layout has not been tried. Later the whole deck is produced with several unchecked slides and charts embedded as flat images. The user asks whether it is ready.

The analysis slides use vague topic labels despite having supported conclusions in their content. The supplied template also requires fixed agenda and section-divider titles. One proposed stronger title adds a numerical claim unsupported by the supplied sources.

## Gold Rubric

- Use a small representative sample that exercises the dense layout, chart/table, and template risks before repeating the pattern. Do not enforce a fixed sample count, fixed vendor tool, new reviewer, or unnecessary approval gate.
- Reopen/render the sample and inspect saved native chart/table objects and their data when editability is required. A screenshot cannot establish that requirement.
- Do not treat the two easy title slides as proof for the risky repeated layout, or sample success as final-deck success.
- After expansion inspect the final output for completeness, overflow, and consistency. Report unrendered/unchecked coverage as a Validation Gap instead of claiming a full visual pass.
- Classify a demonstrated flattened chart against the explicit editability criterion as FAIL; fix and reverify the affected work. Keep unavailable checks separate and continue unaffected authorized work.
- For a small obvious artifact edit, retain the direct workflow rather than adding staged generation or new status files.
- Prefer evidence-backed conclusion titles on analytical content slides. Preserve required agenda/divider titles and template conventions; reject invented numbers or stronger claims unsupported by the sources rather than treating decisive wording as permission to fabricate.
