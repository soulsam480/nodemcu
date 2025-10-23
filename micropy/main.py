from lib.oled_api import I2cOled
from lib.odometer import OdoMeter
from lib.connection import connect
import time
from lib.weather import Weather


class MainBoard:
    def __init__(self):
        self.lcd = I2cOled()
        self.lcd.putstr("Initializing board")
        time.sleep(2)

        connect(self.lcd)

    def get_weather(self):
        weather = Weather(self.lcd)
        weather.fetch()
        time.sleep(2 * 60)

    def run_odo(self):
        odo = OdoMeter(self.lcd)
        odo.run_forever()

    def run(self):
        self.get_weather()

        time.sleep(5 * 60)
        self.run()


main = MainBoard()

# main.run_odo()
main.run()
