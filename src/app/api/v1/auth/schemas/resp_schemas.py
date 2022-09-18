from typing import Optional

from src.app.api.core.schemas.resp_schemas import BaseResp


class UserDataResp(BaseResp):
    uuid: str
    username: Optional[str]
    email: str


class TokenResp(BaseResp):
    user_data: UserDataResp
    access: str
    refresh: str
