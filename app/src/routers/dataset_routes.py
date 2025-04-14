"""
Настраивает пути для endpoint'ов приложения. Сохраняет их в blueprint.
"""
from typing import Union

from flask import Blueprint, Response, request
from werkzeug.exceptions import BadRequest

from app.src.controllers.dataset_controller import DatasetController

bp: Blueprint = Blueprint('datasets', __name__)


@bp.route('/datasets/', methods=['GET'])
def get_datasets() -> str:
    """
    Обращается с методу контроллера для отображения страницы со всеми датасетами.
    """
    return DatasetController.render_all_datasets()


@bp.route('/datasets/add/', methods=['POST'])
def add_dataset() -> Union[str, Response, BadRequest]:
    """
    Обращается к методам контроллера:
        POST - для добавления датасета в БД. Информация о датасете содержится в передаваемом request.
    """
    if request.method == 'POST':
        return DatasetController.add_dataset(request)
    return BadRequest('Invalid method')


@bp.route('/datasets/edit/<dataset_id>/', methods=['PATCH'])
def edit_dataset(dataset_id: str) -> Union[str, Response, BadRequest]:
    """
    Обращается к методам контроллера:
        PATCH - для изменения датасета в БД
    """
    if request.method == 'PATCH':
        return DatasetController.edit_dataset(dataset_id, request)
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
        return DatasetController.get_dataset(dataset_id)
    except Exception:
        return BadRequest('Item can\'t be found')
