from app.models.schemas import CheckIn, CheckInCreate
from app.services.client_service import ClientService
from app.services.membership_service import MembershipService
from app.services.storage import storage


class CheckInService:
    @staticmethod
    def create(payload: CheckInCreate) -> CheckIn:
        ClientService.get_by_id(payload.client_id)
        membership = MembershipService.ensure_active_for_checkin(
            payload.client_id, payload.checked_in_at
        )

        checkin = CheckIn(
            client_id=payload.client_id,
            membership_id=membership.id,
            checked_in_at=payload.checked_in_at,
        )
        storage.checkins[checkin.id] = checkin
        return checkin
