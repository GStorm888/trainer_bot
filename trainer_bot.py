"""
""""""
эти ковычки нужны для удобства ориентации в коде
""""""""
"""
from telebot import types, TeleBot # импорт библиотек и файлов репозитория
from config import TOKEN
from data_base import Database
import sqlite3
from user import User, Training, Goal
import hashlib
import datetime
""""""
bot = TeleBot(TOKEN) #создание бота через токен
"""
"""
"""
"""
@bot.message_handler(commands=['test']) #функция для тестов
def test(message):
    users = Database.get_all_users()
    print("users", users)
    training = Database.get_all_training()
    print("trainings", training)
    goals = Database.get_all_goals()
    print("goals", goals)

    
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Клавиатура удалена", reply_markup=markup)

    # Database.create_table()

    # Database.drop()
"""
"""
"""
"""     
@bot.callback_query_handler(func=lambda call: True)#для обработки кнопок
def callback_query(call):
    message = call.message
    if call.data == "Yes":#заметки
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Хорошо, напиши мне все свои заметки""")
        bot.register_next_step_handler(message, processing_yes)
    elif call.data == "No":#заметки
        global description_training
        description_training = None
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Хорошо, не буду записывать в твою тренировку""")
        save_training(message)
    elif call.data == "register":
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Отличное решение""")
        register(message)
    elif call.data == "login":
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Отличное решение""")
        login(message)
    elif call.data == "time":
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Хорошо, введи время тренировки в минутах""")
        bot.register_next_step_handler(message, processing_time)
    elif call.data == "distance":
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Хорошо, введи дистанцию в метрах""")
        bot.register_next_step_handler(message, processing_distance)   
    elif call.data == "help":#из функции help
        bot.delete_message(message.chat.id, message.message_id)
        help(message)      
    elif call.data == "start":#из функции help
        bot.delete_message(message.chat.id, message.message_id)
        start(message)      
    elif call.data == "add_workout":#из функции help
        bot.delete_message(message.chat.id, message.message_id)
        add_workout(message)      
    elif call.data == "view_workouts":#из функции help
        bot.delete_message(message.chat.id, message.message_id)
        view_workouts(message)      
    elif call.data == "set_goal":#из функции help
        bot.delete_message(message.chat.id, message.message_id)
        set_goal(message)      
    elif call.data == "view_goal":#из функции help
        bot.delete_message(message.chat.id, message.message_id)
        view_goal(message)      
    elif call.data == "statistic":#из функции help
        bot.delete_message(message.chat.id, message.message_id)
        statistic(message)      
    elif call.data == "reminder":#из функции help
        bot.delete_message(message.chat.id, message.message_id)
        reminder(message)      
    elif call.data == "export_data":#из функции help
        bot.delete_message(message.chat.id, message.message_id)
        export_data(message)      
    elif call.data == "type_training":
        bot.delete_message(message.chat.id, message.message_id)
        view_workouts_to_type(message)  
    elif call.data == "date_training":
        bot.delete_message(message.chat.id, message.message_id)
        view_workouts_to_date(message)  
    elif call.data == "type_and_date_training":
        bot.delete_message(message.chat.id, message.message_id)
        view_workouts_to_type_and_date(message)  
    elif call.data == "all_training":
        bot.delete_message(message.chat.id, message.message_id)
        view_workouts_to_all(message)   
"""
"""
"""
"""         
@bot.message_handler(func=lambda message: message.text in ["Назад"])
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
    if Database.examination_status_log_in(1, telegram_user_id) is None:
        markup = types.InlineKeyboardMarkup()
        login_bttn = types.InlineKeyboardButton(text='login', callback_data='login' )
        register_bttn = types.InlineKeyboardButton(text='register', callback_data='register' )
        markup.add(login_bttn, register_bttn)
        bot.send_message(message.chat.id, """вы не в аккаунте, чтобы продолжить использовать бота войдите в него""", reply_markup=markup)
        return
    markup = types.InlineKeyboardMarkup()
    help_bttn = types.InlineKeyboardButton(text='help', callback_data='help')
    markup.add(help_bttn)
    bot.send_message(message.chat.id, """Привет, я твой личный тренер Денис. 
Нажми /help чтобы ознакомиться с командами""", reply_markup=markup)
    start_help_back_button(message)
