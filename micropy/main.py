from lib.lcd_api import I2cLcd
from lib.connection import connect
import time
from lib.weather import Weather
from lib.twitter import Twitter


class MainBoard:
    def __init__(self):
        self.lcd = I2cLcd(0x27, 2, 16)
        self.lcd.putstr("Initializing board")
        time.sleep(2)

        connect()

    def get_weather(self):
        weather = Weather(self.lcd)
        weather.fetch()

    def get_tweets(self):
        twitter = Twitter(self.lcd)
        twitter.fetch()

    def run(self):
        self.get_weather()
        self.get_tweets()

        time.sleep(5 * 60)
        self.run()


main = MainBoard()

main.run()
