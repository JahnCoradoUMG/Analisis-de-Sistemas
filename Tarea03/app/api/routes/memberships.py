from fastapi import APIRouter, status

from app.models.schemas import Membership, MembershipCreate
from app.services.membership_service import MembershipService

router = APIRouter(tags=["memberships"])


@router.post(
    "/memberships",
    response_model=Membership,
    status_code=status.HTTP_201_CREATED,
)
def create_membership(payload: MembershipCreate) -> Membership:
    return MembershipService.create(payload)
