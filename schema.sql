-- схема описывающая пользователя
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE,
    user_password TEXT NOT NULL, --хэш пароль
    status_log_in INTEGER NOT NULL, --статус активности
    telegram_user_id TEXT NOT NULL --id пользователя в тг, нужно для ограничения доступа
)
"""
"""
"""
"""
-- -- схема описывающая тренировку
-- --схема отдельно от users, но зависищая от пользователя
-- --для каждой тренировки отдельная строка в БД
-- --имя пользователя уже не уникально
-- CREATE TABLE IF NOT EXISTS training (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_name TEXT NOT NULL , --должен быть такой же как и в users(автоматизировать)
--     tip TEXT, --тип тренировки
--     date DATE, --дата(надо сделать автозаполнение)
--     time TEXT, --длительность тренировки(запрос пользователя)
--     distance TEXT, --если не время то дистанция(например бег)
--     call INTEGER, --каллории(запрос пользователя)
--     discription TEXT --описание пользователя
-- )
