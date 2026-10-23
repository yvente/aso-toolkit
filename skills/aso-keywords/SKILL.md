---
name: aso-keywords
description: Generate a structured App Store keyword candidate set for one target version and locale, using same-locale research and optional measured data. Use before final metadata optimization; do not claim unmeasured popularity or mix locale conclusions.
---

# ASO Keywords

Bridge product research and quantitative keyword tooling within one target-version/locale directory.

## Inputs

- Require app root, target version, locale, and shared `aso/APP_BRIEF.md`.
- Read `aso/versions/<target-version>/<locale>/research.md` when available; warn and continue from the brief when absent.
- Use only measurement files applicable to the same locale. Record provider, collection date, and column meaning.

Read [the shared system specification](references/aso-system-specification.md), then [the candidate method](references/candidate-method.md).

Expand across `broad`, `feature`, `problem_intent`, and `long_tail` using native market vocabulary, competitors, reviews and verified product workflows. Choose breadth from the market and assignment; a fixed candidate count, translated template or language-name Cartesian product is not completion. Assign evidence-backed P0/P1/P2 research priority and preserve phrases for lookup. Never invent features, search volume, difficulty, rank, or traffic.

Before handing off to optimization, record coverage, measured/unmeasured scope, unresolved high-impact queries, excluded terms and why another expansion wave would or would not change the selection. If title-driving terms are unmeasured or major intent gaps remain, hand off an explicitly exploratory backlog rather than a measurement-backed recommendation. See the candidate method for this gate.

When fetching provider data or changing tracking, read [measurement workflow](references/data-provider-workflow.md); do not assume batch writes are atomic or replay uncertain writes.

Write:

```text
aso/versions/<target-version>/<locale>/keywords.md
aso/versions/<target-version>/<locale>/keyword-measurements-<YYYY-MM-DD>.csv
```

Always create `keywords.md`. Create the dated CSV only when real measurements were obtained or a genuine measurement dataset was formed; do not create an empty placeholder. Keep conclusions locale-specific and never copy unverified metrics across locales. Report exact paths, candidate count, and measurement provenance.
