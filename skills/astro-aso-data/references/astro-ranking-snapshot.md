# Astro ranking snapshot for Storeward

Use this contract when exporting tracked iPhone keyword observations for a Storeward experiment or reading them for `aso-learn`. The selection input `keyword-measurements-<date>.csv` remains a separate artifact for popularity and difficulty.

## Export

Write UTF-8 CSV to `aso/versions/<version>/<locale>/keyword-rank-snapshots-<version>-<storefront>.csv` using a CSV writer that quotes commas, quotes and newlines. Use the exact header below for new exports.

```csv
appStoreId,storefront,platform,keyword,rank,lastUpdate
1234567890,US,iphone,"video compressor, offline",1000,2026-11-06T09:00:00Z
1234567890,US,iphone,"video compressor, offline",22,2026-11-23T09:00:00Z
```

- Read the numeric App Store ID and storefront from the target and verify them against Astro. All rows must use one App ID, one uppercase storefront code and `iphone`. Localization such as `en-US` is distinct from storefront `US`.
- Write one row per keyword and actual Astro observation time. Use the timestamp returned by Astro for that observation, with an ISO 8601 offset or `Z`. UTC normalization is fine. The export time and the date when the file was created are never observation times.
- Use the target app's tracked ranking data. Ranks `1…999` are positions, `1000` means outside Astro's tracked chart, and an empty rank means unknown. An unknown rank needs a real observation time to be included. A current snapshot or a live App Store search cannot reconstruct missing history.
- Include all available observations for the requested window. Before and after observations may share a file and are assigned by actual observation date. Keep notes and coverage summaries outside the CSV. Report the actual date range and missing baseline observations separately.
- Remove exact duplicate observations. A conflict for the same normalized keyword and observation time must be resolved against Astro before delivery. Do not silently choose a rank. Keep each file within 1 MB and 1,000 observations; split larger exports by observation date.

Run the Astro skill's bundled validator before delivering or importing the CSV. It checks the header, target identity, rank, timestamp and duplicate keys.

```bash
python3 <astro-skill-root>/scripts/validate_rank_snapshot.py <file.csv> --app-id <numeric-app-id> --storefront <CC>
```

The validator checks shape and scope. Actual observed values must come from Astro. To import manually use Storeward's **导入 Astro 排名 CSV**. If Storeward MCP is connected, `import_aso_keyword_snapshot` accepts the same CSV text. For review, compare the same keyword, storefront and device across the actual release window. A missing rank is unavailable evidence, and two observations outside the tracked chart do not establish a ranking change.
