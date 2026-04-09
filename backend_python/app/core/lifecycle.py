from __future__ import annotations

import logging

from app.core.orchestrator import PipelineOrchestrator

logger = logging.getLogger(__name__)


class AppLifecycle:
    def __init__(self, orchestrator: PipelineOrchestrator) -> None:
        self.orchestrator = orchestrator

    async def startup(self) -> None:
        logger.info("App startup complete")

    async def shutdown(self) -> None:
        logger.info("App shutdown initiated")
        await self.orchestrator.stop_stream()
        await self.orchestrator.stop()
        logger.info("App shutdown complete")
