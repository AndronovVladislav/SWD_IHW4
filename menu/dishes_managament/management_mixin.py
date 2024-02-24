from typing import Callable, Optional

from flask import Response
from sqlalchemy.orm import Session as DBSession

from common.jwt_mixin import JWTMixin
from menu.models import Dish, OrderDish
from users.models import Session, User


class DishesManagementMixin(JWTMixin):
    make_error: Callable[[str, int], Response]

    @staticmethod
    def get_user(session: DBSession, user_id: int) -> Optional[User]:
        return session.query(User).filter(User.id == user_id).first()

    def user_does_not_exist(self) -> tuple[Optional[Response], bool]:
        return self.make_error('User doesn\'t exist', 404), False

    def user_does_not_authorized(self) -> tuple[Optional[Response], bool]:
        return self.make_error('Authorize, please', 401), False

    def user_are_not_role(self, role: str) -> tuple[Optional[Response], bool]:
        return self.make_error(f'You aren\'t {role}', 403), False

    @staticmethod
    def get_session(session: DBSession, token: str) -> Optional[Session]:
        return session.query(Session).filter(Session.session_token == token).first()

    def reauthorize_need(self) -> tuple[Optional[Response], bool]:
        return self.make_error('Session token expired, please reauthorize', 401), False

    @staticmethod
    def get_dish(session: DBSession, dish_id: int) -> Optional[Dish]:
        return session.query(Dish).filter(Dish.id == dish_id).first()

    def dish_does_not_exist(self) -> tuple[Optional[Response], bool]:
        return self.make_error('Dish doesn\'t exists', 406), False

    @staticmethod
    def get_order_dish_by_dish_id(session: DBSession, dish_id: int) -> Optional[OrderDish]:
        return session.query(OrderDish).filter(OrderDish.dish_id == dish_id).first()

    def dish_in_use(self, additional_message: str) -> tuple[Optional[Response], bool]:
        return self.make_error(f'You can\'t {additional_message} because of exist orders with this dish', 406), False

    def common_checks(self, session: DBSession, token: str, role: str):
        if not self.validate_token(token):
            self.reauthorize_need()

        user_session = self.get_session(session, token)
        if not user_session:
            return self.user_does_not_authorized()

        user = self.get_user(session, user_session.user_id)
        if not user:
            return self.user_does_not_exist()

        if user.role != role:
            return self.user_are_not_role(role)
        return None, True
