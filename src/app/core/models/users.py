from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic.main import BaseModel


class User(BaseModel):
    id: Optional[int]
    uuid: Optional[UUID]
    meta: Optional[dict]
    secret: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    username: Optional[str]
    password_hashed: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    birthday: Optional[datetime]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    is_active: Optional[bool]
