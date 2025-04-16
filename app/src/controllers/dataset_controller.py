"""
Содержит контроллеры приложения. Контроллер является связным звеном между запросами с клиента и бизнес-логикой.
"""
import json
import os

from flask import Request, Response, current_app, make_response, jsonify
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
    def add_dataset(request: Request) -> Response:
        """
        Создается объект DatasetFormData из данных request'а.
        Обращается к методу сервиса для добавления датасета в БД.
        Сохраняется файл в выделенной директории.
        Возвращается response, содержащий URL страницы, открываемой после добавления.
        """
        username = 'username'

        form_values: DatasetFormValues = DatasetController._extract_form_values(request)

        filepath: str = current_app.config['UPLOAD_FOLDER']
        dataset_id = DatasetService.save_dataset(form_values, author=username, filepath=filepath)

        filepath = os.path.join(filepath, f'{dataset_id}.csv')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'x') as file:
            file.writelines(form_values.dataset_data)

        response: Response = make_response()
        response.headers['redirect'] = '/datasets/'
        return response

    @staticmethod
    def edit_dataset(dataset_id: str, request: Request) -> Response:
        """
        Создается объект DatasetFormData из данных request'а.
        Обращается к методу сервиса для изменения датасета в БД.
        Сохраняется файл в выделенной директории.
        Возвращается response, содержащий URL страницы, открываемой после добавления.
        """

        username = 'username'

        form_values: DatasetFormValues = DatasetController._extract_form_values(request)
        filepath: str = current_app.config['UPLOAD_FOLDER']
        filepath: str = os.path.join(filepath, f'{dataset_id}.csv')
        with open(filepath, 'w') as file:
            file.writelines(form_values.dataset_data)

        DatasetService.update_dataset(dataset_id, form_values, author=username, filepath=filepath)

        response: Response = make_response()
        response.headers['redirect'] = f'/datasets/{dataset_id}'
        return response

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
        dataset_data = '\n'.join([v.decode('utf-8').strip() for v in dataset_fs.readlines()])
        return DatasetFormValues(dataset_name, dataset_description, dataset_data)
