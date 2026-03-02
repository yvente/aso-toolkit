# ASO Research

You are an expert App Store Optimization strategist. Follow this 5-step workflow to produce a competitor analysis and ASO growth strategy report.

## Arguments

Parse the following from: $ARGUMENTS

- `--code-path <path>` — App source code path or directory containing APP_BRIEF.md (defaults to current working directory if not provided)
- `--locale <locale>` — Target App Store locale (default: en-US)
- `--refresh-brief` — Force re-scan source code and overwrite existing `APP_BRIEF.md`

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

**Output files** (written to `--code-path`, which defaults to current directory):
- `APP_BRIEF.md` — app profile; created when built from source code or user description; shared with `/aso-optimize`
- `ASO_RESEARCH.md` — full strategy report; written at the end of Step 5

---

## Step 1 · Build App Profile

Resolve `--code-path`: if not provided, use the current working directory. All file reads and writes use this resolved path.

Determine the app's identity using the following priority order:

### Priority 1 — APP_BRIEF.md exists in `--code-path` and `--refresh-brief` is NOT set

Read all sections (Core Features, Target Users, Key Differentiators). Identify app category (e.g. "Photo Editing", "Health & Fitness", "Productivity").

### Priority 2 — No APP_BRIEF.md in `--code-path`, OR `--refresh-brief` is set

Scan the source code at `--code-path`. Focus on main feature files, views, onboarding flows, and UI copy. Skip assets, tests, and third-party libraries. Extract Core Features, Target Users, Key Differentiators, and app category.

If no recognizable app source code is found (e.g. the directory is empty or contains only non-app files), fall through to Priority 3.

Otherwise, write the extracted profile to `APP_BRIEF.md` at `--code-path` before proceeding, using the same format as `/aso-optimize` (sections: Core Features, Target Users, Key Differentiators, Recent Changes). Fill `Last updated` with today's date. Leave `Recent Changes` as an empty template — it is maintained by the user, not extracted from code.

Inform the user: `` `APP_BRIEF.md` created (or updated) at `<path>`. Future runs of `/aso-research` and `/aso-optimize` will use this file instead of scanning source code. Re-run with `--refresh-brief` after major feature updates. ``

### Priority 3 — No recognizable app code found

Ask the user:

> Please describe your app: What does it do? Who is it for? What makes it different from alternatives? Which App Store category does it belong to?

Use the response to build the profile, then write it to `APP_BRIEF.md` at `--code-path` using the same format as Priority 2. Inform the user where the file was saved.

**Output a Product Profile before proceeding:**
- App category
- Core features (bullet list)
- Target users
- Key differentiators / USP

---

## Step 2 · Discover Competitor Candidates

Using the app category and core features from Step 1, perform **at least 4–5** targeted searches in the language of `--locale` to maximize coverage. Vary query angles — functional, aesthetic, and audience-specific:

> "[app category] app App Store [locale language] [current year]"
> "[core feature 1] [core feature 2] iOS app"
> "best [app category] app [current year]"
> "[aesthetic or visual descriptor] [core feature] app iPhone"
> "[target user type] [app category] app iOS"

If `--locale` targets a non-English market, also search in the target language (e.g. Chinese, Japanese) to surface locally popular apps that may not rank in English searches.

After the web searches, use the **iTunes Search API** to find additional candidates and confirm App IDs:

```
https://itunes.apple.com/search?term=<url-encoded-query>&country=<country>&entity=software&limit=10
```

Derive `<country>` from `--locale` (e.g. `en-US` → `us`, `zh-Hans` → `cn`, `ja` → `jp`).

For each candidate found, collect:
- App name
- App ID (numeric, from the App Store URL or iTunes API response)
- App Store URL (`apps.apple.com`)
- Rating count (proxy for relative size — download numbers are not public)
- One-line description of what it does

Aim to identify **10–15 candidates** before moving to segmentation.

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
- **Should not overlap with Benchmark Competitors** — if a Benchmark app is also a category leader, prefer selecting a different, broader reference (e.g. a top-ranked app in an adjacent category that shares the same target user)

Purpose: learn conversion and visual strategy from them — not for keyword competition. Think of these as the "visual bar" users already hold in their heads.

For each selected app note: which group, why selected, rating count, and App Store URL.

---

## Step 4 · Analyze Each Group

### Benchmark Competitors Analysis

For each benchmark competitor:
1. Fetch their metadata via the **iTunes Lookup API** (preferred over fetching the App Store page directly, which is JS-rendered and may not expose full metadata):
   ```
   https://itunes.apple.com/lookup?id=<appId>&country=<country>
   ```
   Extract: `trackName` (App Name), `subtitle`, first 170 chars of `description`, `averageUserRating`, `userRatingCount`.
2. Note keyword patterns visible in their App Name, Subtitle, and description opening
3. Identify which features they emphasize that you share (overlap) and which you don't (gaps)

Close with:
> Recommended next step: export keyword CSVs for these apps from Astro (or a similar keyword research tool) and pass them to `/aso-optimize` via `--competitors` for full data-driven keyword gap analysis.

### Reference Competitors Analysis

For each reference competitor:

1. Use the **iTunes Lookup API** as the primary source for screenshot URLs — App Store pages are JS-rendered and screenshot URLs are not present in the HTML:
   ```
   https://itunes.apple.com/lookup?id=<appId>&country=<country>
   ```
   The response contains a `screenshotUrls` array. Use the first 3 entries as the download URLs.
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

4. Fetch App Store reviews filtered to most critical using the **iTunes RSS feed** — do not rely on web search for this, as search results return second-hand summaries rather than real user text:
   ```
   https://itunes.apple.com/rss/customerreviews/page=1/id=<appId>/sortby=mostcritical/json
   ```
   Read the response and identify the top 2–3 recurring complaints — these are differentiation opportunities for your app. If the RSS feed returns no results, fall back to searching `site:apps.apple.com/[country]/app "[App Name]" reviews` and note that the data is from secondary sources.

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

Rules:
- Exclude any term (or its stem) already present in the App Name candidates or Subtitle — Apple indexes those fields automatically, so repeating them wastes characters
- For each App Name candidate above, note which keyword pack terms become redundant so the user can swap them out once a final name is chosen

**First 3 screenshots strategy**
Based on reference competitor analysis. For each screenshot provide:
- **Scene** — what UI or lifestyle moment to show
- **Headline copy** — primary text (≤ 6 words) and secondary text (≤ 12 words)
- **Device frame** — with iPhone shell (builds trust / contextualizes UI) or without (maximizes visual real estate); note which reference competitors use which and what fits this app's tone
- **Resolution target** — 6.9" (1320 × 2868 px, iPhone 16 Pro Max) as the master; 6.5" can be auto-scaled
- **Localization** — if the app has non-English localizations, flag whether the headline copy needs translation variants
- **Rationale** — why this message order matches the user decision funnel

---

After outputting the report, write it to `ASO_RESEARCH.md` in the same directory as `APP_BRIEF.md` (i.e. `--code-path` or current directory). Prepend the following metadata line as the very first line of the file, before the report content:

```
> Locale: <locale>
```

Inform the user: "Report saved to `<path>/ASO_RESEARCH.md`."
