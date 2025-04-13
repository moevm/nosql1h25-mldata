"""
Содержит сервисы приложения. Сервис представляет бизнес-логику приложения.
"""

from app.src.repository.dataset_repository import DatasetRepository


class DatasetService:
    """
    Класс-сервис для логики, связанной с датасетами.
    """

    @staticmethod
    def get_all_datasets_brief() -> list:
        """
        Обращается к методу репозитория для получения списка Brief'ов всех датасетов в БД.
        """
        return DatasetRepository.get_all_datasets_brief()
