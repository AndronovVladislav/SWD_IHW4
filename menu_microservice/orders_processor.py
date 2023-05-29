from utils.microservice_component_interface import MicroserviceComponentInterface

from sqlalchemy import select, update, delete
from accessify import private, implements
from time import sleep


@implements(MicroserviceComponentInterface)
class OrdersProcessor:
    def __init__(self, db):
        self.__orders = db.orders
        self.__order_dish = db.order_dish
        self.__engine = db.engine
        self.__next_statuses = {'In waiting' : 'In progress',
                                'In progress' : 'Finished',
                                'Finished' : 'Finished',
                                'Cancelled' : 'Cancelled'}

    def action(self):
        with self.__engine.connect() as connection:
            connection.begin()
            while True:
                for order in connection.execute(select(self.__orders.c.id, self.__orders.c.status)
                                                .where(self.__orders.c.status not in ('Finished', 'Cancelled')))\
                                                .fetchall():
                    current_status = order[1]
                    for _ in range(2):
                        sleep(1)
                        current_status = self.__next_statuses[current_status]
                        connection.execute(update(self.__orders)
                                           .where(self.__orders.c.id == order[0])
                                           .values(status=current_status))
                    
                    connection.execute(delete(self.__order_dish)
                                       .where(self.__order_dish.c.order_id == order[0]))
                    connection.commit()

    @private
    def make_error(self, error_description):
        pass

    @private
    def validate_data(self, **kwargs):
        pass