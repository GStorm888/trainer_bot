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
    type_trainig: str
    date_training: date
    time_or_distance_trainig: str
    call_trainig_or_else: int
    discription_trainig: str = None
    id: int = None
