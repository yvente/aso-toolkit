# Learning Method

Use this reference for metrics comparison, attribution, and profile updates.

Do not begin formal evaluation until the target version/locale is confirmed released and real observed data exists. Otherwise stop without creating `learn.md` or updating cumulative state.

## Comparable inputs

Before/after CSVs must use the same metric definitions, storefront scope, acquisition filters, and sufficiently comparable durations. Normalize metric aliases conservatively and stop when units are ambiguous.

Supported app-level metrics commonly include impressions, product page views, downloads/app units, conversion rate, proceeds, and crashes. Keyword rows may additionally include keyword and rank before/after.

## Evaluation window

An explicit user window wins. Otherwise use these as recommendations, not guarantees:

- 28 days when the version is unchanged and data is stable;
- 42 days for moderate volatility;
- 56+ days after a version change or with high volatility;
- 84 days as a conservative option for noisy or seasonal data.

Call out seasonality, featuring, paid acquisition, pricing, product changes, ratings changes, and tracking changes.

## Attribution scope

- High: one material metadata variable changed and confounders are limited.
- Medium: two related variables changed or moderate confounders exist.
- Low: multiple fields/product/marketing conditions changed.

Never describe observational deltas as causal proof.

## Keyword outcome score

Only score keywords with usable before/after rank data. A bounded default score can combine:

```text
0.40 × normalized rank improvement
+ 0.25 × achieved-rank quality
+ 0.20 × experiment conversion signal
+ 0.15 × relevance/confidence
```

Document each component. Missing rank data yields `null`, not zero.

## Profile policy

Deduplicate experiment history by `(round, locale)`. Recompute intent statistics from all non-null stored outcome scores:

- `avg_outcome_score`: arithmetic mean;
- `success_rate`: proportion at or above 0.5;
- `count`: number of scored keywords;
- `outcome_scores_list`: stored component scores.

Keep thresholds unchanged for fewer than three evaluated experiments. At three to five experiments, confidence may become medium; at six or more it may become high, provided data quality is adequate. Any threshold adjustment must be small, bounded, and explained in `thresholds.note`.

Recommend one next experiment that addresses the largest uncertainty rather than maximizing the number of simultaneous changes.
