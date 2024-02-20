from abc import abstractmethod


class MicroserviceInterface:
    @abstractmethod
    def configure(self, **configs):
        """Задаёт изначальные настройки микросервиса"""

    @abstractmethod
    def add_endpoint(self, endpoint, endpoint_name, handler, methods, *args, **kwargs):
        """Создаёт новый эндпоинт микросервиса"""

    @abstractmethod
    def run(self, **kwargs):
        """Запускает микросервис"""
