from typing import Optional, List

from src.app.api.core.schemas.resp_schemas import ListResp, UUIDResp


class UserResp(UUIDResp):
    username: Optional[str]
    email: Optional[str]


class UsersListResp(ListResp):
    results: List[UserResp] = []
