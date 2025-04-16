"""
Настраивает пути для endpoint'ов аутентификации (login/logout).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import LoginManager
from urllib.parse import urlparse

from app.src.repository.user_repository import UserRepository

auth_bp: Blueprint = Blueprint('auth', __name__, template_folder='templates')

# --- Flask-Login Initialization ---
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Для доступа к странице требуется авторизация"
login_manager.login_message_category = "warning"

# --- Routes ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Обрабатывает вход пользователя. GET - показывает форму, POST - проверяет данные.
    """

    # --- Already authenticated user ---
    if current_user.is_authenticated:
        return redirect(url_for('datasets.get_datasets'))

    # --- POST Request Handling ---
    if request.method == 'POST':
        login_attempt = request.form.get('login')
        password_attempt = request.form.get('password')

        if not login_attempt or not password_attempt:
             flash('Требуется логин и пароль', 'warning')
             return render_template_string('auth/login.html'), 400

        user = UserRepository.find_by_login(login_attempt)
        if user and user.check_password(password_attempt):
            if user.is_active:
                login_user(user, remember=False)

                next_page = request.args.get('next')
                if next_page and not next_page.startswith('/'):
                    next_page = None
                return redirect(next_page or url_for('datasets.get_datasets'))
            else:
                flash('Учётная запись неактивна', 'warning')
                return render_template('auth/login.html'), 403
        else:
            flash('Неверный логин или пароль.', 'danger')
            return render_template('auth/login.html'), 401

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Выход пользователя из системы.
    """
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))

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

@auth_bp.route('/')
def index():
    """Переход к страницам в зависимости от состояния авторизации"""
    if current_user.is_authenticated:
        return redirect(url_for('datasets.get_datasets'))
    else:
        return redirect(url_for('auth.login'))
