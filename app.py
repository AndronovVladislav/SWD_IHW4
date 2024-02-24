from argparse import ArgumentParser

from flask import Flask

from users.users_microservice import UsersMicroservice
# from menu.orders_microservice import OrdersMicroservice
from menu.models import Dish
from common.db_manager import DBManager
from common.parse_mealty import parse_mealty


def main(dialect: str, dbapi: str, user: str, password: str, host: str, port: str, db: str):
    flask_app = Flask('SWD_IHW4')
    db_manager = DBManager(dialect, dbapi, user, password, host, port, db)

    parse_mealty(db_manager, Dish)
    app = UsersMicroservice(flask_app, db_manager)
    # app = OrdersMicroservice(flask_app, db_manager)

    app.run(debug=True, port=3000)


if __name__ == '__main__':
    # parser = ArgumentParser()

    # parser.add_argument('--dialect', dest='dialect', default='postgresql')
    # parser.add_argument('--db-api', dest='db_api', default='psycopg')
    # parser.add_argument('--user', dest='user', required=True)
    # parser.add_argument('--password', dest='password', required=True)
    # parser.add_argument('--host', dest='host', default='localhost')
    # parser.add_argument('--port', dest='port', default=5000)
    # parser.add_argument('--db', dest='db', default='restaurant')
    # args = parser.parse_args()
    #
    # main(args.dialect, args.db_api, args.user, args.password, args.host, args.port, args.db)
    main('postgresql', 'psycopg', 'v-andronov', '', 'localhost', '5000', 'restaurant')
