from datetime import datetime
from typing import List

from sqlalchemy.engine.result import RowProxy
import pytest

from src.app.core.repositories.users import UsersRepository

CREATE_USER_ROW_X_VALID_DATA = {
    "meta": {"meta_key": "meta_value_x"},
    "secret": "secret_x",
    "username": "u_name_x",
    "password_hashed": "x",
    "email": "u_name_x@gmail.com",
    "phone": "9379991x",
    "gender": "x_male",
    "birthday": datetime.now(),
    "first_name": "f_name_x",
    "middle_name": "m_name_x",
    "last_name": "l_name_x",
    "is_active": False,
}

CREATE_USER_ROW_VALID_DATA = {
    "meta": {"meta_key": "meta_value_1"},
    "secret": "secret_1",
    "username": "u_name_1",
    "password_hashed": "",
    "email": "u_name_1@gmail.com",
    "phone": "9379991",
    "gender": "male",
    "birthday": None,
    "first_name": "f_name_1",
    "middle_name": "m_name_1",
    "last_name": "l_name_1",
    "is_active": True,
}


CREATE_USERS_VALID_DATA = [
    CREATE_USER_ROW_VALID_DATA,
    {
        "meta": {"meta_key": "meta_value_2"},
        "secret": "secret_2",
        "username": "u_name_2",
        "password_hashed": "",
        "email": "u_name_2@gmail.com",
        "phone": "9379992",
        "gender": "male",
        "birthday": None,
        "first_name": "f_name_2",
        "middle_name": "m_name_2",
        "last_name": "l_name_2",
        "is_active": True,
    },
]

UPDATE_USER_ROW_VALID_DATA = {
    "meta": {"meta_key_update": "meta_value_updated"},
    "secret": "secret_updated",
    "username": "u_name_updated",
    "password_hashed": "updated",
    "email": "u_name_updated@gmail.com",
    "phone": "9379999999",
    "gender": "female",
    "birthday": datetime.now(),
    "first_name": "f_name_updated",
    "middle_name": "m_name_updated",
    "last_name": "l_name_updated",
    "is_active": False,
}


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def db_user() -> RowProxy:
    db_user_ = await UsersRepository.create(CREATE_USER_ROW_VALID_DATA)
    return db_user_


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def db_users() -> List[RowProxy]:
    db_users_ = []
    for data in CREATE_USERS_VALID_DATA:
        row = await UsersRepository.create(data)
        db_users_.append(row)
    return db_users_
