# ASO Optimize

You are an expert App Store Optimization specialist. Follow this 5-step workflow to produce optimized ASO metadata.

## Arguments

Parse the following from: $ARGUMENTS

- `--metadata <path>` — Current ASO metadata CSV (required)
- `--code-path <path>` — App source code path (default: current directory)
- `--keywords <path>` — Own app keyword CSV exported from a keyword research tool e.g. Astro (optional)
- `--competitors <path> [path...]` — Competitor keyword CSVs from a keyword research tool e.g. Astro (optional, supports multiple)
- `--locale <locale>` — Target locale to optimize (default: en-US)
- `--refresh-brief` — Force re-scan source code and overwrite existing APP_BRIEF.md

---

## Step 1 · Understand App Functionality

Check for `APP_BRIEF.md` in `--code-path`.

### Path A — Brief exists and `--refresh-brief` is NOT set

Read all sections from `APP_BRIEF.md` (Core Features, Target Users, Key Differentiators, Recent Changes). Infer the app category from Core Features (e.g. "Photo Editing", "Health & Fitness", "Productivity"). Skip to Step 2.

### Path B — Brief does not exist OR `--refresh-brief` is set

Scan the source code at `--code-path`. Focus on:
- Main feature files and views
- Onboarding and paywall flows
- Any strings or copy that describes the app's purpose

Skip asset files, test files, and third-party libraries.

Extract the following three dimensions from source code and identify the app category (e.g. "Photo Editing", "Health & Fitness", "Productivity"), then **write them to `APP_BRIEF.md`** at `--code-path` before proceeding. Fill `Last updated` with today's date. Leave `Recent Changes` as an empty template — it is maintained by the user, not extracted from code.

```markdown
# App Brief

> Last updated: {today's date}

## Core Features
<!-- What the app does, from the user's perspective -->

## Target Users
<!-- Who uses it and what problem it solves for them -->

## Key Differentiators
<!-- What makes it unique vs alternatives -->

## Recent Changes
<!-- Update before each release. Describe what changed from the user's perspective. -->
<!-- Example: Added dark mode / Improved sync speed / Fixed login issue on iOS 18 -->
```

Inform the user: `APP_BRIEF.md` created (or updated). Future runs will use this file instead of scanning source code. Re-run with `--refresh-brief` after major feature updates.

---

## Step 2 · Load Current ASO Data

### Column identification

The CSV may use any column names. Identify each column using the following three-tier strategy:

**Tier 1 — Known header names (match directly):**

| Field | English | Chinese (ASOMinds) |
|---|---|---|
| Locale | `locale` | `Locale` |
| App Name | `app_name` | `应用名称` |
| Subtitle | `subtitle` | `副标题` |
| Keywords | `keywords` | `关键词` |
| Promotional Text | `promotional_text` | `推广文本` |
| Description | `description` | `描述` |
| What's New | `whats_new` | `此版本的新增内容` |

**Tier 2 — Unknown headers: infer from data content:**

| Data characteristic | Field |
|---|---|
| Values match locale codes (e.g. `en-US`, `zh-Hans`, `ja`) | Locale |
| Short text ≤ 30 chars, appears first among short-text columns | App Name |
| Short text ≤ 30 chars, appears second among short-text columns | Subtitle |
| Comma-separated short words, total ≤ 100 chars | Keywords |
| Short paragraph ≤ 170 chars | Promotional Text |
| Longest text, often contains line breaks | Description |
| Medium-length text, often bullet points or release notes | What's New |

When inferring, report the detected mapping to the user before proceeding:
> Detected column mapping: col1 → Locale, col2 → App Name, … Please confirm or correct.

**Tier 3 — Cannot identify:** stop and list each column with a sample value, ask the user to specify the mapping.

If `--locale` is not found in any row, stop and ask the user to add that locale row before continuing.

### Extract fields for `--locale`

| Field | Limit |
|---|---|
| App Name | ≤ 30 chars |
| Subtitle | ≤ 30 chars |
| Promotional Text | ≤ 170 chars |
| Keywords | ≤ 100 chars (comma-separated, no spaces) |
| Description | ≤ 4000 chars |
| What's New | ≤ 4000 chars |

Note current character counts and flag any fields that are empty or near their limits.

---

## Step 3 · Apply ASO Rules

Core rules are inlined below — no general web search needed.

### Apple Hard Rules

**Indexing:**
- App Name and Subtitle words are automatically indexed — do NOT repeat them in the Keywords field
- Description is NOT indexed for App Store search; it drives conversion, not discovery
- Developer name and in-app purchase names may also be indexed

**Keywords field:**
- Use commas as separators with no spaces (every character counts)
- Use singular OR plural — not both (Apple indexes both from one form)
- Omit articles (a, an, the) and prepositions — wasted characters
- Single words only; multi-word phrases are unnecessary (Apple combines words automatically)
- Competitor brand names are not permitted

