"""
Сервис для бизнес-логики, связанной с пользователями.
"""
from datetime import datetime, timezone
from typing import Optional, Tuple
from werkzeug.security import generate_password_hash

from src.repository.user_repository import UserRepository
from src.models.user import User

class UserService:
    """
    Класс-сервис для логики, связанной с пользователями.
    """
    @staticmethod
    def update_profile(user_id: str, new_username: str, new_password: Optional[str]) -> Tuple[bool, str]:
        """
        Обновляет профиль пользователя (имя пользователя и/или пароль).
        Возвращает кортеж (success: bool, message: str).
        """
        user = UserRepository.find_by_id(user_id)
        if not user:
            return False, "Пользователь не найден."

        update_payload = {}
        changed = False

        # Проверка изменения имени пользователя
        if new_username and new_username != user.username:
            existing_user_with_new_name = UserRepository.find_by_username(new_username)
            if existing_user_with_new_name and existing_user_with_new_name.id != user_id:
                return False, f"Имя пользователя '{new_username}' уже занято. Пожалуйста, выберите другое."
            update_payload['username'] = new_username
            changed = True

        # Проверка изменения пароля
        if new_password:
            update_payload['password'] = generate_password_hash(new_password)
            changed = True
        
        if not changed:
            return True, "Нет изменений для сохранения."

        # Обновление даты последнего изменения, если были изменения
        update_payload['lastAccountModificationDate'] = datetime.now(timezone.utc)

        if UserRepository.update_user_fields(user_id, update_payload):
            return True, "Профиль успешно обновлен."
        else:
            return False, "Не удалось обновить профиль. Попробуйте снова."

    @staticmethod
    def ban_profile(user_id: str):
        """
        Блокирует профиль пользователя        
        Возвращает кортеж (success: bool, message: str).
        """
        
        user = UserRepository.find_by_id(user_id)
        if not user:
            return False, "Пользователь не найден."
        
        if user.status == 0:
            return False, "Нельзя заблокировать привилигированного пользователя."
        if user.status == 2:
            return False, "Пользователь уже заблокирован."

        update_payload = {
            'status': 2,
        }
    
        if not UserRepository.update_user_fields(user_id, update_payload):
            return False, "Не удалось заблокировать профиль. Попробуйте снова."
        return True, "Профиль успешно заблокирован."
    

    @staticmethod
    def unban_profile(user_id: str):
        """
        Разблокирует профиль пользователя        
        Возвращает кортеж (success: bool, message: str).
        """
        
        user = UserRepository.find_by_id(user_id)
        if not user:
            return False, "Пользователь не найден."
        
        if user.status == 0:
            return False, "Нельзя разблокировать привилигированного пользователя."
        if user.status == 1:
            return False, "Пользователь не заблокирован."

        update_payload = {
            'status': 1,
        }
        if not UserRepository.update_user_fields(user_id, update_payload):
            return False, "Не удалось разблокировать профиль. Попробуйте снова."
        return True, "Профиль успешно разблокирован."
    
    @staticmethod
    def get_users():
        """
        Возвращает список всех пользователей
        """ 
        return UserRepository.get_users()
