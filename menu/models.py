from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Numeric

from menu.locals import OrderStatus
from common.db_manager import Model


class Dish(Model):
    __tablename__ = 'dish'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int]
    create_datetime: Mapped[datetime] = mapped_column(default=datetime.now)
    update_datetime: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class Order(Model):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.CREATED)
    special_requests: Mapped[str]
    create_datetime: Mapped[datetime] = mapped_column(default=datetime.now)
    update_datetime: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class OrderDish(Model):
    __tablename__ = 'order_dish'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    dish_id: Mapped[int] = mapped_column(ForeignKey('dish.id'))
    quantity: Mapped[int]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    create_datetime: Mapped[datetime] = mapped_column(default=datetime.now)
    update_datetime: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
