# файл для использования базы данных
import sqlite3
from user import User, Training, Goal, Reminder


class Database:
    SCHEMA = "schema.sql"
    DATABASE = "trainer_bot.db"

    @staticmethod  # работа с таблицей(нужно чтобы не повторялся код)
    def execute(sql, params=()):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute(sql, params)

        connection.commit()

    @staticmethod  # создание таблиц
    def create_table():
        with open(Database.SCHEMA) as schema_file:
            connection = sqlite3.connect(Database.DATABASE)
            cursor = connection.cursor()
            cursor.executescript(schema_file.read())
            connection.commit()
            connection.close()

    @staticmethod  # добавление пользователя
    def save(user: User):
        if Database.return_user_by_name(user.user_name) is not None:
            return False
        Database.execute(
            "INSERT INTO users (user_name, user_password, status_log_in, telegram_user_id) VALUES (?, ?, ?, ?)",
            [
                user.user_name,
                user.user_password,
                user.status_log_in,
                user.telegram_user_id,
            ],
        )
        return True

    @staticmethod  # получение всех пользователей
    def get_all_users():
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

    @staticmethod  # получение пользователя по имени
    def return_user_by_name(user_name):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
        users = cursor.fetchall()

        if len(users) == 0:
            return None

        id, user_name, user_password, status_log_in, telegram_user_id = users[0]
        user = User(user_name, user_password, status_log_in, telegram_user_id, id)
        return user

    @staticmethod  # получение пользователя по telegram_user_id
    def search_user_by_telegram_id(telegram_user_id):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE telegram_user_id = ?", [telegram_user_id]
        )
        users = cursor.fetchall()

        if len(users) == 0:
            return None

        id, user_name, user_password, status_log_in, telegram_user_id = users[0]
        user = User(user_name, user_password, status_log_in, telegram_user_id, id)
        return user

    @staticmethod  # изменить статус активности
    def update_status_log_in(status_log_in, telegram_user_id):
        Database.execute(
            "UPDATE users SET status_log_in=? WHERE telegram_user_id=?",
            [status_log_in, telegram_user_id],
        )
        return True

    @staticmethod  # узнать статус активности
    def examination_status_log_in(status_log_in, telegram_user_id):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE status_log_in=? AND telegram_user_id=?",
            [status_log_in, telegram_user_id],
        )

        users = cursor.fetchall()

        if len(users) == 0:
            return None

        id, user_name, user_password, status_log_in, telegram_user_id = users[0]
        user = User(user_name, user_password, status_log_in, telegram_user_id, id)
        return user

    @staticmethod  # добавление тренировки
    def add_training(training: Training):
        Database.execute(
            """INSERT INTO trainings (user_name, type_training, date_training, call_training,
                         time_training, distance_training, description_training)
                         VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                training.user_name,
                training.type_training,
                training.date_training,
                training.call_training,
                training.time_training,
                training.distance_training,
                training.description_training,
            ],
        )
        return True

    @staticmethod  # получение всех тренировок по имени пользователя
    def get_all_training_by_user_name(user_name):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM trainings WHERE user_name = ?", [user_name])
        all_trainings = cursor.fetchall()
        trainings = []
        for (
            id,
            user_name,
            type_trainig,
            date_training,
            call_training,
            time_training,
            distance_training,
            description_training,
        ) in all_trainings:
            training = Training(
                user_name,
                type_trainig,
                date_training,
                call_training,
                time_training,
                distance_training,
                description_training,
                id,
            )
            trainings.append(training)
        if len(trainings) == 0:
            return None
        return trainings

    @staticmethod  # просмотр тренировок по типу
    def view_workouts_to_type(type_training, user_name):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM trainings WHERE type_training=? AND user_name =?",
            [type_training, user_name],
        )

        all_training = cursor.fetchall()
        trainings = []
        for (
            id,
            user_name,
            type_trainig,
            date_training,
            call_training,
            time_training,
            distance_training,
            description_training,
        ) in all_training:
            training = Training(
                user_name,
                type_trainig,
                date_training,
                call_training,
                time_training,
                distance_training,
                description_training,
                id,
            )
            trainings.append(training)
        if len(trainings) == 0:
            return None
        return trainings

    @staticmethod  # просмотр тренировок по промежутку времени
    def view_workouts_to_date(date_training_start, date_training_fininsh, user_name):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM trainings WHERE date_training>=? AND date_training<=? AND user_name =?",
            [date_training_start, date_training_fininsh, user_name],
        )

        all_training = cursor.fetchall()
        trainings = []
        for (
            id,
            user_name,
            type_trainig,
            date_training,
            call_training,
            time_training,
            distance_training,
            description_training,
        ) in all_training:
            training = Training(
                user_name,
                type_trainig,
                date_training,
                call_training,
                time_training,
                distance_training,
                description_training,
                id,
            )
            trainings.append(training)
        if len(trainings) == 0:
            return None
        return trainings

    @staticmethod  # просмотр тренировки по типу и промежутку времени
    def view_workouts_to_type_and_date(type_training, date_start, today, user_name):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM trainings WHERE user_name=? AND type_training=? AND date_training>=? AND date_training<=?",
            [user_name, type_training, date_start, today],
        )

        all_training = cursor.fetchall()
        trainings = []
        for (
            id,
            user_name,
            type_trainig,
            date_training,
            call_training,
            time_training,
            distance_training,
            description_training,
        ) in all_training:
            training = Training(
                user_name,
                type_trainig,
                date_training,
                call_training,
                time_training,
                distance_training,
                description_training,
                id,
            )
            trainings.append(training)
        if len(trainings) == 0:
            return None
        return trainings

    @staticmethod  # просмотр всех целей по имени пользователя
    def get_all_goals_by_user_name(user: User):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM goals WHERE user_name = ?", [user.user_name])

        all_goals = cursor.fetchall()
        goals = []
        for (
            id,
            user_name,
            date_start,
            type_training,
            distance_training,
            date_finish,
        ) in all_goals:
            goal = Goal(
                user_name, date_start, type_training, distance_training, date_finish, id
            )
            goals.append(goal)
        if len(goals) == 0:
            return None
        return goals

    @staticmethod  # добавление цели
    def set_goal(goal: Goal):
        Database.execute(
            """INSERT INTO goals (user_name, date_start, type_training, distance_training, date_finish)
        VALUES (?, ?, ?, ?, ?)""",
            [
                goal.user_name,
                goal.date_start,
                goal.type_training,
                goal.distance_training,
                goal.date_finish,
            ],
        )
        return True

    @staticmethod  # промотр целей тренировок
    def get_all_goal():
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM goals")

        all_goals = cursor.fetchall()
        goals = []
        for (
            id,
            user_name,
            date_start,
            type_training,
            distance_training,
            date_finish,
        ) in all_goals:
            goal = Goal(
                user_name, date_start, type_training, distance_training, date_finish, id
            )
            goals.append(goal)
        if len(goals) == 0:
            return None
        return goals

    @staticmethod  # получение всех целей пользователя по имени
    def get_all_goal_by_user_name(user_name):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM goals WHERE user_name=?", [user_name])

        all_goals = cursor.fetchall()
        goals = []
        for (
            id,
            user_name,
            date_start,
            type_training,
            distance_training,
            date_finish,
        ) in all_goals:
            goal = Goal(
                user_name, date_start, type_training, distance_training, date_finish, id
            )
            goals.append(goal)
        if len(goals) == 0:
            return None
        return goals

    @staticmethod  # получение всех целей пользователя по имени и типу
    def get_all_goal_by_user_name_and_type(user_name, type_training):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM goals WHERE user_name=? AND type_training=?",
            [user_name, type_training],
        )

        all_goals = cursor.fetchall()
        goals = []
        for (
            id,
            user_name,
            date_start,
            type_training,
            distance_training,
            date_finish,
        ) in all_goals:
            goal = Goal(
                user_name, date_start, type_training, distance_training, date_finish, id
            )
            goals.append(goal)
        if len(goals) == 0:
            return None
        return goals

    @staticmethod  # Удаление цели если дистанция пройдена
    def delete_goal_if_distance_done(goal: Goal):
        Database.execute(
            """DELETE FROM goals WHERE user_name=? AND date_start=?
        AND type_training=? AND distance_training=? AND date_finish=?""",
            [
                goal.user_name,
                goal.date_start,
                goal.type_training,
                goal.distance_training,
                goal.date_finish,
            ],
        )
        return True

    @staticmethod  # удаление цели если время прошло и цель не выполнена
    def delete_goal_if_today_is_day_finish(user_name, today):
        Database.execute(
            """DELETE FROM goals WHERE user_name=? AND date_finish=?""",
            [user_name, today],
        )
        return True

    @staticmethod  # добавление напоминаний
    def set_reminder(reminder: Reminder):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute(
            """INSERT INTO reminder (user_name, day_reminder, time_reminder)
        VALUES (?, ?, ?)""",
            [
                reminder.user_name,
                reminder.day_reminder,
                reminder.time_reminder,
            ],
        )
        connection.commit()
        return True

    @staticmethod  # промотр всех напоминаний
    def get_all_reminder():
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM reminder")

        all_reminders = cursor.fetchall()
        reminders = []
        for id, user_name, day_reminder, time_reminder in all_reminders:
            reminder = Reminder(user_name, day_reminder, time_reminder, id)
            reminders.append(reminder)
        if len(reminders) == 0:
            return None
        return reminders

    @staticmethod  # просмотр всех целей по имени пользователя
    def get_all_reminder_by_user_name(user_name):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM reminder WHERE user_name = ?", [user_name])

        all_reminder = cursor.fetchall()
        reminders = []
        for id, user_name, day_reminder, time_reminder in all_reminder:
            reminder = Reminder(user_name, day_reminder, time_reminder, id)
            reminders.append(reminder)
        if len(reminders) == 0:
            return None
        return reminders

    @staticmethod  # удаление всех напоминаний пользователя
    def delete_reminder(user_name):
        Database.execute("""DELETE FROM reminder WHERE user_name=?""", [user_name])
        return True

    @staticmethod  # удаление профиля и всех данных
    def delete_account(user_name):
        Database.execute("""DELETE FROM users WHERE user_name=?""", [user_name])
        Database.execute("""DELETE FROM trainings WHERE user_name=?""", [user_name])
        Database.execute("""DELETE FROM goals WHERE user_name=?""", [user_name])
        Database.execute("""DELETE FROM reminder WHERE user_name=?""", [user_name])
        return True
