from __future__ import annotations

import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def boundary(name: str):
    try:
        yield
    except Exception:
        logger.exception("Boundary failure: %s", name)
        raise
