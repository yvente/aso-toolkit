---
name: aso-learn
description: Evaluate a released ASO version for one locale from real comparable observations and update cumulative learning state. Use only after release data exists; do not create formal learning from proposals, forecasts, or missing metrics.
---

# ASO Learn

Turn one released target-version/locale experiment into bounded cumulative evidence.

## Gate and inputs

Require confirmation that the target version and locale were released, plus real before/after metrics for comparable periods. Read the same directory's `optimize.md`, live/proposed JSON, measurement files, and any supporting evidence; read root `experiment_log.json` and `app-profile.json`. Select the exact round and locale, never the latest global entry.

If release status is unconfirmed or observed data is absent/incomparable, report what is missing and do not create `learn.md` or update formal learning state.

Read [the shared system specification](references/aso-system-specification.md), then [the learning method](references/learning-method.md). Validate and compare with the bundled helper:

```bash
python3 <skill-root>/scripts/aso_toolkit.py validate-project --root <app-root> --target-version <version> --locale <locale>
python3 <skill-root>/scripts/aso_toolkit.py compare-metrics --before <before.csv> --after <after.csv>
```

Verify comparable definitions, storefronts, filters, durations, and confounders. Calculate app-level deltas and usable rank outcomes, distinguish correlation from causation, classify changed keywords, and preserve missing observations as null rather than failure.

Write `aso/versions/<target-version>/<locale>/learn.md`, then update root `app-profile.json` idempotently with `update-profile` and safely maintain `experiment_log.json` according to its existing append-only design. Never overwrite completed version artifacts. Keep default thresholds for fewer than three evaluated experiments. Finish with paths, release/data evidence, confidence, state updates, and the next single experiment.
