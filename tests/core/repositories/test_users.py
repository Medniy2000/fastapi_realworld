from copy import deepcopy
from typing import Coroutine, AsyncGenerator

import pytest

from src.app.core.repositories.users import UsersRepository
from tests.core.repositories.fixtures import (
    CREATE_USERS_VALID_DATA,
    UPDATE_USER_ROW_VALID_DATA,
    CREATE_USER_ROW_X_VALID_DATA,
)


@pytest.mark.asyncio
async def test_count_empty(async_client: AsyncGenerator) -> None:
    count_before = await UsersRepository.count()
    assert count_before == 0


@pytest.mark.asyncio
async def test_count_not_empty(db_user: Coroutine) -> None:
    _ = await db_user
    count_before = await UsersRepository.count()
    assert count_before == 1


@pytest.mark.asyncio
async def test_get_by_field_id_success(db_user: Coroutine) -> None:
    current_user = await db_user
    user = await UsersRepository.get_first(filter_data={"id": current_user.id})
    assert user.id == current_user.id


@pytest.mark.asyncio
async def test_get_by_field_uuid_success(db_user: Coroutine) -> None:
    current_user = await db_user
    user = await UsersRepository.get_first(filter_data={"uuid": current_user.uuid})
    assert user.id == current_user.id


@pytest.mark.asyncio
async def test_get_by_field_username_success(db_user: Coroutine) -> None:
    current_user = await db_user
    user = await UsersRepository.get_first(filter_data={"username": current_user.username})
    assert user.id == current_user.id


@pytest.mark.asyncio
async def test_get_by_list_success(db_user: Coroutine) -> None:
    await db_user
    users = await UsersRepository.get_list()
    assert isinstance(users, list)
    assert len(users) == 1


@pytest.mark.asyncio
async def test_get_by_list_success_filter() -> None:
    # Prepare users
    for data in CREATE_USERS_VALID_DATA:
        await UsersRepository.create(data)

    # Check users without applied filters
    users = await UsersRepository.get_list()
    assert isinstance(users, list)
    assert len(users) == len(CREATE_USERS_VALID_DATA)
    user_data_to_filter = CREATE_USERS_VALID_DATA[0]

    # Check users with applied filters
    user_email_to_to_filter = user_data_to_filter["email"]
    users_filtered = await UsersRepository.get_list(filter_data={"email": user_email_to_to_filter})
    assert isinstance(users_filtered, list)
    assert len(users_filtered) == 1


@pytest.mark.asyncio
async def test_get_by_list_success_ordering_asc() -> None:
    # Prepare users
    for data in CREATE_USERS_VALID_DATA:
        await UsersRepository.create(data)

    # Check users with applied ordering by id asc
    users = await UsersRepository.get_list(order_by=["id"])
    assert isinstance(users, list)
    # ids = [1, 2, ..]
    assert len(users) == len(CREATE_USERS_VALID_DATA)
    for index, user in enumerate(users):
        assert index + 1 == user.id


@pytest.mark.asyncio
async def test_get_by_list_success_ordering_des() -> None:
    # Prepare users
    for data in CREATE_USERS_VALID_DATA:
        await UsersRepository.create(data)

    # Check users with applied ordering by id desc
    users = await UsersRepository.get_list(order_by=["-id"])
    assert isinstance(users, list)
    assert len(users) == len(CREATE_USERS_VALID_DATA)
    # ids = [.., 2, 1]
    for index, user in enumerate(users):
        assert len(users) - index == user.id


@pytest.mark.asyncio
async def test_get_by_list_success_limit_cause_1() -> None:
    # Prepare users
    for data in CREATE_USERS_VALID_DATA:
        await UsersRepository.create(data)

    # Check users without applied limit
    users = await UsersRepository.get_list(order_by=["id"])
    assert isinstance(users, list)
    assert len(users) == len(CREATE_USERS_VALID_DATA)

    # Check users with applied limit
    users_limited = await UsersRepository.get_list(order_by=["id"], limit=1)
    assert isinstance(users_limited, list)
    assert len(users_limited) == 1

    # Check ordering, limit correct
    user_first = users[0]
    user_limited = users_limited[0]
    assert user_first.id == user_limited.id


