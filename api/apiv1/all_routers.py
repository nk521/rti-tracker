from fastapi import APIRouter

from api.apiv1.status.status import router as status_router
from api.apiv1.user.user import router as auth_router
from api.apiv1.rti.rti import router as rti_router

api_router = APIRouter()
api_router.include_router(status_router, prefix="/status", tags=["Status"])
api_router.include_router(auth_router, prefix="/auth", tags=["Session"])
api_router.include_router(rti_router, prefix="/rti", tags=["RTI"])