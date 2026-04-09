from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def with_retry(
    fn: Callable[[], Awaitable[T]],
    retries: int = 2,
    base_delay: float = 0.2,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> T:
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return await fn()
        except exceptions as exc:  # type: ignore[misc]
            last_exc = exc
            if attempt >= retries:
                break
            await asyncio.sleep(base_delay * (2**attempt))
    assert last_exc is not None
    raise last_exc
