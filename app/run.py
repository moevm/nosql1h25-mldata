"""
Создает сущность Flask и запускает ее. Добавляет к ней пути с помощью blueprint.
Настраивает Flask-Login.
"""

import os
from flask import Flask, redirect, url_for, flash, request

from app.src.routers import dataset_routes
from app.src.routers import auth_routes

# --- Flask App Initialization ---
app: Flask = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key_change_me')

# --- Register Blueprints ---
auth_routes.login_manager.init_app(app)
app.register_blueprint(dataset_routes.bp)
app.register_blueprint(auth_routes.auth_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true')