from __future__ import annotations

import time
from contextlib import contextmanager

from app.models.performance_metrics import PerformanceMetrics


class PerformanceTracker:
    def __init__(self) -> None:
        self.metrics = PerformanceMetrics()
        self._window_start = time.perf_counter()

    @contextmanager
    def time_stage(self, attr: str):
        start = time.perf_counter()
        yield
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        setattr(self.metrics.stage_timing, attr, round(elapsed_ms, 3))

    def on_frame_processed(self) -> None:
        self.metrics.frames_processed += 1
        elapsed = max(0.001, time.perf_counter() - self._window_start)
        self.metrics.fps_actual = round(self.metrics.frames_processed / elapsed, 2)

    def on_frame_dropped(self, count: int) -> None:
        self.metrics.frames_dropped = count

    def update_pressure(self, pressure: float) -> None:
        self.metrics.queue_pressure = pressure

    def set_adaptive_degraded(self, enabled: bool) -> None:
        self.metrics.adaptive_degraded = enabled
