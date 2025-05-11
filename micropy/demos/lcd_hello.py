import time
from lib.lcd_api import I2cLcd

# Init LCD
lcd = I2cLcd(0x27, 2, 16)

# Show messages
lcd.putstr("Hello ESP8266!")
time.sleep(2)
lcd.clear()
lcd.putstr("Demo")
