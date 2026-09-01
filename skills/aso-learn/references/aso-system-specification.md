# ASO Toolkit System Specification

This is the canonical cross-skill contract. Skill-specific methods may add detail but must not redefine these structures.

## Lifecycle

```text
aso-project-init
  → aso-research
  → aso-keywords
  → aso-optimize
  → release and collect comparable metrics
  → aso-learn
  → repeat optimize/learn
```

Research is refreshed after meaningful product or market changes. Keyword generation is optional when measured keyword data already exists.

## Project layout

```text
<app-root>/
├── aso/
│   ├── README.md
│   ├── STRUCTURE.md
│   ├── APP_BRIEF.md
│   ├── ASO_RESEARCH_<locale>.md
│   ├── ASO_KEYWORDS_<locale>.md
│   ├── ASO_OPTIMIZE_<locale>.md
│   ├── ASO_LEARN_<locale>.md
│   ├── screenshots/
│   └── metadata/
├── experiment_log.json
└── app-profile.json
```

`APP_BRIEF.md` and files under `aso/metadata/` are user-maintained inputs. Reports are generated artifacts. `experiment_log.json` and `app-profile.json` are machine-maintained but human-reviewable state.

## Locale rules

- Use BCP 47/App Store locale identifiers such as `en-US`, `zh-Hans`, or `ja`.
- Report filenames always include the locale.
- Metadata and keyword candidates use the target storefront language.
- Storefront country is derived explicitly and recorded; language alone is not evidence of storefront behavior.

## Metadata object

Every snapshot contains:

```json
{
  "app_name": "",
  "subtitle": "",
  "keywords": [],
  "promotional_text": "",
  "description": "",
  "whats_new": ""
}
```

Keywords are stored as an array of individual strings in JSON. They are rendered comma-separated without spaces only for App Store submission.

Default validation limits:

| Field | Characters |
|---|---:|
| App Name | 30 |
| Subtitle | 30 |
| Keywords rendered field | 100 |
| Promotional Text | 170 |
| Description | 4000 |
| What's New | 4000 |

Treat limits and platform indexing behavior as versioned policy. When accuracy matters, verify current Apple documentation before presenting them as current rules.

## Experiment log

```json
{
  "schema_version": 1,
  "app_id": "",
  "app_name": "",
  "exported_at": "2026-01-01T00:00:00Z",
  "before_version": "",
  "after_version": "",
  "entries": [
    {
      "round": 1,
      "date": "2026-01-01",
      "locale": "en-US",
      "metadata_before": {},
      "metadata_after": {},
      "changes": {
        "app_name": {"changed": false},
        "subtitle": {"changed": false},
        "keywords": {"changed": false, "added": [], "removed": []},
        "promotional_text": {"changed": false},
        "description": {"changed": false},
        "whats_new": {"changed": false}
      }
    }
  ]
}
```

### State transitions

- The latest locale-specific `metadata_after` is the next round's baseline once the user confirms it went live.
- A proposed but unpublished round must be identified as proposed in the report; never silently treat it as live performance baseline.
- Append entries; never replace history.
- Round numbers increase per locale. `(round, locale)` is unique.
- Keyword additions/removals are set differences over normalized keyword arrays.

## Learning profile

```json
{
  "schema_version": 1,
  "app_name": "",
  "experiment_history": [],
  "keyword_type_stats": {
    "problem_intent": {"success_rate": null, "avg_outcome_score": null, "outcome_scores_list": [], "count": 0},
    "feature": {"success_rate": null, "avg_outcome_score": null, "outcome_scores_list": [], "count": 0},
    "broad": {"success_rate": null, "avg_outcome_score": null, "outcome_scores_list": [], "count": 0},
    "long_tail": {"success_rate": null, "avg_outcome_score": null, "outcome_scores_list": [], "count": 0}
  },
  "thresholds": {
    "min_popularity": 20,
    "max_difficulty": 70,
    "confidence": "low_confidence",
    "last_updated_by_experiment": null,
    "note": "Defaults until at least three evaluated experiments."
  },
  "preferred_keyword_types": []
}
```

Recompute aggregate statistics from experiment history rather than incrementally mutating totals. Replace an existing history record with the same `(round, locale)` so reruns remain idempotent.

## Keyword intent taxonomy

- `problem_intent`: describes the problem or desired outcome.
- `feature`: names a concrete capability.
- `broad`: generic category discovery.
- `long_tail`: a specific multi-concept query with narrow intent.

Classification is semantic, not determined by volume or difficulty.

## State ownership

- Initialization may create templates and an empty learning profile.
- Research owns the product brief only when creating or explicitly refreshing it.
- Optimize owns experiment-log proposals.
- Learn owns evaluated history and learned profile statistics.
- No skill publishes metadata or changes App Store Connect without a separate explicit user request and an appropriate connected tool.
