-- файл с базой данных описывающая пользователя
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE,
    user_password TEXT NOT NULL,
    status_log_in INTEGER NOT NULL, --статус залогинился или вышел
    telegram_user_id TEXT NOT NULL --id пользователя в тг, нужно для ограничения доступа
)
