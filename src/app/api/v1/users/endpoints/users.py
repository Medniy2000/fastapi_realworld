from fastapi import APIRouter, Depends

from src.app.api.core.dependencies import get_service
from src.app.api.core.schemas.req_schemas import ListReq
from src.app.api.core.utils import to_paginated_resp
from src.app.api.v1.users.schemas.resp_schemas import UsersListResp
from src.app.core.services.jwt import JWTService
from src.app.core.services.users import UsersService


router = APIRouter()


@router.get(path="/users", response_model=UsersListResp, name="users:get-users-list")
async def get_users(
    user_service: UsersService = Depends(get_service(UsersService)),
    data: ListReq = Depends(),
    access_data: dict = Depends(JWTService.access_auth_data),
) -> dict:
    limit = data.limit
    offset = data.offset
    users, total_count = await user_service.get_users(limit=limit, offset=offset)
    return to_paginated_resp(users, total_count)
