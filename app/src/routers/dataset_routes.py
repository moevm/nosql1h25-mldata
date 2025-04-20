"""
Настраивает пути для endpoint'ов приложения. Сохраняет их в blueprint.
"""
import os
from typing import Union

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
def add_dataset() -> Union[str, Response, BadRequest]:
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
def edit_dataset(dataset_id: str) -> Union[str, Response, BadRequest]:
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
def get_dataset(dataset_id: str) -> Union[str, BadRequest]:
    """
    Обращается к методам контроллера:
        GET - получения датасета из БД
    """
    if request.method != 'GET':
        return BadRequest('Invalid method')

    try:
        dataset_info: Dataset = DatasetController.get_dataset(dataset_id)
        return render_template('one_dataset.html', dataset_info=dataset_info)
    except Exception:
        return BadRequest('Item can\'t be found')


@bp.route('/dataset/download/<dataset_id>', methods=['GET'])
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
