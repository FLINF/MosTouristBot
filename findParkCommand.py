import sqlite3

from telebot import types

from main import bot


@bot.message_handler(content_types=['location'])
def location_handler(location):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_help = types.KeyboardButton(text='/help')
    button_find_park = types.KeyboardButton(text='/findPark')
    button_find_sight = types.KeyboardButton(text='/findSight')
    button_weather = types.KeyboardButton(text='/weather')
    keyboard.add(button_help, button_find_park, button_find_sight, button_weather)
    bot.send_message(location.from_user.id, "Три ближайщих парка: ", reply_markup=keyboard)

    db = sqlite3.connect("MosTourist.db")
    coordinates = (location.location.latitude, location.location.longitude)
    cur = db.cursor()
    cur.execute(f"""SELECT title, ent_objects, rating, latitude, longitude FROM park 
        ORDER BY ABS(longitude - {coordinates[0]} + latitude - {coordinates[1]})""")
    result = cur.fetchmany(3)
    for row in result:
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Открыть в Google Maps',
                                                 url=f'https://www.google.com/maps/search/?api=1&query={row[3]},{row[4]}')
        markup.add(btn_my_site)
        bot.send_message(location.from_user.id, "Парк: " + row[0] + '\n' + "На что посмотреть: " + row[1] + '\n' +
                         "Рейтинг: " + str(row[2]), reply_markup=markup)
        markup = types.ReplyKeyboardRemove
