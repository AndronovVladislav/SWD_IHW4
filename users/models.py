from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from utils.locals import Model


class User(Model):
    __table__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column('customer')
    create_datetime: Mapped[datetime] = mapped_column(default=datetime.now)
    update_datetime: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class Session(Model):
    __table__ = 'session'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    session_token: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime]
