from utils.microservice_component_interface import MicroserviceComponentInterface

from flask import request, make_response
from sqlalchemy import select
from datetime import datetime, timedelta
from accessify import implements, private
import jwt


@implements(MicroserviceComponentInterface)
class UsersInformant:
    def __init__(self, db):
        self.__users = db.users
        self.__sessions = db.sessions
        self.__engine = db.engine

        self.__error_message = 'Error code: 404 - Not found<br>'
        self.__error_code = 404

    def action(self):
        token = request.args.get('token')

        with self.__engine.connect() as connection:
            connection.begin()

            output, data_correct = self.validate_data(token=token, connection=connection)
            if not data_correct:
                return output

            information = connection.execute(select(self.__users)\
                                             .where(self.__users.c.id == output))\
                                             .fetchone()
            response = {'username' : information[1],
                        'email' : information[2],
                        'role' : information[4],
                        'created_at' : information[5]}

            return response

    @private
    def make_error(self, error_description):
        return make_response(self.__error_message + error_description, self.__error_code)

    @private
    def validate_data(self, **kwargs):
        connection = kwargs['connection']
        token = kwargs['token']

        session_exist = connection.execute(select(self.__sessions.c.user_id, self.__sessions.c.session_token)\
                                    .where(self.__sessions.c.session_token == token))\
                                    .fetchone()
        if not session_exist:
            return (self.make_error('Invalid JWT token'), False)

        user_id, jwt_token = session_exist[0], session_exist[1]
        if jwt_token:
            jwt_token = jwt.decode(jwt_token, 'kamkino', algorithms=['HS256'])
            try:
                # -timedelta(hours=3) нужно потому, что при декодинге почему-то время увеличивается на 3 часа
                expires_at = datetime.fromtimestamp(jwt_token['exp']) - timedelta(hours=3)
                if expires_at < datetime.now():
                    return (self.make_error('Invalid JWT token'), False)
            except jwt.ExpiredSignatureError:
                return (self.make_error('Invalid JWT token'), False)

        return (user_id, True)