"""
Создает сущность Flask и запускает ее. Добавляет к ней пути с помощью blueprint.
Настраивает Flask-Login.
"""

import os
from flask import Flask, redirect, url_for, flash, request
from flask_login import LoginManager, current_user

try:
    from src.routers import dataset_routes
    from src.routers import auth_routes
    from src.repository.user_repository import UserRepository
except ImportError:
    from app.src.routers import dataset_routes
    from app.src.routers import auth_routes
    from app.src.repository.user_repository import UserRepository


# --- Flask App Initialization ---
app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key_change_me')

# --- Flask-Login Initialization ---
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'auth.login'
login_manager.login_message = "Log in to access this page."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id: str):
    """
    Функция, используемая Flask-Login для перезагрузки 
    пользовательского объекта из идентификатора пользователя, сохраненного в сеансе.
    """
    return UserRepository.find_by_id(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    """
    Обработка несанкционированного доступа. 
    Перенаправляет на страницу входа в систему с сохранением первоначально запрошенного URL.
    """
    flash("Для доступа к странице требуется авторизация", "warning")
    next_url = request.path
    if request.query_string:
        next_url += '?' + request.query_string.decode('utf-8')

    return redirect(url_for('auth.login', next=next_url))


# --- Register Blueprints ---
app.register_blueprint(dataset_routes.bp)
app.register_blueprint(auth_routes.auth_bp)


# --- Root Route ---
@app.route('/')
def index():
    """Переход к страницам в зависимости от состояния авторизации"""
    if current_user.is_authenticated:
        return redirect(url_for('datasets.get_datasets'))
    else:
        return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true')