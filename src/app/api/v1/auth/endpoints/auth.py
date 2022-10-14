from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.app.api.core.schemas.req_schemas import auth_api_key_schema
from src.app.api.v1.auth.schemas.req_schemas import TokenReq
from src.app.api.v1.auth.schemas.resp_schemas import TokenResp
from src.app.core.di_containers import Container
from src.app.core.services.jwt import JWTService
from src.app.core.services.users import UsersService

router = APIRouter(prefix="/auth")


@router.post(path="/tokens/", response_model=TokenResp, name="tokens pair")
@inject
async def tokens(
    data: TokenReq,
    user_service: UsersService = Depends(Provide[Container.users_service]),
    jwt_service: JWTService = Depends(Provide[Container.jwt_service]),
) -> dict:
    """Get new access, refresh tokens [Based on email, password]"""

    user = await user_service.get_authenticated_user(email=data.email, password=data.password)

    new_tokens = await jwt_service.create_tokens_pair(  # noqa
        uuid=str(user.uuid),
        email=user.email,  # type: ignore
        secret=user.secret,  # type: ignore
    )
    tokens_data = {
        "user_data": {"uuid": str(user.uuid), "username": user.username, "email": user.email},
        "access": new_tokens["access"],
        "refresh": new_tokens["refresh"],
    }

    return tokens_data


@router.post(path="/tokens/refresh/", response_model=TokenResp, name="refresh tokens")
@inject
async def tokens_refreshed(
    auth_api_key: str = Depends(auth_api_key_schema),
    user_service: UsersService = Depends(Provide[Container.users_service]),
    jwt_service: JWTService = Depends(Provide[Container.jwt_service]),
) -> dict:
    """Get new access, refresh tokens [Granted by refresh token in header]"""

    refresh_data = await jwt_service.refresh_auth_data(auth_api_key)
    user = await user_service.get_first(filter_data={"uuid": refresh_data["uuid"]})

    new_tokens = await jwt_service.create_tokens_pair(  # noqa
        uuid=str(user.uuid),
        email=user.email,  # type: ignore
        secret=user.secret,  # type: ignore
    )
    tokens_data = {
        "user_data": {"uuid": str(user.uuid), "username": user.username, "email": user.email},
        "access": new_tokens["access"],
        "refresh": new_tokens["refresh"],
    }

    return tokens_data
