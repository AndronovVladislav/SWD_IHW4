from abc import abstractmethod
from typing import Optional

from flask import make_response, Response


class MicroserviceComponentInterface:
    @abstractmethod
    def on_execute(self, *args, **kwargs) -> Response:
        """Выполняет основное действие компонента"""

    @staticmethod
    def make_error(error_description, error_code, *args, **kwargs) -> Response:
        return make_response(error_description, error_code)

    def validate_data(self, *args, **kwargs) -> bool | tuple[Optional[Response], bool]:
        """Проверяет данные на корректность"""
        pass
