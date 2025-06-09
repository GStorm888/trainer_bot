"""
""""""
эти ковычки нужны для удобства ориентации в коде
нужна установка через pip?
""""""""
"""
from telebot import types, TeleBot # импорт библиотек
import sqlite3
import hashlib
import datetime
import csv
import threading
import time
from config import TOKEN#импорт файлов проекта
from data_base import Database
from user import User, Training, Goal, Reminder
"""
"""
"""
"""
bot = TeleBot(TOKEN) #создание бота через токен
"""
"""
"""
"""
@bot.message_handler(commands=['test']) #функция для тестов
def test(message):
    print("\n")
    users = Database.get_all_users()
    print("users", users, "\n")
    training = Database.get_all_training()
    print("trainings", training, "\n")
    goals = Database.get_all_goals()
    print("goals", goals, "\n")
    reminders = Database.get_all_reminder()
    print("reminders", reminders, "\n")
    print("\n")
    # markup = types.ReplyKeyboardRemove()
    # bot.send_message(message.from_user.id, "Клавиатура удалена", reply_markup=markup)

    # Database.create_table()

    # Database.drop()
"""
"""
"""
""" 
def examination_register_and_login_and_status_log_in(message):
    telegram_user_id = str(message.chat.id)
    if Database.get_all_users() is None:
        bot.send_message(message.chat.id, "Увы, но вы не зарегистрированы")
        time.sleep(1)
        register(message)
        return False
    elif Database.search_user_by_telegram_id(telegram_user_id) is None:
        bot.send_message(message.chat.id, "Увы, но вы не зарегистрированы")
        register(message)
        time.sleep(1)
        return False
    elif Database.examination_status_log_in(0, telegram_user_id) is not None:
        bot.send_message(message.chat.id, "Увы, но вы не в аккаунте")
        time.sleep(1)
        login(message)
        return False
    else:
        return True
"""
"""
"""
""" 
@bot.callback_query_handler(func=lambda call: call.data in ["Yes", "No"])#для обработки кнопок add_workout
def callback_query_description(call):
    message = call.message
    if call.data == "Yes":#заметки /add_workout
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Хорошо, напиши мне все свои заметки""")
        bot.register_next_step_handler(message, processing_yes)
    elif call.data == "No":#заметки /add_workout
        global description_training
        description_training = None
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Хорошо, не буду записывать в твою тренировку""")
        save_training(message)
"""
"""
"""
""" 
@bot.callback_query_handler(func=lambda call: call.data in ["register", "login"])#для обработки кнопок register и login
def callback_query_register_and_login(call):
    message = call.message
    if call.data == "register":#переход к регистрации
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Отличное решение""")
        register(message)
    elif call.data == "login":#переход к авторизации
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Отличное решение""")
        login(message)
"""
"""
"""
""" 
@bot.callback_query_handler(func=lambda call: call.data in ["time", "distance"])#для обработки кнопок add_workout
def callback_query_time_or_distance_add_workout(call):
    message = call.message
    if call.data == "time":#выбор /add_workout
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Хорошо, введи время тренировки в минутах""")
        bot.register_next_step_handler(message, processing_time)
    elif call.data == "distance":#выбор /add_workout
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Хорошо, введи дистанцию в метрах""")
        bot.register_next_step_handler(message, processing_distance) 
"""
"""
"""
""" 
# для обработки кнопок в меню help
@bot.callback_query_handler(func=lambda call: call.data in ["help", "start", "add_workout", "view_workouts",
                                                            "set_goal", "view_goals", "statistics", "reminder",
                                                             "export_data", "logout", "delete_account"])
def callback_query_menu_help(call):
    message = call.message   
    if call.data == "help":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        help(message)      
    elif call.data == "start":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        start(message)      
    elif call.data == "add_workout":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        add_workout(message)      
    elif call.data == "view_workouts":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        view_workouts(message)      
    elif call.data == "set_goal":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        set_goal(message)      
    elif call.data == "view_goals":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        view_goals(message)      
    elif call.data == "statistics":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        statistics(message)      
    elif call.data == "reminder":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        reminder(message)      
    elif call.data == "export_data":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        export_data(message)      
    elif call.data == "logout":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        logout(message)  
    elif call.data == "delete_account":#функция help
        bot.delete_message(message.chat.id, message.message_id)
        delete_account(message)  
"""
"""
"""
""" 
#для обработки кнопок view_workouts
@bot.callback_query_handler(func=lambda call: call.data in ["type_training", "date_training",
                                                            "type_and_date_training", "all_training"])
def callback_query_view_workouts(call):
    message = call.message   
    if call.data == "type_training":# тип view_workouts
        bot.delete_message(message.chat.id, message.message_id)
        view_workouts_to_type(message)  
    elif call.data == "date_training":#период view_workouts
        bot.delete_message(message.chat.id, message.message_id)
        view_workouts_to_date(message)  
    elif call.data == "type_and_date_training":#тип и период view_workouts
        bot.delete_message(message.chat.id, message.message_id)
        view_workouts_to_type_and_date(message)  
    elif call.data == "all_training":#все view_workouts
        bot.delete_message(message.chat.id, message.message_id)
        view_workouts_to_all(message)   
