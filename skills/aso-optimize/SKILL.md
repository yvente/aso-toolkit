---
name: aso-optimize
description: Propose and validate localized App Store metadata using an app brief, experiment baseline, and optional keyword CSVs. Use when preparing a concrete metadata experiment; do not use for broad competitor research or post-release outcome analysis.
---

# ASO Optimize

Generate copy-ready metadata and record a reviewable experiment without publishing it.

## Required context

- App root defaults to the current working directory.
- Locale defaults to `en-US`.
- Read `aso/APP_BRIEF.md` and the latest matching locale entry in `experiment_log.json`.
- Optional inputs: own keyword CSV, one or more competitor keyword CSVs, and `app-profile.json`.

Read [the shared system specification](references/aso-system-specification.md) before touching state. Read [the optimization method](references/optimization-method.md) for selection, copy, and risk rules.

Resolve the bundled helper at `scripts/aso_toolkit.py` relative to this `SKILL.md`. Run it before analysis:

```bash
python3 <skill-root>/scripts/aso_toolkit.py validate-project --root <app-root> --locale <locale>
```

If the experiment log does not exist, obtain a user-confirmed baseline instead of inventing current metadata. Legacy metadata CSV may be converted explicitly, but is not a silent substitute.

## Workflow

1. Load current metadata and determine the next locale-specific round.
2. Load learned thresholds only when the profile has enough evidence; otherwise retain defaults.
3. Parse supplied keyword data. Preserve own keywords ranked 1–10, filter other candidates by relevance and thresholds, identify competitor gaps, and classify intent.
4. Produce App Name, Subtitle, Keywords, Promotional Text, Description, and What's New in the locale language. Do not repeat indexed title/subtitle terms in Keywords.
5. Validate field lengths and keyword formatting with `aso_toolkit.py validate-metadata --file <metadata.json>`.
6. Write `aso/ASO_OPTIMIZE_<locale>.md` with before/after counts, intent breakdown, risk analysis, and rationale.
7. Append the approved proposal to `experiment_log.json` using `aso_toolkit.py append-experiment`. Never overwrite history.

## Boundaries

- Do not publish to App Store Connect.
- Separate verified Apple rules from heuristics and date-sensitive market advice.
- Change as few variables as practical per experiment; explain attribution risk when several fields change.
- If `Recent Changes` is empty, omit What's New and tell the user what is missing.

Finish with paths, the recorded round, validation results, and explicit notice that the proposal still requires human review and submission.
