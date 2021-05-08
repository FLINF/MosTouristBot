import sqlite3

from fuzzywuzzy import fuzz
from telebot import types
from main import bot


@bot.message_handler(content_types=['text'])
def get_sight_by_name(name):
    db = sqlite3.connect("MosTourist.db")
    cur = db.cursor()
    cur.execute("""SELECT park_id, title, info, rating, type FROM sight""")
    sight_list = cur.fetchall()
    match_percent = []
    for row in sight_list:
        match = fuzz.token_sort_ratio(name, row[1])
        match_percent.append(match)
    result = sight_list[match_percent.index(max(match_percent))]
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_help = types.KeyboardButton(text='/help')
    button_find_park = types.KeyboardButton(text='/findPark')
    button_find_sight = types.KeyboardButton(text='/findSight')
    button_weather = types.KeyboardButton(text='/weather')
    keyboard.add(button_help, button_find_park, button_find_sight, button_weather)
    bot.send_message(name.from_user.id, text=f"{result[1]} \n \nОписание: \n{result[2]} \n \n"
                                             f"Рейтинг: {result[3]} \nТип: {result[4]}", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_sight_by_name(name):
    db = sqlite3.connect("MosTourist.db")
    cur = db.cursor()
    cur.execute("""SELECT park_id, title, info, rating, type FROM sight""")
    sight_list = cur.fetchall()
    match_percent = []
    for row in sight_list:
        match = fuzz.token_sort_ratio(name, row[1])
        match_percent.append(match)
    result = sight_list[match_percent.index(max(match_percent))]
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_help = types.KeyboardButton(text='/help')
    button_find_park = types.KeyboardButton(text='/findPark')
    button_find_sight = types.KeyboardButton(text='/findSight')
    button_weather = types.KeyboardButton(text='/weather')
    keyboard.add(button_help, button_find_park, button_find_sight, button_weather)
    bot.send_message(name.from_user.id, text=f"{result[1]} \n \nОписание: \n{result[2]} \n \n"
                                             f"Рейтинг: {result[3]} \nТип: {result[4]}", reply_markup=keyboard)