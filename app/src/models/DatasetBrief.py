"""
Структура для хранения краткой информации о датасете.
"""

class DatasetBrief:
    """
    Класс для хранения краткой информации о датасете.
    """

    def __init__(
            self,
            dataset_id: str | None = None,
            dataset_name: str | None = "Unnamed Dataset",
            dataset_description: str | None = "",
            dataset_type: str | None = "Unknown",
            dataset_size: int | None = 0
    ):
        self.dataset_id: str | None = dataset_id
        self.dataset_name: str = dataset_name or "Unnamed Dataset"
        self.dataset_description: str = dataset_description or ""
        self.dataset_type: str = dataset_type or "Unknown"
        self.dataset_size: int = dataset_size or 0

    def to_dict(self) -> dict:
        """
        Преобразует объект в словарь для сериализации в JSON
        """
        return {
            "dataset_id": self.dataset_id,
            "dataset_name": self.dataset_name,
            "dataset_description": self.dataset_description,
            "dataset_type": self.dataset_type,
            "dataset_size": self.dataset_size,
        }