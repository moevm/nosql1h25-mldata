"""
Структура для хранения краткой информации о датасете.
"""


class DatasetBrief:
    """
    Класс для хранения краткой информации о датасете.
    """

    def __init__(
            self,
            dataset_id: str,
            dataset_name: str,
            dataset_description: str,
            dataset_type: str,
            dataset_size: int
    ):
        self.dataset_id: str = dataset_id
        self.dataset_name: str = dataset_name
        self.dataset_description: str = dataset_description
        self.dataset_type: str = dataset_type
        self.dataset_size: int = dataset_size

    def to_dict(self) -> dict:
        """
        Преобразует объект в словарь для сериализации в JSON
        """

        return self.__dict__
