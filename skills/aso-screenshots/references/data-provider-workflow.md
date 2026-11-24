# Measurement acquisition and mutation reconciliation

Read when collecting provider data or adding tracking queries. Provider-specific skills/tools remain optional; this reference does not implement their API or override authorization requirements.

## Connect to the actual host

Discover available tools first. A desktop service listening on a port, a configuration in another client, and callable tools in this session are different observations. Inspect the actual client's configuration when available; do not diagnose Codex from another host's config. A reconnect/restart is a troubleshooting hypothesis, not a guaranteed remedy. Use supported fallback access within existing user authorization and tool permissions. Do not repeatedly request permission already granted for the same scope.

## Read before writing

Use read-only tracked queries, competitor extraction and same-market exports first. Extraction results need relevance and brand screening; they are not all suitable candidates. When further tracking writes are needed, prepare a concrete market/platform/query list, explain the mutation and obtain whatever authorization is required by the active provider/tool. Reuse existing authorization for an approved batch and its permitted retries; a larger batch is not automatically covered. A temporary tracker must be explicitly identified and must never be mistaken for the real App Store ID or used to report its rankings.

## Keep a request ledger

Record provider, tool/schema version when available, tracking identity, platform, storefront, exact requested queries, request ID, collection time and raw response. Use unique request IDs when orchestrating calls. Do not parallelize dependent mutations or share ambiguous request/session state. Set a bounded attempt/time budget appropriate to the provider before writing.

Classify each outcome:

- **Confirmed success:** reconcile persisted query identities and returned counts; obtain real measurements or mark scores pending.
- **Confirmed failure:** reconcile any partial writes, then split/retry only confirmed missing queries within the approved set and budget. Isolate reproducible failing queries; preserve their errors.
- **Unknown outcome (timeout/disconnect):** the request may still be processing or committing. Query persisted state, check progress and provider terminal-status/idempotency support. A temporarily absent row is not proof of failure. Do not blindly replay the mutation while its outcome is uncertain. If terminal state cannot be established safely, preserve the unresolved subset and continue unaffected work read-only.

Do not assume a provider batch is atomic or idempotent based on an old note. Read tool contracts and observe current behavior; record discrepancies. A larger client timeout alone is not a duplicate-prevention guarantee. Never delete duplicate dashboard entries as part of read-only reconciliation; apply the provider's deletion authorization rules.

## Normalize evidence, not facts

Keep raw observations. Deduplicate analyses by provider, tracker/platform, storefront and normalized query, retaining collection timestamps. Declare the selection rule for repeated observations; expose conflicting scores or scopes rather than silently taking the highest. Report requested, persisted, unique measured, pending, failed/unknown and duplicate counts separately. Deduplication for analysis is not cleanup of external tracking state.

Missing popularity/difficulty stays null with a reason. A provider's floor score is not zero demand. Scores are not search counts; do not compare country market size from these indices. A phrase observation is evidence for that query only, not an independent volume for every component token. Never create an empty measurement CSV merely to complete the expected file tree.
