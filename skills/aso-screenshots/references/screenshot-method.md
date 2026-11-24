# Screenshot Storyboard Method

Use this reference to build `screenshot-plan.md` for one target version and locale.

## Why the first three slots

Prioritize the first three slots for the primary message. Use later slots for supporting evidence or secondary use cases. Choose the sequence using the target audience's questions, the app's positioning, and the available product evidence.

## Slot design

This is a starting sequence for an app with a meaningful first action and adjustable controls. Move a differentiator or proof into slots 2–3 when that better addresses a likely user question. Omit slots that lack a distinct, verified benefit.

| Slot | Job | Real UI to capture |
|---|---|---|
| 1 | Show the outcome a searcher came for | A finished result produced by the app, not a settings or empty state |
| 2 | Show how to start | The first meaningful action with a realistic input |
| 3 | Show what can be adjusted | The core editing/control surface |
| 4–5 | Depth | Proof of quality, differentiating mechanism, or a secondary audience/use case |

One slot carries one benefit. A slot that needs two headlines is two slots or a cut feature claim.

## Headlines

- Write three candidates per slot: short, scannable at thumbnail size, one benefit each, in the target App Store locale.
- Derive candidates from the app's implemented features and the optimized title/subtitle story when `optimize.md` exists; keep wording consistent with the metadata.
- Verify current App Store Connect caption and device-frame requirements when the plan will be executed; treat limits as versioned policy, not fixed facts in this document.

## Visual consistency

- Keep palette, typography, margins, and device framing identical across slots; per-slot styling noise reads as a different app.
- Base composition conventions on the `research.md` screenshot analysis: follow category conventions that aid scanning, break them only where the app genuinely differs.
- Design execution happens in external design tools; the plan specifies canvas sizes from current App Store Connect device requirements.

## Honesty rules

- Every slot must map to an implemented feature with evidence from the source inventory; proposed or device-dependent capabilities stay out until the user confirms they ship.
- Screenshots must reflect real workflows: no competitor UI, no invented data or results the app cannot produce.
- Do not borrow another product's visuals; brand terms of competitors stay out of headlines.

## Localization

- Write headlines and caption notes per locale; never machine-copy one locale's plan as another's.
- Keep the storyboard structure stable across locales while adapting phrasing to native vocabulary from research; expand languages that need different example content rather than translated mockups.
- Record the storefront each plan targets.

## Validation checklist

- Shrunk to phone size, every headline and key UI element is still readable.
- Each slot passes the one-benefit test.
- A viewer can answer "what does this app do?" from slot 1 alone.
- No slot claims an unsupported capability, competitor brand, or unverifiable result.
- The plan states which feature evidence backs each slot.

## Naive-user test

Before design work starts, give the storyboard to someone who has not used the product and ask what the app does and who it is for. Use unclear answers to investigate the slot order, headline, or UI example before investing in design. Repeat after the first design pass with the rendered images.

## Experiment hook

When the app has stable traffic, Apple's Product Page Optimization can test creative variants. Record the tested variant and dates so `aso-learn` can later evaluate the creative change with real observations; do not predeclare a winner.