"""
"""
"""
""" 
#для обработки кнопок удаления аккаунта
@bot.callback_query_handler(func=lambda call: call.data in ["del_yes", "del_no", "del_yes_2", "del_no_2"])
def callback_query_del_profile(call):
    message = call.message     
    if call.data == "del_yes":#удаление аккаунта дальше процесс
        bot.delete_message(message.chat.id, message.message_id)
        processing_del_yes(message)   
    elif call.data == "del_no":#удаление аккаунта стоп и переход в help
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Ура, не надо нас покидать""")
        help(message)
    elif call.data == "del_yes_2":#удаление аккаунта стоп и переход в help
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Ура, не надо нас покидать""")
        help(message)
    elif call.data == "del_no_2": #удаление аккаунта конец
        bot.delete_message(message.chat.id, message.message_id)
        processing_del_no_2(message)
"""
"""
"""
""" 
#для обработки кнопок добавления непоминания(дни недели и переход дальше)
@bot.callback_query_handler(func=lambda call: call.data in ["monday", "tuesday", "wednesday",
                                                            "thursday", "friday", "saturday",
                                                             "sunday", "finish_reminder"])
def callback_query_reminder_days_and_next_step(call):
    message = call.message     

    if call.data == "monday": #напоминание на пн
        bot.send_message(message.chat.id, """Хорошо, в Понедельник, в какие еще дни?""")
        processing_day(0)
    elif call.data == "tuesday": #напоминание на вт
        bot.send_message(message.chat.id, """Хорошо, во Вторник, в какие еще дни?""")
        processing_day(1)
    elif call.data == "wednesday": #напоминание на ср
        bot.send_message(message.chat.id, """Хорошо, в Среду, в какие еще дни?""")
        processing_day(2)
    elif call.data == "thursday": #напоминание на чт
        bot.send_message(message.chat.id, """Хорошо, в Четверг, в какие еще дни?""")
        processing_day(3)
    elif call.data == "friday": #напоминание на пт
        bot.send_message(message.chat.id, """Хорошо, в Пятницу, в какие еще дни?""")
        processing_day(4)
    elif call.data == "saturday": #напоминание на сб
        bot.send_message(message.chat.id, """Хорошо, в Субботу, в какие еще дни?""")
        processing_day(5)
    elif call.data == "sunday": #напоминание на вс
        bot.send_message(message.chat.id, """Хорошо, в Воскресенье, в какие еще дни?""")
        processing_day(6)
    elif call.data == "finish_reminder": #регистрации времени для напоминания
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Хорошо, в какое время?""")
        bot.register_next_step_handler(message, processing_time_reminder)
"""
"""
"""
""" 
#для обработки кнопок удаления и создания напоминания
@bot.callback_query_handler(func=lambda call: call.data in ["del_reminder", "add_reminder",
                                                            "del_reminder_yes", "del_reminder_no"])
def callback_query_del_and_add_reminder(call):
    message = call.message     
    if call.data == "del_reminder": #удаление всех напоминаний
        bot.delete_message(message.chat.id, message.message_id)
        del_reminder(message)
    elif call.data == "add_reminder": #добаление напоминаний
        bot.delete_message(message.chat.id, message.message_id)
        add_reminder(message)
    elif call.data == "del_reminder_yes": #удаление всех напоминаний финищ
        bot.delete_message(message.chat.id, message.message_id)
        processing_del_reminder_yes(message)
    elif call.data == "del_reminder_no": #отмена удаления всех напоминаний
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "правильно, не нужно этого делать")
        help(message)
"""
"""
"""
""" 
#для обработки кнопок statistics
@bot.callback_query_handler(func=lambda call: call.data in ["type_statistics", "period_statistics",
                                                            "type_and_period_statistics", "all_statistics"])
def callback_query_statistics(call):
    message = call.message     
    if call.data == "type_statistics": #просмотр статистики по типу
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "хорошо, какой тип тренировок?")
        bot.register_next_step_handler(message, type_statistics)
    elif call.data == "period_statistics": #просмотр статистики по периоду
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "хорошо, какой период?(в днях)")
        bot.register_next_step_handler(message, period_statistics)
    elif call.data == "type_and_period_statistics": #просмотр статистики по типу и периоду
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "хорошо, какой тип?")
        bot.register_next_step_handler(message, type_and_period_statistics)
    elif call.data == "all_statistics": #просмотр всей статистики 
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "хорошо, сейчас отправлю")
        bot.register_next_step_handler(message, all_statistics)
"""
"""
"""
"""         
@bot.message_handler(func=lambda message: message.text == "Назад")#для обработки сообщения 'Назад'
def handle_button(message):
    if message.text == "Назад":
        bot.send_message(message.chat.id, "Хорошо, возвращаю вас в Help")
        help(message)
"""
"""
"""
"""   
@bot.message_handler(commands=['start'])  #функция start для начала работы бота
def start(message):
    telegram_user_id = str(message.chat.id)

    if Database.get_all_users() is None:#если БД пользователей пуста
        markup = types.InlineKeyboardMarkup()
        register_bttn = types.InlineKeyboardButton(text='register', callback_data='register' )
        markup.add(register_bttn)
        bot.send_message(message.chat.id, """вы не зарегистрированы, чтобы продолжить использовать бота зарегистрируйтесь""", reply_markup=markup)
        return
    elif Database.examination_status_log_in(0, telegram_user_id) is not None:#если пользователь не активен
        markup = types.InlineKeyboardMarkup()
        login_bttn = types.InlineKeyboardButton(text='login', callback_data='login' )
        markup.add(login_bttn)
        bot.send_message(message.chat.id, """вы не в аккаунте, чтобы продолжить использовать бота войдите в него""", reply_markup=markup)
        return
    elif Database.search_user_by_telegram_id(telegram_user_id) is None:#если пользователь не найден
        markup = types.InlineKeyboardMarkup()
        register_bttn = types.InlineKeyboardButton(text='register', callback_data='register' )
        markup.add(register_bttn)
        bot.send_message(message.chat.id, """вы не зарегистрированы, чтобы продолжить использовать бота зарегистрируйтесь""", reply_markup=markup)
        return

    markup = types.InlineKeyboardMarkup()#если все хорошо
    help_bttn = types.InlineKeyboardButton(text='help', callback_data='help')
    markup.add(help_bttn)
    bot.send_message(message.chat.id, """Привет, я твой личный тренер Денис. 
