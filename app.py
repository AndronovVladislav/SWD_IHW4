from flask import Flask
from users_microservice.users_manager import UsersManager
from menu_microservice.orders_manager import OrdersManager


if __name__ == '__main__':
    flask_app = Flask(__name__)
    app = UsersManager('mysql', 'root', 'vlad', '127.0.0.1', '3306', 'IHW4', flask_app)
    app = OrdersManager('mysql', 'root', 'vlad', '127.0.0.1', '3306', 'IHW4', flask_app)

    app.run(debug=True)