"""
Содержит контроллеры приложения. Контроллер является связным звеном между запросами с клиента и бизнес-логикой.
"""
import os
from pathlib import PosixPath

from typing import Optional
from flask import render_template, Request, Response, current_app, make_response, jsonify
from flask_login import current_user
from werkzeug.datastructures import FileStorage

from src.models.FilterValues import FilterValues
from src.models.Dataset import Dataset
from src.models.DatasetFormValues import DatasetFormValues
from src.services.dataset_service import DatasetService


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
        return render_template('all_datasets.html', datasets_brief=all_datasets_brief)

    @staticmethod
    def filter_datasets(request: Request) -> Response:
        """
        Обращается к методу сервиса для получения списка Brief'ов датасетов, которые прошли фильтрацию.
        """

        filters: FilterValues = DatasetService.extract_filter_values(request)
        filtered_briefs: list = DatasetService.get_filtered_briefs(filters)

        response: Response = make_response(jsonify([brief.to_dict() for brief in filtered_briefs]), 200)
        return response

    @staticmethod
    def add_dataset(request: Request) -> Response:
        """
        Создается объект DatasetFormData из данных request'а.
        Обращается к методу сервиса для добавления датасета в БД.
        Сохраняется файл в выделенной директории.
        Возвращается response, содержащий URL страницы, открываемой после добавления.
        """
        try:
            username = current_user.username
        except Exception:
            username = 'noname'

        form_values: DatasetFormValues = DatasetController._extract_form_values(request)

        filepath: str = current_app.config['UPLOAD_FOLDER']
        dataset_id = DatasetService.save_dataset(form_values, author=username, filepath=filepath)

        filepath = os.path.join(filepath, f'{dataset_id}.csv')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'x') as file:
            file.writelines(form_values.dataset_data)

        DatasetService.save_plots(dataset_id)
        response: Response = make_response()
        response.headers['redirect'] = '/datasets/'
        return response

    @staticmethod
    def render_add_dataset() -> str:
        """
        Отображает страницу добавления датасета.
        """
        return render_template('add_dataset.html')

    @staticmethod
    def render_edit_dataset(dataset_id: str) -> str:
        """
        Обращается к методу сервиса для получения объекта Brief для датасета с индексом dataset_id.
        """
        dataset_brief: Dataset = DatasetService.get_dataset(dataset_id)
        return render_template('edit_dataset.html', dataset_brief=dataset_brief)

    @staticmethod
    def remove_dataset(dataset_id: str) -> Response:
        """
        Обращается к методу сервиса для удаления объекта датасета с индексом dataset_id.
        При удалении датасета, так же удаляются связанные с ним графики.
        """
        DatasetService.remove_dataset(dataset_id)
        DatasetService.remove_graphs(dataset_id)

        filepath: str = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(filepath, f'{dataset_id}.csv')
        PosixPath(filepath).unlink()

        response: Response = make_response()
        response.headers['redirect'] = f'/datasets/{dataset_id}'
        return response

    @staticmethod
    def edit_dataset(dataset_id: str, request: Request) -> Response:
        """
        Создается объект DatasetFormData из данных request'а.
        Обращается к методу сервиса для изменения датасета в БД.
        Сохраняется файл в выделенной директории.
        Возвращается response, содержащий URL страницы, открываемой после добавления.
        В случае смены файла, графики перерисовываются.
        """

        try:
            username = current_user.username
        except Exception:
            username = 'noname'

        form_values: DatasetFormValues = DatasetController._extract_form_values(request)

        file_changed: bool = False
        if request.files['dataset']:
            filepath: str = current_app.config['UPLOAD_FOLDER']
            filepath: str = os.path.join(filepath, f'{dataset_id}.csv')
            with open(filepath, 'w') as file:
                file.writelines(form_values.dataset_data)
            file_changed = True

        DatasetService.update_dataset(dataset_id, form_values, editor=username,
                                      filepath=current_app.config['UPLOAD_FOLDER'])
        if file_changed:
            DatasetService.update_graphs(dataset_id)

        response: Response = make_response()
        response.headers['redirect'] = f'/datasets/'
        return response

    @staticmethod
    def get_dataset(dataset_id: str) -> Dataset:
        """
        Возвращается структура, содержащая данные о датасете.
        """
        dataset: Dataset = DatasetService.get_dataset(dataset_id)
        return dataset

    @staticmethod
    def get_plots(dataset_id: str) -> Optional[dict[list]]:
        return DatasetService.get_plots(dataset_id)

    @staticmethod
    def _extract_form_values(request) -> DatasetFormValues:
        form_data = request.form
        dataset_name: str = form_data['name']
        dataset_description: str = form_data['description']

        dataset_fs: FileStorage = request.files['dataset']
        dataset_data = '\n'.join([v.decode('utf-8').strip() for v in dataset_fs.readlines()])
        return DatasetFormValues(dataset_name, dataset_description, dataset_data)
