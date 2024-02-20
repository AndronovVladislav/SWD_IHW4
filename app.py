from flask import Flask

from users.users_microservice import UsersMicroservice
from menu.orders_microservice import OrdersMicroservice


def main():
    flask_app = Flask(__name__)
    app = UsersMicroservice('mysql', 'root', 'vlad', '127.0.0.1', '3306', 'IHW4', flask_app)
    app = OrdersMicroservice('mysql', 'root', 'vlad', '127.0.0.1', '3306', 'IHW4', flask_app)

    app.run()


if __name__ == '__main__':
    main()