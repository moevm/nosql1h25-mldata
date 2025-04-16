"""
Структура для хранения основных данных из формы создания датасета.
"""


class DatasetFormValues:
    """
    Структура для хранения данных из формы создания датасета.
    """

    def __init__(self, dataset_name: str, dataset_description: str, dataset_data: str):
        self.dataset_name: str = dataset_name
        self.dataset_description: str = dataset_description
        self.dataset_data: str = dataset_data
