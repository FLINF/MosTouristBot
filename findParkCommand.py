import sqlite3

from telebot import types

from main import bot, standart_markup


@bot.message_handler(content_types=['location'])  # Поиск по локации
def location_handler(location):
    bot.send_message(location.from_user.id, "Три ближайших парка: ", reply_markup=standart_markup())
    # Выводим стандартную клавиатуру т.к старая уже не нужна

    db = sqlite3.connect("MosTourist.db")  # Подключаемся к базе данных
    coordinates = (location.location.latitude, location.location.longitude)  # Записываем координаты в переменную
    cur = db.cursor()
    cur.execute(f"""SELECT title, ent_objects, rating, latitude, longitude, park_id FROM park 
            ORDER BY ABS((longitude - {coordinates[1]})*(longitude - {coordinates[1]}) +
             (latitude - {coordinates[0]})*(latitude - {coordinates[0]})) ASC""")  # Поиск парков
    result = cur.fetchmany(3)
    for row in result:  # Вывод результата
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Открыть в Google Maps',
                                                 url=f'https://www.google.com/maps/search/?api=1&query={row[3]},{row[4]}')
        markup.add(btn_my_site)
        result_message = f"Парк:  {row[0]} \nНа что посмотреть: {row[1]} \nРейтинг: {str(row[2])}"
        cur.execute(f"""SELECT title FROM restaurant WHERE park_id = {row[5]}""")
        restaurant_list = cur.fetchall()
        if restaurant_list[0][0] is not None:  # Проверка на наличие ресторанов
            result_message += "\n\nГде покушать:\n"
            for restaurant in restaurant_list:
                result_message += f"{restaurant[0]}, "
            result_message = result_message[:-2]  # Убираем последние два символа в строке (" ,")
        bot.send_message(location.from_user.id, result_message, reply_markup=markup)
