from utils.microservice_component_interface import MicroserviceComponentInterface

from flask import request, make_response
from sqlalchemy import select, insert
import jwt
from datetime import datetime, timedelta
from accessify import private, implements

@implements(MicroserviceComponentInterface)
class CreateDish:
    def __init__(self, db):
        self.__users = db.users
        self.__dishes = db.dishes
        self.__sessions = db.sessions
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

            params['is_available'] = params['quantity'] >= 0
            connection.execute(insert(self.__dishes)
                               .values(**params))

            connection.commit()

        return make_response('New dish registered!', 200)

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
        
        user_role = connection.execute(select(self.__users.c.role)\
                                        .where(self.__users.c.id == user_id[0]))\
                                        .fetchone()[0]
        
        if user_role != 'chef':
            return (self.make_error('You aren\'t chef'), False)

        if params['quantity'] < 0 or params['price'] <= 0:
            return (self.make_error('You can\'t create negative amount of dish or set non-positive price for new dish'), False)
            
        return (True, True)