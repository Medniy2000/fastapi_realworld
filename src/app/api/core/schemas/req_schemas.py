from fastapi import Query
from pydantic import BaseModel

from src.app.config.settings import settings


class BaseReq(BaseModel):
    pass


class ListReq(BaseReq):
    limit: int = Query(default=settings.BATCH_SIZE, gt=0, description="Limit items in query")
    offset: int = Query(default=0, gt=-1, description="Offset items in query")