Нажми /help чтобы ознакомиться с командами""", reply_markup=markup)
    start_help_back_button(message)
""""""
def start_help_back_button(message):#появление кнопки 'Назад'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("Назад") 
    markup.add(back)
    bot.send_message(message.chat.id, "чтобы откуда угодно попасть в Help, просто нажми на кнопку 'Назад', или напиши слово 'Назад'",  reply_markup=markup)
"""
"""
"""
"""
@bot.message_handler(commands=["help"]) #функция Help для получения информации
def help(message):
    if not examination_register_and_login_and_status_log_in(message):
        return None
    markup = types.InlineKeyboardMarkup()
    
    help_bttn = types.InlineKeyboardButton(text='help', callback_data='help')
    start_bttn = types.InlineKeyboardButton(text='start', callback_data='start')

    register_bttn = types.InlineKeyboardButton(text='register', callback_data='register')
    login_bttn = types.InlineKeyboardButton(text='login', callback_data='login')

    add_workout_bttn = types.InlineKeyboardButton(text='add_workout', callback_data='add_workout')
    view_workout_bttn = types.InlineKeyboardButton(text='view_workouts', callback_data='view_workouts')

    set_goal_bttn = types.InlineKeyboardButton(text='set_goal', callback_data='set_goal')
    view_goals_bttn = types.InlineKeyboardButton(text='view_goals', callback_data='view_goals')

    statistics_bttn = types.InlineKeyboardButton(text='statistics', callback_data='statistics')
    reminder_bttn = types.InlineKeyboardButton(text='reminder', callback_data='reminder')
 
    export_data_bttn = types.InlineKeyboardButton(text='export_data', callback_data='export_data')
    logout_bttn = types.InlineKeyboardButton(text='logout', callback_data='logout')

    delete_account_bttn = types.InlineKeyboardButton(text='delete_account', callback_data='delete_account')

    markup.add(help_bttn, start_bttn)
    markup.add(register_bttn, login_bttn)
    markup.add(add_workout_bttn, view_workout_bttn)
    markup.add(set_goal_bttn, view_goals_bttn)
    markup.add(statistics_bttn, reminder_bttn)
    markup.add(export_data_bttn, logout_bttn)
    markup.add(delete_account_bttn)

    bot.send_message(message.chat.id,
"""📌 Команды для тренера:
/help — Справка по командам
/start — Запуск бота
/register — Регистрация нового пользователя
/login — Вход в аккаунт
/add_workout — Добавить тренировку
/view_workouts — Посмотреть тренировки
/set_goal — Установить цель
/view_goals — Проверить цели и прогресс
/statistics — Показать статистику
/reminder — Управление напоминаниями
/export_data — Экспорт тренировок в файл
/logout — Выход из аккаунта
/delete_account — Удаление аккаунта
                    """,  reply_markup=markup)
"""
"""
"""
"""
#функция register для регистрации нового пользователя
@bot.message_handler(commands=['register']) #начало и ввод имени
def register(message):
    if message.text == "Назад":
        handle_button(message)
        return
    telegram_user_id = str(message.chat.id)
    if Database.search_user_by_telegram_id(telegram_user_id):
        bot.send_message(message.chat.id, f"Увы, но вы уже зарегистрированы, попробуйте ввести ваше имя и войти в аккаунт")
        bot.register_next_step_handler(message, login_username)
        return None
    bot.send_message(message.chat.id, "Для регистрации введи имя пользователя")
    bot.register_next_step_handler(message, register_username)
""""""
def register_username(message): #проверка на уникальность в БД и ввод пароля
    if message.text == "Назад":
        handle_button(message)
        return
    user_name = message.text
    if Database.return_user_by_name(user_name) is not None:
        bot.send_message(message.chat.id, f"Увы, но пользователь с именем {user_name} уже есть, попробуй ввести новое имя")
        bot.register_next_step_handler(message, register_username)
        return None
    bot.send_message(message.chat.id, "А теперь придумай пароль")
    bot.register_next_step_handler(message, register_password, user_name)
""""""
def register_password(message, user_name): #хэширование и добавление записи в БД
    if message.text == "Назад":
        handle_button(message)
        return
    user_password = hashlib.md5((message.text).encode()).hexdigest()
    status_log_in = 1
    telegram_user_id = str(message.chat.id)
    user = User(user_name, user_password, status_log_in, telegram_user_id)
    Database.save(user)
    bot.send_message(message.chat.id, "Поздравляю! Ты успешно зарегистрировался")
    start(message)
"""
"""
"""
"""
@bot.message_handler(commands=['login']) #функция login для авторизации пользователя
def login(message):#начало, ввод имени и проверка на наличие записей в БД
    if message.text == "Назад":
        handle_button(message)
        return
    telegram_user_id = str(message.chat.id)
    if Database.get_all_users() is None:#если БД пуста
        bot.send_message(message.chat.id, """Увы, но вы не зарегистрированы""")
        register_username(message)
        return None
    if Database.examination_status_log_in(1, telegram_user_id):#если пользователь активен
        bot.send_message(message.chat.id, f"Поздравляю,  вы уже в аккаунте")
        start(message)
    bot.send_message(message.chat.id, "Для входа введи имя пользователя")
    bot.register_next_step_handler(message, login_username)
""""""
def login_username(message):#проверка имени на совпадение в БД и ввод пароля
    if message.text == "Назад":
        handle_button(message)
        return
    user_name = message.text
    if Database.return_user_by_name(user_name) is None:
        bot.send_message(message.chat.id, "Увы, но я не нашел пользователя с таким именем, попробуй ввести другое имя")
        bot.register_next_step_handler(message, login_username)
        return None

    bot.send_message(message.chat.id, "А теперь вспомни пароль")

    bot.register_next_step_handler(message, login_password, user_name)
""""""
def login_password(message, user_name): #проверка совпадения пароля и имени и запись в БД со статусом активности 1(true)
    if message.text == "Назад":
        handle_button(message)
        return
    user_password = hashlib.md5((message.text).encode()).hexdigest()
    telegram_user_id = str(message.chat.id)
    user = Database.return_user_by_name(user_name)
    if user.user_name == user_name and user.user_password == user_password:
        if user.status_log_in == 0: 
            Database.update_status_log_in(1, telegram_user_id)
        bot.send_message(message.chat.id, f"Ура, вы вошли в аккаунт, добро пожаловать {user_name}")
        help(message)
        return None
    bot.send_message(message.chat.id, f"Увы, но вы не вошли в аккаунт, неверный пароль, попробуй ввести его завново")
    bot.register_next_step_handler(message, login_password)

"""
"""
"""
"""
@bot.message_handler(commands=['logout'])  #функция logout для выхода из аккаунта
def logout(message):
    if message.text == "Назад":
        handle_button(message)
        return
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    if user is None:#если пользователь не зарегистрирован
        bot.send_message(message.chat.id, "Увы, но вы не зарегистрированы(")
        return None
    elif user.status_log_in == 0: #если пользователь не активен
        bot.send_message(message.chat.id, "Вы сейчас не активны(")
        return None
    elif user.status_log_in == 1:#если все по плану выход с аккаунта и перевод на доп. сообщение
            Database.update_status_log_in(0, telegram_user_id)
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, "Вы успешно вышли из аккаунта", reply_markup=markup)
            logout_finish(message)
""""""
def logout_finish(message):#функция для кнопки логин после выхода с аккаунта
    if message.text == "Назад":
        handle_button(message)
        return
    markup = types.InlineKeyboardMarkup()
    login = types.InlineKeyboardButton(text='login', callback_data='login' )
    markup.add(login)
    bot.send_message(message.chat.id, "когда захотите вернуться нажмите на кнопку", reply_markup=markup)
"""
"""
"""
"""
@bot.message_handler(commands=['add_workout'])  #функция add_worckout для добавления тренировки
def add_workout(message):#проверки и начальное сообщение
    if message.text == "Назад":
        handle_button(message)
        return
    if not examination_register_and_login_and_status_log_in(message):
        return None
    bot.send_message(message.chat.id, """Я готов записать твою тренировку, как ее назвать?""")
    bot.register_next_step_handler(message, type_training_register_type)
""""""
def type_training_register_type(message):#обработка типа тренировки и запрос каллорий
    if message.text == "Назад":
        handle_button(message)
        return
    global type_training
    type_training = message.text
    bot.send_message(message.chat.id, """Ого, и сколько ты сжег каллорий?""")
    bot.register_next_step_handler(message, call_training_register_call)
""""""
def call_training_register_call(message):#обработка каллорий и выбор продолжительность или дистанция
    if message.text == "Назад":
        handle_button(message)
        return
    global call_training
    call_training = message.text
    markup = types.InlineKeyboardMarkup()
    time = types.InlineKeyboardButton(text="Продолжительность(мин)", callback_data="time")
    distance = types.InlineKeyboardButton(text="Дистанция(км)", callback_data="distance")
    markup.add(time, distance)
    bot.send_message(message.chat.id, """Отлично, теперь выбери что ввести длительность или дистанцию?""", reply_markup=markup)
""""""
def processing_time(message):#если выбрал продолжительность потом переход к описанию
    if message.text == "Назад":
        handle_button(message)
        return
    global time_training
    time_training = message.text
    global distance_training
    distance_training = None
    if not time_training.isdigit():
        bot.send_message(message.chat.id, """ты должен ввести только число, попробуй сейчас""")
        bot.register_next_step_handler(message.chat.id, processing_time)
    bot.send_message(message.chat.id, """хорошо, отличная продолжительность""")
    description(message)
""""""
def processing_distance(message):#если выбрал дистанцию потом переход к описанию
    if message.text == "Назад":
        handle_button(message)
        return
    global distance_training
    distance_training = message.text
    global time_training
    time_training = None
    bot.send_message(message.chat.id, """хорошо, отличная дистанция""")
    description(message)
""""""
def description(message):#запрос описания
    if message.text == "Назад":
        handle_button(message)
        return
    markup = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data="Yes")
    no = types.InlineKeyboardButton(text="Нет", callback_data="No")
    markup.add(yes, no)
    bot.send_message(message.chat.id, """Почти готово, есть ли какие заметки к тренировке?""", reply_markup=markup)
""""""
def processing_yes(message):#если ответил да, то обработка описания и переход к сохранению
    if message.text == "Назад":
        handle_button(message)
        return
    global description_training
    description_training = message.text
    bot.send_message(message.chat.id, """так и записал в твою тренировку""")
    save_training(message)
""""""
def save_training(message):#сохранение в БД
    if message.text == "Назад":
        handle_button(message)
        return
    telegram_user_id = str(message.chat.id)
    user_name = Database.search_user_by_telegram_id(telegram_user_id).user_name
    date_training = datetime.datetime.today().date()
    training = Training(str(user_name), type_training, date_training, call_training,
                        time_training, distance_training, description_training)
    Database.add_training(training)
    bot.send_message(message.chat.id, """Хорошо, я записал твою тренировку""")
""""""
""""""
""""""
""""""
@bot.message_handler(commands=['view_workouts'])#функция view_workouts для просмотра тренировок
def view_workouts(message):#выбор как смотреть тренировки
    if message.text == "Назад":
        handle_button(message)
        return
    if not examination_register_and_login_and_status_log_in(message):
        return None
    markup = types.InlineKeyboardMarkup()
    type_training = types.InlineKeyboardButton(text="посмотреть за тип", callback_data="type_training")
    date_training = types.InlineKeyboardButton(text="посмотреть за период", callback_data="date_training")
    type_and_date_training = types.InlineKeyboardButton(text="посмотреть за тип и период", callback_data="type_and_date_training")
    all_training = types.InlineKeyboardButton(text="посмотреть все тренировки", callback_data="all_training")
    markup.add(type_training)
    markup.add(date_training)
    markup.add(type_and_date_training)
    markup.add(all_training)
    bot.send_message(message.chat.id, """выбери что ты хочешь посмотреть""", reply_markup=markup)
""""""
def view_workouts_to_type(message):#если выбрал тип
    if message.text == "Назад":
        handle_button(message)
        return
    bot.send_message(message.chat.id, """Хорошо, какой тип тренировки?""")
    bot.register_next_step_handler(message, view_workouts_to_type_register_type)
""""""
def view_workouts_to_type_register_type(message):#обработка если выбрал тип
    if message.text == "Назад":
        handle_button(message)
        return
    global type_training
    type_training = message.text
    telegram_user_id = str(message.chat.id)
    view_workouts_to_type_print(message)
""""""
def view_workouts_to_type_print(message):#вывод тренировок если выбрал тип
    if message.text == "Назад":
        handle_button(message)
        return
    telegram_user_id = str(message.chat.id)
    if Database.search_user_by_telegram_id(telegram_user_id) is None:
        bot.send_message(message.chat.id, """я не нашел у вас тренировок""")
    count = 0
    user = Database.search_user_by_telegram_id(telegram_user_id)
    user_name = user.user_name
    workouts_to_type = Database.view_workouts_to_type(type_training, user_name)
    bot.send_message(message.chat.id, f"""готово, все тренировки пользователя- {workouts_to_type[0].user_name}, по типу {workouts_to_type[0].type_training}""")
    for workouts in workouts_to_type:
        count += 1
        print_text = f"""
{count}:
дата тренировки {workouts.date_training};
созженные каллорие - {workouts.call_training}
"""
        if workouts.time_training is not None:
            print_text += f"""время тренировки - {workouts.time_training}
