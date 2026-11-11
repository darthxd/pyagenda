from fastapi import APIRouter

from pyagenda.app.users.router import router as user_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user_router)


@api_router.get("/health")
def health_check():
    return {"message": "ok"}
