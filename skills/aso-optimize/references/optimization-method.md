# Optimization Method

Use this reference when preparing a concrete metadata experiment.

## Baseline

Use `live-<baseline-version>.json` in the active target-version/locale directory only after verifying its source and capture date. Experiment-log history can help locate context but is not proof that `metadata_after` went live. If live state is not confirmed, ask for or collect the current baseline.

## Keyword data

Expected columns are `keyword`, `popularity`, `difficulty`, and optional `rank`. Infer unknown headers only when the mapping is unambiguous; otherwise show samples and ask.

Selection order:

1. preserve own terms ranked 1–10 unless irrelevant after a product change;
2. filter remaining own and competitor terms using learned thresholds only when profile confidence is adequate;
3. require confirmed product relevance;
4. prioritize popularity, then lower difficulty, with intent-history used as a bounded tie-breaker;
5. retain phrase-level provenance while decomposing final keyword tokens;
6. remove terms already used in App Name or Subtitle and remove competitor brands.

Default thresholds are popularity above 20 and difficulty below 70. They are heuristics, not universal App Store facts.

## Copy rules

- App Name: communicate identity and primary search intent naturally.
- Subtitle: add a distinct benefit or secondary intent; do not paraphrase the title.
- Keywords: comma-separated tokens without spaces at submission time; no title/subtitle duplication.
- Promotional Text: lead with the strongest timely user benefit.
- Description: front-load value in the first three lines and use feature-to-benefit language.
- What's New: derive only from `Recent Changes`; write benefit-first release notes.

Verify current Apple policies when the decision depends on indexing or submission behavior.

## Experiment design

Prefer one primary hypothesis per round. If several fields must change together, label attribution scope:

- High: one meaningful field or one tightly coupled keyword set changed.
- Medium: two related fields changed.
- Low: broad repositioning, creative, pricing, product, and metadata changed together.

The report must list the hypothesis, primary metric, guardrail metrics, expected observation window, and confounders.

## Output report

Include:

- current vs proposed values and character counts;
- complete copy-ready values;
- keyword intent/evidence table;
- additions/removals with measured values when supplied;
- validation results;
- risk and attribution analysis;
- experiment hypothesis and follow-up plan.

Write the report as `optimize.md`. Write the pending metadata first to `proposed-<target-version>.json`, validate it, and derive that locale's `deliverable.xlsx` from the JSON. Verify every workbook value against the JSON before delivery; the workbook never becomes an independent metadata source.
