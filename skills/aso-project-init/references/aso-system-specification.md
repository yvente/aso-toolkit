# ASO Toolkit System Specification

This is the canonical 0.3.0 cross-skill contract. Skill-specific methods may add detail but must not redefine these paths, roles, or state transitions.

## Lifecycle

```text
aso-project-init
  → aso-research
  → aso-keywords
  → aso-optimize
  → human review and App Store release
  → collect comparable observed data
  → aso-learn
  → start the next target version without changing completed history
```

Research may be refreshed after meaningful product or market changes. Keyword generation is optional when valid measured keyword data already exists for the same version and locale.

## Project layout

```text
<app-root>/
├── aso/
│   ├── README.md
│   ├── STRUCTURE.md
│   ├── APP_BRIEF.md
│   └── versions/
│       └── <target-version>/
│           ├── en-US/
│           │   ├── research.md
│           │   ├── keywords.md
│           │   ├── optimize.md
│           │   ├── live-<baseline-version>.json
│           │   ├── proposed-<target-version>.json
│           │   ├── keyword-measurements-<date>.csv
│           │   ├── deliverable.xlsx
│           │   ├── screenshots/
│           │   └── learn.md
│           ├── ja/
│           └── zh-Hant/
├── experiment_log.json
└── app-profile.json
```

The tree shows possible lifecycle artifacts, not initialization output. Create a file or `screenshots/` only when the workflow actually produces content. Initialization creates `aso/README.md`, `aso/STRUCTURE.md`, `aso/APP_BRIEF.md`, `aso/versions/`, and `app-profile.json`; it does not create empty reports, metadata, workbooks, screenshots, learning files, or `experiment_log.json`.

`APP_BRIEF.md` is the one long-lived app-wide input. Do not copy it into version or locale directories. Every version-dependent research artifact, measurement, proposal, screenshot, deliverable, and learning report belongs in `aso/versions/<target-version>/<locale>/`.

`<target-version>` is the version being prepared for release. It is a safe single directory name, not necessarily strict SemVer. `<locale>` is an App Store locale such as `en-US`, `ja`, or `zh-Hant`. Both reject slashes, backslashes, `..`, whitespace, absolute paths, and path traversal.

Completed version directories are immutable history. A new optimization round uses a new target-version directory; never overwrite a completed older version.

Do not add parallel status trees such as `drafts/`, `archive/`, `current/`, `shared/`, or `exports/`. `experiment_log.json` and `app-profile.json` remain in the app root.

## Artifact ownership

- Project init owns the shared ASO documentation, brief template, `versions/` directory, and initial app profile.
- Research writes `research.md` and evidence under the same target-version/locale directory.
- Keywords writes `keywords.md` and writes `keyword-measurements-<YYYY-MM-DD>.csv` only when real measurements were obtained or formed.
- Optimize writes `optimize.md`, one live baseline snapshot, the proposed snapshot, and `deliverable.xlsx` in the same directory.
- Learn writes `learn.md` only after release and real observations, then safely updates root `experiment_log.json` and `app-profile.json`.
- No skill publishes metadata or changes App Store Connect without a separate explicit request and an appropriate connected tool.

## Locale isolation

- Use App Store locale identifiers and record the target storefront country explicitly.
- Keep metadata, research evidence, measurements, conclusions, and the workbook isolated by locale.
- Never use one locale's keyword measurements as proof for another locale.
- Each locale has its own `deliverable.xlsx`; do not create a combined multilingual workbook.

## Metadata snapshots

Metadata fields live under a role-aware wrapper so tooling can distinguish observed live state from a proposal.

### Live baseline

`live-<baseline-version>.json` records metadata verified as live:

```json
{
  "schema_version": 1,
  "role": "live",
  "version": "1.0.0",
  "locale": "en-US",
  "captured_at": "2026-01-01",
  "source": "App Store URL or App Store Connect export",
  "metadata": {
    "app_name": "",
    "subtitle": "",
    "keywords": [],
    "promotional_text": "",
    "description": "",
    "whats_new": ""
  }
}
```

The source and capture date must make the baseline auditable. Never copy proposed content into a live file unless the user confirms it is actually live and the snapshot is recaptured as observed state.

### Proposed metadata

`proposed-<target-version>.json` is the sole source of truth for the pending locale-specific release:

```json
{
  "schema_version": 1,
  "role": "proposed",
  "target_version": "1.1.0",
  "baseline_version": "1.0.0",
  "locale": "en-US",
  "generated_at": "2026-01-02",
  "metadata": {
    "app_name": "",
    "subtitle": "",
    "keywords": [],
    "promotional_text": "",
    "description": "",
    "whats_new": ""
  }
}
```

The filename, role, target version, and locale must agree with the containing directory. `deliverable.xlsx` is a readable delivery layer derived from this JSON, never a separately maintained source. A complete optimize run must generate and verify the workbook against the proposed JSON. If the environment truly lacks spreadsheet creation capability, report the run as blocked; do not omit, fake, or substitute the workbook silently.

Keywords are arrays of individual strings in JSON and render comma-separated without spaces for submission. Default validation limits are:

| Field | Characters |
|---|---:|
| App Name | 30 |
| Subtitle | 30 |
| Keywords rendered field | 100 |
| Promotional Text | 170 |
| Description | 4000 |
| What's New | 4000 |

Treat limits and indexing behavior as versioned policy. Verify current Apple documentation when accuracy depends on current rules.

## Experiment log

The root `experiment_log.json` preserves append-only, locale-specific experiment state. Entries keep `(round, locale)` unique, store validated before/after metadata snapshots, and mark new optimization records as `proposed`. A proposal is not a live baseline. Promote or evaluate it only after confirmed release and observed data.

Round numbers increase per locale. Keyword additions and removals are case-insensitive set differences over normalized arrays. Existing reasonable experiment-log fields remain compatible with 0.2.0.

## Learning profile

The root `app-profile.json` keeps cumulative experiment history, four intent types (`problem_intent`, `feature`, `broad`, `long_tail`), learned statistics, thresholds, and preferred types. Recompute aggregates from history. Replace a history record with the same `(round, locale)` so reruns are idempotent.

Keep default thresholds for fewer than three evaluated experiments. `learn.md` requires a released version and comparable real observations; missing or forecast data must not become a formal learning conclusion.

## Legacy 0.2.x layout

Legacy indicators include root-level `aso/ASO_RESEARCH_<locale>.md`, `ASO_KEYWORDS_...`, `ASO_OPTIMIZE_...`, `ASO_LEARN_...`, plus root `aso/metadata/`, `aso/deliverables/`, or `aso/screenshots/`.

The 0.3.0 helper detects and reports these paths but never moves, deletes, or rewrites them. Migration is manual:

1. Back up the app repository and choose the target version represented by each old artifact.
2. Run `init-project`, then `prepare-version` for each version/locale.
3. Keep the single existing `aso/APP_BRIEF.md` at the ASO root.
4. Move research, keywords, optimization, screenshots, and measured CSVs into the matching target-version/locale directory and rename reports to their 0.3.0 names.
5. Convert verified online metadata to `live-<baseline-version>.json`; convert pending metadata to `proposed-<target-version>.json`. Do not infer which role applies.
6. Regenerate each locale's `deliverable.xlsx` from its proposed JSON.
7. Move a learning report only when the version was released and backed by real observations.
8. Validate the new layout before manually removing old copies. Leave root `experiment_log.json` and `app-profile.json` in place.
