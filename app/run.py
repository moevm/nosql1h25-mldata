"""
Создает сущность Flask и запускает ее. Добавляет к ней пути с помощью blueprint.
Настраивает Flask-Login.
"""

import os
from flask import Flask, redirect, url_for, flash
from flask_login import LoginManager, current_user

from app.src.routers import dataset_routes
from app.src.routers import auth_routes
from app.src.repository.user_repository import UserRepository

# --- Flask App Initialization ---
app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'secret_key')

# --- Flask-Login Initialization ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "Log in to access this page."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id: str):
    """
    Callback function used by Flask-Login to reload the user object from the user ID stored in the session.
    """
    return UserRepository.find_by_id(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    """
    Handles unauthorized access attempts. Redirects to login page.
    """
    flash("You need to be logged in to view this page.", "warning")
    
    next_url = request.path
    if request.query_string:
        next_url += '?' + request.query_string.decode('utf-8')

    return redirect(url_for('auth.login', next=next_url))


app.register_blueprint(dataset_routes.bp)
app.register_blueprint(auth_routes.auth_bp)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('datasets.get_datasets'))
    else:
        return redirect(url_for('auth.login'))


if __name__ == '__main__':
    print('App starting...')
    print('Login available at: http://127.0.0.1:5000/login')
    print('Datasets available at: http://127.0.0.1:5000/datasets (requires login)')

    app.run(host='0.0.0.0', port=5000, debug=True)