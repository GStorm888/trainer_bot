# класс для описания пользователя
from dataclasses import dataclass


@dataclass  # класс пользователя
class User:
    user_name: str
    user_password: str
    status_log_in: int
    telegram_user_id: str
    id: int = None


@dataclass  # класс тренировки
class Training:
    user_name: str
    type_training: str
    date_training: str
    call_training: str
    time_training: int = None
    distance_training: int = None
    description_training: str = None
    id: int = None


@dataclass  # класс цели
class Goal:
    user_name: str
    date_start: str
    type_training: str
    distance_training: str
    date_finish: str
    id: int = None


@dataclass  # класс напоминаний
class Reminder:
    user_name: str  # такой же как в других таблицах
    day_reminder: int  # день недели 0-6
    time_reminder: str  # время напоминания(HH-MM)
    id: int = None
    # дни недели и их int значения
    # 0-пн
    # 1-вт
    # 2-ср
    # 3-чт
    # 4-пт
    # 5-сб
    # 6-вс
