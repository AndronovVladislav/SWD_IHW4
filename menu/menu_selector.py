from flask import make_response, Response
from sqlalchemy.orm import Session

from common.db_manager import DBManager
from common.microservice_component_interface import MicroserviceComponentInterface
from menu.models import Dish


class MenuSelector(MicroserviceComponentInterface):
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def on_execute(self) -> Response:
        with Session(self.db_manager.engine) as session:
            response = []
            for position in session.query(Dish).filter(Dish.quantity > 0).fetchall():
                response.append({'name': position.name,
                                 'description': position.description,
                                 'price': position.price
                                 })

            return make_response(response, 200)
