from io import BytesIO

from PIL import Image
from selenium import webdriver


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

    im = im.crop((left, top+25, right, bottom+25))

    return im
