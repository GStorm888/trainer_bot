
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE,
    user_password TEXT NOT NULL, 
    status_log_in INTEGER NOT NULL, 
    telegram_user_id TEXT NOT NULL 
);

CREATE TABLE IF NOT EXISTS trainings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL, 
    type_training TEXT NOT NULL, 
    date_training TEXT NOT NULL,
    call_training TEXT NOT NULL, 
    time_training INTEGER, 
    distance_training INTEGER, 
    description_training TEXT,

    FOREIGN KEY(user_name) REFERENCES users (iuser_named)
);

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL, 
    date_start TEXT NOT NULL, 
    type_training TEXT NOT NULL, 
    distance_training INTEGER NOT NULL, 
    date_finish TEXT NOT NULL, 
    FOREIGN KEY (user_name) REFERENCES users(user_name)
);

CREATE TABLE IF NOT EXISTS reminder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL, 
    day_reminder INTEGER NOT NULL,
    time_reminder TEXT NOT NULL, 
    FOREIGN KEY (user_name) REFERENCES users(user_name)
)
