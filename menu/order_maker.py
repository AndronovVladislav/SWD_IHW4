from typing import Iterable, Optional

from flask import request, make_response, Response
from sqlalchemy.orm import Session as DBSession

from common.db_manager import DBManager
from common.jwt_mixin import JWTMixin
from common.session_mixin import SessionMixin
from common.microservice_component_interface import MicroserviceComponentInterface
from menu.models import Dish, Order, OrderDish
from users.models import Session, User


class OrderMaker(MicroserviceComponentInterface, JWTMixin, SessionMixin):
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def on_execute(self):
        with DBSession(self.db_manager.engine) as session:
            user = session.query(User).filter(User.username == request.form['username']).first()

            if not user:
                return make_response('User doesn\'t exist!', 403)

            session_info = self.get_session(session, user.id)

            dishes_names = request.form.getlist('dishes[]')
            quantities = request.form.getlist('quantities[]')
            dishes = zip(dishes_names, quantities)

            response, data_is_correct = self.validate_data(session, session_info, *dishes)
            if not data_is_correct:
                return response

            new_order = Order(user_id=user.id, special_requests=request.form.get('special_requests'))
            session.add(new_order)

            for dish_name, amount in dishes:
                dish = session.query(Dish).filter(Dish.name == dish_name)
                session.add(OrderDish(order_id=new_order.id, dish_id=dish.id, quantity=amount, price=dish.price))

                dish.quantity -= amount
                session.add(dish)

            session.commit()

        return make_response('Your order registered!', 200)

    def validate_data(self,
                      session: DBSession,
                      session_info: Session,
                      dishes: Iterable[tuple[str, int]],
                      ) -> tuple[Optional[Response], bool]:
        if not self.validate_token(session_info.session_token):
            return self.make_error('Session token expired, please reauthorize', 401), False

        for dish, amount in dishes:
            dish = session.query(Dish).filter(Dish.name == dish).fetchone()

            if not dish:
                return self.make_error('You tried to order dish that we haven\'t', 406), False

            if amount <= 0:
                return self.make_error('You can\'t to order non-positive amount of dish', 406), False

            if dish.quantity < amount:
                return self.make_error(f'Unfortunately we haven\'t {amount} of {dish}', 406), False

        return None, True
