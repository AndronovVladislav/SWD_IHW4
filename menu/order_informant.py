from typing import Optional

from flask import request, make_response, Response
from sqlalchemy.orm import Session

from common.db_manager import DBManager
from common.microservice_component_interface import MicroserviceComponentInterface
from menu.models import Dish, Order, OrderDish


class OrderInformant(MicroserviceComponentInterface):
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def on_execute(self) -> Response:
        with Session(self.db_manager.engine) as session:
            order_id = int(request.form['order_id'])
            order = self.get_order(session, order_id)
            response, data_is_correct = self.validate_data(order)

            if not data_is_correct:
                return response

            dishes = session.query(OrderDish).filter(OrderDish.order_id == order_id).all()

            dishes_names = list()
            for dish in dishes:
                dishes_names.append(session.query(Dish).filter(Dish.id == dish.id).first().name)

            response = {'dishes': dishes_names,
                        'status': order.id}

            return make_response(response, 200)

    @staticmethod
    def get_order(session: Session, order_id: int):
        return session.query(Order).filter(Order.id == order_id).first()

    def validate_data(self, order: Optional[Order]) -> tuple[Optional[Response], bool]:
        if not order:
            return self.make_error('Invalid OrderID', 404), False

        return None, True
