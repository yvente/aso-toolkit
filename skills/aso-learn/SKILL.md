---
name: aso-learn
description: Evaluate a released App Store Optimization experiment from before/after metrics and update the cumulative learning profile. Use after an ASO change has collected data; do not use to generate initial metadata or infer outcomes without comparable metrics.
---

# ASO Learn

Turn one released ASO experiment into bounded, cumulative evidence.

## Inputs

- Before and after metrics CSVs for comparable periods.
- `experiment_log.json` containing the evaluated round and locale.
- App root defaults to the current working directory.
- Evaluation window may be explicit; otherwise recommend a window from version changes and data stability.

Read [the shared system specification](references/aso-system-specification.md), then [the learning method](references/learning-method.md).

Resolve the bundled helper at `scripts/aso_toolkit.py` relative to this `SKILL.md`. Validate inputs first:

```bash
python3 <skill-root>/scripts/aso_toolkit.py validate-project --root <app-root> --locale <locale>
python3 <skill-root>/scripts/aso_toolkit.py compare-metrics --before <before.csv> --after <after.csv>
```

## Workflow

1. Select the exact experiment by round and locale; do not assume the last global entry is correct.
2. Verify comparable windows and metric definitions. Flag version changes, seasonality, acquisition changes, insufficient duration, or missing keyword ranks.
3. Calculate app-level deltas and keyword-rank outcomes. Treat correlation as a directional signal, not causal proof.
4. Set attribution scope from the number and type of changed fields.
5. Classify changed keywords as `problem_intent`, `feature`, `broad`, or `long_tail`; score only when adequate rank data exists.
6. Write `aso/ASO_LEARN_<locale>.md` with metrics, attribution limits, patterns, conclusions, and the next single experiment.
7. Update `app-profile.json` with `aso_toolkit.py update-profile`. Deduplicate by `(round, locale)` and recompute statistics from all stored experiments.

## Learning guardrails

- Keep thresholds at defaults for fewer than three evaluated experiments.
- Do not convert missing rank data into failure.
- Do not recommend broad threshold changes from one experiment.
- Preserve raw before/after metrics and the reason for every learned adjustment.

Finish with the report/profile paths, evidence confidence, and the next recommended experiment.
