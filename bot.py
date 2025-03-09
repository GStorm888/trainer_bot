#импотр библиотек и других файлов для работ
# import telebot
from telebot import types, TeleBot
from config import TOKEN

USERS = {}

bot = TeleBot(TOKEN)

"""
НАЧАЛО| функция start для начала работы бота
"""
@bot.message_handler(commands=['start']) 
def start(message):
    markup = types.ReplyKeyboardMarkup()
    help_bttn = types.KeyboardButton("/help")
    markup.add(help_bttn)
    bot.send_message(message.chat.id, """Привет, я твой личный тренер Денис. 
Нажми /help чтобы ознакомиться с командами""")

"""
КОНЕЦ| функция start для начала работы бота
"""

"""
 # НАЧАЛО| функция Help для получения информации
 """
@bot.message_handler(commands=["help"])
def information(message):
    murkup = types.ReplyKeyboardMarkup()

    help_bttn = types.KeyboardButton("/help")
    start_bttn = types.KeyboardButton("/start")

    register_bttn = types.KeyboardButton("/register")
    login_bttn = types.KeyboardButton("/login")

    add_workout_bttn = types.KeyboardButton("/add_workout")
    view_workout_bttn = types.KeyboardButton("/view_workout")


    set_goal_bttn = types.KeyboardButton("/set_goal")
    view_goals_bttn = types.KeyboardButton("/view_goals")

    statistics_bttn = types.KeyboardButton("/statistics")
    reminder_bttn = types.KeyboardButton("/reminder")
    export_data_bttn = types.KeyboardButton("/export_data")

    murkup.row(help_bttn, start_bttn)
    murkup.row(register_bttn, login_bttn)
    murkup.row(add_workout_bttn, view_workout_bttn)
    murkup.row(set_goal_bttn, view_goals_bttn)
    murkup.row(statistics_bttn, reminder_bttn, export_data_bttn)

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
                     
                    """,  reply_markup=murkup)
"""
КОНЕЦ| функция Help для получения информации
"""


"""
НАЧАЛО| функция register для регистрации нового пользователя
"""
@bot.message_handler(commands=['register']) 
def register(message):

    bot.send_message(message.chat.id, "Для регистрации введи имя пользователя")

    bot.register_next_step_handler(message, register_username)

def register_username(message):
    global username
    username = message.text
    bot.send_message(message.chat.id, "А теперь придумай пароль")

    bot.register_next_step_handler(message, register_password)

def register_password(message):
    password = message.text
    USERS[username] = password
    bot.send_message(message.chat.id, "Поздравляю! Ты успешно зарегистрировался")
"""
КОНЕЦ| функция register для регистрации нового пользователя
"""

"""
НАЧАЛО| функция login для авторизации пользователя
"""
@bot.message_handler(commands=['login']) 
def login(message):

    bot.send_message(message.chat.id, "Для входа введи имя пользователя")

    bot.register_next_step_handler(message, login_username)

def login_username(message):
    global username
    username = message.text
    bot.send_message(message.chat.id, "А теперь вспомни пароль")

    bot.register_next_step_handler(message, login_password)

def login_password(message):
    password = message.text
    USERS[username] = password
    for i in USERS:
        print(i)
    bot.send_message(message.chat.id, "Поздравляю! Ты успешно вошел")
"""
КОНЕЦ| функция login для авторизации пользователя
"""

bot.infinity_polling()