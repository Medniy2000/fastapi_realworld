import uuid
from typing import List, Any

from pydantic import BaseModel
from pydantic.class_validators import validator


class BaseResp(BaseModel):
    pass


class UUIDResp(BaseResp):
    uuid: uuid.UUID

    @validator("uuid")
    def hexlify_uuid(cls, value: Any) -> str:  # noqa
        return uuid.UUID(str(value)).hex


class ListResp(BaseResp):
    count: int = 0
    results: List[Any] = []
