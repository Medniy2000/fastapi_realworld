from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from src.app.main import app
from src.app.config.settings import settings
from src.app.extensions.db import db


@pytest.fixture(scope="function", autouse=True)
def prepared_db(event_loop: AbstractEventLoop) -> Generator:
    db_ = event_loop.run_until_complete(db.set_bind(settings.POSTGRES_DB_URL))
    event_loop.run_until_complete(db.gino.create_all())
    yield db_
    event_loop.run_until_complete(db.gino.drop_all())
    event_loop.run_until_complete(db.bind.close())


@pytest.mark.asyncio
@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8800/") as client:
        yield client


pytest_plugins = [
    "tests.core.repositories.fixtures",
]
