from flask import Flask
from users_microservice.users_microservice import UsersMicroservice
from menu_microservice.orders_microservice import OrdersMicroservice


if __name__ == '__main__':
    flask_app = Flask(__name__)
    app = UsersMicroservice('mysql', 'root', 'vlad', '127.0.0.1', '3306', 'IHW4', flask_app)
    app = OrdersMicroservice('mysql', 'root', 'vlad', '127.0.0.1', '3306', 'IHW4', flask_app)

    app.run()