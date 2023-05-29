from utils.microservice_interface import MicroserviceInterface
from .registrar import Registrar
from .authorizer import Authorizer
from .users_informant import UsersInformant
from utils.database import DB

from accessify import private, implements


@implements(MicroserviceInterface)
class UsersMicroservice:
    def __init__(self, dialect, user, password, host, port, db, app, **configs):
        self.__app = app
        self.__app.config['SQLALCHEMY_DATABASE_URI'] = '{0}+pymysql://{1}:{2}@{3}:{4}/{5}'.format(dialect, user, password, host, port, db)

        self.__db = DB(dialect, user, password, host, port, db)

        self.configure(**configs)

        self.add_endpoint('/signup', 'signUpPage', Registrar(self.__db).action, methods=['GET', 'POST'])
        self.add_endpoint('/signin', 'signInPage', Authorizer(self.__db).action, methods=['GET', 'POST'])
        self.add_endpoint('/getinfo', 'getInformationPage', UsersInformant(self.__db).action, methods=['GET'])

    @private
    def configure(self, **configs):
        for config, value in configs:
            self.__app.config[config.upper()] = value

    @private
    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.__app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.__app.run(**kwargs)