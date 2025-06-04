-- схема описывающая пользователя
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE,
    user_password TEXT NOT NULL, --хэш пароль
    status_log_in INTEGER NOT NULL, --статус активности
    telegram_user_id TEXT NOT NULL --id пользователя в тг, нужно для ограничения доступа
);
-- """
-- """
-- """
-- """
-- схема описывающая тренировку
--схема отдельно от users, но зависищая от пользователя
--для каждой тренировки отдельная строка в БД
--имя пользователя уже не уникально
CREATE TABLE IF NOT EXISTS training (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL, --должен быть такой же как и в users(автоматизировать)
    type_trainig TEXT NOT NULL, --тип тренировки
    date_training DATE NOT NULL, --дата(надо сделать автозаполнение)
    time_or_distance_trainig TEXT NOT NULL, --длительность тренировки(запрос пользователя)
    call_trainig_or_else TEXT NOT NULL, --каллории(запрос пользователя)
    discription_trainig TEXT --описание пользователя
)
