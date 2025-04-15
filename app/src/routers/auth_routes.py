"""
Настраивает пути для endpoint'ов аутентификации (логин, логаут).
"""
from flask import Blueprint, render_template_string, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.src.repository.user_repository import UserRepository

auth_bp: Blueprint = Blueprint('auth', __name__)

# --- Basic HTML Templates (Inline for simplicity) ---
LOGIN_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login</title>
  </head>
  <body>
    <h1>Login</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <ul class=flashes>
        {% for category, message in messages %}
          <li class="{{ category }}">{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="post">
      <p><label for="login">Login:</label><br>
         <input type="text" id="login" name="login" required></p>
      <p><label for="password">Password:</label><br>
         <input type="password" id="password" name="password" required></p>
      <p><input type="submit" value="Login"></p>
    </form>
  </body>
</html>
"""

# --- Routes ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Обрабатывает вход пользователя. GET - показывает форму, POST - проверяет данные.
    """
    # --- POST Request Handling ---
    if request.method == 'POST':
        login_attempt = request.form.get('login')
        password_attempt = request.form.get('password')

        if not login_attempt or not password_attempt:
             flash('Login and Password are required.', 'warning')
             return render_template_string(LOGIN_TEMPLATE), 400

        user = UserRepository.find_by_login(login_attempt)

        if user and user.check_password(password_attempt):
            if user.is_active:
                if current_user.is_authenticated:
                    logout_user()

                login_user(user, remember=False)
                flash('Logged in successfully.', 'success')

                next_page = request.args.get('next')
                if next_page and not next_page.startswith('/'):
                    next_page = None
                return redirect(next_page or url_for('datasets.get_datasets'))
            else:
                 flash('Account is inactive or blocked.', 'warning')
        else:
            flash('Invalid login or password.', 'danger')

    # --- GET Request Handling ---
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for('datasets.get_datasets'))

    return render_template_string(LOGIN_TEMPLATE)


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Выход пользователя из системы.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))