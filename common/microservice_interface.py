from abc import abstractmethod
from typing import Callable


class MicroserviceInterface:
    @abstractmethod
    def configure(self, **configs) -> None:
        """Задаёт изначальные настройки микросервиса"""

    @abstractmethod
    def add_endpoint(self,
                     endpoint: str,
                     endpoint_name: str,
                     handler: Callable,
                     methods: list[str],
                     *args,
                     **kwargs,
                     ) -> None:
        """Создаёт новый эндпоинт микросервиса"""

    @abstractmethod
    def run(self, **kwargs) -> None:
        """Запускает микросервис"""
