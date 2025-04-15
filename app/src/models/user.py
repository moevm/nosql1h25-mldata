"""
Модель пользователя для работы с Flask-Login и хранения данных пользователя.
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class User(UserMixin):
    """
    Класс пользователя. Использует UserMixin для интеграции с Flask-Login.
    """
    def __init__(self, user_data: dict):
        """
        Инициализирует пользователя из словаря данных MongoDB.
        """
        self._id: str = str(user_data.get('_id', str(uuid.uuid4())))
        self.username: str = user_data.get('username')
        self.login: str = user_data.get('login')
        self.password_hash: str = user_data.get('password')
        self.status: int = user_data.get('status')
        self.createdDatasetsCount: int = user_data.get('createdDatasetsCount')
        self.accountCreationDate = user_data.get('accountCreationDate')
        self.lastAccountModificationDate = user_data.get('lastAccountModificationDate')

    @property
    def id(self) -> str:
        """
        Возвращает ID пользователя (требуется UserMixin).
        Flask-Login использует это для получения ID пользователя для сессии.
        """
        return self._id

    def set_password(self, password: str) -> None:
        """
        Генерирует хеш пароля и сохраняет его.
        (Используется при создании/изменении пароля, не для проверки)
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Проверяет предоставленный пароль против сохраненного хеша.
        """
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        """
        Проверяет, является ли пользователь администратором.
        Статус 0 - админ.
        """
        return self.status == 0

    @property
    def is_active_user(self) -> bool:
        """
        Проверяет, является ли пользователь активным (не заблокированным).
        Статус 1 - активен.
        """
        return self.status == 1

    @property
    def is_active(self) -> bool:
        return self.status in [0, 1]
        
    def to_dict(self) -> dict:
        """
        Преобразует объект пользователя в словарь (без пароля).
        """
        return {
            "_id": self._id,
            "username": self.username,
            "login": self.login,
            "status": self.status,
            "createdDatasetsCount": self.createdDatasetsCount,
            "accountCreationDate": self.accountCreationDate,
            "lastAccountModificationDate": self.lastAccountModificationDate
        }
