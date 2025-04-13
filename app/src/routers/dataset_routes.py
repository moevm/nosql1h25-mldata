"""
Настраивает пути для endpoint'ов приложения. Сохраняет их в blueprint.
"""
from flask import Blueprint

from app.src.controllers.dataset_controller import DatasetController

bp: Blueprint = Blueprint('datasets', __name__)


@bp.route('/datasets/', methods=['GET'])
def get_datasets() -> str:
    """
    Обращается с методу контроллера для отображения страницы со всеми датасетами.
    """
    return DatasetController.render_all_datasets()
