from datetime import datetime, timedelta
from typing import Any

import jwt


class JWTMixin:
    encryption_key = 'KAMKINO'

    def validate_token(self, token: str) -> bool:
        try:
            # FIXME: -timedelta(hours=3) это костыль, в идеале разобраться с тайм-зонами
            decoded_token = jwt.decode(token, self.encryption_key, algorithms=['HS256'])
            expires_at = datetime.fromtimestamp(decoded_token['exp']) - timedelta(hours=3)
            if expires_at > datetime.now():
                return True
            return False
        except jwt.ExpiredSignatureError:
            return False

    def emit_token(self, payload: dict[Any, Any]) -> str:
        return jwt.encode(payload, self.encryption_key)
