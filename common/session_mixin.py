from typing import Optional

from sqlalchemy.orm import Session as DBSession

from users.models import Session


class SessionMixin:

    @staticmethod
    def get_session(session: DBSession, user_id: int) -> Optional[Session]:
        return session.query(Session).filter(Session.user_id == user_id).first()
