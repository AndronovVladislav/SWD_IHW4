import hashlib
from datetime import datetime, timedelta

from flask import make_response, redirect, render_template, request, Response
from sqlalchemy.orm import Session as DBSession

from common.jwt_mixin import JWTMixin
from common.session_mixin import SessionMixin
from users.locals import AUTH_TEMPLATE
from users.models import User, Session
from common.db_manager import DBManager
from common.microservice_component_interface import MicroserviceComponentInterface


class AuthorizerComponent(MicroserviceComponentInterface, JWTMixin, SessionMixin):
    def __init__(self, db_manager: DBManager, register_url: str):
        self.db_manager = db_manager

        self.register_url = register_url

    def on_execute(self) -> Response:
        if not request.method == 'POST':
            return make_response(render_template(AUTH_TEMPLATE), 300)

        with DBSession(self.db_manager.engine) as session:
            user = session.query(User).filter(User.username == request.form['username']).first()

            if not user:
                return redirect(self.register_url)

            if not self.password_is_correct(request.form['password'], user.hashed_password):
                return make_response(render_template(AUTH_TEMPLATE), 300)

            user_session = self.get_session(session, user.id)

            next_day = datetime.now() + timedelta(days=1)
            jwt_token = self.emit_token({'userID': str(user.id), 'exp': next_day})

            if not user_session:
                session.add(Session(user_id=user.id, session_token=jwt_token))
            elif not self.validate_data(user_session.session_token):
                user_session.session_token = jwt_token
                session.add(user_session)

            session.commit()
            return make_response(f'Welcome, {user.username}!', 200)

    @staticmethod
    def password_is_correct(user_password: str, hashed_password: str) -> bool:
        password, salt = hashed_password.split(':')
        return password == str(hashlib.sha256(user_password.encode() + salt.encode()).hexdigest())

    def validate_data(self, jwt_token: str) -> bool:
        return self.validate_token(jwt_token)
