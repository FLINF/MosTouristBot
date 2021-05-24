import logging

import telebot
from telebot import types

from variables import *

bot = telebot.TeleBot(TOKEN)

def standart_markup(): #  Стандартная клавиатура со списком комманд
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_help = types.KeyboardButton(text='/help')
    button_find_park = types.KeyboardButton(text='/find_park')
    button_find_sight = types.KeyboardButton(text='/find_sight')
    button_weather = types.KeyboardButton(text='/weather')
    keyboard.add(button_help, button_find_park, button_find_sight, button_weather)
    return keyboard;

import weatherCommand #  Импортируем команды только сейчас во избежание ошибки из-за импортирования неинциализированных перемнных
import findParkCommand
import findSightCommand

@bot.message_handler(commands=['start'])  # Команда для начала работы
def start_handler(message):
    bot.send_message(message.from_user.id, startMessage, reply_markup=standart_markup())


@bot.message_handler(commands=['help'])  # Список команд
def help_handler(message):
    bot.send_message(message.from_user.id, helpMessage)


@bot.message_handler(commands=['weather'])  # Погода на сегодня
def weather_handler(message):
    im = weatherCommand.get_weather()  # Получаем скриншот погоды в Москве с gismeteo.ru
    bot.send_photo(message.from_user.id, im)


@bot.message_handler(commands=['find_park'])  # Найти ближайший парк
def find_park_handler(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(sendLocationButtonText, request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.from_user.id, sendLocationMessage, reply_markup=keyboard)
    # Клавитура с кнопкой для отправки геолокации

    @bot.message_handler(content_types=['location']) # Ждём локацию от от пользователя
    def find_park(message):
        findParkCommand.location_handler(message)

@bot.message_handler(commands=['find_sight'])  # Поиск достопримечательности
def find_sight_handler(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) # Клавитура с выбором способа поиска
    button_by_name = types.KeyboardButton(text='/byName')
    button_by_photo = types.KeyboardButton(text='/byPhoto')
    keyboard.add(button_by_photo, button_by_name)
    bot.send_message(message.from_user.id, text = 'Выберите способ сравнения. \n byName - по названию. '
                                                  '\n byPhoto - по фото', reply_markup=keyboard)

    @bot.message_handler(commands=['byName']) # По имени
    def name_search(message):
        bot.send_message(message.from_user.id, text="Напишите название.")
        @bot.message_handler(content_types=['text']) # Ждём назавние от пользователя
        def get_sight(message):
            findSightCommand.get_sight_by_name(message)

    @bot.message_handler(commands=['byPhoto']) # По фотографии
    def name_search(message):
        bot.send_message(message.from_user.id, text="Отправьте фотографию.")

        @bot.message_handler(content_types=['photo']) # Ждём фотографию от пользователя
        def get_sight(message):
            findSightCommand.get_sight_by_photo(message)

def main(use_logging, level_name):  # Проверка сообщений
    if use_logging:
        telebot.logger.setLevel(logging.getLevelName(level_name))
    bot.polling(none_stop=True, interval=0.5)


if __name__ == '__main__':  # Вызов функции
    main(True, 'DEBUG')
