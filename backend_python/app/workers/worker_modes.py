from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WorkerModeStatus:
    mode: str
    supported: bool
    reason: str = ""


def resolve_worker_mode(mode: str, remote_url: str) -> WorkerModeStatus:
    if mode == "local":
        return WorkerModeStatus(mode=mode, supported=True)
    if mode == "subprocess":
        return WorkerModeStatus(mode=mode, supported=False, reason="subprocess worker mode placeholder")
    if mode == "remote":
        return WorkerModeStatus(mode=mode, supported=bool(remote_url), reason="remote URL required" if not remote_url else "")
    return WorkerModeStatus(mode=mode, supported=False, reason="unknown mode")
