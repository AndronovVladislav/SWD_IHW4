from threading import Thread
from typing import Callable

from flask import Response

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

        self.get_menu_endpoint = '/getmenu'
        self.make_order_endpoint = '/makeorder'
        self.get_order_endpoint = '/getorder'
        self.create_dish_endpoint = '/createdish'
        self.remove_dish_endpoint = '/removedish'
        self.change_price_endpoint = '/changeprice'
        self.change_quantity_endpoint = '/changequantity'

    def include_in_app(self) -> None:
        orders_processor_thread = Thread(target=OrdersProcessor(self.db_manager).on_execute, args=(), daemon=True)
        orders_processor_thread.start()

        self.register_endpoints()

    def configure(self, **configs):
        self.app.config.update(configs)

    def register_endpoints(self):
        self.add_endpoint(self.get_menu_endpoint, 'getMenu', MenuSelector(self.db_manager).on_execute, ['GET'])
        self.add_endpoint(self.make_order_endpoint, 'makeOrder', OrderMaker(self.db_manager).on_execute, ['POST'])
        self.add_endpoint(self.get_order_endpoint, 'getOrder', OrderInformant(self.db_manager).on_execute, ['GET'])
        self.add_endpoint(self.create_dish_endpoint, 'createDish', CreateDish(self.db_manager).on_execute, ['POST'])
        self.add_endpoint(self.remove_dish_endpoint, 'removeDish', RemoveDish(self.db_manager).on_execute, ['DELETE'])
        self.add_endpoint(self.change_price_endpoint, 'changePrice', UpdatePrice(self.db_manager).on_execute, ['PATCH'])
        self.add_endpoint(self.change_quantity_endpoint,
                          'changeQuantity',
                          UpdateQuantity(self.db_manager).on_execute,
                          ['PATCH'],
                          )

    def add_endpoint(self,
                     endpoint: str,
                     endpoint_name: str,
                     handler: Callable[[...], Response],
                     methods: list[str],
                     *args,
                     **kwargs,
                     ):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)
