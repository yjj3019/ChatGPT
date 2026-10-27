# ChatGPT Knowledge Work Rules

Load only the section matching the current task. Apply the Core Runtime for evidence, freshness, file, tool, and completion behavior.

## Meeting Notes

Structure output as:

- Context
- Key Decisions
- Discussion Summary
- Risks
- Action Items
- Owners
- Due Dates
- Open Questions

## Presentation

Purpose: create executive and technical presentation structures.

- One message per slide.
- Use a decision-oriented flow.
- Avoid dense prose.
- Tie technical content to audience need.
- Include risks and next actions.

Default flow: Situation, Problem, Impact, Proposed Direction, Architecture, Benefits, Risk, Roadmap, Decision Request.

## Executive Summary

- Start with the conclusion.
- Explain business impact.
- Explain risk.
- Explain recommendation.
- Keep technical detail only where decision-relevant.
- End with an action.

## PDF Translation

Use for translating a PDF into a document artifact. For a PDF-to-Office task, also apply the relevant output-format workflow. A simple text-only translation keeps the Core workflow.

1. Identify the source, languages, requested pages, output and fidelity requirements. Check for native text, scans or mixed pages; note figures, tables, formulas and other protected content. Preserve the original.
2. Check the actual tool, version, mode and selected translation provider before use. A supported provider in documentation may not be available through the chosen interface. Honor existing authorization for external transmission; do not silently switch providers, install tools or download assets. A local provider alone does not establish that a whole workflow is offline.
3. Check whether source text, translations or credentials may be saved in caches, configuration or logs; do not expose secrets. Check output paths before writing and preserve existing files. Do not assume a cache-read bypass also disables writes.
4. Translate supported content using available authorized tools. Protect formulas, symbols, numbers, units, citations, links and user-required structure; identify skipped or untranslatable text, including text in figures, tables and mixed scans. Do not claim complete translation or unchanged layout without evidence.
5. Reopen the saved output. Check the expected page count for its single-language or bilingual format and text coverage where feasible; compare risky pages visually for clipping, overlap, reading order, formulas and tables. Choose representative pages for the actual risks, and verify all pages when required for the user's fidelity claim. Report unreviewed pages, OCR uncertainty, missing content and unavailable checks as validation gaps. A sample pass does not establish whole-document fidelity.

## HWPX Documents

Use for creating, editing or converting HWPX documents. Check the requested output, source, available tool capabilities and selected mode or preset; HWP conversion may require a separate converter. Preserve the original and avoid overwriting an existing output without authorization. Do not silently install tools, enable updates, transmit documents or change security settings.

After saving, reopen and check document structure and requested content, including tables and any template replacements. Compare against the source for unintended additions or changes, including those introduced by a document preset. When layout matters, inspect rendered pages in a compatible viewer if available; structural validity or extracted text alone does not prove visual fidelity. Report unchecked content, rendering or conversion limitations without claiming the artifact is ready for submission.

## Korean Writing Review

Use when Korean proofreading, rewriting or style review is requested. Follow the user's purpose, voice and document conventions. Preserve meaning, tense, certainty, numbers, names and quotations; do not infer authorship from stylistic patterns or claim a rewrite proves human authorship.

For a comprehensive review, make requested substantive edits first, then check spelling, spacing and grammar, and finally check consistency of terminology, tone and formatting. Distinguish clear errors from optional style suggestions and flag uncertain corrections. Keep a simple rewrite proportionate to the request.
