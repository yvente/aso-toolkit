---
name: aso-optimize
description: Prepare first-release or update App Store metadata for one target version and locale, reviewing query coverage and naming scope, separating live evidence from proposals, and deriving a locale workbook. Use for a concrete metadata experiment; do not use for research or post-release learning.
---

# ASO Optimize

Generate copy-ready metadata and a readable workbook without publishing or marking the proposal live.

## Required context

Require app root, target version, locale and an explicit release mode. For an update, require the baseline version and a user-verified live baseline source. For a confirmed first release, use `release_type: "first_release"` with `baseline_version: null`; there is no live baseline to invent. A missing public lookup alone does not establish first-release status. Read the shared `aso/APP_BRIEF.md`, then same-directory `research.md`, `keywords.md`, valid measured CSVs, and root `app-profile.json` when present. Do not mix versions or locales.

Read [the shared system specification](references/aso-system-specification.md), then [the optimization method](references/optimization-method.md). Prepare and validate the work directory using the bundled helper:

```bash
python3 <skill-root>/scripts/aso_toolkit.py prepare-version --root <app-root> --target-version <version> --locale <locale>
python3 <skill-root>/scripts/aso_toolkit.py validate-project --root <app-root> --target-version <version> --locale <locale>
```

## Decision gate

Establish from the brief/user context: acquisition goal, confirmed vs temporary brand, permitted naming changes and product constraints. Reuse existing user decisions; do not assume the working project name is a protected brand or ask again when the strategy is already authorized.

Check the keyword handoff for core-intent coverage, meaningful measurements and unresolved alternatives. Explain selection and compare plausible title/subtitle options within the allowed naming strategy. If critical evidence is missing, label the proposal exploratory and identify the gap; do not call it data-backed, optimal or complete merely because files exist.

## Outputs

Write these outputs to `aso/versions/<target-version>/<locale>/`:

- `optimize.md` with baseline/proposal comparison, character counts, evidence, hypothesis, attribution risk, and release/observation plan;
- For updates only: `live-<baseline-version>.json` containing verified online metadata with role `live`; first releases omit this file.
- `proposed-<target-version>.json` containing the pending metadata with role `proposed`;
- `deliverable.xlsx`, derived from and verified against the proposed JSON.

The proposed JSON is the sole source of truth. Generate one workbook per locale; never make a multilingual combined workbook or maintain Excel independently. Use available spreadsheet capability for workbook creation and verification. If the environment truly cannot create spreadsheets, stop and explicitly report the complete optimize run as blocked; do not omit, fake, or substitute `deliverable.xlsx`.

Validate filename, role, version, locale, field limits, and keyword format:

```bash
# Updates only: validate the verified live snapshot.
python3 <skill-root>/scripts/aso_toolkit.py validate-metadata --file <live-json> --role live --version <baseline-version> --locale <locale>
python3 <skill-root>/scripts/aso_toolkit.py validate-metadata --file <proposed-json> --role proposed --version <target-version> --locale <locale>
python3 <skill-root>/scripts/aso_toolkit.py audit-metadata --file <proposed-json>
# Add --temporary-name <name> when the brief identifies a working name.
```

Technical validation, decision quality review and release readiness are separate results. Audit warnings require review or a reasoned disposition; a full 100-character field with no warnings is not business approval. Near-full keyword usage is normally desirable when it adds qualified coverage; never pad or optimize a character-count objective ahead of relevance.

Use learned thresholds only when evidence supports them. Do not invent a baseline, copy a proposal into a live file, automatically mark a proposal released, overwrite completed versions, or publish to App Store Connect. Preserve existing experiment/profile behavior and append a before/after proposed experiment only for updates with a real baseline and validated outputs. For first releases, keep the hypothesis/observation plan in `optimize.md`; do not feed a fabricated before snapshot to the experiment log. Finish with separate technical checks, selection rationale/limitations, remaining release prerequisites and exact output paths. Apply names to app source or write to App Store Connect only within an explicit request or existing authorization.
