from selenium import webdriver
from PIL import Image
from io import BytesIO


def get_weather():
    edge = webdriver.Edge()
    edge.get('https://www.gismeteo.ru/')

    element = edge.find_element_by_class_name('weather_frames')
    location = element.location
    size = element.size
    png = edge.get_screenshot_as_png()
    edge.quit()

    im = Image.open(BytesIO(png))

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top+20, right, bottom+20))

    return im
