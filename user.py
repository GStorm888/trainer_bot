#класс для описания пользователя
from dataclasses import dataclass

@dataclass 
class User:
    user_name: str
    user_password: str
    status_log_in: int
    telegram_user_id: str
    id: int = None

@dataclass
class Training
    user_name: str
    type_trainig: str
    date_training: #?
    time_trainig: = None #?
    distance_trainig: str = None
    call_trainig: int = None
    discription_trainig: str = None
    id: int: None
