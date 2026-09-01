---
name: aso-optimize
description: Propose and validate App Store metadata for one target version and locale, separating verified live baseline data from the pending proposal and deriving a locale workbook. Use for a concrete metadata experiment; do not use for research or post-release learning.
---

# ASO Optimize

Generate copy-ready metadata and a readable workbook without publishing or marking the proposal live.

## Required context

Require app root, target version, locale, baseline version, and a user-verified live baseline source. Read the shared `aso/APP_BRIEF.md`, then same-directory `research.md`, `keywords.md`, valid measured CSVs, and root `app-profile.json` when present. Do not mix versions or locales.

Read [the shared system specification](references/aso-system-specification.md), then [the optimization method](references/optimization-method.md). Prepare and validate the work directory using the bundled helper:

```bash
python3 <skill-root>/scripts/aso_toolkit.py prepare-version --root <app-root> --target-version <version> --locale <locale>
python3 <skill-root>/scripts/aso_toolkit.py validate-project --root <app-root> --target-version <version> --locale <locale>
```

## Outputs

Write all four outputs to `aso/versions/<target-version>/<locale>/`:

- `optimize.md` with baseline/proposal comparison, character counts, evidence, hypothesis, attribution risk, and release/observation plan;
- `live-<baseline-version>.json` containing only verified online metadata with role `live`;
- `proposed-<target-version>.json` containing the pending metadata with role `proposed`;
- `deliverable.xlsx`, derived from and verified against the proposed JSON.

The proposed JSON is the sole source of truth. Generate one workbook per locale; never make a multilingual combined workbook or maintain Excel independently. Use available spreadsheet capability for workbook creation and verification. If the environment truly cannot create spreadsheets, stop and explicitly report the complete optimize run as blocked; do not omit, fake, or substitute `deliverable.xlsx`.

Validate filename, role, version, locale, field limits, and keyword format:

```bash
python3 <skill-root>/scripts/aso_toolkit.py validate-metadata --file <live-json> --role live --version <baseline-version> --locale <locale>
python3 <skill-root>/scripts/aso_toolkit.py validate-metadata --file <proposed-json> --role proposed --version <target-version> --locale <locale>
```

Use learned thresholds only when evidence supports them. Do not invent a baseline, copy a proposal into a live file, automatically mark a proposal released, overwrite completed versions, or publish to App Store Connect. Preserve existing experiment/profile behavior and append a proposed experiment only after all outputs validate. Finish with output paths, validation/workbook consistency results, and explicit human release status.
