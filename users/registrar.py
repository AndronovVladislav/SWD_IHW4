import hashlib
import uuid
from typing import Optional

from flask import make_response, redirect, render_template, request, Response
from sqlalchemy.orm import Session

from users.locals import REGISTER_TEMPLATE
from users.models import User
from common.db_manager import DBManager
from common.microservice_component_interface import MicroserviceComponentInterface


class RegistrarComponent(MicroserviceComponentInterface):
    def __init__(self, db_manager: DBManager, signin_url: str):
        self.db_manager = db_manager

        self.signin_url = signin_url

    def on_execute(self) -> Response:
        if not request.method == 'POST':
            return make_response(render_template(REGISTER_TEMPLATE), 200)

        username, password, email, role = (request.form.get(k) for k in ('username', 'password', 'email', 'role'))

        with Session(self.db_manager.engine) as session:
            if self.user_exists(session, username, email):
                return redirect(self.signin_url)

            response, data_is_correct = self.validate_data(email, password, role)

            if not data_is_correct:
                return response

            new_user = User(username=username,
                            email=email,
                            hashed_password=self.hash_password(password),
                            role=(role if role else 'customer'),
                            )

            session.add(new_user)
            session.commit()

        return make_response('New user registered!', 200)

    @staticmethod
    def hash_password(password):
        salt = uuid.uuid4().hex.encode()
        return f'{hashlib.sha256(password.encode() + salt).hexdigest()!s}:{salt.decode()}'

    @staticmethod
    def user_exists(session: Session, username: str, email: str) -> bool:
        if session.query(User).where(User.username == username, User.email == email).count():
            return True

    def validate_data(self,
                      email: str,
                      password: str,
                      role: str | None = None,
                      ) -> tuple[Optional[Response], bool]:
        if '@' not in email:
            return self.make_error('Invalid email format', 406), False

        if len(password) < 8:
            return self.make_error('Too short password', 406), False

        if role not in ('customer', 'chef', 'manager', None):
            return self.make_error('Invalid role', 406), False
        
        return None, True
