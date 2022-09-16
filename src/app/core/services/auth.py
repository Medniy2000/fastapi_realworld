from fastapi import HTTPException, status
from passlib.context import CryptContext

from src.app.core.services.base import Service


class AuthService(Service):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
