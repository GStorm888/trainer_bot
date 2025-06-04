#класс для описания пользователя
from dataclasses import dataclass
from datetime import date
@dataclass 
class User:
    user_name: str
    user_password: str
    status_log_in: int
    telegram_user_id: str
    id: int = None

@dataclass
class Training:
    user_name: str
    type_training: str
    date_training: str
    call_training: str
    time_training: int = None
    distance_training: int = None
    description_training: str = None
    id: int = None
