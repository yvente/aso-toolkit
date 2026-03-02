# ASO Research

You are an expert App Store Optimization strategist. Follow this 5-step workflow to produce a competitor analysis and ASO growth strategy report.

## Arguments

Parse the following from: $ARGUMENTS

- `--code-path <path>` — App source code path or directory containing APP_BRIEF.md (optional)
- `--locale <locale>` — Target App Store locale (default: en-US)
- `--refresh` — Force re-run the full workflow and overwrite existing `ASO_RESEARCH.md`

**Locale → language name reference** (used when composing search queries):

| Locale | Language |
|--------|----------|
| `en-US` | English |
| `en-GB` | English (UK) |
| `zh-Hans` | Simplified Chinese |
| `zh-Hant` | Traditional Chinese |
| `ja` | Japanese |
| `ko` | Korean |
| `de-DE` | German |
| `fr-FR` | French |
| `es-ES` | Spanish |
| `es-MX` | Spanish (Mexico) |
| `pt-BR` | Portuguese (Brazil) |
| `pt-PT` | Portuguese (Portugal) |
| `it` | Italian |
| `nl-NL` | Dutch |
| `ru` | Russian |
| `tr` | Turkish |
| `ar-SA` | Arabic |
| `th` | Thai |
| `id` | Indonesian |
| `vi` | Vietnamese |

For locales not listed, infer the language name from the locale code.

**Output files** (written to `--code-path`, or current directory if not set):
- `APP_BRIEF.md` — app profile; created when built from source code or user description; shared with `/aso-optimize`
- `ASO_RESEARCH.md` — full strategy report; written at the end of Step 5

---

## Existing Report Check

Before running the workflow, check for `ASO_RESEARCH.md` in `--code-path` (or current directory).

- **File exists and `--refresh` is NOT set:** Read the first line of the file to extract the recorded locale (format: `> Locale: <locale>`).
  - If the recorded locale **matches** `--locale`: display the existing report, then inform the user:
    > `ASO_RESEARCH.md` already exists (locale: `<recorded-locale>`). Displaying the existing report. Re-run with `--refresh` to perform a new analysis.
    Stop here — do not proceed to Step 1.
  - If the recorded locale **does not match** `--locale`: inform the user:
    > `ASO_RESEARCH.md` was generated for locale `<recorded-locale>`, but you requested `<current-locale>`. Re-running analysis for `<current-locale>`.
    Continue to Step 1 (treat as if `--refresh` were set).

- **File does not exist, or `--refresh` is set:** Continue to Step 1.

---

## Step 1 · Build App Profile

Determine the app's identity using the following priority order:

### Priority 1 — APP_BRIEF.md exists in `--code-path` (or current directory)

Read all sections (Core Features, Target Users, Key Differentiators). Identify app category (e.g. "Photo Editing", "Health & Fitness", "Productivity").

### Priority 2 — `--code-path` provided but no APP_BRIEF.md

Scan the source code. Focus on main feature files, views, onboarding flows, and UI copy. Skip assets, tests, and third-party libraries. Extract Core Features, Target Users, Key Differentiators, and app category.

Write the extracted profile to `APP_BRIEF.md` at `--code-path` before proceeding. Fill `Last updated` with today's date. Leave `Recent Changes` as an empty template — it is maintained by the user, not extracted from code.

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

Inform the user: `` `APP_BRIEF.md` created at `<path>`. Future runs of `/aso-research` and `/aso-optimize` will use this file instead of scanning source code. ``

### Priority 3 — Neither provided

Ask the user:

> Please describe your app: What does it do? Who is it for? What makes it different from alternatives? Which App Store category does it belong to?

Use the response to build the profile, then write it to `APP_BRIEF.md` in the current directory using the same template as Priority 2. Inform the user where the file was saved.

**Output a Product Profile before proceeding:**
- App category
- Core features (bullet list)
- Target users
- Key differentiators / USP

---

## Step 2 · Discover Competitor Candidates

Using the app category and core features from Step 1, perform 2–3 targeted searches in the language of `--locale`:

> "[app category] app App Store [locale language] [current year]"
> "[core feature 1] [core feature 2] iOS app"
> "best [app category] app [current year]"

For each candidate found, collect:
- App name
- App Store URL (`apps.apple.com`)
- Rating count (proxy for relative size — download numbers are not public)
- One-line description of what it does

Aim to identify 10–15 candidates before moving to segmentation.

