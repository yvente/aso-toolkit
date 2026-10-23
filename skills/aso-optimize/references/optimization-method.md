# Optimization Method

Use this reference when preparing a concrete metadata experiment.

## Goal and naming contract

Resolve release mode, acquisition objective, brand status (`temporary`, `confirmed`, `none`, `unknown`) and permitted naming strategy from the brief and existing conversation. A project title is identity context, not proof it must occupy store-title space. When naming is open, compare functional, hybrid or brand-led options as relevant to the user's objective; do not impose one strategy on every app. Resolve genuinely decision-changing unknowns before calling a name recommended.

## Baseline

Use `live-<baseline-version>.json` in the active target-version/locale directory only after verifying its source and capture date. Experiment-log history can help locate context but is not proof that `metadata_after` went live. For updates, if live state is not confirmed, ask for or collect the current baseline. For a confirmed first release, write `release_type: "first_release"` and `baseline_version: null`, omit the live file, and leave initial-release notes empty when appropriate. Do not use a fake version such as `unreleased` as a baseline. Compare naming options and evidence rather than fabricating before/after metadata.

## Keyword data

Expected columns are `keyword`, `popularity`, `difficulty`, and optional `rank`. Infer unknown headers only when the mapping is unambiguous; otherwise show samples and ask.

Before selection, assess the keyword expansion handoff: native basic queries, feature and use-case coverage, measured title drivers, alternatives, rejected terms and remaining gaps. Existing same-locale measurements can satisfy this gate without rerunning research; a CSV file's mere presence cannot.

Selection order:

1. preserve own terms ranked 1–10 unless irrelevant after a product change;
2. filter remaining own and competitor terms using learned thresholds only when profile confidence is adequate;
3. require confirmed product relevance;
4. prioritize popularity, then lower difficulty, with intent-history used as a bounded tie-breaker;
5. retain phrase-level provenance while decomposing final keyword tokens;
6. remove terms already used in App Name or Subtitle and remove competitor brands.

Default thresholds are popularity above 20 and difficulty below 70. They are heuristics, not universal App Store facts. Consider intent and product fit alongside competition; do not automatically discard an essential category identity or select a misleading high-volume word.

## Allocate the three fields together

Compare a small set of meaningful title/subtitle alternatives (unless already fixed by the user), with supporting queries, relevance, evidence gaps and tradeoffs. Explain why the recommended pair beats the alternatives; component scores cannot be added to invent a new compound query's volume.

Treat App Name, Subtitle and Keywords as one coverage allocation. Show keyword characters used/remaining and title/subtitle overlaps. Use spare keyword space for additional relevant intents, not mechanically translated tails, competitor brands, unsupported capabilities or redundant forms. Near-full usage (often 95–100 characters) is an efficiency goal, not a universal minimum. If useful room remains, explain the omitted candidates and why adding them would not improve coverage. Never choose a weaker set solely because it totals exactly 100.

Preserve query-to-token provenance: exact-query measurement, component of a measured phrase, or unmeasured product-relevant token. Only the first is an independent measurement of that token. Do not claim substring checks simulate CJK segmentation, stemming or Apple's indexing.

Use `audit-metadata` for space and exact-text warnings; it cannot decide language naturalness, relevance, name availability or expected acquisition. A heuristic weighting/knapsack score is a declared selection aid, not an empirically validated ASO objective.

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
- expansion readiness and measurement scope, including unresolved decision-changing gaps;
- naming status/strategy, considered title alternatives and selection rationale;
- keyword characters used/remaining, overlaps and a reasoned disposition of audit warnings;
- technical validation results separately from decision-quality review and release prerequisites;
- risk and attribution analysis;
- experiment hypothesis and follow-up plan.

Write the report as `optimize.md`. Write the pending metadata first to `proposed-<target-version>.json`, validate it, and derive that locale's `deliverable.xlsx` from the JSON. Verify every workbook value against the JSON before delivery; the workbook never becomes an independent metadata source.
