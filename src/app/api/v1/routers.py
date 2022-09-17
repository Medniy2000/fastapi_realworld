from fastapi import APIRouter

from src.app.api.v1.users.endpoints.users import router as user_router
from src.app.api.v1.auth.endpoints.auth import router as auth_router


V1_PREFIX = "v1"

v1_router = APIRouter(prefix=f"/{V1_PREFIX}")
v1_router.include_router(user_router, tags=[f"{V1_PREFIX}:users"])
v1_router.include_router(auth_router, tags=[f"{V1_PREFIX}:auth"])