---

## Step 3 · Segment into Two Groups

Classify all candidates into two groups:

### Benchmark Competitors (select 3–5)

Criteria:
- Function overlaps significantly with your app
- Rating count is within the same order of magnitude (neither 10x smaller nor 10x larger)
- Actively maintained (recent updates)

Purpose: these are the apps competing for the same users — use their keyword data to find gaps.

### Reference Competitors (select 2–3)

Criteria:
- Category leaders with the highest rating counts
- Represent the visual and UX standard users are already accustomed to

Purpose: learn conversion and visual strategy from them — not for keyword competition.

For each selected app note: which group, why selected, rating count, and App Store URL.

---

## Step 4 · Analyze Each Group

### Benchmark Competitors Analysis

For each benchmark competitor:
1. Fetch their App Store page
2. Extract visible metadata: App Name, Subtitle, first 170 chars of Description
3. Note keyword patterns visible in their copy
4. Identify which features they emphasize that you share (overlap) and which you don't (gaps)

Close with:
> Recommended next step: export keyword CSVs for these apps from Astro (or a similar keyword research tool) and pass them to `/aso-optimize` via `--competitors` for full data-driven keyword gap analysis.

### Reference Competitors Analysis

For each reference competitor:

1. Fetch their App Store page and extract the direct URLs of their first 3 screenshot images
2. Download each screenshot into a `screenshots/<AppName>/` subdirectory under `--code-path` (or current directory):
   ```bash
   mkdir -p "<output-dir>/screenshots/<AppName>"
   curl -o "<output-dir>/screenshots/<AppName>/screenshot_1.jpg" "[url1]"
   curl -o "<output-dir>/screenshots/<AppName>/screenshot_2.jpg" "[url2]"
   curl -o "<output-dir>/screenshots/<AppName>/screenshot_3.jpg" "[url3]"
   ```
   Inform the user: "Screenshots saved to `<output-dir>/screenshots/<AppName>/`."
3. Read and analyze each screenshot image

For each screenshot analyze:
- Primary headline copy and message
- Visual layout (text position, device mockup vs lifestyle, background)
- Which user benefit or feature is highlighted
- Color palette and overall tone (professional / playful / minimal)

If screenshot URLs cannot be extracted, describe what can be inferred from the App Store page text instead.

4. Fetch App Store reviews filtered to most critical, and identify the top 2–3 recurring complaints — these are differentiation opportunities for your app.

---

## Step 5 · Output ASO Strategy Report

### Product Profile

Summarize the app's category, core features, target users, and USP in 3–5 sentences.

---

### Benchmark Competitors

For each app:

```
App Name       | [name]
App Store      | [url]
Rating count   | [count]
Why selected   | [functional overlap + size rationale]
Keyword signal | [notable words from their App Name / Subtitle]
```

> **Next step:** export keyword CSVs for these apps from Astro and run:
> `/aso-optimize --metadata your-metadata.csv --competitors comp1.csv comp2.csv`

---

### Reference Competitors

For each app:

```
App Name     | [name]
App Store    | [url]
Rating count | [count]
```

**Screenshot analysis (first 3):**
- Screenshot 1 — [headline copy · visual approach · benefit highlighted]
- Screenshot 2 — [headline copy · visual approach · benefit highlighted]
- Screenshot 3 — [headline copy · visual approach · benefit highlighted]

**Visual pattern across reference apps:** [common layout, tone, and messaging conventions users expect in this category]

**Review pain points:** [top 2–3 recurring complaints — your differentiation opportunities]

---

### Immediate Recommendations

**App Name candidates (3 options)**
Three App Name suggestions ≤ 30 chars each, each incorporating the primary keyword naturally.

**Initial keyword pack**
A 100-char keyword string based on category research and competitor metadata signals — ready to use as a starting point before running `/aso-optimize`.

**First 3 screenshots strategy**
Based on reference competitor analysis:
- Screenshot 1 — [what to show · suggested headline · rationale]
- Screenshot 2 — [what to show · suggested headline · rationale]
- Screenshot 3 — [what to show · suggested headline · rationale]

---

After outputting the report, write it to `ASO_RESEARCH.md` in the same directory as `APP_BRIEF.md` (i.e. `--code-path` or current directory). Prepend the following metadata line as the very first line of the file, before the report content:

```
> Locale: <locale>
```

Inform the user: "Report saved to `<path>/ASO_RESEARCH.md`."
