#класс для описания пользователя
from dataclasses import dataclass

@dataclass 
class User:
    user_name: str
    user_password: str
    status_log_in: int
    id: int = None
