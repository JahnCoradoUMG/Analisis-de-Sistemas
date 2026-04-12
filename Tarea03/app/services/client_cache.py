from redis.asyncio import Redis

from app.core.config import CACHE_TTL_CLIENT_SECONDS


def client_cache_key(client_id: str) -> str:
    return f"gymflow:client:{client_id}"


async def get_client_json(redis: Redis, client_id: str) -> str | None:
    return await redis.get(client_cache_key(client_id))


async def set_client_json(redis: Redis, client_id: str, payload_json: str) -> None:
    await redis.set(
        client_cache_key(client_id),
        payload_json,
        ex=CACHE_TTL_CLIENT_SECONDS,
    )
