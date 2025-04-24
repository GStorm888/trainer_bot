import sqlite3
from user import User

class Database:
    users = []

    SCHEMA = "schema.sql"
    DATABASE = "database.db"

    @staticmethod
    def execute(sql, params=()):
        # ПОДКЛЮЧАЕМСЯ К БАЗЕ ДАННЫХ
        connection = sqlite3.connect(Database.DATABASE)

        # получаем курсор
        cursor = connection.cursor()

        # выполнение скрипта для базы данных
        cursor.execute(sql, params)

        # фиксируем измнения в бвзе данных
        connection.commit()

    @staticmethod
    def create_table():
        with open(Database.SCHEMA) as schema_file:
            Database.execute(schema_file.read())

    @staticmethod
    def save(user:User):
        if Database.find_user_by_name(user.user_name) is not None:
            return False
        Database.execute("INSERT INTO users VALUES (?, ?)",
                       [user.user_name, user.user_password])
        return True

    @staticmethod
    def get_all_users():
        return Database.users
    
    @staticmethod
    def find_user_by_name(user_name):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
        users = cursor.fetchall()

        if len(users) == 0:
            return None
        
        user = User(
            users[0][0],
            users[0][1],
            users[0][2])
        return user

    @staticmethod
    def search_user_by_name(user_name):
        if Database.find_user_by_name(user_name) is not None:
            return True
        return False