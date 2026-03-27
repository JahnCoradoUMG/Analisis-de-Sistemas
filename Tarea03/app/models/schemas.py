from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class MembershipStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    TRANSFER = "transfer"


class ClientCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(default=None, min_length=8, max_length=20)


class Client(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)


class MembershipCreate(BaseModel):
    client_id: str = Field(min_length=1)
    plan_name: str = Field(min_length=3, max_length=80)
    start_date: datetime
    end_date: datetime
    status: MembershipStatus = MembershipStatus.ACTIVE

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, value: datetime, info):
        start_date = info.data.get("start_date")
        if start_date and value <= start_date:
            raise ValueError("end_date must be after start_date")
        return value


class Membership(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    client_id: str
    plan_name: str
    start_date: datetime
    end_date: datetime
    status: MembershipStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)


class PaymentCreate(BaseModel):
    client_id: str = Field(min_length=1)
    membership_id: str = Field(min_length=1)
    amount: Decimal = Field(gt=0)
    method: PaymentMethod
    paid_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("amount")
    @classmethod
    def validate_amount_precision(cls, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"))


class Payment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    client_id: str
    membership_id: str
    amount: Decimal
    method: PaymentMethod
    paid_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)


class CheckInCreate(BaseModel):
    client_id: str = Field(min_length=1)
    checked_in_at: datetime = Field(default_factory=datetime.utcnow)


class CheckIn(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    client_id: str
    membership_id: str
    checked_in_at: datetime

    model_config = ConfigDict(from_attributes=True)
