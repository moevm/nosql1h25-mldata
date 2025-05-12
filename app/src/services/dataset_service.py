"""
Содержит сервисы приложения. Сервис представляет бизнес-логику приложения.
"""
import uuid
from datetime import datetime, timezone
from typing import Optional, Tuple

from flask_login import current_user

from src.models.Dataset import Dataset
from src.models.DatasetFormValues import DatasetFormValues
from src.models.FilterValues import FilterValues
from src.repository.dataset_repository import DatasetRepository

from src.repository.user_repository import UserRepository
from werkzeug.datastructures import FileStorage

from io import BytesIO


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
    def save_dataset(form_values: DatasetFormValues, author_username: str, filepath: str) -> str:
        """
        Создает объект Dataset на основе `form_values`.
        Обращается к методу репозитория для добавления датасета в БД.
        Обновляет статистику пользователя.
        """
        dataset_id: str = str(uuid.uuid4())

        # add relation `author login` to created dataset
        author: Optional[User] = UserRepository.find_by_username(author_username)
        author_login = ""
        if author:
            author_login = author.login

        dataset_csv: Dataset = Dataset.from_form_values(form_values, dataset_id, author_username, author_login, filepath)

        inserted_id = DatasetRepository.add_dataset(dataset_csv)
        if current_user and current_user.is_authenticated:
            user = UserRepository.find_by_id(current_user.id)

            if user:
                update_payload = {
                    'createdDatasetsCount': user.createdDatasetsCount + 1
                }
                UserRepository.update_user_fields(user.id, update_payload)
                current_user.createdDatasetsCount = user.createdDatasetsCount + 1

        return inserted_id

    @staticmethod
    def update_dataset(dataset_id: str, form_values: DatasetFormValues, editor_username: str, filepath: str) -> None:
        """
        Создает объект Dataset на основе `form_values`.
        Обращается к методу репозитория для изменения датасета в БД.
        """
        old_dataset: Dataset = DatasetRepository.get_dataset(dataset_id)

        dataset: Dataset = Dataset.from_form_values(form_values, old_dataset.dataset_id, old_dataset.dataset_author,
                                                    old_dataset.dataset_author_login,
                                                    filepath)
        if not form_values.dataset_data:
            dataset.dataset_columns = old_dataset.dataset_columns
            dataset.dataset_rows = old_dataset.dataset_rows
            dataset.dataset_size = old_dataset.dataset_size

        dataset.dataset_creation_date = old_dataset.dataset_creation_date
        dataset.dataset_version = old_dataset.dataset_version + 1
        dataset.dataset_last_editor = editor_username

        DatasetRepository.edit_dataset(dataset)

    @staticmethod
    def get_dataset(dataset_id: str) -> Dataset:
        return DatasetRepository.get_dataset(dataset_id)

    @staticmethod
    def edit_dataset(dataset_id: str) -> Dataset:
        return DatasetRepository.edit_dataset(dataset_id)

    @staticmethod
    def remove_dataset(dataset_id: str) -> None:
        """
        Удаляет датасет и обновляет статистику пользователя.
        """
        dataset_to_remove: Optional[Dataset] = DatasetRepository.get_dataset(dataset_id)

        if not dataset_to_remove:
            DatasetRepository.remove_dataset(dataset_id)
            return

        author_login: str = dataset_to_remove.dataset_author_login

        DatasetRepository.remove_dataset(dataset_id)
        author_user: Optional[User] = UserRepository.find_by_login(author_login)

        if author_user:
            new_created_datasets_count = author_user.createdDatasetsCount - 1
            if new_created_datasets_count < 0:
                new_created_datasets_count = 0

            update_payload = {
                'createdDatasetsCount': new_created_datasets_count
            }
            UserRepository.update_user_fields(author_user.id, update_payload)

            # If the current logged-in user is the author of the removed dataset,
            # update their in-memory (session) object attributes as well.
            if current_user and current_user.is_authenticated and hasattr(current_user, 'id') and current_user.id == author_user.id:
                if hasattr(current_user, 'createdDatasetsCount'):
                    current_user.createdDatasetsCount = new_created_datasets_count
        else:
            # user not found?
            pass

    @staticmethod
    def export_datasets_archive() -> Tuple[BytesIO, str]:
        return DatasetRepository.export_datasets_archive()

    @staticmethod
    def import_datasets_archive(backup: FileStorage) -> None:
        return DatasetRepository.import_datasets_archive(backup)

    @staticmethod
    def extract_filter_values(request) -> FilterValues:
        form_data: dict = request.form

        name: str = form_data['name']

        size_from: Optional[float] = float(form_data['size-from']) if form_data['size-from'] != '' else None
        size_to: Optional[float] = float(form_data['size-to']) if form_data['size-to'] != '' else None

        row_size_from: Optional[int] = int(float(form_data['row-size-from'])) if form_data[
                                                                                     'row-size-from'] != '' else None
        row_size_to: Optional[int] = int(float(form_data['row-size-to'])) if form_data['row-size-to'] != '' else None

        column_size_from: Optional[int] = int(float(form_data['column-size-from'])) if form_data[
                                                                                           'column-size-from'] != '' else None
        column_size_to: Optional[int] = int(float(form_data['column-size-to'])) if form_data[
                                                                                       'column-size-to'] != '' else None

        creation_date_from: Optional[datetime] = datetime.strptime(form_data['creation-date-from'], '%Y-%m-%d') if \
        form_data['creation-date-from'] != '' else None
        creation_date_to: Optional[datetime] = datetime.strptime(form_data['creation-date-to'], '%Y-%m-%d') if \
        form_data['creation-date-to'] != '' else None

        modify_date_from: Optional[datetime] = datetime.strptime(form_data['modify-date-from'], '%Y-%m-%d') if \
        form_data['modify-date-from'] != '' else None
        modify_date_to: Optional[datetime] = datetime.strptime(form_data['modify-date-to'], '%Y-%m-%d') if form_data[
                                                                                                               'modify-date-to'] != '' else None

        sort: Optional[dict] = DatasetService._extract_sort(form_data)

        return FilterValues(
            name,
            size_from, size_to,
            row_size_from, row_size_to,
            column_size_from, column_size_to,
            creation_date_from, creation_date_to,
            modify_date_from, modify_date_to,
            sort
        )

    @staticmethod
    def _extract_sort(form_data: dict) -> Optional[dict]:
        if form_data['size-sort'] != '':
            return {'field': 'size', 'order': form_data['size-sort']}

        if form_data['row-size-sort'] != '':
            return {'field': 'rowCount', 'order': form_data['row-size-sort']}

        if form_data['column-size-sort'] != '':
            return {'field': 'columnCount', 'order': form_data['column-size-sort']}

        if form_data['creation-date-sort'] != '':
            return {'field': 'creationDate', 'order': form_data['creation-date-sort']}

        if form_data['modify-date-sort'] != '':
            return {'field': 'lastModifiedDate', 'order': form_data['modify-date-sort']}

        return None