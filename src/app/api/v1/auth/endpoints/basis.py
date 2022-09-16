from fastapi import APIRouter, Depends

from src.app.api.v1.auth.schemas.resp_schemas import AccessTokenResp
from src.app.core.services.jwt import JWTService
from src.app.core.services.users import UsersService
from src.app.core.services.utils import get_service

router = APIRouter(prefix="/auth")


@router.post(path="/tokens/access/", response_model=AccessTokenResp, name="tokens_access")
async def tokens_access(
    refresh_data: dict = Depends(JWTService.refresh_auth_data),
    user_service: UsersService = Depends(get_service(UsersService)),
) -> dict:
    """Get new access token [Granted by refresh token in header]"""

    user = await user_service.get_by_field(field="secret", value=refresh_data["secret"])

    user_data = {
        "uuid": str(user.uuid),
        "username": user.username,
        "email": user.email,
        "sid": refresh_data.get("sid"),
    }
    access_token = JWTService.create_access_token(user_data)
    data = {"access_token": access_token}
    return data
