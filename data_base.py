import sqlite3 #инмпорт библиотеки для базы данных

class Database:
    # Создаем подключение к базе данных (файл trainer_bot_base.db будет создан)
    __connection = sqlite3.connect('trainer_bot_base.db')

    cursor = __connection.cursor()

    # Создаем таблицу Users
    cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL)
    """)

    # Сохраняем изменения 
    __connection.commit()