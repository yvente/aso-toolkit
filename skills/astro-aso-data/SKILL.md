---
name: astro-aso-data
description: Collect Astro keyword popularity, difficulty and tracked rankings for iOS ASO. Use for Astro MCP data, keyword measurements, and Storeward ranking snapshot exports. Verify live ranking claims with Apple’s public iTunes APIs.
---

# Astro ASO Data

## Identity iron rule

Match apps **only by numeric App Store ID** — `appStoreId` in Astro responses, `trackId` in Apple APIs.

- Never identify an app by name or subtitle. A verified real case: competitor `955000203` (LiveBird) shares a byte-identical subtitle with another app, and that match was once mistaken for identity, producing a false ranking claim.
- Astro tools take `appId` (exact) or `appName` (partial); as of astro-mcp-server 2026.13.0 no tool accepts bundleId (checked against schemas). Resolve identity across sources with `https://itunes.apple.com/lookup?id=<trackId>` or `lookup?bundleId=<bundleId>&country=<cc>`.
- **Locale codes must match Apple's registered form exactly** — Apple uses full codes for some languages (fr-FR, de-DE, es-ES, pt-BR, en-US) and bare codes for others (ja, ko, ru, it, zh-Hans/zh-Hant). Saving under the wrong code (e.g. `fr` instead of `fr-FR`) creates an orphan draft whose sync fails with "Apple 当前没有该语言的本地化" issues even though the localization exists under the full code. Verify with `list_aso_locales` before writing.

## Reporting a ranking

A ranking is only reportable from two agreeing sources:

1. **Tracker**: `get_app_keywords` / `get_keyword_performance`. `currentRanking: 1000` means outside the tracked chart (Astro's own definition, not an error). Always report the tracker's `lastUpdate` with the number.
2. **Apple live**: `https://itunes.apple.com/search?term=<kw>&country=<cc>&entity=software&limit=50`, then scan the results for the trackId; array position = live rank within that window (state the window).

Never read self-rank from an Astro SERP position, even with correct identification: Astro SERP ordering drifts 1–2 positions vs Apple live (verified 2026-10-01, single comparison). Astro SERPs are competitor-metadata reference only. If the two sources disagree, report both with timestamps — never pick one silently.

## Observed tool quirks (not visible in schemas)

- `get_app_keywords` returns popularity, difficulty, currentRanking, rankingChange, and appsCount for every tracked keyword in one call — prefer it over per-keyword calls.
- `extract_competitors_keywords` can fail with upstream "error 5" (seen 3× on 2026-10-01). Retry later; never improvise substitute numbers. The same "error 5" can also be **keyword-specific**: certain phrases fail the upstream popularity fetch deterministically while others succeed at the same moment (verified 2026-10-01: `offline voice recorder`, `offline ai voice recorder` failed while 21 sibling words succeeded).
- **`add_keywords` is atomic per call** — if ANY word in the batch fails its popularity fetch, the whole batch is rejected (0 added, verified 2026-10-01: one poison word blocked all 23). When a batch fails, retry word-by-word or in small chunks to isolate poison words; a failed batch does not mean the service is down (test with a generic word like coffee first).
- `get_keyword_suggestions` returned a single irrelevant result in testing; do not rely on it.
- `add_keywords` (max 100/batch) **writes to the user's Astro dashboard — confirm the batch with the user first.** New keywords have no popularity/difficulty until Astro's refresh cycle runs (cadence undocumented; observed around 01:30 UTC and after opening the dashboard). Until then say "pending", never estimate. `remove_keywords` undoes a batch.

## Where this fits (aso-toolkit pipeline)

This skill is the measurement-acquisition step of the ASO loop:

`aso-research` → **astro-aso-data** (this skill: snapshot + candidate measurement) → `aso-keywords` → `aso-optimize` → release → `aso-learn`

`aso-keywords` consumes the measurements CSV written here (its contract — provider, collection date, column meaning — is satisfied by the output conventions below). `aso-learn` later re-reads tracker data for before/after comparisons. This skill ships with aso-toolkit. Use the repository version for Astro collection and exports.

## Output contract (aso-toolkit)

Write measurements to `aso/versions/<version>/<locale>/keyword-measurements-<YYYY-MM-DD>.csv`, leading `#` rows recording provider, tool, app ID, collection date, and column meaning. Never invent popularity, difficulty, rank, or traffic — missing data is null plus a mention in the summary. Conclusions are locale/store-specific; never copy metrics across stores.

If the app's `aso/APP_BRIEF.md` exists, read it first: it holds the app's identity block. When a target app's brief lacks an Identity section, create it (App Store ID via Apple bundleId lookup, bundleId, ASC App Info IDs via storeward `list_app_infos`) **before any data pull** — identity comes from there in every future run, never from names or guesses.

For Storeward experiments and released-version rank comparisons, use the separate [ranking snapshot contract](references/astro-ranking-snapshot.md). Validate the CSV with the bundled script before delivery or import. Exported historical tracker observations keep their original timestamps and provenance. Apply the live verification steps above when making a claim about the current App Store ranking.

## Tools not registered?

Astro MCP tools register at session start. Verify the Astro desktop app is running (port 8089) and `~/.zcode/cli/config.json` → `mcp.servers.astro` exists, then restart the session or check Settings → MCP. Use the raw-HTTP handshake in `references/raw-http-fallback.md` only if the user explicitly asks to proceed without restarting.