"""
        if workouts.distance_training is not None:
            print_text += f"""дистанция тренировки - {workouts.distance_training}
"""
        if workouts.description_training is not None:
            print_text += f"""заметка к тренировке - {workouts.description_training}
"""
        bot.send_message(message.chat.id, print_text)
""""""
""""""
def view_workouts_to_date(message):#если выбрал период
    if message.text == "Назад":
        handle_button(message)
        return
    bot.send_message(message.chat.id, """Хорошо, какой тпериод времени (в днях)?""")
    bot.register_next_step_handler(message, view_workouts_to_date_register_date)
""""""
def view_workouts_to_date_register_date(message):#вывод из БДесли выбрал период
    if message.text == "Назад":
        handle_button(message)
        return
    global period_training
    period_training = message.text
    view_workouts_to_date_print(message)
""""""
def view_workouts_to_date_print(message):# вывод тренировок если выбрал период
    if message.text == "Назад":
        handle_button(message)
        return
    today = datetime.datetime.today().date()
    date_start = today - datetime.timedelta(days=int(period_training))
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    user_name = user.user_name
    workouts_to_date = Database.view_workouts_to_date(date_start, today, user_name)
    count = 0
    bot.send_message(message.chat.id, f"""готово, все тренировки пользователя- {workouts_to_date[0].user_name}, с {date_start}""")
    for workouts in workouts_to_date:
        count += 1
        print_text = f"""
{count}:
дата тренировки {workouts.date_training};
созженные каллорие - {workouts.call_training}
"""
        if workouts.time_training is not None:
            print_text += f"""время тренировки - {workouts.time_training}