"""
"""
"""
"""
def start_help_back_button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("Назад") 
    markup.add(back)
    bot.send_message(message.chat.id, "чтобы откуда угодно попасть в Help, просто нажми на кнопку 'Назад', или напиши слово 'Назад'",  reply_markup=markup)

@bot.message_handler(commands=["help"]) #функция Help для получения информации
def help(message):
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
    logout = types.InlineKeyboardButton(text='logout', callback_data='logout')

    markup.add(help_bttn, start_bttn)
    markup.add(register_bttn, login_bttn)
    markup.add(add_workout_bttn, view_workout_bttn)
    markup.add(set_goal_bttn, view_goals_bttn)
    markup.add(statistics_bttn, reminder_bttn)
    markup.add(export_data_bttn, logout)

    bot.send_message(message.chat.id,
"""Список команд:
1)/start - Начало работы бота 
2)/help - Список команд(ты здесь)
3)/register - Регистраци
4)/login - Авторизация
5)/add_workout[тип][дата[продолжительность/дистанция][калории][примечания] - Добавление новой тренировки.
6)/view_workouts[период/тип] - Просмотр истории тренировок
    Примеры:
    */view_workouts неделя – показать все тренировки за последнюю неделю.
    */view_workouts бег – показать все беговые тренировки за весь период.   
    */view_workouts месяц велосипед – показать велосипедные тренировки за текущий месяц.
7)/set_goal[описание][значение/срок] - Установка цели. 
    Пример:
    */set_goal "Пробежать 50км" месяц.
8)/view_goals – Просмотр списка текущих целей и прогресса по ним
9)/statistics[период][тип] – Просмотр статистики и аналитики
10)/reminder[установка/отключение/список] – Настройка напоминаний о тренировках.
    Пример:
    */reminder установить "каждый вторник и четверг в 7:00"`.
11)/export_data – Экспорт данных о тренировках (опционально).
12)/logout - выход из аккаунта.
                    """,  reply_markup=markup)
"""
"""
"""
"""
#функция register для регистрации нового пользователя
@bot.message_handler(commands=['register']) #начало и ввод имени
def register(message):
    telegram_user_id = str(message.chat.id)
    if Database.search_user_by_telegram_id(telegram_user_id):
        bot.send_message(message.chat.id, f"Увы, но вы уже зарегистрированы, попробуйте ввести ваше имя и войти в аккаунт")
        bot.register_next_step_handler(message, login_username)
        return None
    bot.send_message(message.chat.id, "Для регистрации введи имя пользователя")
    bot.register_next_step_handler(message, register_username)
""""""
def register_username(message): #проверка на уникальность в БД и ввод пароля
    global user_name
    user_name = message.text
    if Database.search_user_by_teleg(user_name):
        bot.send_message(message.chat.id, f"Увы, но пользователь с именем {user_name} уже есть, попробуй ввести новое имя")
        bot.register_next_step_handler(message, register_username)
        return None
    bot.send_message(message.chat.id, "А теперь придумай пароль")
    bot.register_next_step_handler(message, register_password)
""""""
def register_password(message): #завершение и добавление записи в БД
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
#функция login для авторизации пользователя
@bot.message_handler(commands=['login']) #начало, ввод имени и проверка на наличие записей в БД
def login(message):
    telegram_user_id = str(message.chat.id)
    if Database.get_all_users() is None:
        bot.send_message(message.chat.id, """Увы, но сейчас нет зарегистрированых пользователей, попробуй зарегистрировать.Для этого просто введи имя""")
        bot.register_next_step_handler(message, register_username)
        return None
    if Database.examination_status_log_in(1, telegram_user_id):
        bot.send_message(message.chat.id, f"Поздравляю,  вы уже в аккаунте")
        start(message)
    bot.send_message(message.chat.id, "Для входа введи имя пользователя")
    bot.register_next_step_handler(message, login_username)
