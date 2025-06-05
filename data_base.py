#файл для пользования к базой данных
import sqlite3
from user import User, Training
"""
"""
"""
"""
class Database:
    SCHEMA = "schema.sql"
    DATABASE = "trainer_bot.db"
    """
    """
    """
    """
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
    """
    """
    """
    """
    @staticmethod
    def create_table():
        with open(Database.SCHEMA) as schema_file:
            connection = sqlite3.connect(Database.DATABASE)
            cursor = connection.cursor()
            cursor.executescript(schema_file.read())
            connection.commit()
            connection.close()
    """
    """
    """
    """
    @staticmethod
    def save(user:User): #функция для новых записей
        if Database.return_user_by_name(user.user_name) is not None:
            return False
        Database.execute("INSERT INTO users (user_name, user_password, status_log_in, telegram_user_id) VALUES (?, ?, ?, ?)",
                       [user.user_name, user.user_password, user.status_log_in, user.telegram_user_id])
        return True
    """
    """
    """
    """
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
    """
    """
    """
    """
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
    """
    """
    """
    """
    @staticmethod #функция для проверки существования пользователя
    def search_user_by_name(user_name):
        if Database.return_user_by_name(user_name) is not None:
            return True
        return False
    """
    """
    """
    """
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
    """
    """
    """
    """
    @staticmethod #изменить статус активности при logout
    def update_status_log_in(status_log_in, telegram_user_id):
        # Database.execute("UPDATE users SET status_log_in=? WHERE id=?",
        #                     [user.status_log_in, user.id])
        Database.execute("UPDATE users SET status_log_in=? WHERE telegram_user_id=?",
                       [status_log_in, telegram_user_id])
        return True
    """
    """
    """
    """
    @staticmethod #узнать статус активности при logout
    def examination_status_log_in(status_log_in, telegram_user_id):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE status_log_in=? AND telegram_user_id=?", [status_log_in, telegram_user_id])

        users = cursor.fetchall()

        if len(users) == 0:
            return None
        
        id, user_name, user_password, status_log_in, telegram_user_id = users[0]
        user = User(user_name, user_password, status_log_in, telegram_user_id, id)
        return user
    """
    """
    """
    """
    @staticmethod #добавление тренировки
    def add_training(training:Training):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute("""INSERT INTO training (user_name, type_training, date_training, call_training, time_training, distance_training, description_training)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [training.user_name, training.type_training, training.date_training, training.call_training,
        training.time_training, training.distance_training, training.description_training])

        print(cursor.execute("""INSERT INTO training (user_name, type_training, date_training, call_training, time_training, distance_training, description_training)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [training.user_name, training.type_training, training.date_training, training.call_training,
        training.time_training, training.distance_training, training.description_training])
        )
        return True
    """
    """
    """
    """ 
    @staticmethod
    def get_all_training():
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM training")

        all_trainings = cursor.fetchall()
        trainings = []
        for id, user_name, type_trainig, date_training, call_training, time_training, distance_training, description_trainig in all_trainings:
            training = Training(user_name, type_trainig, date_training, call_training, time_training, distance_training, description_training,  id)
            trainings.append(training) 
        if len(trainings) == 0:
            return None
        return trainings
    """
    """
    """
    """ 
    @staticmethod
    def view_workouts_to_type_and_date(type_training, date_training):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM training WHERE type_training=? AND date_training=?",
        [type_training, date_training])


        all_training = cursor.fetchall()
        trainings = []
        for id, user_name, type_trainig, date_training, call_training, time_training, distance_training, description_trainig in all_training:
            training = Training(user_name, type_trainig, date_training, call_training, time_training, distance_training, description_training,  id)
            trainings.append(training) 
        if len(trainings) == 0:
            return None
        return trainings
    #для тестов чтобы не было мусорных пользователей и тренировок
    # @staticmethod
    # def drop():
    #     connection = sqlite3.connect(Database.DATABASE)

    #     cursor = connection.cursor()
    #     cursor.execute("DROP TABLE users")
    #     cursor.execute("DROP TABLE training")
    #     # cursor.execute("""ALTER TABLE users
    #     #                     ADD register TEXT NOT NULL;""")
    #     return True

