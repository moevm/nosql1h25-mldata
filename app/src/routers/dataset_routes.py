"""
Настраивает пути для endpoint'ов приложения. Сохраняет их в blueprint.
"""
from flask import Blueprint
from flask_login import login_required, current_user

from app.src.controllers.dataset_controller import DatasetController

bp: Blueprint = Blueprint('datasets', __name__, url_prefix='/datasets')


@bp.route('/', methods=['GET'])
@login_required
def get_datasets() -> str:
    """
    Обращается с методу контроллера для отображения страницы со всеми датасетами.
    Требует аутентификации.
    """
    print(f"User {current_user.login} (Admin: {current_user.is_admin}) accessing datasets.")

    return DatasetController.render_all_datasets()