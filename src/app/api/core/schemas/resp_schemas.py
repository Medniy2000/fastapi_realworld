from typing import Optional, List, Any
import uuid
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
    prev: Optional[str]
    next: Optional[str]
    count: int = 0
    results: List[Any] = []
