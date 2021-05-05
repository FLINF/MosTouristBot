from main import bot, cur


def get_location():
    @bot.message_handler(content_types=['location'])
    def location_to_variable(message):
        coordinates = (message.location.latitude, message.location.longitude)
        return coordinates


def find_park(coordinates):
    cur.execute(f"""SELECT TOP 3 FROM park ORDER BY ABS( longitude - {coordinates[0]} + latitude - {coordinates[1]})""")
    result = cur.fetchall()
    return result