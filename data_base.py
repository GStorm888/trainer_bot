#файл для пользования к базой данных
import sqlite3
from user import User

class Database:
    SCHEMA = "schema.sql"
    DATABASE = "trainer_bot.db"

    @staticmethod
    def execute(sql, params=()): #функция для предотвращения повторяющегося кода
        # ПОДКЛЮЧАЕМСЯ К БАЗЕ ДАННЫХ
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        # получаем курсор
        cursor = connection.cursor()

        # выполнение скрипта для базы данных
        cursor.execute(sql, params)

        # фиксируем измнения в базе данных
        connection.commit()

    @staticmethod
    def create_table(): #функция для создание таблицы
        with open(Database.SCHEMA) as schema_file:
            Database.execute(schema_file.read())

    @staticmethod
    def save(user:User): #функция для новых записей
        if Database.return_user_by_name(user.user_name) is not None:
            return False
        Database.execute("INSERT INTO users (user_name, user_password, status_log_in, telegram_user_id) VALUES (?, ?, ?, ?)",
                       [user.user_name, user.user_password, user.status_log_in, user.telegram_user_id])
        return True

    @staticmethod
    def get_all_users(): #функция для получения всех пользователей
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users")

        all_users = cursor.fetchall()
        users = []
        for id, user_name, user_password, status_log_in, telegram_user_id in all_users:
            user = User(user_name, user_password, status_log_in, telegram_user_id, id)
            users.append(user) 
        if len(users) == 0:
            return None
        return users
    
    @staticmethod
    def return_user_by_name(user_name): #функция для получения пользователя по имени
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
        users = cursor.fetchall()

        if len(users) == 0:
            return None
        
        id, user_name, user_password, status_log_in, telegram_user_id = users[0]
        user = User(user_name, user_password, status_log_in, telegram_user_id, id)
        return user

    @staticmethod #функция для проверки существования пользователя
    def search_user_by_name(user_name):
        if Database.return_user_by_name(user_name) is not None:
            return True
        return False

    @staticmethod #функция для нахождения пользователя по telegram_user_id
    def search_user_by_telegram_id(telegram_user_id):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE telegram_user_id = ?", [telegram_user_id])
        users = cursor.fetchall()

        if len(users) == 0:
            return None
        
        id, user_name, user_password, status_log_in, telegram_user_id = users[0]
        user = User(user_name, user_password, status_log_in, telegram_user_id, id)
        return user

    @staticmethod
    def update_status_log_in(user:User):
        # Database.execute("UPDATE users SET status_log_in=? WHERE id=?",
        #                     [user.status_log_in, user.id])
        Database.execute("UPDATE users SET status_log_in=? WHERE id=?",
                       [user.status_log_in, user.id])
        return True



    #для тестов чтобы не было мусорных пользователей
    # @staticmethod
    # def drop():
    #     connection = sqlite3.connect(Database.DATABASE)

    #     cursor = connection.cursor()
    #     cursor.execute("DROP TABLE users")
    #     # cursor.execute("""ALTER TABLE users
    #     #                     ADD register TEXT NOT NULL;""")
    #     return True
