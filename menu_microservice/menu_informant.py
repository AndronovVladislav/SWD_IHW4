from utils.microservice_component_interface import MicroserviceComponentInterface

from flask import request, make_response
from sqlalchemy import select
from accessify import private, implements


@implements(MicroserviceComponentInterface)
class MenuInformant:
    def __init__(self, db):
        self.__orders = db.orders
        self.__order_dish = db.order_dish
        self.__dishes = db.dishes
        self.__engine = db.engine

        self.__error_message = 'Error code: 404 - Not found<br>'
        self.__error_code = 404

    def action(self):
        params = request.get_json()

        with self.__engine.connect() as connection:
            connection.begin()

            status, data_correct = self.validate_data(id=params['id'], connection=connection)
            if not data_correct:
                return status

            dishes_id = connection.execute(select(self.__order_dish.c.dish_id)\
                                .where(self.__order_dish.c.order_id == params['id']))\
                                .fetchall()

            dishes_names = list()
            for dish in dishes_id:
                dishes_names.append(connection.execute(select(self.__dishes.c.name)\
                                .where(self.__dishes.c.id == dish[0]))\
                                .fetchone()[0])

            response = {'dishes': dishes_names,
                        'status': status}

            return response

    @private
    def make_error(self, error_description):
        return make_response(self.__error_message + error_description, self.__error_code)

    @private
    def validate_data(self, **kwargs):
        connection = kwargs['connection']
        order_id = kwargs['id']

        order_status = connection.execute(select(self.__orders.c.status)\
                                    .where(self.__orders.c.id == order_id))\
                                    .fetchone()

        if not order_status:
            return (self.make_error('Invalid order id'), False)

        return (order_status[0], True)