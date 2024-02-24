from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from common.db_manager import Model


class User(Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role: Mapped[str] = mapped_column('customer')
    create_datetime: Mapped[datetime] = mapped_column(default=datetime.now)
    update_datetime: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class Session(Model):
    __tablename__ = 'session'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    session_token: Mapped[str] = mapped_column(unique=True)
