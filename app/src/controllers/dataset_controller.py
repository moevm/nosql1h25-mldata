"""
Содержит контроллеры приложения. Контроллер является связным звеном между запросами с клиента и бизнес-логикой.
"""
import os

from io import BytesIO
from pathlib import PosixPath
from typing import Optional
from flask import render_template, Request, Response, current_app, make_response, jsonify, flash, redirect, url_for, send_file
from flask_login import current_user
from werkzeug.datastructures import FileStorage

from src.models.Dataset import Dataset
from src.models.DatasetActivity import DatasetActivity
from src.models.DatasetFormValues import DatasetFormValues
from src.models.FilterValues import FilterValues
from src.services.dataset_service import DatasetService
from werkzeug.exceptions import BadRequest


class DatasetController:
    """
    Класс-контроллер для запросов, связанных с датасетами.
    """
    @staticmethod
    def update_dataset(dataset_id: str, form_values: DatasetFormValues, editor_username: str, filepath: str) -> None:
        old_dataset: Dataset = DatasetService.get_dataset(dataset_id)

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

        DatasetService.edit_dataset(dataset)

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
        dataset_id = DatasetService.save_dataset(form_values, author_username=username, filepath=filepath)

        filepath = os.path.join(filepath, f'{dataset_id}.csv')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'x') as file:
            file.writelines(form_values.dataset_data)

        DatasetService.init_dataset_activity(dataset_id)

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
    def render_edit_dataset(dataset_id: str) -> str | BadRequest:
        """
        Обращается к методу сервиса для получения объекта Brief для датасета с индексом dataset_id.
        """
        dataset_brief: Dataset = DatasetService.get_dataset(dataset_id)
        if dataset_brief.dataset_author_login != current_user.login and not current_user.is_admin:
            return BadRequest('Invalid user')

        return render_template('edit_dataset.html', dataset_brief=dataset_brief)

    @staticmethod
    def remove_dataset(dataset_id: str) -> Response | BadRequest:
        """
        Обращается к методу сервиса для удаления объекта датасета с индексом dataset_id.
        При удалении датасета, так же удаляются связанные с ним графики.
        """
        try:
            DatasetService.remove_dataset(dataset_id)
        except Exception as e:
            return BadRequest(f'Invalid user: {e}')

        DatasetService.remove_graphs(dataset_id)

        filepath: str = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(filepath, f'{dataset_id}.csv')
        PosixPath(filepath).unlink()

        response: Response = make_response()
        response.headers['redirect'] = f'/datasets/{dataset_id}'
        return response
    
    @staticmethod
    def edit_dataset(dataset_id: str, request: Request) -> BadRequest | Response:
        """
        Создается объект DatasetFormData из данных request'а.
        Обращается к методу сервиса для изменения датасета в БД.
        Сохраняется файл в выделенной директории.
        Возвращается response, содержащий URL страницы, открываемой после добавления.
        В случае смены файла, графики перерисовываются.
        """

        try:
            username = current_user.username
        except Exception as e:
            return BadRequest(f'Invalid user: {e}')

        form_values: DatasetFormValues = DatasetController._extract_form_values(request)

        try:
            DatasetService.update_dataset(dataset_id, form_values, editor_username=username,
                                          filepath=current_app.config['UPLOAD_FOLDER'])
        except Exception as e:
            return BadRequest(f'Invalid user: {e}')

        file_changed: bool = False
        if request.files['dataset']:
            filepath: str = current_app.config['UPLOAD_FOLDER']
            filepath: str = os.path.join(filepath, f'{dataset_id}.csv')
            with open(filepath, 'w') as file:
                file.writelines(form_values.dataset_data)
            file_changed = True

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
    def incr_dataset_views(dataset_id: str) -> None:
        DatasetService.incr_dataset_views(dataset_id)
    
    @staticmethod
    def incr_dataset_downloads(dataset_id: str) -> None:
        DatasetService.incr_dataset_downloads(dataset_id)
    
    @staticmethod
    def get_dataset_activity(dataset_id: str) -> Dataset:
        """
        Возвращается структура, содержащая данные о датасете.
        """
        activity: DatasetActivity = DatasetService.get_dataset_activity(dataset_id)
        return activity

    @staticmethod
    def get_plots(dataset_id: str) -> Optional[dict[list]]:
        return DatasetService.get_plots(dataset_id)

    @staticmethod
    def export_datasets() -> Response:
        """
        Обращается к методу сервиса для получения архива, содержащего дамп БД.
        """
        zip_file_bytes: BytesIO
        file_name: str
        zip_file_bytes, file_name = DatasetService.export_datasets_archive()

        response = make_response(send_file(
            zip_file_bytes,
            mimetype='application/zip',
            as_attachment=True,
            download_name=file_name
        ))
        return response

    @staticmethod
    def import_datasets(request: Request) -> Response:
        """
        Обращается к методу сервиса для загрузки архива, содержащего дамп БД.
        """
        backup: FileStorage = request.files['backup']
        DatasetService.import_datasets_archive(backup)

        response: Response = make_response()
        response.headers['redirect'] = f'/datasets/'
        return response

    @staticmethod
    def _extract_form_values(request) -> DatasetFormValues:
        form_data = request.form
        dataset_name: str = form_data['name']
        dataset_description: str = form_data['description']

        dataset_fs: FileStorage = request.files['dataset']
        dataset_data = '\n'.join([v.decode('utf-8').strip() for v in dataset_fs.readlines()])
        return DatasetFormValues(dataset_name, dataset_description, dataset_data)