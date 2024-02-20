from utils.microservice_component_interface import MicroserviceComponentInterface

from flask import request, make_response
from sqlalchemy import select, update
import jwt
from datetime import datetime, timedelta
from accessify import private, implements

@implements(MicroserviceComponentInterface)
class UpdateQuantity:
    def __init__(self, db):
        self.__users = db.users
        self.__dishes = db.dishes
        self.__sessions = db.sessions
        self.__order_dish = db.order_dish
        self.__engine = db.engine

        self.__error_message = 'Error code: 409 - Conflict<br>'
        self.__error_code = 409

    def action(self):
        params = request.get_json()
        token = request.args.get('token')

        with self.__engine.connect() as connection:
            connection.begin()

            error, data_correct = self.validate_data(token=token, params=params, connection=connection)
            if not data_correct:
                return error

            connection.execute(update(self.__dishes)
                                .where(self.__dishes.c.id == params['id'])
                                .values(quantity=params['new_quantity'], is_available=params['new_quantity'] > 0))

            connection.commit()

        return make_response('Dish price updated!', 200)

    @private
    def make_error(self, error_description):
        return make_response(self.__error_message + error_description, self.__error_code)

    @private
    def validate_data(self, **kwargs):
        token = kwargs['token']
        params = kwargs['params']
        connection = kwargs['connection']

        try:
            # -timedelta(hours=3) нужно потому, что при декодинге время увеличивается на 3 часа
            jwt_token = jwt.decode(token, 'kamkino', algorithms=['HS256'])
            expires_at = datetime.fromtimestamp(jwt_token['exp']) - timedelta(hours=3)
            if expires_at < datetime.now():
                return (self.make_error('Session token expired, please reauthorize'), False)
        except jwt.ExpiredSignatureError:
            return (self.make_error('Session token expired, please reauthorize'), False)

        user_id = connection.execute(select(self.__sessions.c.user_id)\
                                     .where(self.__sessions.c.session_token == token))\
                                     .fetchone()
        if not user_id:
            return (self.make_error('User doesn\'t exist'), False)

        if connection.execute(select(self.__users.c.role)\
                              .where(self.__users.c.id == user_id[0]))\
                              .fetchone()[0] != 'manager':
            return (self.make_error('You aren\'t manager'), False)
        
        if not connection.execute(select(self.__dishes)\
                                       .where(self.__dishes.c.id == params['id']))\
                                       .fetchone():
            return (self.make_error('Dish doesn\'t exists'), False)

        if connection.execute(select(self.__order_dish)\
                              .where(self.__order_dish.c.dish_id == params['id']))\
                              .fetchall():
            return (self.make_error('You can\'t change price of'
                                    'this dish because of exist orders with this dish'), False)
            
        return (True, True)