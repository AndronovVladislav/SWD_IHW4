import json
from typing import Optional

from flask import make_response, request, Response
from sqlalchemy.orm import Session as DBSession

from common.jwt_mixin import JWTMixin
from users.models import User, Session
from common.db_manager import DBManager
from common.microservice_component_interface import MicroserviceComponentInterface


class UsersInformantComponent(MicroserviceComponentInterface, JWTMixin):
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def on_execute(self) -> Response:
        token = request.args.get('token')

        with DBSession(self.db_manager.engine) as session:
            user_id, jwt_token = self.get_session_data(session, token)

            if not all((user_id, jwt_token)):
                return self.make_error('Authorize, please', 406)

            data_is_correct = self.validate_data(token)

            if not data_is_correct:
                return self.make_error('Reauthorize, please', 406)

            user = session.query(User).filter(User.id == user_id).first()
            structured_information = {info_part: f'{getattr(user, info_part)!s}'
                                      for info_part in ('username', 'email', 'role', 'create_datetime')}

            return make_response(json.dumps(structured_information), 200)

    @staticmethod
    def get_session_data(session: DBSession, jwt_token: str) -> tuple[Optional[int], Optional[str]]:
        session_data = session.query(Session).filter(Session.session_token == jwt_token).first()

        if not session_data:
            return None, None

        return session_data.user_id, session_data.session_token

    def validate_data(self, jwt_token: str) -> bool:
        return self.validate_token(jwt_token)
