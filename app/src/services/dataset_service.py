"""
Содержит сервисы приложения. Сервис представляет бизнес-логику приложения.
"""
import uuid
from typing import Optional

from bson import ObjectId

from app.src.models.Dataset import Dataset
from app.src.models.DatasetFormValues import DatasetFormValues
from app.src.models.FilterValues import FilterValues
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

    @staticmethod
    def get_filtered_briefs(filters: FilterValues) -> list:
        """
        Обращается к методу репозитория для получения списка Brief'ов датасетов, которые прошли фильтрацию.
        """
        return DatasetRepository.get_filtered_briefs(filters)

    @staticmethod
    def save_dataset(form_values: DatasetFormValues, author: str, filepath: str) -> str:
        """
        Создает объект Dataset на основе `form_values`.
        Обращается к методу репозитория для добавления датасета в БД.
        """
        dataset_id: str = str(uuid.uuid4())
        dataset_csv: Dataset = Dataset.from_form_values(form_values, dataset_id, author, filepath)

        return DatasetRepository.add_dataset(dataset_csv)

    @staticmethod
    def update_dataset(dataset_id: str, form_values: DatasetFormValues, editor: str, filepath: str) -> None:
        """
        Создает объект Dataset на основе `form_values`.
        Обращается к методу репозитория для изменения датасета в БД.
        """
        old_dataset: Dataset = DatasetRepository.get_dataset(dataset_id)

        dataset: Dataset = Dataset.from_form_values(form_values, old_dataset.dataset_id, old_dataset.dataset_author, filepath)
        if not form_values.dataset_data:
            dataset.dataset_columns = old_dataset.dataset_columns
            dataset.dataset_rows = old_dataset.dataset_rows
            dataset.dataset_size = old_dataset.dataset_size

        dataset.dataset_creation_date = old_dataset.dataset_creation_date
        dataset.dataset_version = old_dataset.dataset_version + 1
        dataset.dataset_last_editor = editor

        DatasetRepository.edit_dataset(dataset)

    @staticmethod
    def get_dataset(dataset_id: str) -> Dataset:
        return DatasetRepository.get_dataset(dataset_id)

    @staticmethod
    def remove_dataset(dataset_id: str) -> None:
        return DatasetRepository.remove_dataset(dataset_id)

    @staticmethod
    def extract_filter_values(request) -> FilterValues:
        form_data = request.form

        name: str = form_data['name']

        size_from: Optional[int] = int(form_data['size-from']) if form_data['size-from'] != '' else None
        size_to: Optional[int] = int(form_data['size-to']) if form_data['size-to'] != '' else None

        row_size_from: Optional[int] = int(form_data['row-size-from']) if form_data['row-size-from'] != '' else None
        row_size_to: Optional[int] = int(form_data['row-size-to']) if form_data['row-size-to'] != '' else None

        column_size_from: Optional[int] = int(form_data['column-size-from']) if form_data[
                                                                                    'column-size-from'] != '' else None
        column_size_to: Optional[int] = int(form_data['column-size-to']) if form_data['column-size-to'] != '' else None

        return FilterValues(name, size_from, size_to, row_size_from, row_size_to, column_size_from, column_size_to)
