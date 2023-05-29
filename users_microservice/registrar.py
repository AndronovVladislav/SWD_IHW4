from utils.microservice_component_interface import MicroserviceComponentInterface

from accessify import private, implements
from flask import request, make_response
from sqlalchemy import select, insert
import uuid, hashlib


@implements(MicroserviceComponentInterface)
class Registrar(object):
    def __init__(self, dwh):
        self.__users = dwh.users
        self.__engine = dwh.engine

        self.__error_code = 409
        self.__error_message = 'Error code: {0} - CONFLICT<br>'.format(self.__error_code)
        self.__post_form = \
        '''
        <form method="POST"> 
            <div><label>Username: <input type="text" name="username"></label></div>
            <div><label>Email: <input type="text" name="email"></label></div>
            <div><label>Password: <input type="password" name="password"></label></div>
            <div><label>Role: <input type="text" name="role"></label></div>
            <input type="submit" value="Enter">
        </form>
        '''

    def action(self):
        if request.method == 'POST':
            params = request.get_json()

            with self.__engine.connect() as connection:
                connection.begin()

                error, data_correct = self.validate_data(params=params, connection=connection)
                if not data_correct:
                    return error

                insertion_instruction = insert(self.__users).values(
                    username = params['username'],
                    email = params['email'],
                    password_hash = self.hash_password(params['password']),
                    role = (params['role'] if params.get('role') else 'customer')
                )

                connection.execute(insertion_instruction)
                connection.commit()

            return make_response('New user registered!', 200)

        return self.__post_form

    @private
    def hash_password(self, password):
        salt = uuid.uuid4().hex.encode()
        return str(hashlib.sha256(password.encode() + salt).hexdigest()) + ':' + salt.decode()
    
    @private
    def validate_data(self, **kwargs):
        params = kwargs['params']
        connection = kwargs['connection']

        if connection.execute(select(self.__users.c.username) \
                                .where(self.__users.c.username == params['username'])) \
                                .fetchall() or \
            connection.execute(select(self.__users.c.email) \
                                .where(self.__users.c.email == params['email'])) \
                                .fetchall():
            return (self.make_error('A user with the same name or email already exists'), False)

        if '@' not in params['email']:
            return (self.make_error('Invalid email format'), False)

        if len(params['password']) < 8:
            return (self.make_error('Too short password'), False)

        if params.get('role') not in ('customer', 'chef', 'manager', None):
            return (self.make_error('Invalid role'), False)
        
        return (True, True)

    @private
    def make_error(self, error_description):
        return make_response(self.__error_message + error_description, self.__error_code)