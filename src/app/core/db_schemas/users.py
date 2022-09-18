import uuid
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy import func
from src.app.extensions.db import db
from src.app.core.utils.common import generate_str


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    uuid = db.Column(UUID, primary_key=True, nullable=False, index=True, default=uuid.uuid4())
    meta = db.Column(JSON, nullable=False, default=dict())
    secret = db.Column(db.String(24), nullable=False, unique=True, default=generate_str())
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )
    username = db.Column(db.String(64), nullable=True)
    password_hashed = db.Column(db.String(64), default=None)
    email = db.Column(db.String(64), nullable=True, index=True, unique=True)
    phone = db.Column(db.String(24), nullable=True, default=None, index=True)
    gender = db.Column(db.String(24), nullable=True)
    birthday = db.Column(db.DateTime, nullable=True, default=None)
    first_name = db.Column(db.String(64), nullable=True)
    middle_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
