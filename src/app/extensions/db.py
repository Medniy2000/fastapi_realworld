import sqlalchemy

from src.app.config.settings import settings
from gino.ext.starlette import Gino  # noqa

metadata = sqlalchemy.MetaData()

db = Gino(
    ssl=None,
    echo=settings.DEBUG,
    dsn=settings.POSTGRES_DB_URL,  # URL for SqlAlchemy
    pool_min_size=settings.POSTGRES_POOL_MIN_SIZE,
    pool_max_size=settings.POSTGRES_POOL_MAX_SIZE,
    retry_limit=5,
    retry_interval=3,
)
