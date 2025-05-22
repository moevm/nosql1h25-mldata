"""
Настраивает пути для endpoint'ов аутентификации (login/logout).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import LoginManager
from urllib.parse import urlparse

from src.repository.user_repository import UserRepository
from src.services.user_service import UserService

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
             return render_template('auth/login.html'), 400

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

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Обрабатывает регистрацию нового пользователя.
    GET - показывает форму регистрации.
    POST - проверяет данные и пытается создать пользователя.
    Доступно только для неаутентифицированных пользователей.
    """
    if current_user.is_authenticated:
        flash('Вы уже авторизованы. Для регистрации новой учетной записи сначала выйдите из системы.', 'info')
        return redirect(url_for('datasets.get_datasets'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        login_val = request.form.get('login', '').strip() 
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # To re-populate form with submitted values (except password) on validation error
        form_input_values = {'username': username, 'login': login_val}

        if not all([username, login_val, password, password_confirm]):
            flash('Все поля обязательны для заполнения.', 'warning')
            return render_template('auth/register.html', **form_input_values), 400

        if password != password_confirm:
            flash('Пароли не совпадают.', 'danger')
            return render_template('auth/register.html', **form_input_values), 400
        
        if len(password) < 6: 
            flash('Пароль должен содержать не менее 6 символов.', 'danger')
            return render_template('auth/register.html', **form_input_values), 400
        
        if ' ' in password: 
            flash('Пароль не может содержать пробелы.', 'danger')
            return render_template('auth/register.html', **form_input_values), 400

        success, message = UserService.register_user(
            username=username,
            login=login_val,
            password=password
        )

        if success:
            flash(message, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'Не удалось зарегистрироваться.')
            return render_template('auth/register.html', **form_input_values), 400

    # For GET request, or if POST fails and re-renders template
    return render_template('auth/register.html')

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
        response = redirect(url_for('datasets.get_datasets'))
    else:
        response = redirect(url_for('auth.login'))

    response.status_code = 200
    return response

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Отображает страницу профиля пользователя и обрабатывает обновление данных.
    """
    if request.method == 'POST':
        new_username = request.form.get('username', '').strip()
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        if not new_username:
            flash('Имя пользователя (Никнейм) не может быть пустым.', 'danger')
            return render_template('auth/profile.html', current_user=current_user)

        if new_password:
            if len(new_password) < 6:
                flash('Новый пароль должен содержать не менее 6 символов.', 'danger')
                return render_template('auth/profile.html', current_user=current_user)
            if ' ' in new_password:
                flash('Пароль не может содержать пробелы.', 'danger')
                return render_template('auth/profile.html', current_user=current_user)
            if new_password != confirm_new_password:
                flash('Новые пароли не совпадают.', 'danger')
                return render_template('auth/profile.html', current_user=current_user)
        
        # UserService handles uniqueness check for username
        success, message = UserService.update_profile(
            user_id=current_user.id,
            new_username=new_username,
            new_password=new_password if new_password else None
        )

        if success:
            flash(message, 'success')
            updated_user = UserRepository.find_by_id(current_user.id)
            if updated_user:
                current_user.username = updated_user.username
                current_user.lastAccountModificationDate = updated_user.lastAccountModificationDate
            return redirect(url_for('auth.profile')) 
        else:
            flash(message, 'danger')
            return render_template('auth/profile.html', current_user=current_user)

    # For GET request, just render the profile page
    return render_template('auth/profile.html', current_user=current_user)