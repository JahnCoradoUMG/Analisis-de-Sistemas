from fastapi import APIRouter, status

from app.models.schemas import Payment, PaymentCreate
from app.services.payment_service import PaymentService

router = APIRouter(tags=["payments"])


@router.post("/payments", response_model=Payment, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate) -> Payment:
    return PaymentService.create(payload)
