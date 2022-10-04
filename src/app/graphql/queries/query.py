from datetime import datetime
from typing import List, Optional

import strawberry
from strawberry.types import Info

from src.app.config.settings import settings
from src.app.core.services.users import UsersService


@strawberry.type
class User:
    id: int
    uuid: Optional[str]
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


@strawberry.type
class Query:
    @strawberry.field
    async def users(self, info: Info, offset: int = 0, limit: int = settings.BATCH_SIZE) -> List[User]:
        users_service = UsersService(request=info.context["request"])
        users, total_count = await users_service.get_users(filter_data={}, offset=offset, limit=limit)
        return users  # type: ignore
