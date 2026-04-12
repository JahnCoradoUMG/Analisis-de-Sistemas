from fastapi import APIRouter, Request, Response, status
from redis.exceptions import RedisError

from app.models.schemas import Client, ClientCreate
from app.services.client_cache import get_client_json, set_client_json
from app.services.client_service import ClientService

router = APIRouter(tags=["clients"])


@router.post("/clients", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate) -> Client:
    return ClientService.create(payload)


@router.get("/clients/{client_id}", response_model=Client)
async def get_client(client_id: str, request: Request, response: Response) -> Client:
    redis_client = getattr(request.app.state, "redis", None)
    if redis_client is None:
        response.headers["X-Cache"] = "BYPASS"
        return ClientService.get_by_id(client_id)
    try:
        cached = await get_client_json(redis_client, client_id)
        if cached is not None:
            response.headers["X-Cache"] = "HIT"
            return Client.model_validate_json(cached)
        client = ClientService.get_by_id(client_id)
        await set_client_json(redis_client, client_id, client.model_dump_json())
        response.headers["X-Cache"] = "MISS"
        return client
    except RedisError:
        response.headers["X-Cache"] = "BYPASS"
        return ClientService.get_by_id(client_id)
