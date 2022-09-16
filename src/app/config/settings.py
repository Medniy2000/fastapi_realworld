import os
from enum import Enum
from typing import List, Union, Optional

from environs import Env
from pydantic import AnyHttpUrl
from pydantic import BaseSettings as PydanticSettings
from slugify import slugify

env = Env()


class SettingsBase(PydanticSettings):
    ROOT_DIR = os.path.abspath(os.path.dirname("src"))

    if env.bool("READ_ENV", default=True):
        env.read_env(f"{ROOT_DIR}/.env")

    # Base settings
    # --------------------------------------------------------------------------
    PROJECT_NAME: str = "FastAPI Real World"
    PROJECT_NAME_SLUG: str = slugify(PROJECT_NAME)

    SECRET_KEY: str = env.str("SECRET_KEY", "secret")
    DEBUG: bool = env.bool("DEBUG", False)
    DOCS_URL: Optional[str] = "/docs"
    REDOC_URL: Optional[str] = "/redoc"

    CORS_ORIGIN_WHITELIST: List[AnyHttpUrl] = env.list(  # noqa
        "CORS_ORIGIN_WHITELIST", ["http://127.0.0.1:8000/"]  # noqa
    )

    # Auth settings
    # --------------------------------------------------------------------------
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES = env.int("ACCESS_TOKEN_EXPIRES_MINUTES", 30)
    REFRESH_TOKEN_EXPIRES_DAYS = env.int("REFRESH_TOKEN_EXPIRES_DAYS", 7)

    # API settings
    # --------------------------------------------------------------------------
    API: str = "/api"
    OPENAPI_URL: Optional[str] = f"{API}/openapi.json"
    BATCH_SIZE: int = env.int("BATCH_SIZE", 25)  # default limit of items

    # Postgres settings
    # --------------------------------------------------------------------------
    POSTGRES_HOST: str = env.str("POSTGRES_HOST")
    POSTGRES_PORT: int = env.str("POSTGRES_PORT")
    POSTGRES_USER: str = env.str("POSTGRES_USER")
    POSTGRES_PASSWORD: str = env.str("POSTGRES_PASSWORD")
    POSTGRES_DB: str = env.str("POSTGRES_DB")
    POSTGRES_DB_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}" f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    POSTGRES_POOL_MIN_SIZE: int = env.int("POSTGRES_POOL_MIN_SIZE", 5)
    POSTGRES_POOL_MAX_SIZE: int = env.int("POSTGRES_POOL_MAX_SIZE", 75)


class SettingsLocal(SettingsBase):
    pass


class SettingsTest(SettingsBase):
    pass


class SettingsProd(SettingsBase):
    DEBUG: bool = False
    DOCS_URL: Optional[str] = None
    REDOC_URL: Optional[str] = None
    OPENAPI_URL: Optional[str] = None


class LaunchMode(str, Enum):
    LOCAL = "local"
    PRODUCTION = "prod"
    TEST = "test"


LAUNCH_MODE = os.environ.get("LAUNCH_MODE")

SettingsType = Union[SettingsLocal, SettingsTest, SettingsProd]


def _get_settings() -> SettingsType:

    if LAUNCH_MODE == LaunchMode.LOCAL.value:
        settings_class = SettingsLocal  # type: ignore
    elif LAUNCH_MODE == LaunchMode.TEST.value:
        settings_class = SettingsTest  # type: ignore
    else:
        settings_class = SettingsProd  # type: ignore
    return settings_class()


settings = _get_settings()
