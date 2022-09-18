from fastapi import APIRouter, Depends

from src.app.api.core.dependencies import get_service
from src.app.api.v1.auth.schemas.req_schemas import TokenReq
from src.app.api.v1.auth.schemas.resp_schemas import TokenResp
from src.app.core.services.jwt import JWTService
from src.app.core.services.users import UsersService

router = APIRouter(prefix="/auth")


@router.post(path="/tokens/", response_model=TokenResp, name="tokens pair")
async def tokens(
    data: TokenReq,
    user_service: UsersService = Depends(get_service(UsersService)),
    jwt_service: JWTService = Depends(get_service(JWTService)),
) -> dict:
    """Get new access, refresh tokens [Based on email, password]"""

    user = await user_service.get_authenticated_user(email=data.email, password=data.password)

    new_tokens = jwt_service.create_tokens_pair(  # noqa
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
async def tokens_refreshed(
    refresh_data: dict = Depends(JWTService.refresh_auth_data),
    user_service: UsersService = Depends(get_service(UsersService)),
    jwt_service: JWTService = Depends(get_service(JWTService)),
) -> dict:
    """Get new access, refresh tokens [Granted by refresh token in header]"""

    user = await user_service.get_first(filter_data={"uuid": refresh_data["uuid"]})

    new_tokens = jwt_service.create_tokens_pair(  # noqa
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
