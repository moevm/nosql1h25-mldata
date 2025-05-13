"""
Создает сущность Flask и запускает ее. Добавляет к ней пути с помощью blueprint.
Настраивает Flask-Login.
"""

import os

from urllib.parse import quote_plus
from flask import Flask
from flask_cors import CORS
from flask_apscheduler import APScheduler

from src.routers import dataset_routes
from src.routers import auth_routes

from src.repository.dataset_repository import DatasetRepository

# --- Flask App Initialization ---
app: Flask = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key_change_me')

# --- Register Blueprints ---
auth_routes.login_manager.init_app(app)
app.register_blueprint(dataset_routes.bp)
app.register_blueprint(auth_routes.auth_bp)
user = os.getenv("MONGO_ROOT_USER")
password = os.getenv("MONGO_ROOT_PASS")
host = os.getenv("HOST")
port = os.getenv("PORT")

app.config['MONGO_URI'] = f"mongodb://root:pass@db:27017"
app.config['UPLOAD_FOLDER'] = os.getenv('DATASET_DIR', './datasets')

app.config['JOBS'] = [
    {
        'id': 'daily_dataset_activity_update',
        'func': 'src.repository.dataset_repository:DatasetRepository.reset_day',  # Static method reference
        'trigger': 'cron',
        'hour': 0,                     
        'minute': 0,
        'timezone': 'UTC'
    }
]

scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

with app.app_context():
    DatasetRepository.reset_day()



CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true')