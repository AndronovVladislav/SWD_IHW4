from sqlalchemy.orm import DeclarativeBase


ORDER_STATUS = {
    'CR': 'Created',
    'IP': 'In progress',
    'RE': 'Ready',
    'CA': 'Canceled',
}


class Model(DeclarativeBase):
    pass
