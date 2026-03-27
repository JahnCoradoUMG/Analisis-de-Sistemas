from fastapi import HTTPException, status

from app.models.schemas import Client, ClientCreate
from app.services.storage import storage


class ClientService:
    @staticmethod
    def create(payload: ClientCreate) -> Client:
        if any(client.email == payload.email for client in storage.clients.values()):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Client email already exists",
            )

        client = Client(**payload.model_dump())
        storage.clients[client.id] = client
        return client

    @staticmethod
    def get_by_id(client_id: str) -> Client:
        client = storage.clients.get(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found",
            )
        return client
