from utils.microservice_component_interface import MicroserviceComponentInterface

from flask import request, make_response
from sqlalchemy import select, insert, update, desc
from datetime import datetime, timedelta
from accessify import private, implements
import jwt


@implements(MicroserviceComponentInterface)
class OrderMaker:
    def __init__(self, db):
        self.__dishes = db.dishes
        self.__sessions = db.sessions
        self.__orders = db.orders
        self.__order_dish = db.order_dish
        self.__engine = db.engine

        self.__error_message = 'Error code: 409 - Conflict<br>'
        self.__error_code = 409

    def action(self):
        params = request.get_json()

        with self.__engine.connect() as connection:
            connection.begin()

            user_info = connection.execute(select(self.__sessions.c.session_token)\
                                           .where(self.__sessions.c.user_id == params['user_id']))\
                                           .fetchone()

            error, data_correct = self.validate_data(user_info=user_info, params=params, connection=connection)
            if not data_correct:
                return error

            connection.execute(insert(self.__orders)
                               .values(user_id=params['user_id'],
                                       special_requests=(params['special_requests'] if
                                                         params.get('special_requests') else
                                                         '')))

            order_id = connection.execute(select(self.__orders.c.id).order_by(desc(self.__orders.c.id))).fetchone()[0]
            for dish, amount in params['dishes'].items():
                dish_id, price = connection.execute(select(self.__dishes.c.id, self.__dishes.c.price).where(self.__dishes.c.name == dish)).fetchone()
                
                connection.execute(insert(self.__order_dish)
                                   .values(order_id=order_id,
                                           dish_id=dish_id,
                                           quantity=amount,
                                           price=price))

                connection.execute(update(self.__dishes)
                                   .where(self.__dishes.c.id == dish_id)
                                   .values(quantity=self.__dishes.c.quantity - amount))

            connection.commit()

        return make_response('Your order registered!', 200)

    @private
    def make_error(self, error_description):
        return make_response(self.__error_message + error_description, self.__error_code)

    @private
    def validate_data(self, **kwargs):
        user_info = kwargs['user_info']
        params = kwargs['params']
        connection = kwargs['connection']

        if not user_info:
            return (self.make_error('Incorrect user ID'), False)

        try:
            # -timedelta(hours=3) нужно потому, что при декодинге время увеличивается на 3 часа
            jwt_token = jwt.decode(user_info[0], 'kamkino', algorithms=['HS256'])
            expires_at = datetime.fromtimestamp(jwt_token['exp']) - timedelta(hours=3)
            if expires_at < datetime.now():
                return (self.make_error('Session token expired, please reauthorize'), False)
        except jwt.ExpiredSignatureError:
            return (self.make_error('Session token expired, please reauthorize'), False)

        if not all(dish > 0 for dish in params['dishes'].values()):
            return (self.make_error('You can\'t to order non-positive amount of dish'), False)

        for dish, amount in params['dishes'].items():
            dish_exist = connection.execute(select(self.__dishes.c.quantity).where(self.__dishes.c.name == dish)).fetchone()

            if not dish_exist:
                return (self.make_error('You tried to order dish that we haven\'t'), False)

            if dish_exist[0] < amount:
                return (self.make_error('Unfortunely we haven\'t {0} {1}'.format(dish, amount)), False)

        return (True, True)