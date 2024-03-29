from typing import Optional

from flask import request, make_response, Response
from sqlalchemy.orm import Session

from common.db_manager import DBManager
from common.microservice_component_interface import MicroserviceComponentInterface
from menu.dishes_managament.management_mixin import DishesManagementMixin


class RemoveDish(MicroserviceComponentInterface, DishesManagementMixin):
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def on_execute(self) -> Response:
        with Session(self.db_manager.engine) as session:
            dish_id = int(request.form['dish_id'])
            error, data_is_correct = self.validate_data(session, request.args.get('token'), dish_id)

            if not data_is_correct:
                return error

            session.delete(self.get_dish(session, dish_id))
            session.commit()

        return make_response('Dish removed!', 200)

    def validate_data(self, session: Session, token: str, dish_id: int) -> tuple[Optional[Response], bool]:
        response, user_is_correct = self.common_checks(session, token, 'chef')

        if not user_is_correct:
            return response

        if not self.get_dish(session, dish_id):
            return self.dish_does_not_exist()

        if self.get_order_dish_by_dish_id(session, dish_id):
            return self.dish_in_use('remove this dish')

        return None, True
