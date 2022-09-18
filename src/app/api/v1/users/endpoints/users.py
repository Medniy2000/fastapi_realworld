from fastapi import APIRouter, Depends

from src.app.api.core.dependencies import get_service
from src.app.api.v1.users.schemas.resp_schemas import UserResp
from src.app.core.services.jwt import JWTService
from src.app.core.services.users import UsersService

router = APIRouter(prefix="/users")


@router.get(path="/me/", response_model=UserResp, name="users:get-current-user-info")
async def get_users(
    user_service: UsersService = Depends(get_service(UsersService)),
    access_data: dict = Depends(JWTService.access_auth_data),
) -> dict:
    user = await user_service.get_first(filter_data={"uuid": access_data["uuid"]})
    return user.dict()
