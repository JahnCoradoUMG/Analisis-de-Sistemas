from fastapi import APIRouter, status

from app.models.schemas import CheckIn, CheckInCreate
from app.services.checkin_service import CheckInService

router = APIRouter(tags=["check-in"])


@router.post("/check-in", response_model=CheckIn, status_code=status.HTTP_201_CREATED)
def create_checkin(payload: CheckInCreate) -> CheckIn:
    return CheckInService.create(payload)
