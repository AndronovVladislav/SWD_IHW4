from argparse import ArgumentParser

from flask import Flask

from users.users_microservice import UsersMicroservice
from menu.orders_microservice import OrdersMicroservice
from menu.models import Dish
from common.db_manager import DBManager
from common.parse_mealty import parse_mealty


def main(dialect: str,
         dbapi: str,
         user: str,
         password: str,
         db_host: str,
         db_port: str,
         db: str,
         flask_host: str,
         flask_port: int,
         ) -> None:
    db_manager = DBManager(dialect, dbapi, user, password, db_host, db_port, db)
    parse_mealty(db_manager, Dish)
    app = Flask('SWD_IHW4')

    for microservice in UsersMicroservice(app, db_manager), OrdersMicroservice(app, db_manager):
        microservice.include_in_app()

    app.run(host=flask_host, port=flask_port)


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--dialect', dest='dialect', default='postgresql')
    parser.add_argument('--db-api', dest='db_api', default='psycopg')

    parser.add_argument('--user', dest='user', required=True)
    parser.add_argument('--password', dest='password', required=True)
    parser.add_argument('--db-host', dest='db_host', default='localhost')
    parser.add_argument('--db-port', dest='db_port', default=5000)
    parser.add_argument('--db', dest='db', default='restaurant')

    parser.add_argument('--flask-host', dest='flask_host', default='localhost')
    parser.add_argument('--flask-port', dest='flask_port', default=3000)
    args = parser.parse_args()

    main(args.dialect,
         args.db_api,
         args.user,
         args.password,
         args.db_host,
         args.db_port,
         args.db,
         args.flask_host,
         int(args.flask_port),
         )
