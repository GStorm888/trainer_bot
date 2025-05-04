"""
""
эти ковычки нужны для удобства ориентации в коде
""
"""
from telebot import types, TeleBot
from config import TOKEN
from data_base import Database
import sqlite3
from user import User
import hashlib

bot = TeleBot(TOKEN) #создание бота
"""
"""
"""
"""
@bot.message_handler(commands=['test']) #функция для тестов
def test(message):
    users = Database.get_all_users()
    print(users)
    print(message.chat.id)
"""
"""
"""
"""
@bot.message_handler(commands=['start'])  #функция start для начала работы бота
def start(message):
    markup = types.ReplyKeyboardMarkup()
    help_bttn = types.KeyboardButton("/help")
    markup.add(help_bttn)
    bot.send_message(message.chat.id, """Привет, я твой личный тренер Денис. 
Нажми /help чтобы ознакомиться с командами""")
"""
"""
"""
"""
@bot.message_handler(commands=["help"]) #функция Help для получения информации
def information(message):
    markup = types.InlineKeyboardMarkup()
    
    help_bttn = types.InlineKeyboardButton(text='help', callback_data='help')
    start_bttn = types.InlineKeyboardButton(text='start', callback_data='start_bttn')

    register_bttn = types.InlineKeyboardButton(text='register', callback_data='register_bttn')
    login_bttn = types.InlineKeyboardButton(text='login', callback_data='login_bttn')

    add_workout_bttn = types.InlineKeyboardButton(text='add_workout', callback_data='add_workout_bttn')
    view_workout_bttn = types.InlineKeyboardButton(text='view_workout', callback_data='view_workout_bttn')

    set_goal_bttn = types.InlineKeyboardButton(text='set_goal', callback_data='set_goal_bttn')
    view_goals_bttn = types.InlineKeyboardButton(text='view_goals', callback_data='view_goals_bttn')

    statistics_bttn = types.InlineKeyboardButton(text='statistics', callback_data='statistics_bttn')
    reminder_bttn = types.InlineKeyboardButton(text='reminder', callback_data='reminder_bttn')
    export_data_bttn = types.InlineKeyboardButton(text='export_data', callback_data='export_data_bttn')

    markup.add(help_bttn, start_bttn)
    markup.add(register_bttn, login_bttn)
    markup.add(add_workout_bttn, view_workout_bttn)
    markup.add(set_goal_bttn, view_goals_bttn)
    markup.add(statistics_bttn, reminder_bttn, export_data_bttn)

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
                     
                    """,  reply_markup=markup)
"""
"""
"""
"""
#функция register для регистрации нового пользователя
@bot.message_handler(commands=['register']) #начало и ввод имени
def register(message):
    bot.send_message(message.chat.id, "Для регистрации введи имя пользователя")
    bot.register_next_step_handler(message, register_username)
""""""
def register_username(message): #проверка на уникальность в БД и ввод пароля
    global user_name
    user_name = message.text
    if Database.search_user_by_name(user_name):
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
"""
"""
"""
"""
#функция login для авторизации пользователя
@bot.message_handler(commands=['login']) #начало, ввод имени и проверка на наличие записей в БД
def login(message):
    if Database.get_all_users() is None:
        bot.send_message(message.chat.id, """Увы, но сейчас нет зарегистрированых пользователей, попробуй зарегистрировать.
Для этого просто введи имя""")
        bot.register_next_step_handler(message, register_username)
        return None

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
    user = Database.return_user_by_name(user_name)
    if user.user_name == user_name and user.user_password == user_password:
        print(user.status_log_in)
        if user.status_log_in == 0: # надо сделать 
            Database.update_status_log_in(user) # надо сделать 
            print(user.status_log_in)
        bot.send_message(message.chat.id, f"Ура, вы прошли регистрацию, добро пожаловать {user_name}")
        return None
    bot.send_message(message.chat.id, f"Увы, но вы не прошли регистрацию, неверный пароль, попробуй ввести его завново")
    bot.register_next_step_handler(message, login_password)
"""
"""
"""
"""
@bot.message_handler(commands=['logout'])  #функция logout для выхода из аккаунта
def logout(message):
    telegram_id = str(message.chat.id)
    user = Database.search_user_by_telegram_id(telegram_id)
    print(user.status_log_in)
    if user is None:
        bot.send_message(message.chat.id, "Увы, но вы не зарегистрированы(")
        return None
    elif user.status_log_in == 0: # надо сделать 
        print(user.status_log_in)
        bot.send_message(message.chat.id, "Вы сейчас не активны(")
        return None
    Database.update_status_log_in(user) # надо сделать 
    print(user.status_log_in)

    bot.send_message(message.chat.id, "Вы успешно вышли из аккаунта, чтобы вернуться нажмите /start")

bot.infinity_polling()
