from common.microservice_interface import MicroserviceInterface
from common.microservice_component_interface import MicroserviceComponentInterface
from users.registrar import RegistrarComponent
from users.authorizer import AuthorizerComponent
from users.users_informant import UsersInformantComponent

from common.db_manager import DBManager


class UsersMicroservice(MicroserviceInterface):
    def __init__(self, app, db_manager: DBManager, **configs):
        self.app = app
        self.db_manager = db_manager

        self.configure(SQLALCHEMY_DATABASE_URI=self.db_manager.settings, **configs)

        self.sign_up_endpoint = '/signup'
        self.sign_in_endpoint = '/signin'
        self.get_info_endpoint = '/getinfo'

        self.register_endpoints()

    def configure(self, **configs):
        self.app.config.update(configs)

    def register_endpoints(self):
        self.add_endpoint(self.sign_up_endpoint,
                          'signUpPage',
                          RegistrarComponent(self.db_manager, self.sign_in_endpoint).on_execute,
                          ['GET', 'POST'],
                          )
        self.add_endpoint(self.sign_in_endpoint,
                          'signInPage',
                          AuthorizerComponent(self.db_manager, self.sign_up_endpoint).on_execute,
                          ['GET', 'POST'],
                          )
        self.add_endpoint(self.get_info_endpoint,
                          'getInformationPage',
                          UsersInformantComponent(self.db_manager).on_execute,
                          ['GET'],
                          )

    def add_endpoint(self,
                     endpoint: str,
                     endpoint_name: str,
                     handler: MicroserviceComponentInterface.on_execute,
                     methods: list[str],
                     *args,
                     **kwargs,
                     ):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)
