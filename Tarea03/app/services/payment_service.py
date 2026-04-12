from fastapi import HTTPException, status

from app.models.schemas import Payment, PaymentCreate
from app.services.client_service import ClientService
from app.services.storage import storage


class PaymentService:
    @staticmethod
    def create(payload: PaymentCreate) -> Payment:
        ClientService.get_by_id(payload.client_id)

        membership = storage.memberships.get(payload.membership_id)
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Membership not found",
            )

        if membership.client_id != payload.client_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Membership does not belong to client",
            )

        payment = Payment(**payload.model_dump())
        storage.payments[payment.id] = payment
        return payment
