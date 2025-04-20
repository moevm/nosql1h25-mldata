"""
Настраивает пути для endpoint'ов приложения. Сохраняет их в blueprint.
"""
import os
import pandas as pd

from flask import Blueprint, Response, request, send_from_directory, current_app, render_template
from flask_login import login_required
from werkzeug.exceptions import BadRequest

from app.src.controllers.dataset_controller import DatasetController
from app.src.models import Dataset

bp: Blueprint = Blueprint('datasets', __name__)


@bp.route('/datasets', methods=['GET'], strict_slashes=False)
@login_required
def get_datasets() -> str:
    """
    Обращается с методу контроллера для отображения страницы со всеми датасетами.
    Требует аутентификации.
    """
    return DatasetController.render_all_datasets()


@bp.route('/datasets/add/', methods=['GET', 'POST'])
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


@bp.route('/datasets/edit/<dataset_id>/', methods=['GET', 'PATCH'])
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
def get_dataset(dataset_id: str) -> BadRequest | tuple[str, int] | str:
    """
    Обращается к методам контроллера:
        GET - получения датасета из БД
    """
    if request.method != 'GET':
        return BadRequest('Invalid method')

    try:
        dataset_info: Dataset = DatasetController.get_dataset(dataset_id)
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

        return render_template(
            'one_dataset.html',
            dataset_info=dataset_info,
            headers=headers,
            rows=rows,
            max_cols_num=max_cols_num,
        )

    except FileNotFoundError:
        return "CSV file not found on server", 404

    except Exception:
        return "Something went wrong", 500


@bp.route('/dataset/download/<dataset_id>', methods=['GET'])
def download_dataset(dataset_id: str):
    """
    Обращается к методам контроллера:
        GET - получения файла с датасетом из БД
    """

    if request.method != 'GET':
        return BadRequest('Invalid method')

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'], f'{dataset_id}.csv'
    )
