from typing import Any, Optional
from fastapi import HTTPException
from pydantic import validate_email

from src.app.config.settings import settings
from src.app.core.models.users import User
from src.app.core.repositories.users import UsersRepository
from src.app.core.services.auth import AuthService
from src.app.core.services.base import Service


class UsersService(Service):
    async def get_users(  # noqa
        self,
        filter_data: Optional[dict] = None,
        order_by: Optional[list] = None,
        limit: int = settings.BATCH_SIZE,
        offset: int = 0,
    ) -> tuple[list[User], int]:

        users_rows = await UsersRepository.get_list(
            filter_data=filter_data, order_by=order_by, limit=limit, offset=offset
        )
        users = [User(**item) for item in users_rows]
        total_count = await UsersRepository.count(filter_data=filter_data)
        return users, total_count

    async def update_or_create_user(self, data: dict) -> User:  # noqa

        row = await UsersRepository.get_first(filter_data={"email": data["email"]})
        if row:
            meta_: dict = row.meta or {}
            meta_.update(data["meta"])
            data["meta"] = meta_
            row = await UsersRepository.update_by_obj(obj=row, data=data)
        else:
            row = await UsersRepository.create(data=data)

        return User(**row.to_dict())

    async def get_by_field(self, value: Any, field: str = "uuid") -> User:  # noqa
        row = await UsersRepository.get_first(filter_data={field: value})
        return User(**row)  # type: ignore

    async def get_authenticated_user(self, email: str, password: str) -> User:
        try:
            email_validated = validate_email(email)[1]
        except Exception:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid value {email}"
            )

        auth_service = AuthService(request=self.request)
        row = await UsersRepository.get_first(
            filter_data={"email": email_validated}
        )
        is_password_verified = await auth_service.verify_password(password, getattr(row, "password_hashed"))
        if not row or not is_password_verified:
            raise HTTPException(
                status_code=422,
                detail="Value email or password is incorrect"
            )
        return User(**row)
