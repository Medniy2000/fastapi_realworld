from src.app.api.core.schemas.resp_schemas import BaseResp


class AccessTokenResp(BaseResp):
    access_token: str
