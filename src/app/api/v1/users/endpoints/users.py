from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.app.api.core.schemas.req_schemas import auth_api_key_schema
from src.app.api.v1.users.schemas.resp_schemas import UserResp
from src.app.core.di_containers import Container
from src.app.core.services.jwt import JWTService
from src.app.core.services.users import UsersService

router = APIRouter(prefix="/users")


@router.get(path="/me/", response_model=UserResp, name="users:get-current-user-info")
@inject
async def get_users(
    auth_api_key: str = Depends(auth_api_key_schema),
    user_service: UsersService = Depends(Provide[Container.users_service]),
    jwt_service: JWTService = Depends(Provide[Container.jwt_service]),
) -> dict:
    access_data = await jwt_service.access_auth_data(auth_api_key)
    user = await user_service.get_first(filter_data={"uuid": access_data["uuid"]})
    return user.dict()
