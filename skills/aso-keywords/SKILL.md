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

Generate 40–60 unique candidates across `broad`, `feature`, `problem_intent`, and `long_tail`; assign evidence-backed P0/P1/P2 priority; keep terms in the target storefront language; and preserve phrases useful for rank lookup. Never invent features, search volume, difficulty, rank, or traffic.

Write:

```text
aso/versions/<target-version>/<locale>/keywords.md
aso/versions/<target-version>/<locale>/keyword-measurements-<YYYY-MM-DD>.csv
```

Always create `keywords.md`. Create the dated CSV only when real measurements were obtained or a genuine measurement dataset was formed; do not create an empty placeholder. Keep conclusions locale-specific and never copy unverified metrics across locales. Report exact paths, candidate count, and measurement provenance.
