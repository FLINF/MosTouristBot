import sqlite3
import telebot
import logging
from variables import *
from telebot import types

bot = telebot.TeleBot(TOKEN)

import weatherCommand
import findParkCommand
import findSightCommand


@bot.message_handler(commands=['start'])  # Команда для начала работы
def start_handler(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_help = types.KeyboardButton(text='/help')
    button_find_park = types.KeyboardButton(text='/findPark')
    button_find_sight = types.KeyboardButton(text='/findSight')
    button_weather = types.KeyboardButton(text='/weather')
    keyboard.add(button_help, button_find_park, button_find_sight, button_weather)
    bot.send_message(message.from_user.id, startMessage, reply_markup=keyboard)


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
    button_geo = types.KeyboardButton(sendLocationButtonText, request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.from_user.id, sendLocationMessage, reply_markup=keyboard)

    @bot.message_handler(content_types=['location'])
    def find_park(message):
        findParkCommand.location_handler(message)

@bot.message_handler(commands=['findSight'])  # Поиск достопримечательности
def find_sight_handler(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_by_name = types.KeyboardButton(text='/byName')
    button_by_photo = types.KeyboardButton(text='/byPhoto')
    keyboard.add(button_by_photo, button_by_name)
    bot.send_message(message.from_user.id, text = 'Выберите способ сравнения. \n byName - по названию. '
                                                  '\n byPhoto - оп фото', reply_markup=keyboard)

    @bot.message_handler(commands=['byName'])
    def name_search(message):
        bot.send_message(message.from_user.id, inDevMessage)
        bot.send_message(message.from_user.id, text="Напишите название.")
        print("debugsdjhkjghksjdhgksdjhglskjdhgksjhgkjsdghkjsghldkjghlsj")
        @bot.message_handler(content_types=['text'])
        def get_sight(message):
            print("debugsdjhkjghksjdhgksdjhglskjdhgksjhgkjsdghkjsghldkjghlsj")
            findSightCommand.get_sight_by_name(message)



# @bot.message_handler(func=lambda message: True)
# def forward_handler(message):  # Перессылка сообщенеий в приватный чат
#     try:
#         if message.chat.id == int(CHAT):
#             bot.send_message(message.reply_to_message.forward_from_id, message.text)
#         else:
#             bot.forward_message(CHAT, message.chat.id, message.message_id)
#     except Exception as error:
#         print('Exception in forward handler. Info: {}'.format(error))


def main(use_logging, level_name):  # Проверка сообщений
    if use_logging:
        telebot.logger.setLevel(logging.getLevelName(level_name))
    bot.polling(none_stop=True, interval=0.5)


if __name__ == '__main__':  # Вызов функции
    main(True, 'DEBUG')
