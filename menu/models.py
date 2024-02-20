from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Numeric
from sqlalchemy_utils import ChoiceType

from utils.locals import ORDER_STATUS, Model


class Dish(Model):
    __table__ = 'dish'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int]
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column()
    is_available: Mapped[bool]
    create_datetime: Mapped[datetime] = mapped_column(default=datetime.now)
    update_datetime: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class Order(Model):
    __table__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str] = mapped_column(ChoiceType(ORDER_STATUS.items()), default='CR')
    special_requests: Mapped[str]
    create_datetime: Mapped[datetime] = mapped_column(default=datetime.now)
    update_datetime: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class OrderDish(Model):
    __table__ = 'order_dish'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    dish_id: Mapped[int] = mapped_column(ForeignKey('dish.id'))
    quantity: Mapped[int]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    create_datetime: Mapped[datetime] = mapped_column(default=datetime.now)
    update_datetime: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
