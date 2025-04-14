"""
Содержит контроллеры приложения. Контроллер является связным звеном между запросами с клиента и бизнес-логикой.
"""
import json

from flask import jsonify
from werkzeug.datastructures import FileStorage

from app.src.models.Dataset import Dataset
from app.src.models.DatasetFormValues import DatasetFormValues
from app.src.services.dataset_service import DatasetService


class DatasetController:
    """
    Класс-контроллер для запросов, связанных с датасетами.
    """

    @staticmethod
    def render_all_datasets() -> str:
        """
        Обращается к методу сервиса для получения списка Brief'ов всех датасетов в БД.
        Отображает страницу с полученными датасетами.
        """
        all_datasets_brief = DatasetService.get_all_datasets_brief()
        return json.dumps([brief.to_dict() for brief in all_datasets_brief])

    @staticmethod
    def get_dataset(dataset_id: str):
        """
        Возвращается json, содержащий данные о датасете.
        """
        dataset: Dataset = DatasetService.get_dataset(dataset_id)
        return jsonify(dataset.to_dict())

    @staticmethod
    def _extract_form_values(request) -> DatasetFormValues:
        form_data = request.form
        dataset_name: str = form_data['name']
        dataset_description: str = form_data['description']

        dataset_fs: FileStorage = request.files['dataset']
        dataset_data = ''.join([v.decode('utf-8') for v in dataset_fs.readlines()])
        return DatasetFormValues(dataset_name, dataset_description, dataset_data)
