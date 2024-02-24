from time import sleep

from sqlalchemy.orm import Session

from menu.models import Order, OrderDish
from menu.locals import STATUS_TRANSITIONS
from common.db_manager import DBManager


class OrdersProcessor:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def on_execute(self) -> None:
        with Session(self.db_manager.engine) as session:
            while True:
                for order in session.query(Order).filter(Order.status.not_in(('RE', 'CA'))).all():
                    for _ in range(len(STATUS_TRANSITIONS)):
                        sleep(1)
                        next_status = STATUS_TRANSITIONS[order.status]
                        session.query(Order).filter(Order.id == order.id).update({'status': next_status})

                    session.delete(session.query(OrderDish).filter(OrderDish.order_id == order[0]))
                    session.commit()
