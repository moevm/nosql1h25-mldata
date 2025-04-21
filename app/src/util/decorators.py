from functools import wraps
from flask import abort, flash
from flask_login import current_user


def admin_required(func):
    """
    Декоратор гарантирует, что текущий пользователь вошел в систему И является администратором.

    Если пользователь не вошел в систему, поведение Flask-Login по умолчанию (перенаправление
    на login) должно обрабатываться с помощью декоратора @login_required, который
    должен использоваться перед этим декоратором.

    Если пользователь вошел в систему, но не является администратором выдаётся ошибка 403 Forbidden.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # @login_required должен использоваться до этого декоратора
        if not current_user.is_authenticated:
            return login_manager.unauthorized()

        if not current_user.is_admin:
            flash('Доступ разрешен только администраторам', 'danger')
            abort(403)

        return func(*args, **kwargs)
    return decorated_view