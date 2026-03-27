from fastapi import APIRouter, status

from app.models.schemas import Client, ClientCreate
from app.services.client_service import ClientService

router = APIRouter(tags=["clients"])


@router.post("/clients", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate) -> Client:
    return ClientService.create(payload)


@router.get("/clients/{client_id}", response_model=Client)
def get_client(client_id: str) -> Client:
    return ClientService.get_by_id(client_id)
