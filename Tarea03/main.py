import asyncio
import logging
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI, Request

from app.api.router import api_router
from app.core.config import REDIS_URL

logger = logging.getLogger(__name__)

REDIS_CONNECT_ATTEMPTS = 40
REDIS_RETRY_DELAY_SEC = 0.5


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = redis.from_url(
        REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=5,
    )
    app.state.redis = None
    last_error: Exception | None = None

    for attempt in range(1, REDIS_CONNECT_ATTEMPTS + 1):
        try:
            await client.ping()
            app.state.redis = client
            logger.info("Redis listo para cache (intento %s/%s)", attempt, REDIS_CONNECT_ATTEMPTS)
            break
        except Exception as exc:
            last_error = exc
            logger.debug("Redis intento %s fallido: %s", attempt, exc)
            await asyncio.sleep(REDIS_RETRY_DELAY_SEC)
    else:
        logger.warning(
            "Redis no disponible tras %s intentos; API sin cache: %s",
            REDIS_CONNECT_ATTEMPTS,
            last_error,
        )
        await client.aclose()

    try:
        yield
    finally:
        if getattr(app.state, "redis", None) is not None:
            await app.state.redis.aclose()


app = FastAPI(
    title="GymFlow API",
    version="1.1.0",
    description="Gym management API con almacenamiento en memoria y cache Redis (cache-aside).",
    lifespan=lifespan,
)
app.include_router(api_router)


@app.get("/health", tags=["health"])
def health_check(request: Request) -> dict[str, str]:
    redis_up = getattr(request.app.state, "redis", None) is not None
    return {
        "status": "ok",
        "redis": "up" if redis_up else "down",
    }
