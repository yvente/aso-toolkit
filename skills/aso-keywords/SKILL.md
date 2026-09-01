---
name: aso-keywords
description: Generate a structured, localized App Store keyword candidate set from an existing app brief and optional competitor research. Use before obtaining volume/rank data; do not use to claim keyword popularity or to produce final App Store metadata.
---

# ASO Keywords

Bridge product research and quantitative keyword tooling.

## Inputs

- App root defaults to the current working directory.
- Locale defaults to `en-US`.
- Require `aso/APP_BRIEF.md`.
- Read `aso/ASO_RESEARCH_<locale>.md` when available; warn and continue without it when absent.

Read [the shared system specification](references/aso-system-specification.md) for naming and intent definitions, then read [the candidate method](references/candidate-method.md).

## Workflow

1. Extract only confirmed category, feature, audience, problem, differentiation, and competitor signals.
2. Generate 40–60 unique candidates across `broad`, `feature`, `problem_intent`, and `long_tail`.
3. Assign P0/P1/P2 priority. P0 requires a concrete reason such as direct core-feature relevance, strong competitor signal, missing current coverage, or a defensible product moat.
4. Keep keywords in the target storefront language. Write explanatory prose in the user's language unless requested otherwise.
5. Deduplicate normalized candidates, but preserve meaningful phrases for third-party rank lookup.

Do not invent features, popularity, difficulty, rank, or traffic estimates. This step creates a measurement backlog, not final metadata.

## Output

Write `aso/ASO_KEYWORDS_<locale>.md` with:

- input provenance and generation date;
- intent definitions;
- candidate tables grouped by intent and priority;
- a recommended lookup order for Astro or another keyword tool;
- instructions to export measured CSV data for `$aso-optimize`.

Report the exact path and candidate count.
