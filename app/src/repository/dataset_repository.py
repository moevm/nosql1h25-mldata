"""
Содержит репозитории приложения. Репозиторий напрямую работает с БД - добавляет, изменяет, удаляет и ищет записи в БД.
Необходимо полностью переделать, так как на данный момент вместо MongoDB используется локальный массив db.
"""
from app.src.models.DatasetBrief import DatasetBrief


class DatasetRepository:
    """
    Класс-репозиторий для данных, связанных с датасетами.
    """

    @staticmethod
    def get_all_datasets_brief() -> list:
        """
        Возвращает список Brief'ов всех датасетов в БД. Если БД пустая, то возвращается пустой список.
        """
        briefs = [
            DatasetBrief(
                "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
                "name",
                "description",
                "CSV",
                1
            )
        ]

        return briefs
