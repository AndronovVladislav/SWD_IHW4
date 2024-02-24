from typing import Optional

from flask import request, make_response, Response
from sqlalchemy.orm import Session as DBSession

from common.db_manager import DBManager
from common.microservice_component_interface import MicroserviceComponentInterface
from menu.models import Dish
from menu.dishes_managament.management_mixin import DishesManagementMixin


class CreateDish(MicroserviceComponentInterface, DishesManagementMixin):
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def on_execute(self) -> Response:
        with DBSession(self.db_manager.engine) as session:
            response, data_is_correct = self.validate_data(session,
                                                           request.args.get('token'),
                                                           int(request.form['quantity']),
                                                           int(request.form['price']),
                                                           )
            if not data_is_correct:
                return response

            session.add(Dish(**request.form))
            session.commit()

        return make_response('New dish registered!', 200)

    def validate_data(self,
                      session: DBSession,
                      token: str,
                      quantity: int,
                      price: int,
                      ) -> tuple[Optional[Response], bool]:
        response, user_is_correct = self.common_checks(session, token, 'chef')

        if not user_is_correct:
            return response

        if quantity < 0 or price <= 0:
            response = self.make_error('You can\'t create negative amount of dish '
                                       'or set non-positive price for new dish', 406)
            return response, False

        return None, True
