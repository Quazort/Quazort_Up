class AppBaseError(Exception):
    """Базовый класс для всех ошибок приложения"""
    pass


# Ошибки авторизации
class InvalidToken(AppBaseError):
    """Токен подписи неверный"""
    pass

class ExpiredToken(AppBaseError):
    """Токен истёк"""
    pass

class UserNotFound(AppBaseError):
    """Пользователь не найден"""
    pass

class PermissionDenied(AppBaseError):
    """Нет прав на действие"""
    pass

class NoRefreshToken(AppBaseError):
    """Нет refresh токена"""
    pass


class UniquenessError(AppBaseError):
    """Ошибка бд уникальность"""
    pass

class DataBaseError(AppBaseError):
    """Ошибка с бд"""
    pass