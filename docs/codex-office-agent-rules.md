# Codex Office Agent Rules

Public-safe Codex guidance for Office artifact work. Tool-specific agent deployment settings and private template references are intentionally omitted.

## Scope

Use these rules for Office artifacts:

- PowerPoint: `.pptx`
- Word: `.docx`
- Excel: `.xlsx`, `.xls`, `.csv`, `.tsv`

For PDF-only work, use PDF-specific workflow instead.

## Default Storage

Save Office outputs under:

- `outputs/`
- reusable generation scripts under `scripts/office/`

Never overwrite an existing artifact. Add `_v2`, `_v3`, etc. when needed.

## Workflow

1. Identify document type, audience, language, approximate length, and source material.
2. If the requested structure is ambiguous or the artifact is substantial, produce a short blueprint first.
3. Build the artifact using the relevant Codex skill or bundled workspace dependency.
4. Preserve any generation script when it helps reproduce the output.
5. Reopen or render the artifact for the smallest meaningful verification.
6. Report file path, verification result, and remaining visual/manual review limits.

For small, obvious edits, skip the blueprint and apply the edit directly.

## Branding

- Use generic styling by default.
- Apply brand styling only when the user explicitly asks for a brand/company format or provides a template.
- If branding requirements are ambiguous, ask once.
- Do not invent brand fonts, colors, logos, or claims. Mark missing brand assets in notes.

## Format Rules

### PPTX

- Use 16:9 unless the user asks otherwise.
- Keep one main message per slide.
- Include title/section/closing slides when building a deck from scratch.
- Verify slide count and basic placeholder/text presence.
- Visual rendering remains the final check when layout matters.

### DOCX

- Use heading hierarchy consistently.
- Preserve or create styles rather than manual one-off formatting when practical.
- Verify headings, paragraph count, tables, and obvious empty sections.
- Render pages when layout matters.

### XLSX

- Separate summary/dashboard from raw data when useful.
- Freeze header rows and apply filters for tabular data.
- Prefer formulas over hardcoded calculated values.
- Reopen with a spreadsheet library and scan formulas for common errors when possible.

## Result Metadata

For substantial Office work, write a JSON result file under `outputs/`:

```json
{
  "task": "short title",
  "phase": "blueprint | build",
  "file": "outputs/name_YYYYMMDD.ext",
  "type": "pptx | docx | xlsx",
  "mode": "generic | brand",
  "verified": true,
  "script": "scripts/office/build_name.py",
  "notes": []
}
```

## Stop Conditions

- Missing required source/template.
- Same generation or validation error repeats 3 times.
- Artifact size is likely too large for one pass: more than 30 slides, 100 Word pages, or 100k spreadsheet rows.
- Required brand assets are unavailable and generic fallback is not acceptable to the user.
