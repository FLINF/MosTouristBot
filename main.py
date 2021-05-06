import sqlite3
import telebot
import logging

from telebot import types

import weatherCommand
import findParkCommand
from variables import *

bot = telebot.TeleBot(TOKEN)

#db = sqlite3.connect("MosTourist.db")
#cur = db.cursor()


@bot.message_handler(commands=['start'])  # Команда для начала работы
def start_handler(message):
    bot.send_message(message.from_user.id, startMessage)


@bot.message_handler(commands=['help'])  # Список команд
def help_handler(message):
    bot.send_message(message.from_user.id, helpMessage)


@bot.message_handler(commands=['weather'])  # Погода на сегодня
def weather_handler(message):
    im = weatherCommand.get_weather()  # Получаем скриншот погоды в Москве с gismeteo.ru
    bot.send_photo(message.from_user.id, im)


@bot.message_handler(commands=['findPark'])  # Найти ближайший парк
def find_park_handler(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отрпавить геолокацию", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.from_user.id, sendLocationMessage, reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location_handler(location):
    db = sqlite3.connect("MosTourist.db")
    print("debug......................................")
    coordinates = (location.location.latitude, location.location.longitude)
    print(coordinates)
  # result = findParkCommand.find_park(coordinates)  # На основе полученных координат find_park выполняет SQL запрос
    cur1 = db.cursor()
    cur1.execute(f"""SELECT * FROM park ORDER BY ABS(longitude - {coordinates[0]} + latitude - {coordinates[1]})""")
    result = cur1.fetchall()
    bot.send_message(location.from_user.id, result)


@bot.message_handler(commands=['findSight'])  # Поиск достопримечательности
def find_sight_handler(message):
    bot.send_message(message.from_user.id, inDevMessage)


@bot.message_handler(func=lambda message: True)
def forward_handler(message):  # Перессылка сообщенеий в приватный чат
    try:
        if message.chat.id == int(CHAT):
            bot.send_message(message.reply_to_message.forward_from_id, message.text)
        else:
            bot.forward_message(CHAT, message.chat.id, message.message_id)
    except Exception as error:
        print('Exception in forward handler. Info: {}'.format(error))


def main(use_logging, level_name):  # Проверка сообщений
    if use_logging:
        telebot.logger.setLevel(logging.getLevelName(level_name))
    bot.polling(none_stop=True, interval=0.5)


if __name__ == '__main__':  # Вызов функции
    main(True, 'DEBUG')
