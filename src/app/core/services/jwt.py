from loguru import logger
from datetime import datetime, timedelta
from typing import Optional, Dict

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from jose import jwt

from src.app.config.settings import settings
from src.app.core.services.base import Service
from src.app.core.utils.common import generate_str

token_auth_scheme = HTTPBearer()


class JWTService(Service):
    SECRET = settings.SECRET_KEY
    ACCESS_TOKEN_EXPIRES_MINUTES = settings.ACCESS_TOKEN_EXPIRES_MINUTES
    REFRESH_TOKEN_EXPIRES_DAYS = settings.REFRESH_TOKEN_EXPIRES_DAYS
    ALGORITHM = settings.ALGORITHM
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    @classmethod
    def _decode(cls, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token=token, key=cls.SECRET, algorithms=[settings.ALGORITHM])
            return payload
        except Exception as e:  # noqa
            logger.info(e)
            return None

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        user_data = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRES_MINUTES)
        payload = {"user": user_data, "exp": expire}
        encoded_jwt = jwt.encode(payload, cls.SECRET, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_refresh_token(cls, data: dict) -> str:
        user_data = data.copy()
        expire = datetime.utcnow() + timedelta(days=cls.REFRESH_TOKEN_EXPIRES_DAYS)
        payload = {"user": user_data, "exp": expire}
        encoded_jwt = jwt.encode(payload, cls.SECRET, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_tokens_pair(cls, uuid: str, username: str, email: str, secret: str) -> Dict[str, str]:
        sid: str = generate_str()
        access_token_payload = {
            "uuid": uuid,
            "username": username,
            "email": email,
            "sid": sid,
        }
        refresh_token_payload = {
            "secret": secret,
            "sid": sid,
        }
        access_token = JWTService.create_access_token(access_token_payload)
        refresh_token = JWTService.create_refresh_token(refresh_token_payload)
        # TODO save to redis
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @classmethod
    def verify_access_token(cls, token: str) -> dict:
        payload = cls._decode(token)
        if payload:
            user_data = payload.get("user", {})
            expire = payload.get("exp", None)  # noqa: F841
            return user_data
        # TODO verify via redis
        raise cls.exception

    @classmethod
    def verify_refresh_token(cls, token: str) -> dict:
        payload = cls._decode(token)
        if payload:
            user_data = payload.get("user", {})
            expire = payload.get("exp", None)  # noqa: F841
            return user_data
        # TODO verify via redis
        raise cls.exception

    @classmethod
    def access_auth_data(cls, api_auth_scheme: str = Depends(token_auth_scheme)) -> dict:
        return cls.verify_access_token(api_auth_scheme.credentials)  # type: ignore

    @classmethod
    def refresh_auth_data(cls, api_auth_scheme: str = Depends(token_auth_scheme)) -> dict:
        return cls.verify_refresh_token(api_auth_scheme.credentials)  # type: ignore
