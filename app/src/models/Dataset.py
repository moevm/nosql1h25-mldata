"""
Структура для хранения информации о датасете.
"""
from datetime import datetime
from io import StringIO

import pandas as pd

from app.src.models.DatasetFormValues import DatasetFormValues


class Dataset:
    """
    Структура для хранения информации о датасете.
    """

    def __init__(
            self,
            dataset_id: str,
            dataset_name: str,
            dataset_description: str,
            dataset_creation_date: datetime,
            dataset_author: str,
            dataset_rows: int,
            dataset_columns: int,
            dataset_size: float,
            dataset_version: int,
            dataset_last_update: datetime,
            dataset_path: str,
            dataset_last_editor: str,
    ):
        self.dataset_id: str = dataset_id
        self.dataset_name: str = dataset_name
        self.dataset_description: str = dataset_description
        self.dataset_creation_date: datetime = dataset_creation_date
        self.dataset_author: str = dataset_author
        self.dataset_columns: int = dataset_columns
        self.dataset_rows: int = dataset_rows
        self.dataset_size: float = dataset_size
        self.dataset_version: int = dataset_version
        self.dataset_last_update: datetime = dataset_last_update
        self.dataset_path: str = dataset_path
        self.dataset_last_editor: str = dataset_last_editor

    @classmethod
    def from_form_values(cls, form_values: DatasetFormValues, author: str, filepath: str):
        """
        Альтернативный конструктор для создания класса из `DatasetFormValues` и дополнительных аргументов
        """

        dataset_creation_date: datetime = datetime.now()
        dataset_last_update: datetime = dataset_creation_date
        dataset_path: str = filepath
        dataset_version: int = 1

        df: pd.DataFrame = pd.read_csv(StringIO(form_values.dataset_data))
        dataset_rows: int = df.shape[0]
        dataset_columns: int = df.shape[1]
        dataset_size: float = round(len(form_values.dataset_data.encode()) / 1024, 2)

        return cls('-1',
                   form_values.dataset_name, form_values.dataset_description,
                   dataset_creation_date, author, dataset_rows,
                   dataset_columns, dataset_size, dataset_version,
                   dataset_last_update, dataset_path, author)

    def to_dict(self) -> dict:
        """
        Метод для представления объекта класса в виде словаря.
        """
        return {
            'name':              self.dataset_name,
            'description':       self.dataset_description,
            'creationDate':      self.dataset_creation_date,
            'author':            self.dataset_author,
            'rowCount':          self.dataset_rows,
            'columnCount':       self.dataset_columns,
            'size':              self.dataset_size,
            'lastVersionNumber': self.dataset_version,
            'lastModifiedDate':  self.dataset_last_update,
            'path':              self.dataset_path,
            'lastModifiedBy':    self.dataset_author,
        }