"""
        if workouts.distance_training is not None:
            print_text += f"""дистанция тренировки - {workouts.distance_training}
"""
        if workouts.description_training is not None:
            print_text += f"""заметка к тренировке - {workouts.description_training}
"""
        bot.send_message(message.chat.id, print_text)
""""""
""""""
def view_workouts_to_type_and_date(message):#если выбрал тип и период запрос типа
    if message.text == "Назад":
        handle_button(message)
        return
    bot.send_message(message.chat.id, """Хорошо, какой тип тренировки?""")
    bot.register_next_step_handler(message, view_workouts_to_type_and_date_register_type)
""""""
def view_workouts_to_type_and_date_register_type(message):#обработка типа и запрос периода если выбрал тип и период
    if message.text == "Назад":
        handle_button(message)
        return
    global type_training
    type_training = message.text
    bot.send_message(message.chat.id, """Хапомнил, какой промежуток времени?""")
    bot.register_next_step_handler(message, view_workouts_to_type_and_date_register_period)
""""""
def view_workouts_to_type_and_date_register_period(message):#обработка периода если выбрал тип и период
    if message.text == "Назад":
        handle_button(message)
        return
    global period_training
    period_training = message.text
    view_workouts_to_type_and_date_print(message)
""""""
def view_workouts_to_type_and_date_print(message):#вывод тренировок если выбрал тип и период
    if message.text == "Назад":
        handle_button(message)
        return
    today = datetime.datetime.today().date()
    date_start = today - datetime.timedelta(days=int(period_training))
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    user_name = user.user_name
    workouts_to_type_and_date = Database.view_workouts_to_type_and_date(type_training, date_start, today, user_name)

    count = 0
    bot.send_message(message.chat.id, f"""готово, все тренировки пользователя- {workouts_to_type_and_date[0].user_name}, по типу {workouts_to_type_and_date[0].type_training} с {date_start}""")
    for workouts in workouts_to_type_and_date:
        count += 1
        print_text = f"""
{count}:
дата тренировки {workouts.date_training};
созженные каллорие - {workouts.call_training}
"""
        if workouts.time_training is not None:
            print_text += f"""время тренировки - {workouts.time_training}
