# Astro ranking snapshots for Storeward

Use the Astro desktop app's ranking CSV format for Storeward experiments and `aso-learn` ranking comparisons. The `keyword-measurements-<date>.csv` selection input has its own contract for popularity and difficulty.

## Export

Save an Astro desktop export as UTF-8 CSV at `aso/versions/<version>/<locale>/keyword-rank-snapshots-<version>-<storefront>.csv`. When collecting observations through Astro MCP, write the same columns in the same order with a CSV writer. Keep unavailable auxiliary fields empty and record collection provenance and coverage alongside the file.

```csv
App Name,App Id,Platform,Keyword,Store Domain,Store,Note,Last Update,Ranking,Change,Popularity,Difficulty,Apps in Ranking,Tags
Example App,1234567890,iphone,"video compressor, offline",us,🇺🇸 US,,2026-11-06 09:00:00 +0000,1000,,,,,
Example App,1234567890,iphone,"video compressor, offline",us,🇺🇸 US,,2026-11-23 09:00:00 +0000,22,,,,,
```

- Set `App Id` to the numeric App Store ID, `Platform` to `iphone`, and `Store Domain` to the two-letter lowercase storefront. Match the experiment using these three fields. `Store` is a display label such as `🇺🇸 US`. The experiment's localization is tracked separately.
- Set `Keyword` and `Ranking` from the tracked observation. Ranks 1 through 999 are positions, 1000 means outside Astro's tracked chart, and an empty rank means unknown. An unknown rank still requires an observation timestamp.
- Write each actual observation time as `yyyy-MM-dd HH:mm:ss ±HHMM` in `Last Update`. UTC with `+0000` is valid. Use Astro's observation time. Preserve earlier observations from the requested window when they exist. A desktop export is a snapshot of the rows and timestamps it contains.
- Deduplicate identical keyword and timestamp pairs. Resolve conflicting ranks against Astro before exporting. Keep each file within 1 MB and 1,000 observations. Split larger exports by observation date.

Run the validator before delivery or import.

```bash
python3 <astro-skill-root>/scripts/validate_rank_snapshot.py <file.csv> --app-id <numeric-app-id> --storefront <CC>
```

Use Storeward's **导入 Astro 排名 CSV** button or the CSV input of `import_aso_keyword_snapshot`. Compare observations for the same keyword, storefront, and device across the actual release windows. Report missing observations and the dates covered. Two results outside the tracked chart provide no evidence of a ranking change.
