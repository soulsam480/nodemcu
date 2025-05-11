import network
from lib.lcd_api import I2cLcd
import time


def connect():
    lcd = I2cLcd(0x27, 2, 16)

    lcd.putstr("Connecting to WiFi...")
    time.sleep(2)
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)

    wlan.connect("Airtel_Jai Jagannath", "Mahaprabhu@123")  # connect to an AP

    # Wait until connected
    while not wlan.isconnected():
        pass

    lcd.clear()
    lcd.putstr("Connected to WiFi!")
