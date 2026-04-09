# Deployment Modes

## local (implemented)
- all workers run in-process in backend API service.

## subprocess (placeholder)
- mode exposed in config and diagnostics; implementation boundary prepared.

## remote (guarded)
- remote worker health probe supported via `REMOTE_WORKER_BASE_URL`.
- full task RPC routing is a next step.
