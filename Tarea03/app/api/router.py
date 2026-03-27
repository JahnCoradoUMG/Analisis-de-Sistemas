from fastapi import APIRouter

from app.api.routes.checkins import router as checkins_router
from app.api.routes.clients import router as clients_router
from app.api.routes.memberships import router as memberships_router
from app.api.routes.payments import router as payments_router

api_router = APIRouter()
api_router.include_router(clients_router)
api_router.include_router(memberships_router)
api_router.include_router(payments_router)
api_router.include_router(checkins_router)
