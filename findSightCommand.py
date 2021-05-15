import os
import sqlite3

from selenium import webdriver
from fuzzywuzzy import fuzz
from selenium.common.exceptions import NoSuchElementException
from telebot import types
from main import bot
from PIL import Image
from io import BytesIO
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


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


@bot.message_handler(content_types=['photo'])
def get_sight_by_photo(message):
    db = sqlite3.connect("MosTourist.db")
    cur = db.cursor()

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    photo = bot.download_file(file_info.file_path)
    im = Image.open(BytesIO(photo))
    im.save(os.getcwd()+fr"/temp/photo{message.from_user.id}.jpg")
    edge = webdriver.Edge()
    edge.get("https://yandex.ru/images/")
    WebDriverWait(edge, 30).until(ec.element_to_be_clickable((By.XPATH, ".//*[@class='button2 button2_theme_clear "
                                                                        "button2_size_m button2_view_classic"
                                                                        " i-bem']"))).click()
    element = edge.find_element_by_xpath('.//input[@class="cbir-panel__file-input"]')
    element.send_keys(os.getcwd()+fr"/temp/photo{message.from_user.id}.jpg")

    try:
        WebDriverWait(edge, 10).until(ec.presence_of_element_located((By.XPATH, ".//*[@class='ObjectResponse-Title']")))
        name = edge.find_element_by_class_name('ObjectResponse-Title').text
        cur.execute("""SELECT park_id, title, info, rating, type FROM sight""")
        sight_list = cur.fetchall()

        match_percent = []
        for row in sight_list:
            match = fuzz.token_sort_ratio(name, row[1])
            match_percent.append(match)
        result = sight_list[match_percent.index(max(match_percent))]

    except NoSuchElementException:
        print('Element noе found exception')
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_help = types.KeyboardButton(text='/help')
        button_find_park = types.KeyboardButton(text='/findPark')
        button_find_sight = types.KeyboardButton(text='/findSight')
        button_weather = types.KeyboardButton(text='/weather')
        keyboard.add(button_help, button_find_park, button_find_sight, button_weather)
        bot.send_message(message.from_user.id, 'К сожалению, нам не удалось найти достопимечательность на фотографии.',
                         reply_markup=keyboard)
        edge.quit()
        os.remove(os.getcwd()+fr"/temp/photo{message.from_user.id}.jpg")
        return 0

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_help = types.KeyboardButton(text='/help')
    button_find_park = types.KeyboardButton(text='/findPark')
    button_find_sight = types.KeyboardButton(text='/findSight')
    button_weather = types.KeyboardButton(text='/weather')
    keyboard.add(button_help, button_find_park, button_find_sight, button_weather)
    bot.send_message(message.from_user.id, text=f'{result[1]} \n \nОписание: \n{result[2]} \n \n'
                                                f'Рейтинг: {result[3]} \nТип: {result[4]}', reply_markup=keyboard)
    edge.quit()
    os.remove(os.getcwd() + fr"/temp/photo{message.from_user.id}.jpg")
