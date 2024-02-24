from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    pass


class DBManager:

    def __init__(self, dialect: str, dbapi: str, user: str, password: str, host: str, port: str, db: str):
        engine_settings = f'{dialect}+{dbapi}'
        user_settings = f'{user}:{password}'
        db_settings = f'{host}:{port}/{db}'
        self.settings = f'{engine_settings}://{user_settings}@{db_settings}'
        self.engine = create_engine(self.settings)

        Model.metadata.create_all(self.engine)

    # def __del__(self):
    #     Model.metadata.drop_all(self.engine)
