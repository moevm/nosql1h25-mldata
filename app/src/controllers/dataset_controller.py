"""
Содержит контроллеры приложения. Контроллер является связным звеном между запросами с клиента и бизнес-логикой.
"""
import json

from app.src.services.dataset_service import DatasetService


class DatasetController:
    """
    Класс-контроллер для запросов, связанных с датасетами.
    """

    @staticmethod
    def render_all_datasets() -> str:
        """
        Обращается к методу сервиса для получения списка Brief'ов всех датасетов в БД. Отображает страницу с полученными датасетами.
        """
        all_datasets_brief = DatasetService.get_all_datasets_brief()
        return json.dumps([brief.to_dict() for brief in all_datasets_brief])
