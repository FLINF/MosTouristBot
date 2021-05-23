import sqlite3

from telebot import types

from main import bot, standart_markup


@bot.message_handler(content_types=['location'])  # Изпользование локации
def location_handler(location):
    bot.send_message(location.from_user.id, "Три ближайщих парка: ", reply_markup=standart_markup())
    # Выводим стандартную клавиатуру т.к старая уже не нужна

    db = sqlite3.connect("MosTourist.db")  # Подключаемя к базе данных
    coordinates = (location.location.latitude, location.location.longitude)  # Записываем координаты в переменную
    cur = db.cursor()
    cur.execute(f"""SELECT title, ent_objects, rating, latitude, longitude FROM park 
        ORDER BY ABS((longitude - {coordinates[1]})*(longitude - {coordinates[1]}) +
         (latitude - {coordinates[0]})*(latitude - {coordinates[0]})) ASC""")  # Плиск парков
    result = cur.fetchmany(3)
    print(result)
    for row in result:  # Вывож результата
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Открыть в Google Maps',
                                                 url=f'https://www.google.com/maps/search/?api=1&query={row[3]},{row[4]}')
        markup.add(btn_my_site)
        bot.send_message(location.from_user.id, "Парк: " + row[0] + '\n' + "На что посмотреть: " + row[1] + '\n' +
                         "Рейтинг: " + str(row[2]), reply_markup=markup)
        markup = types.ReplyKeyboardRemove
