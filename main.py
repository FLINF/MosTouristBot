import telebot
import logging
from weatherCommand import im
from variables import *

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start']) #Команда для начала работы
def start_handler(message):
    bot.send_message(message.from_user.id, startMessage)
@bot.message_handler(commands=['help']) #Список команд
def help_handler(message):
    bot.send_message(message.from_user.id, helpMessage)
@bot.message_handler(commands=['weather']) #Погода на сегодня
def help_handler(message):
    bot.send_message(message.from_user.id, inDevMessage)
@bot.message_handler(commands=['findPark']) #Найти ближайший парк
def help_handler(message):
    bot.send_message(message.from_user.id, inDevMessage)
    bot.send_photo(message.from_user.id, im)
@bot.message_handler(commands=['findSight']) #Поиск достопримечательности
def help_handler(message):
    bot.send_message(message.from_user.id, inDevMessage)
@bot.message_handler(func=lambda message: True)
def forward_handler(message): #Перессылка сообщенеий в приватный чат
    try:
        if message.chat.id == int(CHAT):
            bot.send_message(message.reply_to_message.forward_from_id, message.text)
        else:
            bot.forward_message(CHAT, message.chat.id, message.message_id)
    except Exception as error:
        print('Exception in forward handler. Info: {}'.format(error))
def main(use_logging, level_name): #Проверка сообщений
    if use_logging:
        telebot.logger.setLevel(logging.getLevelName(level_name))
    bot.polling(none_stop=True, interval=0.5)
if __name__ == '__main__': #Вызов функции
    main(True, 'DEBUG')