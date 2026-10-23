# Keyword Candidate Method

Generate a broad measurement set before optimizing metadata. This is an iterative coverage task, not a candidate-count quota.

## Expansion and handoff gate

1. Map the primary job, native category words/synonyms and core feature queries before adding audience, problem and language-pair tails. Keep product limits visible; a keyword's popularity cannot make an unsupported feature relevant.
2. Expand from more than a translated seed list: same-store competitor names/subtitles, local review vocabulary and concrete workflows. Preserve per-query provenance, including whether wording is observed or generated. Review extracted brand terms and ambiguous words before adopting them.
3. Measure the plausible title/subtitle drivers and meaningful alternative intents first, then use what the measurements reveal to expand missing areas. Retain unmeasured candidates as hypotheses. No universal candidate count or measured percentage proves sufficient coverage.
4. State a stopping reason: core intents and leading alternatives are covered, successive waves have diminishing relevant discoveries, or a declared budget/provider limitation prevents more work. List remaining gaps and their likely decision impact. Do not silently turn a limited sample into a final claim of optimality.

`keywords.md` must summarize source diversity, candidate/measured counts, rejected concepts, unresolved queries and readiness (`exploratory` or `ready for selection`). A small focused app can justify a compact pool; a broad app may need substantially more. Neither 40 candidates nor 100 measured queries is an automatic pass.

## Intent groups

| Intent | Meaning | Typical use |
|---|---|---|
| `broad` | Category-level discovery | Track reach; avoid overcommitting scarce metadata space |
| `feature` | Specific capability | Connect product evidence to direct demand |
| `problem_intent` | Desired outcome or pain | Capture solution-seeking searches |
| `long_tail` | Narrow multi-concept phrase | Find precise, often lower-volume opportunities |

Aim for coverage across all four groups, not equal quotas. A specialized app may legitimately emphasize feature and long-tail candidates.

## Sources

Derive candidates from:

- category and synonyms;
- every confirmed core feature and user-visible feature label;
- user pains and desired outcomes;
- audience/context combinations;
- benchmark App Names and subtitles;
- review vocabulary;
- uncovered product differentiators.

Do not turn every word in competitor copy into a candidate. Exclude competitor brands, unsupported capabilities, vague adjectives, articles, and queries with no plausible user intent.

## Priority

- P0: essential discovery term or defensible moat signal with direct product evidence.
- P1: relevant term likely worth measuring and potentially using.
- P2: exploratory or adjacent term worth monitoring.

For each candidate, include its intent, priority, evidence/source, and rationale. Preserve phrases here because keyword tools measure queries; decomposition into App Store keyword tokens happens during optimization.

## Output quality

- Normalize casing and whitespace for deduplication.
- Keep distinct singular/plural forms only when the measurement tool treats them separately or the locale requires it.
- Never attach estimated popularity/difficulty without measured data.
- Recommend a search order: P0 first, then missing benchmark signals, then product moats, then exploratory terms.
