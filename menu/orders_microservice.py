from utils.microservice_interface import MicroserviceInterface
from utils.database import DB
from .menu_selector import MenuSelector
from .order_maker import OrderMaker
from .menu_informant import MenuInformant
from .orders_processor import OrdersProcessor
from menu.dishes_managament.create_dish import CreateDish
from menu.dishes_managament.remove_dish import RemoveDish
from menu.dishes_managament.update_price import UpdatePrice
from menu.dishes_managament.update_quantity import UpdateQuantity

from accessify import private, implements
from threading import Thread


@implements(MicroserviceInterface)
class OrdersMicroservice:
    def __init__(self, dialect, user, password, host, port, db, app, **configs):
        self.__app = app
        self.__app.config['SQLALCHEMY_DATABASE_URI'] = '{0}+pymysql://{1}:{2}@{3}:{4}/{5}'.format(dialect, user, password, host, port, db)

        self.__db = DB(dialect, user, password, host, port, db)
        self.configure(**configs)

        orders_processor_thread = Thread(target=OrdersProcessor(self.__db).action, args=(), daemon=True)
        orders_processor_thread.start()

        self.add_endpoint('/getmenu', 'getMenu', MenuSelector(self.__db).action, methods=['GET'])
        self.add_endpoint('/makeorder', 'makeOrder', OrderMaker(self.__db).action, methods=['POST'])
        self.add_endpoint('/getorder', 'getOrder', MenuInformant(self.__db).action, methods=['GET'])
        self.add_endpoint('/appenddish', 'appendDish', CreateDish(self.__db).action, methods=['POST'])
        self.add_endpoint('/removedish', 'removeDish', RemoveDish(self.__db).action, methods=['DELETE'])
        self.add_endpoint('/changeprice', 'changePrice', UpdatePrice(self.__db).action, methods=['PATCH'])
        self.add_endpoint('/changequantity', 'changeQuantity', UpdateQuantity(self.__db).action, methods=['PATCH'])

    @private
    def configure(self, **configs):
        for config, value in configs:
            self.__app.config[config.upper()] = value

    @private
    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.__app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.__app.run(**kwargs)