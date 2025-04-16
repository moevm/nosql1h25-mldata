"""
Настраивает пути для endpoint'ов аутентификации (логин, логаут).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse

from app.src.repository.user_repository import UserRepository

auth_bp: Blueprint = Blueprint('auth', __name__, template_folder='templates')

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