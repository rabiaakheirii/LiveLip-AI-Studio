# Architecture (Phase 4)

## Reliability and lifecycle
- Structured startup/shutdown via `AppLifecycle`.
- Worker cancellation and timeout-aware stop in `WorkerManager`.
- Retry helper + error boundaries around stream worker loops.

## Observability
- Configurable structured logging.
- Diagnostics APIs for capabilities and stream state.
- Stream metrics (queue pressure, dropped frames, AV drift).

## Stream pipeline
- capture -> audio -> inference -> publisher worker loops.
- bounded queues with old-frame drop behavior.
- fallback to degraded mode when lipsync engine fails.

## Compatibility
- Existing Phase 1/2/3 routes and event model preserved.
- New diagnostics and metrics routes are additive.
