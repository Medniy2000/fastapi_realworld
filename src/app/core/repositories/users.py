from src.app.core.db_schemas.users import User
from src.app.core.repositories.base import BasePSQLRepository  # type: ignore


class UsersRepository(BasePSQLRepository):
    MODEL = User
    FIELDS_TO_SELECT = [
        "id",
        "uuid",
        "meta",
        "secret",
        "created_at",
        "updated_at",
        "username",
        "password_hashed",
        "email",
        "phone",
        "gender",
        "birthday",
        "first_name",
        "middle_name",
        "last_name",
        "is_active",
    ]
    FIELDS_ORDER_BY = ["-id"]
