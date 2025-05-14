from src.services.user_service import UserService
from flask import Response, make_response, jsonify

class AdminController:
    """
    Класс-контроллер для запросов, связанных привелигированными пользователями.
    """

    @staticmethod
    def ban_user(user_id: str):
        """
        Блокирует пользователя по id
        """
        return UserService.ban_profile(user_id) 
    
    
    @staticmethod
    def unban_user(user_id: str):
        """
        Разблокирует пользователя по id
        """
        return UserService.unban_profile(user_id) 
    
    @staticmethod
    def get_users():
        """
        Получить всех пользоватей
        """
        
        return jsonify(UserService.get_users())
