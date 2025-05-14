"""
Настраивает пути для endpoint'ов приложения. Сохраняет их в blueprint.
"""
import os
import pandas as pd

from flask import Blueprint, Response, request, send_from_directory, current_app, render_template
from flask_login import login_required
from werkzeug.exceptions import BadRequest
from typing import Optional

from src.controllers.dataset_controller import DatasetController
from src.controllers.admin_controller import AdminController

from src.models import Dataset
from src.util.decorators import admin_required

bp: Blueprint = Blueprint('datasets', __name__)


@bp.route('/datasets', methods=['GET'], strict_slashes=False)
@login_required
def get_datasets() -> str:
    """
    Обращается с методу контроллера для отображения страницы со всеми датасетами.
    Требует аутентификации.
    """
    return DatasetController.render_all_datasets()


@bp.route('/datasets/filter/', methods=['POST'])
@login_required
def filter_datasets() -> Response | BadRequest:
    """
    Обращается с методу контроллера для получения списка Brief'ов датасетов, которые прошли фильтарцию.
    Требует аутентификации.
    """
    if request.method != 'POST':
        return BadRequest('Invalid method')
    return DatasetController.filter_datasets(request)

@bp.route('/datasets/add/', methods=['GET', 'POST'])
@login_required
def add_dataset() -> str | Response | BadRequest:
    """
    Обращается к методам контроллера:
        POST - для добавления датасета в БД. Информация о датасете содержится в передаваемом request.
    """
    if request.method == 'POST':
        return DatasetController.add_dataset(request)
    elif request.method == 'GET':
        return DatasetController.render_add_dataset()
    return BadRequest('Invalid method')


@bp.route('/datasets/delete/<dataset_id>', methods=['DELETE'])
@login_required
def delete_dataset(dataset_id: str) -> str | Response | BadRequest:
    if request.method != 'DELETE':
        return BadRequest('Invalid method')
    return DatasetController.remove_dataset(dataset_id)


@bp.route('/datasets/edit/<dataset_id>/', methods=['GET', 'PATCH'])
@login_required
def edit_dataset(dataset_id: str) -> str | Response | BadRequest:
    """
    Обращается к методам контроллера:
        PATCH - для изменения датасета в БД
    """
    if request.method == 'PATCH':
        return DatasetController.edit_dataset(dataset_id, request)
    elif request.method == 'GET':
        return DatasetController.render_edit_dataset(dataset_id)

    raise BadRequest('Invalid method')


@bp.route('/dataset/<dataset_id>/', methods=['GET'])
@login_required
def get_dataset(dataset_id: str) -> BadRequest | tuple[str, int] | str:
    """
    Обращается к методам контроллера:
        GET - получения датасета из БД
    """
    if request.method != 'GET':
        return BadRequest('Invalid method')

    try:
        dataset_info: Dataset = DatasetController.get_dataset(dataset_id)
        dataset_graphs: Optional[list[dict]] = DatasetController.get_plots(dataset_id)
        filepath: str = f'{dataset_info.dataset_path}/{dataset_info.dataset_id}.csv'

        max_cols_num: int = int(os.getenv('MAX_COLS_NUM'))
        max_rows_num: int = int(os.getenv('MAX_ROWS_NUM'))

        df = pd.read_csv(filepath, nrows=max_rows_num, usecols=range(min(dataset_info.dataset_columns, max_cols_num)))

        if dataset_info.dataset_columns > max_cols_num:
            df['...'] = '...'

        headers = df.columns.tolist()
        rows = df.values.tolist()

        if dataset_info.dataset_rows > max_rows_num:
            rows.append(['...'] * min(dataset_info.dataset_columns, max_cols_num))

        dataset_graphs = [] if dataset_graphs is None else dataset_graphs
        for d in dataset_graphs:
            d['data'] = d['data'].decode('utf-8')

        return render_template(
            'one_dataset.html',
            dataset_info=dataset_info,
            headers=headers,
            rows=rows,
            max_cols_num=max_cols_num,
            plots=dataset_graphs,
        )

    except FileNotFoundError:
        return "CSV file not found on server", 404

    except Exception:
        return "Something went wrong", 500


@bp.route('/dataset/download/<dataset_id>', methods=['GET'])
@login_required
def download_dataset(dataset_id: str):
    """
    Обращается к методам контроллера:
        GET - получения файла с датасетом из БД
    """

    if request.method != 'GET':
        return BadRequest('Invalid method')

    dr = os.getcwd() + current_app.config['UPLOAD_FOLDER'][1:]  # slice: ./dir_name => dir_name
    return send_from_directory(
       directory=dr, path=f'{dataset_id}.csv', as_attachment=True
    )

@bp.route('/datasets/export', methods=['GET'])
@admin_required
def export_datasets() -> Response | BadRequest:
    """
    Обращается к методу контроллера для массового экспорта датасетов.
    """
    if request.method != 'GET':
        return BadRequest('Invalid method')

    return DatasetController.export_datasets()

@bp.route('/datasets/import', methods=['POST'])
@admin_required
def import_datasets() -> Response | BadRequest:
    """
    Обращается к методу контроллера для массового импорта датасетов.
    """
    if request.method != 'POST':
        return BadRequest('Invalid method')

    return DatasetController.import_datasets(request)

@bp.route('/ban/<user_id>', methods=['POST'])
@admin_required
def ban_user(user_id: str) -> str | BadRequest:
    """
    Обращается к методу контроллера для блокирования пользователя
    """
    if request.method != 'POST':
        return BadRequest('Invalid method')
    
    ban_result = AdminController.ban_user(user_id=user_id)
    if ban_result[0]:
        return ban_result[1]
    return BadRequest(ban_result[1])


@bp.route('/unban/<user_id>', methods=['POST'])
@admin_required
def unban_user(user_id: str) -> str | BadRequest:
    """
    Обращается к методу контроллера для разблокирования пользователя
    """
    if request.method != 'POST':
        return BadRequest('Invalid method')
    
    unban_result = AdminController.unban_user(user_id=user_id)
    if unban_result[0]:
        return unban_result[1]
    return BadRequest(unban_result[1])