""""""
def login_username(message):#проверка имени на совпадение в БД и ввод пароля
    global user_name
    user_name = message.text
    if Database.return_user_by_name(user_name) is None:
        bot.send_message(message.chat.id, "Увы, но я не нашел пользователя с таким именем, попробуй ввести другое имя")
        bot.register_next_step_handler(message, login_username)
        return None

    bot.send_message(message.chat.id, "А теперь вспомни пароль")

    bot.register_next_step_handler(message, login_password)
""""""
def login_password(message): #проверка совпадения пароля и имени и запись в БД с статусом активности 1(true)
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
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    if user is None:
        bot.send_message(message.chat.id, "Увы, но вы не зарегистрированы(")
        return None
    elif user.status_log_in == 0: # надо сделать 
        bot.send_message(message.chat.id, "Вы сейчас не активны(")
        return None
    elif user.status_log_in == 1:
            Database.update_status_log_in(0, telegram_user_id) # надо сделать 
            bot.send_message(message.chat.id, "Вы успешно вышли из аккаунта, чтобы вернуться нажмите /start")
"""
"""
"""
"""
@bot.message_handler(commands=['add_workout'])  #функция add_worckout для добавления тренировки
def add_workout(message):
    telegram_user_id = str(message.chat.id)
    if Database.search_user_by_telegram_id(telegram_user_id) is None:#проверка на зарегистрированность пользователя
        markup = types.InlineKeyboardMarkup()
        register = types.InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")
        markup.add(register)
        bot.send_message(message.chat.id, """чтобы я смог записать тренировку тебе нужно зарегистрироваться""", reply_markup=markup)
        bot.register_next_step_handler(message, callback_query)

    elif Database.examination_status_log_in(1, telegram_user_id) is None:#проверка на активность пользователя
        markup = types.InlineKeyboardMarkup()
        login = types.InlineKeyboardButton(text="Войти", callback_data="login")
        markup.add(login)
        bot.send_message(message.chat.id, """чтобы я смог записать тренировку тебе нужно войти в аккаунт""", reply_markup=markup)
        bot.register_next_step_handler(message, callback_query)

    else:#если все проверки пройдены
        bot.send_message(message.chat.id, """Я готов записать твою тренировку, как ее назвать?""")
        bot.register_next_step_handler(message, type_training)
""""""
def type_training(message):#запрос типа тренировки
    global type_training
    type_training = message.text
    bot.send_message(message.chat.id, """Ого, и сколько ты сжег каллорий?""")
    bot.register_next_step_handler(message, call_training)
""""""
def call_training(message):#запрос каллорий и выбор продолжительность или дистанция
    global call_training
    call_training = message.text
    markup = types.InlineKeyboardMarkup()
    time = types.InlineKeyboardButton(text="Продолжительность(мин)", callback_data="time")
    distance = types.InlineKeyboardButton(text="Дистанция(км)", callback_data="distance")
    markup.add(time, distance)
    bot.send_message(message.chat.id, """Отлично, теперь выбери что ввести длительность или дистанцию?""", reply_markup=markup)
""""""
def processing_time(message):#если выбрал продолжительность
    global time_training
    time_training = message.text
    global distance_training
    distance_training = None
    bot.send_message(message.chat.id, """хорошо, отличная продолжительность""")
    description(message)
""""""
def processing_distance(message):#если выбрал дистанцию
    global distance_training
    distance_training = message.text
    global time_training
    time_training = None
    bot.send_message(message.chat.id, """хорошо, отличная дистанция""")
    description(message)
""""""
def description(message):#запрос описания
    markup = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data="Yes")
    no = types.InlineKeyboardButton(text="Нет", callback_data="No")
    markup.add(yes, no)
    bot.send_message(message.chat.id, """Почти готово, есть ли какие заметки к тренировке?""", reply_markup=markup)
""""""
def processing_yes(message):#если ответил да, то обработка описания
    global description_training
    description_training = message.text
    bot.send_message(message.chat.id, """так и записал в твою тренировку""")
    save_training(message)
