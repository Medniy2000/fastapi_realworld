from datetime import datetime
from typing import Optional

from src.app.api.core.schemas.resp_schemas import UUIDResp


class UserResp(UUIDResp):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    username: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    birthday: Optional[datetime]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
