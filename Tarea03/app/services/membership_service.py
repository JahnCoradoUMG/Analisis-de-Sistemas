from datetime import datetime

from fastapi import HTTPException, status

from app.models.schemas import Membership, MembershipCreate, MembershipStatus
from app.services.client_service import ClientService
from app.services.storage import storage


class MembershipService:
    @staticmethod
    def create(payload: MembershipCreate) -> Membership:
        ClientService.get_by_id(payload.client_id)

        membership = Membership(**payload.model_dump())
        storage.memberships[membership.id] = membership
        return membership

    @staticmethod
    def get_latest_for_client(client_id: str) -> Membership | None:
        memberships = [
            membership
            for membership in storage.memberships.values()
            if membership.client_id == client_id
        ]

        if not memberships:
            return None

        memberships.sort(key=lambda item: item.created_at, reverse=True)
        return memberships[0]

    @staticmethod
    def ensure_active_for_checkin(client_id: str, at_time: datetime) -> Membership:
        membership = MembershipService.get_latest_for_client(client_id)

        if not membership:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client has no membership",
            )

        if membership.status != MembershipStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Membership is not active",
            )

        if not (membership.start_date <= at_time <= membership.end_date):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Membership is not currently valid",
            )

        return membership