"""
        if workouts.distance_training is not None:
            print_text += f"""дистанция тренировки - {workouts.distance_training}
"""
        if workouts.description_training is not None:
            print_text += f"""заметка к тренировке - {workouts.description_training}
"""
        bot.send_message(message.chat.id, print_text)
""""""
""""""
def view_workouts_to_all(message):#просмотр всех тренировок пользователя
    if message.text == "Назад":
        handle_button(message)
        return
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    all_trainings = Database.get_all_training_by_user_name(user.user_name)
    count = 0
    print(all_trainings)
    bot.send_message(message.chat.id, f"""готово, все тренировки пользователя- {user.user_name}""")
    for workouts in all_trainings:
        print(workouts)
        print(workouts.user_name)

        count += 1
        print_text = f"""
{count}:
дата тренировки {workouts.date_training};
созженные каллорие - {workouts.call_training}
"""
        if workouts.time_training is not None:
            print_text += f"""время тренировки - {workouts.time_training}
"""
        if workouts.distance_training is not None:
            print_text += f"""дистанция тренировки - {workouts.distance_training}
"""
        if workouts.description_training is not None:
            print_text += f"""заметка к тренировке - {workouts.description_training}
"""
        bot.send_message(message.chat.id, print_text)
"""
"""
"""
"""
@bot.message_handler(commands=['set_goal'])  #функция set_goal для  установки цели(работает осталось оформление)
def set_goal(message):#запрос типа
    if message.text == "Назад":
        handle_button(message)
        return
    if not examination_register_and_login_and_status_log_in(message):
        return None
    bot.send_message(message.chat.id, """Какой тип тренировки?""")
    bot.register_next_step_handler(message, set_goal_register_type)
""""""
def set_goal_register_type(message):#обработка типа и запрос дистанции
    if message.text == "Назад":
        handle_button(message)
        return
    global type_training
    type_training = message.text
    bot.send_message(message.chat.id, """Какая дистанция цели?""")
    bot.register_next_step_handler(message, set_goal_register_distance)
""""""
def set_goal_register_distance(message):#обработка дистанции и запрос срока
    if message.text == "Назад":
        handle_button(message)
        return
    global distance_training
    distance_training = message.text
    bot.send_message(message.chat.id, """Сколько дней на выполнение цели?""")
    bot.register_next_step_handler(message, set_goal_register_date_finish)
""""""
def set_goal_register_date_finish(message):#обработка срока и переход на сохранение
    if message.text == "Назад":
        handle_button(message)
        return
    global period_training
    period_training = message.text
    bot.send_message(message.chat.id, """отлично, я записал""")
    set_goal_save(message)
""""""
def set_goal_save(message):#сохранение данных в БД
    if message.text == "Назад":
        handle_button(message)
        return
    date_start = datetime.datetime.today().date()
    date_finish = date_start + datetime.timedelta(days=int(period_training))
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    user_name = user.user_name
    goal = Goal(user_name, date_start, type_training, distance_training, date_finish)
    Database.set_goal(goal)
"""
"""
"""
"""
@bot.message_handler(commands=['view_goals'])  #функция view_goals для  просмотра целей и их прогресса(не работает)
def view_goals(message):
    if message.text == "Назад":
        handle_button(message)
        return
    if not examination_register_and_login_and_status_log_in(message):
        return None
    today = datetime.datetime.today().date()
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    all_goals = Database.get_all_goal_by_user_name(user.user_name)
    count = 0
    bot.send_message(message.chat.id, f"""готово, все цели пользователя - {user.user_name}""")
    for goal in all_goals:
        left_distance = int(goal.distance_training)
        workouts = Database.view_workouts_to_type_and_date(goal.type_training, goal.date_start, goal.date_finish, user.user_name)
        if workouts is not None:
            for workout in workouts:
                    if workout.distance_training is not None:
                        left_distance -= int(workout.distance_training)
        left_days = datetime.datetime.strptime(goal.date_finish, "%Y-%m-%d") - datetime.datetime.strptime(str(today), "%Y-%m-%d")
        count += 1
        print_text = f"""
{count}:
дата установки цели - {goal.date_start};
тип тренировки - {goal.type_training}
дистанция цели - {goal.distance_training}
осталась дистанция -{left_distance}
дата окончания - {goal.date_finish}
осталось дней - {left_days.days}
"""
        bot.send_message(message.chat.id, print_text)
"""
"""
"""
"""
@bot.message_handler(commands=['statistics'])  #функция statistics для  просмотра статистики(работает нужен вывод)
def statistics(message):
    if message.text == "Назад":
        handle_button(message)
        return
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    all_trainings = Database.get_all_training_by_user_name(user.user_name)
    bot.send_message(message.chat.id, f"""a: {all_trainings}""")
"""
"""
"""
"""
@bot.message_handler(commands=['reminder'])  #функция reminder для  работы с напоминаниями(работает нужен вывод)
def reminder(message):
    if message.text == "Назад":
        handle_button(message)
        return
    if not examination_register_and_login_and_status_log_in(message):
        return None
    markup = types.InlineKeyboardMarkup()
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    user_name = user.user_name
    
    if Database.get_all_reminder_by_user_name(user_name) is not None:
        markup = types.InlineKeyboardMarkup()
        add_reminder_bttn = types.InlineKeyboardButton(text='add_reminder', callback_data='add_reminder')
        del_reminder_bttn = types.InlineKeyboardButton(text='del_reminder', callback_data='del_reminder')
        markup.add(add_reminder_bttn, del_reminder_bttn)
        bot.send_message(message.chat.id, "ты хочешь удалить или добавить напоминания?", reply_markup=markup)
    else: 
        add_reminder(message)
""""""
def add_reminder(message):
    if message.text == "Назад":
        handle_button(message)
        return
    global days_lst
    days_lst = []
    markup = types.InlineKeyboardMarkup()
    
    monday = types.InlineKeyboardButton(text='monday', callback_data='monday')
    tuesday = types.InlineKeyboardButton(text='tuesday', callback_data='tuesday')

    wednesday = types.InlineKeyboardButton(text='wednesday', callback_data='wednesday')
    thursday = types.InlineKeyboardButton(text='thursday', callback_data='thursday')

    friday = types.InlineKeyboardButton(text='friday', callback_data='friday')
    saturday = types.InlineKeyboardButton(text='saturday', callback_data='saturday')

    sunday = types.InlineKeyboardButton(text='sunday', callback_data='sunday')
    finish_reminder = types.InlineKeyboardButton(text='это все', callback_data='finish_reminder')

    markup.add(monday, tuesday)
    markup.add(wednesday, thursday)
    markup.add(friday, saturday)
    markup.add(sunday, finish_reminder)

    bot.send_message(message.chat.id, "Выбери дни в которые нужны напоминания", reply_markup=markup)
""""""
def processing_day(day_int):
    global days_lst
    days_lst.append(day_int)
""""""
def processing_time_reminder(message):
    if message.text == "Назад":
        handle_button(message)
        return
    global time_reminder
    time_reminder = message.text
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    user_name = user.user_name
    for day_reminder in days_lst:
        reminder = Reminder(user_name, day_reminder, time_reminder)
        Database.set_reminder(reminder)
    bot.send_message(message.chat.id, "Я буду вам напоминать")
""""""
""""""
def check_reminder_every_minutes():
    while True:
        now = datetime.datetime.now()
        today = now.weekday() 
        time_now = now.strftime("%H:%M")
        all_reminders = Database.get_all_reminder()
        for reminder in all_reminders:
            if int(reminder.day_reminder) == today and reminder.time_reminder == time_now:
                print("if1")
                user = Database.return_user_by_name(reminder.user_name)
                if user.status_log_in == 1:
                    bot.send_message(user.telegram_user_id, "Я не забываю отправлять вам напоминания")
                else:
                    return None
        time.sleep(60)
""""""
""""""
def del_reminder(message):
    if message.text == "Назад":
        handle_button(message)
        return
    markup = types.InlineKeyboardMarkup()
    del_reminder_yes = types.InlineKeyboardButton(text="да", callback_data="del_reminder_yes")
    del_reminder_no = types.InlineKeyboardButton(text="нет", callback_data="del_reminder_no")
    markup.add(del_reminder_yes, del_reminder_no)
    bot.send_message(message.chat.id, """вы уверены?""", reply_markup=markup)
""""""
def processing_del_reminder_yes(message):
    if message.text == "Назад":
        handle_button(message)
        return
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    user_name = user.user_name
    Database.delete_reminder(user_name)
    bot.send_message(message.chat.id, """все ваши напоминания удалены""")
"""
"""
"""
""" 
@bot.message_handler(commands=['export_data'])  #функция export_data для возвращения файла csv с данными
def export_data(message):
    if not examination_register_and_login_and_status_log_in(message):
        return None
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    user_name = user.user_name
    trainings = Database.get_all_training_by_user_name(user_name)
    trainings_lst = []
    for workout in trainings:
        trainings_lib = {"Тип тренировки": workout.type_training,
        "Дата тренировки": workout.date_training, 
        "Каллории": workout.call_training,
        "Продолжительность": workout.time_training, 
        "Дистанция": workout.distance_training, 
        "Заметка": workout.description_training, 
        }  
        trainings_lst.append(trainings_lib)
    csv_filename = "training.csv"
    with open(csv_filename, "w", newline="") as file:
        fieldnames = ["Тип тренировки", "Дата тренировки", "Каллории",
        "Продолжительность", "Дистанция", "Заметка"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(trainings_lst)
    send_scv_file(telegram_user_id, writer, csv_filename)
""""""
def send_scv_file(telegram_user_id, file, csv_filename):
    doc = open(csv_filename, 'rb')
    bot.send_document(telegram_user_id, doc)
"""
"""
"""
""" 
@bot.message_handler(commands=['delete_account'])#функция для удаления аккаунта
def delete_account(message):#вопрос уверенности
    if message.text == "Назад":
        handle_button(message)
        return
    if not examination_register_and_login_and_status_log_in(message):
        return None
    markup = types.InlineKeyboardMarkup()
    del_yes = types.InlineKeyboardButton(text="да", callback_data="del_yes")
    del_no = types.InlineKeyboardButton(text="нет", callback_data="del_no")
    markup.add(del_yes, del_no)
    bot.send_message(message.chat.id, """вы уверены?""", reply_markup=markup)
""""""
def processing_del_yes(message):#второй вопрос уверенности если в первом ответил "да"
    if message.text == "Назад":
        handle_button(message)
        return
    markup = types.InlineKeyboardMarkup()
    del_yes_2 = types.InlineKeyboardButton(text="да", callback_data="del_yes_2")
    del_no_2 = types.InlineKeyboardButton(text="нет", callback_data="del_no_2")
    markup.add(del_yes_2, del_no_2)
    bot.send_message(message.chat.id, """вы потеряете все записи о себе, может все таки останетесь?""", reply_markup=markup)
""""""
def processing_del_no_2(message):#удаление аккаунта и кнопки "Назад" если во втором вопросе ответ "нет"
    if message.text == "Назад":
        handle_button(message)
        return
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    user_name = user.user_name
    Database.delete_account(user_name)
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, """мне очень грустно что вы уходите, но я всегда жду вас обратно""", reply_markup=markup)
    processing_del_finish(message)
""""""
def processing_del_finish(message):#дополнительное сообщение для возможности зарегистрироваться
    if message.text == "Назад":
        handle_button(message)
        return
    markup = types.InlineKeyboardMarkup()
    register = types.InlineKeyboardButton(text='register', callback_data='register' )
    markup.add(register)
    bot.send_message(message.chat.id, """если захотите вернуться, просто нажмите на кнопку""", reply_markup=markup)
"""
"""
"""
"""
# reminder_thread = threading.Thread(target=check_reminder_every_minutes, daemon=True)
# reminder_thread.start()
bot.infinity_polling()
