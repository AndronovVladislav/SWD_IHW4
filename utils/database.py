from sqlalchemy import Table, Column, VARCHAR, ForeignKey, create_engine, MetaData, DECIMAL, TEXT, INT, TIMESTAMP, BOOLEAN
from datetime import datetime

class DB:
    def __init__(self, dialect, user, password, host, port, db):
        self.__metadata = MetaData()
        self.__engine = create_engine('{0}+pymysql://{1}:{2}@{3}:{4}/{5}'.format(dialect, user, password, host, port, db))

        self.__users = Table('users', self.__metadata, 
            Column('id', INT, autoincrement=True, primary_key=True),
            Column('username', VARCHAR(50), nullable=False, unique=True),
            Column('email', VARCHAR(100),  nullable=False, unique=True),
            Column('password_hash', VARCHAR(255), nullable=False),
            Column('role', VARCHAR(10), default='customer'),
            Column('created_at', TIMESTAMP, default=datetime.now),
            Column('updated_at', TIMESTAMP, default=datetime.now, onupdate=datetime.now)
        )

        self.__sessions = Table('sessions', self.__metadata, 
            Column('id', INT, autoincrement=True, primary_key=True),
            Column('user_id', ForeignKey('users.id'), nullable=False),
            Column('session_token', VARCHAR(255), nullable=False, unique=True),
            Column('expires_at', TIMESTAMP, nullable=False)
        )

        self.__dishes = Table('dishes', self.__metadata,
            Column('id', INT, primary_key=True, autoincrement=True),
            Column('name', VARCHAR(100), nullable=False),
            Column('description', TEXT),
            Column('price', DECIMAL(10, 2), nullable=False),
            Column('quantity', INT, nullable=False),
            Column('is_available', BOOLEAN, nullable=False),
            Column('created_at', TIMESTAMP, default=datetime.now),
            Column('updated_at', TIMESTAMP, default=datetime.now, onupdate=datetime.now)
        )

        self.__orders = Table('orders', self.__metadata,
            Column('id', INT, primary_key=True, autoincrement=True),
            Column('user_id', ForeignKey('users.id'), nullable=False),
            Column('status', VARCHAR(50), nullable=False, default='In waiting'),
            Column('special_requests', TEXT),
            Column('created_at', TIMESTAMP, default=datetime.now),
            Column('updated_at', TIMESTAMP, default=datetime.now, onupdate=datetime.now)
        )

        self.__order_dish = Table('order_dish', self.__metadata,
            Column('id', INT, primary_key=True, autoincrement=True),
            Column('order_id', ForeignKey('orders.id'), nullable=False),
            Column('dish_id', ForeignKey('dishes.id'), nullable=False),
            Column('quantity', INT, nullable=False),
            Column('price', DECIMAL(10, 2), nullable=False),
            Column('created_at', TIMESTAMP, default=datetime.now),
            Column('updated_at', TIMESTAMP, default=datetime.now, onupdate=datetime.now)
        )

        # self.__metadata.drop_all(self.__engine)
        self.__metadata.create_all(self.__engine)

    @property
    def users(self):
        return self.__users

    @users.setter
    def users(self, *args, **kwargs):
        raise RuntimeError('Changing the database from the outside is prohibited')

    @property
    def sessions(self):
        return self.__sessions

    @sessions.setter
    def sessions(self, *args, **kwargs):
        raise RuntimeError('Changing the database from the outside is prohibited')

    @property
    def dishes(self):
        return self.__dishes

    @dishes.setter
    def dishes(self, *args, **kwargs):
        raise RuntimeError('Changing the database from the outside is prohibited')
    
    @property
    def orders(self):
        return self.__orders

    @orders.setter
    def orders(self, *args, **kwargs):
        raise RuntimeError('Changing the database from the outside is prohibited')
    
    @property
    def order_dish(self):
        return self.__order_dish

    @order_dish.setter
    def order_dish(self, *args, **kwargs):
        raise RuntimeError('Changing the database from the outside is prohibited')

    @property
    def metadata(self):
        return self.__metadata

    @metadata.setter
    def metadata(self, *args, **kwargs):
        raise RuntimeError('Changing the database from the outside is prohibited')

    @property
    def engine(self):
        return self.__engine

    @engine.setter
    def engine(self, *args, **kwargs):
        raise RuntimeError('Changing the database from the outside is prohibited')