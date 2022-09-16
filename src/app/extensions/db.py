import sqlalchemy


from src.app.config.settings import settings
from gino.ext.starlette import Gino  # noqa

metadata = sqlalchemy.MetaData()

db = Gino(
    ssl=None,
    pool_min_size=settings.POSTGRES_POOL_MIN_SIZE,
    pool_max_size=settings.POSTGRES_POOL_MAX_SIZE,
    dsn=settings.POSTGRES_DB_URL,  # URL for SqlAlchemy
    echo=settings.DEBUG,
    retry_limit=5,
    retry_interval=3,
)
