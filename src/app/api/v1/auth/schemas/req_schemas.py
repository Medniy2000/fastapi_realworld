from src.app.api.core.schemas.req_schemas import BaseReq


class TokenReq(BaseReq):
    email: str
    password: str