@pytest.mark.asyncio
async def test_get_by_list_success_offset_cause_1() -> None:
    # Prepare users
    for data in CREATE_USERS_VALID_DATA:
        await UsersRepository.create(data)

    # Check users without applied limit
    users = await UsersRepository.get_list(order_by=["id"])
    assert isinstance(users, list)
    assert len(users) == len(CREATE_USERS_VALID_DATA)

    # Check users with applied limit
    users_offset = await UsersRepository.get_list(order_by=["id"], offset=1)
    assert isinstance(users_offset, list)
    assert len(users_offset) == 1

    # Check ordering, offset correct
    user_last = users[1]
    user_offset = users_offset[0]
    assert user_last.id == user_offset.id


@pytest.mark.parametrize("data", CREATE_USERS_VALID_DATA)
@pytest.mark.asyncio
async def test_create_user_success(async_client: AsyncGenerator, data: dict) -> None:
    count_before = await UsersRepository.count()
    assert count_before == 0

    user = await UsersRepository.create(data)

    count_after = await UsersRepository.count()
    assert count_after == 1

    assert isinstance(user.id, int) is True
    assert user.uuid is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.meta == data["meta"]  # noqa
    assert user.secret == data["secret"]
    assert user.username == data["username"]
    assert user.password_hashed == data["password_hashed"]
    assert user.email == data["email"]
    assert user.phone == data["phone"]
    assert user.gender == data["gender"]
    assert user.birthday == data["birthday"]
    assert user.first_name == data["first_name"]
    assert user.middle_name == data["middle_name"]
    assert user.last_name == data["last_name"]
    assert user.is_active == data["is_active"]