""""""
def save_training(message):#сохранение в БД
    telegram_user_id = str(message.chat.id)
    user_name = Database.search_user_by_telegram_id(telegram_user_id).user_name
    date_training = datetime.datetime.today().date()
    training = Training(user_name, type_training, date_training, call_training,
                        time_training, distance_training, description_training)
    Database.add_training(training)
    bot.send_message(message.chat.id, """Хорошо, я записал твою тренировку""")
""""""
""""""
""""""
""""""
@bot.message_handler(commands=['view_workouts'])  #функция view_workouts для просмотра тренировок
def view_workouts(message):#выбор как смотртеь транировки
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
def view_workouts_to_type(message):#если выбрал тип(работает, нужен визуал)
    bot.send_message(message.chat.id, """Хорошо, какой тип тренировки?""")
    bot.register_next_step_handler(message, view_workouts_to_type_register_type)
""""""
# def view_workouts_to_type_register_type(message):#вывод из БД если выбрал тип
#     global type_training
#     type_training = message.text
#     view_workouts_to_type = Database.view_workouts_to_type_and_date(type_training, "*")
#     bot.send_message(message.chat.id, f"""готово, {view_workouts_to_type}""")
""""""
""""""
def view_workouts_to_date(message):#если выбрал период(не работает)
    bot.send_message(message.chat.id, """Хорошо, какой тпериод времени?""")
    bot.register_next_step_handler(message, view_workouts_to_type_register_type)
""""""
def view_workouts_to_type_register_type(message):#вывод из БД если выбрал период(не работает)
    global period_training
    period_training = message.text
    telegram_user_id = str(message.chat.id)
    if Database.search_user_by_telegram_id(telegram_user_id) is None:
        bot.send_message(message.chat.id, """я не нашел у вас тренировок""")
    user_name = Database.search_user_by_telegram_id(telegram_user_id)

    view_workouts_to_date = Database.view_workouts_to_type(period_training, user_name)
    bot.send_message(message.chat.id, f"""готово, {view_workouts_to_date}""")
""""""
""""""
def view_workouts_to_type_and_date(message):#если выбрал тип и период
    bot.send_message(message.chat.id, """Хорошо, какой тип тренировки?""")
    bot.register_next_step_handler(message, view_workouts_to_type_and_date_register_type)
""""""
def view_workouts_to_type_and_date_register_type(message):#запрос типа если выбрал тип и период
    global type_training
    type_training = message.text
    bot.send_message(message.chat.id, """Хапомнил, какой промежуток времени?""")
    bot.register_next_step_handler(message, view_workouts_to_type_and_date_register_period)
""""""
def view_workouts_to_type_and_date_register_period(message):#запрос периода если выбрал тип и период(не работает)
    global period_training
    period_training = message.text

    date_training = "?????"
    Database.view_workouts_to_type_and_date(type_training, date_training)
""""""
""""""
def view_workouts_to_all(message):# для просмаотра всех тренировок, нужен красивый вывод(частично работает)
    a = Database.get_all_training()
    bot.send_message(message.chat.id, f"""a: {a}""")
"""
"""
"""
"""
@bot.message_handler(commands=['set_goal'])  #функция set_goal для просмотра статистики
def set_goal(message):
    bot.send_message(message.chat.id, """Какой тип тренировки?""")
    bot.register_next_step_handler(message, set_goal_register_type)

def set_goal_register_type(message):
    global type_training
    type_training = message.text
    bot.send_message(message.chat.id, """Какая дистанция цели?""")
    bot.register_next_step_handler(message, set_goal_register_distance)

def set_goal_register_distance(message):
    global distance_training
    distance_training = message.text
    bot.send_message(message.chat.id, """Сколько дней на выполнение цели?""")
    bot.register_next_step_handler(message, set_goal_register_date_finish)

def set_goal_register_date_finish(message):
    global period_training
    period_training = message.text
    bot.send_message(message.chat.id, """отлично, сейчас запишу""")
    bot.register_next_step_handler(message, set_goal_save)

def set_goal_save(message):
    date_finish = "???????"
    telegram_user_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_user_id)
    user_name = user.user
    goal = Goal(user_name, date_start, type_training, distance_training, date_finish)

    Database.set_goal(goal)
"""
"""
"""
"""
bot.infinity_polling()
