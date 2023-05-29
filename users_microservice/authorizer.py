from utils.microservice_component_interface import MicroserviceComponentInterface

from flask import request, make_response
from accessify import private, implements
from sqlalchemy import select, insert, update
from datetime import datetime, timedelta
import hashlib, jwt


@implements(MicroserviceComponentInterface)
class Authorizer(object):
    def __init__(self, db):
        self.__users = db.users
        self.__sessions = db.sessions
        self.__engine = db.engine

        self.__error_message = 'Error code: 409 - CONFLICT<br>'
        self.__error_code = 409
        self.__post_form = \
        '''
        <form method="POST"> 
            <div><label>Username: <input type="text" name="username"></label></div>
            <div><label>Password: <input type="password" name="password"></label></div>
            <input type="submit" value="Enter">
        </form>
        '''

    def action(self):
        if request.method == 'POST':
            params = request.get_json()

            with self.__engine.connect() as connection:
                connection.begin()

                user_info = connection.execute(select(self.__users.c.id, self.__users.c.password_hash)\
                                                                 .where(self.__users.c.username == params['username']))\
                                                                 .fetchone()
                
                if not user_info:
                    return self.make_error('User doesn\'t exist')
                
                user_id, user_password_hash = user_info

                response, token_is_valid = self.validate_data(params=params,
                                                           user_password_hash=user_password_hash,
                                                           user_id=user_id,
                                                           connection=connection)

                if token_is_valid:
                    return response[0]

                next_day = datetime.now() + timedelta(days=1)
                jwt_token = jwt.encode({'userID': str(user_id), 'exp': next_day}, 'kamkino')

                if response:
                    connection.execute(update(self.__sessions)
                                       .where(self.__sessions.c.user_id == user_id)
                                       .values(session_token=jwt_token))
                else:
                    connection.execute(insert(self.__sessions)
                                       .values(session_token=jwt_token, user_id=user_id,
                                               expires_at=next_day))
                connection.commit()
                return jwt_token

        return self.__post_form

    def check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password != str(hashlib.sha256(user_password.encode() + salt.encode()).hexdigest())

    @private
    def make_error(self, error_description):
        return make_response(self.__error_message + error_description, self.__error_code)
    
    @private
    def validate_data(self, **kwargs):
        params = kwargs['params']
        user_password_hash = kwargs['user_password_hash']
        connection = kwargs['connection']
        user_id = kwargs['user_id']

        if not user_password_hash or self.check_password(user_password_hash, params['password']):
            return (self.make_error('User doesn\'t exist or incorrect password'), False)

        jwt_token = connection.execute(select(self.__sessions.c.session_token)\
                                        .where(self.__sessions.c.user_id == user_id))\
                                        .fetchone()
        if jwt_token:
            try:
                # -timedelta(hours=3) нужно потому, что при декодинге почему-то время увеличивается на 3 часа
                decoded_token = jwt.decode(jwt_token[0], 'kamkino', algorithms=['HS256'])
                expires_at = datetime.fromtimestamp(decoded_token['exp']) - timedelta(hours=3)
                if expires_at > datetime.now():
                    return (jwt_token, True)
                else:
                    return (jwt_token, False)
            except jwt.ExpiredSignatureError:
                return (jwt_token, False)
        return (False, False)