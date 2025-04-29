#класс для описания пользователя
from dataclasses import dataclass

@dataclass 
class User:
    user_name: str
    user_password: str
    status_log_in: int
    telegram_user_id: str
    id: int = None