**Metadata update rules:**
- Promotional Text can be updated at any time without triggering a new App Store review
- All other fields (Name, Subtitle, Keywords, Description) require a new app version submission

### Category Research

Using the app category identified in Step 1 and the language of `--locale`, perform one targeted search:

> "[app category] App Store ASO keywords [locale language] [current year]"

For example: `photo editing App Store ASO keywords Japanese 2026` for `ja`, or `photo editing App Store ASO keywords Simplified Chinese 2026` for `zh-Hans`.

Extract only insights not already covered by the rules above:
- High-volume category keywords in the target language worth targeting
- Seasonal or trending terms relevant to the category and locale
- Category-specific user intent patterns in the target market

---

## Step 4 · Analyze Keyword Data (if provided)

If neither `--keywords` nor `--competitors` is provided, skip this step. Keyword selection in Step 5 will rely solely on the category research from Step 3.

### Expected CSV formats

**`--keywords` (own app keywords from a keyword research tool e.g. Astro):**

```csv
keyword,popularity,difficulty,rank
habit tracker,45,58,12
daily planner,62,71,
to do list,80,85,4
```

- `rank` — your app's current ranking position; leave empty if not ranking

**`--competitors` (competitor keywords from a keyword research tool e.g. Astro, one file per competitor):**

```csv
keyword,popularity,difficulty,rank
habit tracker,45,58,3
daily planner,62,71,1
focus timer,38,42,7
```

- `rank` — the competitor's ranking position for that keyword

For both files: if column names don't match known names, identify columns by data characteristics:

| Data characteristic | Field |
|---|---|
| Text values (search queries) | `keyword` |
| Numeric 0–100, higher values common | `popularity` |
| Numeric 0–100, distribution differs from popularity | `difficulty` |
| Small integers or empty values | `rank` |

### Filter criteria

Apply to competitor keywords and non-ranking own keywords:
- Popularity > 20 (meaningful search volume)
- Difficulty < 70 (achievable ranking)
- Relevant to app features confirmed in Step 1

### Analysis process

1. **Own keywords** — first, unconditionally preserve any where `rank` ≤ 10 (already in top 10, regardless of popularity or difficulty); then apply the filter to the remaining own keywords
2. **Competitor keywords** — apply the filter, then identify gaps: keywords the competitor ranks for that are absent from your own keywords file; if `--keywords` was not provided, compare against the current Keywords field in `--metadata` instead
3. **Prioritize candidates** by: highest popularity first, then lowest difficulty as a tiebreaker
4. **Decompose phrases** — keyword research tools export multi-word search queries (e.g. `face blur app`); extract the individual words for use in the Keywords field
5. **Exclude** any words already present in App Name or Subtitle

---

## Step 5 · Output Optimized ASO Data

### Writing guidelines

All optimized content must be written in the language of `--locale` (e.g. `ja` → Japanese, `zh-Hans` → Simplified Chinese, `de-DE` → German). Apply these rules while writing each field:

- **App Name** — include the primary keyword naturally; every word is indexed with highest weight
- **Subtitle** — include a secondary keyword; must meaningfully differ from App Name
- **Keywords** — no words already in App Name or Subtitle; use singular or plural (not both); omit articles and prepositions; maximize keyword count within 100 chars
- **Promotional Text** — lead with the strongest user benefit; can be updated anytime without resubmission
- **Description** — front-load key benefits in the first 3 lines (shown before "more" fold); use feature–benefit format, not a feature list; avoid keyword stuffing (Description is not indexed)
- **What's New** — source content from `Recent Changes` in `APP_BRIEF.md`; lead with the most impactful change; write benefit-first ("Now you can…" not "Fixed bug where…"); 2–4 bullet points is enough even though 4000 chars are available; if `Recent Changes` is empty, skip this field and notify the user to update `APP_BRIEF.md` before the next release

### Validation

Before producing output, verify every field stays within its limit. Revise any field that exceeds its limit before proceeding.

### Summary table

```
Field            | Current      | Optimized
-----------------|--------------|----------
App Name         |   xx / 30   |   xx / 30
Subtitle         |   xx / 30   |   xx / 30
Promotional Text |  xxx / 170  |  xxx / 170
Keywords         |   xx / 100  |   xx / 100
Description      | xxxx / 4000 | xxxx / 4000
What's New       | xxxx / 4000 | xxxx / 4000
```

### Optimized values

Output each field's final value in full, ready to copy into App Store Connect.

### Keyword change rationale

List the key additions and removals with reasoning.

If `--keywords` / `--competitors` were provided, cite data:
- Added: `[keyword]` — [e.g. competitor gap, popularity 45 / difficulty 32]
- Removed: `[keyword]` — [e.g. already in Subtitle / popularity 8]

If no keyword data was provided, cite rule or category research:
- Added: `[keyword]` — [e.g. high-volume category term from Step 3 research]
- Removed: `[keyword]` — [e.g. duplicates word in App Name / generic article]
