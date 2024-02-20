from abc import abstractmethod


class MicroserviceComponentInterface:
    @abstractmethod
    def on_execute(self):
        """Выполняет основное действие"""

    @abstractmethod
    def make_error(self, error_description):
        """Формирует сообщение об ошибке"""

    @abstractmethod
    def validate_data(self, **kwargs):
        """Проверяет данные на корректность"""
