-- схема описывающая пользователя
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE,--ввод пользователя
    user_password TEXT NOT NULL, --хэш пароль
    status_log_in INTEGER NOT NULL, --статус активности(автозаполнение)
    telegram_user_id TEXT NOT NULL --id пользователя в тг, нужно для ограничения доступа(автозаполнение)
);
-- """
-- """
-- """
-- """
-- схема описывающая тренировку
--схема отдельно от users, но зависищая от пользователя
--для каждой тренировки отдельная строка в БД
--имя пользователя уже не уникально
CREATE TABLE IF NOT EXISTS trainings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL, --должен быть такой же как и в users(автозаполнение)
    type_training TEXT NOT NULL, --тип тренировки
    date_training TEXT NOT NULL, --дата(формат: YYYY-MM-DD)(автозаполнение)
    call_training TEXT NOT NULL, --каллории(запрос пользователя)
    time_training INTEGER, --длительность тренировки(вместо возможна distance_training)
    distance_training INTEGER, --дистанция тренировки(вместо возможна time_training)
    description_training TEXT --описание пользователя(не обязательно)
    FOREIGN KEY (user_name) REFERENCES users(user_name)
);
-- """
-- """
-- """
-- """
-- схема описывающая цели пользователей
-- зависит от 2 верхних таблиц
-- каждая цель - отдельная строка
-- user_name и type_training такие же как в 2 верхних таблицах
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL, --такой же как в таблице пользователей(автозаполнение)
    date_start TEXT NOT NULL, --сегодняшняя дата(автозаполнение)
    type_training TEXT NOT NULL, --тип тренировки(ввод пльзоватя)
    distance_training INTEGER NOT NULL, --дистанция цели(ввод пользователя в метрах)
    date_finish TEXT NOT NULL --дедлайн(ввод пользователя и преобразование)
    FOREIGN KEY (user_name) REFERENCES users(user_name)
);
-- """
-- """
-- """
-- """
-- схема описывающая напоминания пользователей
-- зависит от users
-- каждое напоминание - отдельная строка
-- user_name такой же как в 3 верхних таблицах
CREATE TABLE IF NOT EXISTS reminder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL, --такой же как в таблице пользователей
    day_reminder INTEGER NOT NULL, --день недеи (0-6)
    time_reminder TEXT NOT NULL --время напоминания (HH-MM)
    FOREIGN KEY (user_name) REFERENCES users(user_name)
)
