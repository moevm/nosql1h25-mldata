"""
Настраивает пути для endpoint'ов аутентификации (логин, логаут).
"""
from flask import Blueprint, render_template_string, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse

from app.src.repository.user_repository import UserRepository

auth_bp: Blueprint = Blueprint('auth', __name__)

# --- Basic HTML Templates (Inline for simplicity) ---
LOGIN_TEMPLATE = """
<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Вход</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body { padding: 20px; }
      .form-signin { max-width: 330px; padding: 15px; margin: auto; }
    </style>
  </head>
  <body>
    <main class="form-signin w-100 m-auto text-center">
        <h1 class="h3 mb-3 fw-normal">Вход в систему</h1>
        {# Display flashed messages #}
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              {# Use 'danger' for errors, 'warning' for warnings, 'info' for info, 'success' for success #}
              <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <form method="post">
          <div class="form-floating mb-2">
            <input type="text" class="form-control" id="login" name="login" placeholder="Логин" required autofocus>
            <label for="login">Логин</label>
          </div>
          <div class="form-floating mb-3">
            <input type="password" class="form-control" id="password" name="password" placeholder="Пароль" required>
            <label for="password">Пароль</label>
          </div>

          <button class="w-100 btn btn-lg btn-primary" type="submit">Войти</button>
        </form>
    </main>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
"""

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
             return render_template_string(LOGIN_TEMPLATE), 400

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
                return render_template_string(LOGIN_TEMPLATE), 403
        else:
            flash('Неверный логин или пароль.', 'danger')
            return render_template_string(LOGIN_TEMPLATE), 401

    return render_template_string(LOGIN_TEMPLATE)


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Выход пользователя из системы.
    """
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))