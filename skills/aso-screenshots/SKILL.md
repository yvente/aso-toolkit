---
name: aso-screenshots
description: Plan App Store screenshot storyboards for one target version and locale from verified product features and competitor patterns, prioritizing the first three slots. Use when preparing release creatives or reviewing existing screenshots; do not fabricate screenshots or replace design tools.
---

# ASO Screenshots

Turn verified product capabilities and researched competitor patterns into a per-locale screenshot storyboard that a human can execute in design tools.

## Required context

Resolve or obtain before planning:

- app root, target version, and App Store locale;
- shared `aso/APP_BRIEF.md`;
- `aso/versions/<target-version>/<locale>/research.md` with competitor screenshot analysis when available; use the brief and mark market assumptions as provisional when absent;
- `aso/versions/<target-version>/<locale>/optimize.md` when present, so headlines and metadata tell one story;
- the app source or a product walkthrough the user points at, as evidence for implemented features.

Read [the shared system specification](references/aso-system-specification.md), then [the screenshot method](references/screenshot-method.md). Use the exact target version and locale path shown below. Create its parent directories when ready to save the plan.

## Workflow

1. Inventory implemented, user-visible features from the app source with file evidence; separate proposed or device-dependent capabilities and mark them unusable until confirmed.
2. When research exists, extract the competitor screenshot patterns and message sequence. Note which conventions support the app's positioning and where different examples would help.
3. Lead with the outcome. Order the next slots around the target user's likely questions, using the screenshot method as a starting point. Give each slot a purpose, real UI to capture, and headline options supported by the evidence.
4. Add the validation checklist and the naive-user test script from the screenshot method.
5. Note an optional Product Page Optimization experiment when stable traffic exists, so `aso-learn` can later evaluate the creative change.

A planning run may render a local preview of the storyboard when the host supports it; `screenshot-plan.md` remains the contract.

## Outputs

Write only:

```text
aso/versions/<target-version>/<locale>/screenshots/screenshot-plan.md
```

Create `screenshots/` only when the plan exists. Save exported creative assets there only when the user provides them, with sanitized filenames. Never generate fake device screenshots as deliverables, never claim unimplemented capabilities, and keep each locale's plan isolated. Do not modify app source or publish creatives.

Finish with the exact path created, the feature evidence used, open questions for the user, and the design-tool steps that remain.
