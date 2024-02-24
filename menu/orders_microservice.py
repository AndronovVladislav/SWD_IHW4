from threading import Thread

from menu.menu_selector import MenuSelector
from menu.order_maker import OrderMaker
from menu.order_informant import OrderInformant
from menu.orders_processor import OrdersProcessor
from menu.dishes_managament.create_dish import CreateDish
from menu.dishes_managament.remove_dish import RemoveDish
from menu.dishes_managament.update_price import UpdatePrice
from menu.dishes_managament.update_quantity import UpdateQuantity
from common.microservice_interface import MicroserviceInterface
from common.db_manager import DBManager


class OrdersMicroservice(MicroserviceInterface):
    def __init__(self, app, db_manager: DBManager, **configs):
        self.app = app
        self.db_manager = db_manager

        self.configure(SQLALCHEMY_DATABASE_URI=self.db_manager.settings, **configs)

        orders_processor_thread = Thread(target=OrdersProcessor(self.db_manager).on_execute, args=(), daemon=True)
        orders_processor_thread.start()

        self.add_endpoint('/getmenu', 'getMenu', MenuSelector(self.db_manager).action, methods=['GET'])
        self.add_endpoint('/makeorder', 'makeOrder', OrderMaker(self.db_manager).on_execute, methods=['POST'])
        self.add_endpoint('/getorder', 'getOrder', OrderInformant(self.db_manager).action, methods=['GET'])
        self.add_endpoint('/appenddish', 'appendDish', CreateDish(self.db_manager).action, methods=['POST'])
        self.add_endpoint('/removedish', 'removeDish', RemoveDish(self.db_manager).action, methods=['DELETE'])
        self.add_endpoint('/changeprice', 'changePrice', UpdatePrice(self.db_manager).action, methods=['PATCH'])
        self.add_endpoint('/changequantity', 'changeQuantity', UpdateQuantity(self.db_manager).action, methods=['PATCH'])

    def configure(self, **configs):
        self.app.config.update(configs)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None, *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)