@pytest.mark.asyncio
async def test_update_user_by_id_data_success(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    assert current_user.meta != UPDATE_USER_ROW_VALID_DATA["meta"]
    assert current_user.secret != UPDATE_USER_ROW_VALID_DATA["secret"]
    assert current_user.username != UPDATE_USER_ROW_VALID_DATA["username"]
    assert current_user.password_hashed != UPDATE_USER_ROW_VALID_DATA["password_hashed"]
    assert current_user.email != UPDATE_USER_ROW_VALID_DATA["email"]
    assert current_user.phone != UPDATE_USER_ROW_VALID_DATA["phone"]
    assert current_user.gender != UPDATE_USER_ROW_VALID_DATA["gender"]
    assert current_user.birthday != UPDATE_USER_ROW_VALID_DATA["birthday"]
    assert current_user.first_name != UPDATE_USER_ROW_VALID_DATA["first_name"]
    assert current_user.middle_name != UPDATE_USER_ROW_VALID_DATA["middle_name"]
    assert current_user.last_name != UPDATE_USER_ROW_VALID_DATA["last_name"]
    assert current_user.is_active != UPDATE_USER_ROW_VALID_DATA["is_active"]

    updated_user = await UsersRepository.update(
        filter_data={"id": current_user.id}, data=UPDATE_USER_ROW_VALID_DATA, return_updated=True
    )

    assert updated_user.id == current_user.id  # noqa
    assert updated_user.meta == UPDATE_USER_ROW_VALID_DATA["meta"]
    assert updated_user.secret == UPDATE_USER_ROW_VALID_DATA["secret"]
    assert updated_user.username == UPDATE_USER_ROW_VALID_DATA["username"]
    assert updated_user.password_hashed == UPDATE_USER_ROW_VALID_DATA["password_hashed"]
    assert updated_user.email == UPDATE_USER_ROW_VALID_DATA["email"]
    assert updated_user.phone == UPDATE_USER_ROW_VALID_DATA["phone"]
    assert updated_user.gender == UPDATE_USER_ROW_VALID_DATA["gender"]
    assert updated_user.birthday == UPDATE_USER_ROW_VALID_DATA["birthday"]
    assert updated_user.first_name == UPDATE_USER_ROW_VALID_DATA["first_name"]
    assert updated_user.middle_name == UPDATE_USER_ROW_VALID_DATA["middle_name"]
    assert updated_user.last_name == UPDATE_USER_ROW_VALID_DATA["last_name"]
    assert updated_user.is_active == UPDATE_USER_ROW_VALID_DATA["is_active"]


@pytest.mark.asyncio
async def test_update_user_by_uuid_data_success(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    assert current_user.meta != UPDATE_USER_ROW_VALID_DATA["meta"]
    assert current_user.secret != UPDATE_USER_ROW_VALID_DATA["secret"]
    assert current_user.username != UPDATE_USER_ROW_VALID_DATA["username"]
    assert current_user.password_hashed != UPDATE_USER_ROW_VALID_DATA["password_hashed"]
    assert current_user.email != UPDATE_USER_ROW_VALID_DATA["email"]
    assert current_user.phone != UPDATE_USER_ROW_VALID_DATA["phone"]
    assert current_user.gender != UPDATE_USER_ROW_VALID_DATA["gender"]
    assert current_user.birthday != UPDATE_USER_ROW_VALID_DATA["birthday"]
    assert current_user.first_name != UPDATE_USER_ROW_VALID_DATA["first_name"]
    assert current_user.middle_name != UPDATE_USER_ROW_VALID_DATA["middle_name"]
    assert current_user.last_name != UPDATE_USER_ROW_VALID_DATA["last_name"]
    assert current_user.is_active != UPDATE_USER_ROW_VALID_DATA["is_active"]

    updated_user = await UsersRepository.update(
        filter_data={"uuid": current_user.uuid}, data=UPDATE_USER_ROW_VALID_DATA, return_updated=True
    )

    assert updated_user.id == current_user.id  # noqa
    assert updated_user.meta == UPDATE_USER_ROW_VALID_DATA["meta"]
    assert updated_user.secret == UPDATE_USER_ROW_VALID_DATA["secret"]
    assert updated_user.username == UPDATE_USER_ROW_VALID_DATA["username"]
    assert updated_user.password_hashed == UPDATE_USER_ROW_VALID_DATA["password_hashed"]
    assert updated_user.email == UPDATE_USER_ROW_VALID_DATA["email"]
    assert updated_user.phone == UPDATE_USER_ROW_VALID_DATA["phone"]
    assert updated_user.gender == UPDATE_USER_ROW_VALID_DATA["gender"]
    assert updated_user.birthday == UPDATE_USER_ROW_VALID_DATA["birthday"]
    assert updated_user.first_name == UPDATE_USER_ROW_VALID_DATA["first_name"]
    assert updated_user.middle_name == UPDATE_USER_ROW_VALID_DATA["middle_name"]
    assert updated_user.last_name == UPDATE_USER_ROW_VALID_DATA["last_name"]
    assert updated_user.is_active == UPDATE_USER_ROW_VALID_DATA["is_active"]


@pytest.mark.asyncio
async def test_update_user_by_email_data_success(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    assert current_user.meta != UPDATE_USER_ROW_VALID_DATA["meta"]
    assert current_user.secret != UPDATE_USER_ROW_VALID_DATA["secret"]
    assert current_user.username != UPDATE_USER_ROW_VALID_DATA["username"]
    assert current_user.password_hashed != UPDATE_USER_ROW_VALID_DATA["password_hashed"]
    assert current_user.email != UPDATE_USER_ROW_VALID_DATA["email"]
    assert current_user.phone != UPDATE_USER_ROW_VALID_DATA["phone"]
    assert current_user.gender != UPDATE_USER_ROW_VALID_DATA["gender"]
    assert current_user.birthday != UPDATE_USER_ROW_VALID_DATA["birthday"]
    assert current_user.first_name != UPDATE_USER_ROW_VALID_DATA["first_name"]
    assert current_user.middle_name != UPDATE_USER_ROW_VALID_DATA["middle_name"]
    assert current_user.last_name != UPDATE_USER_ROW_VALID_DATA["last_name"]
    assert current_user.is_active != UPDATE_USER_ROW_VALID_DATA["is_active"]

    updated_user = await UsersRepository.update(
        filter_data={"email": current_user.email},
        data=UPDATE_USER_ROW_VALID_DATA,
        return_updated=True,
    )

    assert updated_user.id == current_user.id  # noqa
    assert updated_user.meta == UPDATE_USER_ROW_VALID_DATA["meta"]
    assert updated_user.secret == UPDATE_USER_ROW_VALID_DATA["secret"]
    assert updated_user.username == UPDATE_USER_ROW_VALID_DATA["username"]
    assert updated_user.password_hashed == UPDATE_USER_ROW_VALID_DATA["password_hashed"]
    assert updated_user.email == UPDATE_USER_ROW_VALID_DATA["email"]
    assert updated_user.phone == UPDATE_USER_ROW_VALID_DATA["phone"]
    assert updated_user.gender == UPDATE_USER_ROW_VALID_DATA["gender"]
    assert updated_user.birthday == UPDATE_USER_ROW_VALID_DATA["birthday"]
    assert updated_user.first_name == UPDATE_USER_ROW_VALID_DATA["first_name"]
    assert updated_user.middle_name == UPDATE_USER_ROW_VALID_DATA["middle_name"]
    assert updated_user.last_name == UPDATE_USER_ROW_VALID_DATA["last_name"]
    assert updated_user.is_active == UPDATE_USER_ROW_VALID_DATA["is_active"]


@pytest.mark.asyncio
async def test_update_user_by_obj_success(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    assert current_user.meta != UPDATE_USER_ROW_VALID_DATA["meta"]
    assert current_user.secret != UPDATE_USER_ROW_VALID_DATA["secret"]
    assert current_user.username != UPDATE_USER_ROW_VALID_DATA["username"]
    assert current_user.password_hashed != UPDATE_USER_ROW_VALID_DATA["password_hashed"]
    assert current_user.email != UPDATE_USER_ROW_VALID_DATA["email"]
    assert current_user.phone != UPDATE_USER_ROW_VALID_DATA["phone"]
    assert current_user.gender != UPDATE_USER_ROW_VALID_DATA["gender"]
    assert current_user.birthday != UPDATE_USER_ROW_VALID_DATA["birthday"]
    assert current_user.first_name != UPDATE_USER_ROW_VALID_DATA["first_name"]
    assert current_user.middle_name != UPDATE_USER_ROW_VALID_DATA["middle_name"]
    assert current_user.last_name != UPDATE_USER_ROW_VALID_DATA["last_name"]
    assert current_user.is_active != UPDATE_USER_ROW_VALID_DATA["is_active"]

    updated_user = await UsersRepository.update_by_obj(obj=current_user, data=UPDATE_USER_ROW_VALID_DATA)

    assert updated_user.id == current_user.id  # noqa
    assert updated_user.meta == UPDATE_USER_ROW_VALID_DATA["meta"]
    assert updated_user.secret == UPDATE_USER_ROW_VALID_DATA["secret"]
    assert updated_user.username == UPDATE_USER_ROW_VALID_DATA["username"]
    assert updated_user.password_hashed == UPDATE_USER_ROW_VALID_DATA["password_hashed"]
    assert updated_user.email == UPDATE_USER_ROW_VALID_DATA["email"]
    assert updated_user.phone == UPDATE_USER_ROW_VALID_DATA["phone"]
    assert updated_user.gender == UPDATE_USER_ROW_VALID_DATA["gender"]
    assert updated_user.birthday == UPDATE_USER_ROW_VALID_DATA["birthday"]
    assert updated_user.first_name == UPDATE_USER_ROW_VALID_DATA["first_name"]
    assert updated_user.middle_name == UPDATE_USER_ROW_VALID_DATA["middle_name"]
    assert updated_user.last_name == UPDATE_USER_ROW_VALID_DATA["last_name"]
    assert updated_user.is_active == UPDATE_USER_ROW_VALID_DATA["is_active"]


@pytest.mark.asyncio
async def test_get_or_create_success_get_email(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    data = deepcopy(CREATE_USER_ROW_X_VALID_DATA)
    data["email"] = current_user.email

    user_created = await UsersRepository.get_or_create(filter_data={"email": data["email"]}, data=data)

    assert user_created.id == current_user.id
    assert user_created.first_name != data["first_name"]


@pytest.mark.asyncio
async def test_get_or_create_success_get_id(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    data = deepcopy(CREATE_USER_ROW_X_VALID_DATA)
    data["email"] = current_user.email

    user_created = await UsersRepository.get_or_create(filter_data={"id": current_user.id}, data=data)

    assert user_created.id == current_user.id
    assert user_created.first_name != data["first_name"]


@pytest.mark.asyncio
async def test_get_or_create_success_create_email(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    data = deepcopy(CREATE_USER_ROW_X_VALID_DATA)
    user_created = await UsersRepository.get_or_create(filter_data={"email": data["email"]}, data=data)

    assert current_user.id != user_created.id
    assert user_created.meta == data["meta"]
    assert user_created.secret == data["secret"]
    assert user_created.username == data["username"]
    assert user_created.password_hashed == data["password_hashed"]
    assert user_created.email == data["email"]
    assert user_created.phone == data["phone"]
    assert user_created.gender == data["gender"]
    assert user_created.birthday == data["birthday"]
    assert user_created.first_name == data["first_name"]
    assert user_created.middle_name == data["middle_name"]
    assert user_created.last_name == data["last_name"]
    assert user_created.is_active == data["is_active"]


@pytest.mark.asyncio
async def test_update_or_create_success_update(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    data = deepcopy(CREATE_USER_ROW_X_VALID_DATA)
    user_created = await UsersRepository.update_or_create(field="email", value=current_user.email, data=data)

    assert current_user.id == user_created.id
    assert user_created.meta == data["meta"]
    assert user_created.secret == data["secret"]
    assert user_created.username == data["username"]
    assert user_created.password_hashed == data["password_hashed"]
    assert user_created.email == data["email"]
    assert user_created.phone == data["phone"]
    assert user_created.gender == data["gender"]
    assert user_created.birthday == data["birthday"]
    assert user_created.first_name == data["first_name"]
    assert user_created.middle_name == data["middle_name"]
    assert user_created.last_name == data["last_name"]
    assert user_created.is_active == data["is_active"]


@pytest.mark.asyncio
async def test_update_or_create_success_update_partial(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    data = deepcopy(CREATE_USER_ROW_X_VALID_DATA)
    data.pop("first_name")
    data.pop("last_name")
    data.pop("middle_name")
    user_affected = await UsersRepository.update_or_create(field="email", value=current_user.email, data=data)

    assert current_user.id == user_affected.id
    assert user_affected.meta == data["meta"]
    assert user_affected.secret == data["secret"]
    assert user_affected.username == data["username"]
    assert user_affected.password_hashed == data["password_hashed"]
    assert user_affected.email == data["email"]
    assert user_affected.phone == data["phone"]
    assert user_affected.gender == data["gender"]
    assert user_affected.birthday == data["birthday"]
    assert user_affected.is_active == data["is_active"]
    assert user_affected.first_name == current_user.first_name
    assert user_affected.middle_name == current_user.middle_name
    assert user_affected.last_name == current_user.last_name


@pytest.mark.asyncio
async def test_update_or_create_success_create(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    data = deepcopy(CREATE_USER_ROW_X_VALID_DATA)
    user_affected = await UsersRepository.update_or_create(field="email", value=data["email"], data=data)

    assert current_user.id != user_affected.id
    assert user_affected.meta == data["meta"]
    assert user_affected.secret == data["secret"]
    assert user_affected.username == data["username"]
    assert user_affected.password_hashed == data["password_hashed"]
    assert user_affected.email == data["email"]
    assert user_affected.phone == data["phone"]
    assert user_affected.gender == data["gender"]
    assert user_affected.birthday == data["birthday"]
    assert user_affected.first_name == data["first_name"]
    assert user_affected.middle_name == data["middle_name"]
    assert user_affected.last_name == data["last_name"]
    assert user_affected.is_active == data["is_active"]


@pytest.mark.asyncio
async def test_delete_by_field_success(db_user: Coroutine) -> None:
    current_user = await db_user  # noqa
    count_before = await UsersRepository.count()
    assert count_before == 1
    await UsersRepository.delete(filter_data={"email": current_user.email})
    count_after = await UsersRepository.count()
    assert count_after == 0
