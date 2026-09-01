# Research Method

Use this reference for competitor collection, segmentation, and report details.

## Storefront mapping

Derive an explicit country code from the requested locale. Common mappings include `en-US → us`, `en-GB → gb`, `zh-Hans → cn`, `zh-Hant → tw`, `ja → jp`, `ko → kr`, `de-DE → de`, `fr-FR → fr`, `es-ES → es`, and `pt-BR → br`. Ask when the locale does not determine a storefront safely.

## Candidate discovery

Use at least four complementary query angles in the target language: category, paired features, audience/problem, and current “best apps” lists. For non-English locales, include native-language searches.

Prefer structured Apple endpoints when available:

```text
https://itunes.apple.com/search?term=<encoded>&country=<country>&entity=software&limit=10
https://itunes.apple.com/lookup?id=<app-id>&country=<country>
https://itunes.apple.com/rss/customerreviews/page=1/id=<app-id>/sortby=mostcritical/json
```

Record app ID, canonical App Store URL, name, developer, rating count, rating, current version/update date, and one-line functional summary. Verify important fields against the current response.

## Segmentation

Benchmark competitors must share the primary job-to-be-done. Score:

- Functional overlap: High for the same primary job, Medium for partial overlap, Low for adjacent signal.
- Size match: High within 3× rating count or both under 500 ratings; Medium from 3× to 10×; Low beyond 10×.
- Confidence: High when both dimensions are High; Medium when one is High and the other Medium; otherwise Low.

Reference competitors set the conversion/visual bar and must not duplicate benchmarks. Prefer category leaders or adjacent products serving the same audience.

## Screenshot analysis

Use the first three phone screenshots for the requested storefront. For each, capture headline, visual composition, benefit, device framing, palette, and tone. Then identify cross-app conventions and propose a message sequence: outcome, differentiating mechanism, proof/depth.

Do not download screenshots unless analysis requires local visual inspection. When downloaded, sanitize filenames and keep assets under the active `aso/versions/<target-version>/<locale>/screenshots/` directory.

## Review analysis

Analyze recurring complaints rather than isolated anecdotes. Record approximate recurrence and separate current-version complaints from stale reviews when possible. Never reproduce personal reviewer data.

## Positioning output

Provide three concise options:

1. feature differentiation;
2. audience differentiation;
3. use-case differentiation.

Each option must be supported by product evidence and a competitor gap. Mark it as a hypothesis until the user selects or validates it.
