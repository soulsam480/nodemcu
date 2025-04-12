from machine import I2C, Pin
import time


# --- LCD API Base Class ---
class LcdApi:

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.clear()

    def clear(self):
        self.hal_write_command(0x01)
        time.sleep_ms(2)
        self.hal_write_command(0x02)
        time.sleep_ms(2)

    def putstr(self, string):
        for char in string:
            self.hal_write_data(ord(char))


# --- I2C LCD Class ---
class I2cLcd(LcdApi):
    LCD_BACKLIGHT = 0x08
    ENABLE = 0x04

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = self.LCD_BACKLIGHT
        self._init_lcd()
        super().__init__(num_lines, num_columns)

    def _init_lcd(self):
        self._write_byte(0x03 << 4)
        time.sleep_ms(5)
        self._write_byte(0x03 << 4)
        time.sleep_ms(5)
        self._write_byte(0x03 << 4)
        time.sleep_ms(5)
        self._write_byte(0x02 << 4)

        self.hal_write_command(0x28)  # 4-bit mode, 2 lines, 5x8 font
        self.hal_write_command(0x08)  # Display off
        self.hal_write_command(0x01)  # Clear display
        time.sleep_ms(2)
        self.hal_write_command(0x06)  # Entry mode
        self.hal_write_command(0x0C)  # Display on

    def hal_write_command(self, cmd):
        self._write_byte(cmd & 0xF0)
        self._write_byte((cmd << 4) & 0xF0)

    def hal_write_data(self, data):
        self._write_byte(data & 0xF0, rs=1)
        self._write_byte((data << 4) & 0xF0, rs=1)

    def _write_byte(self, data, rs=0):
        byte = data | self.backlight
        if rs:
            byte |= 0x01
        self._pulse(byte)

    def _pulse(self, data):
        self.i2c.writeto(self.i2c_addr, bytes([data | self.ENABLE]))
        time.sleep_us(500)
        self.i2c.writeto(self.i2c_addr, bytes([data & ~self.ENABLE]))
        time.sleep_us(100)


# --- Main Program ---

# Set up I2C
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)  # D1 = GPIO5, D2 = GPIO4

# Scan for devices
i2c_devices = i2c.scan()
print("I2C devices found:", i2c_devices)
lcd_addr = i2c_devices[0] if i2c_devices else 0x27  # Default to 0x27

# Init LCD
lcd = I2cLcd(i2c, lcd_addr, 2, 16)

# Show messages
lcd.putstr("Hello ESP8266!")
time.sleep(2)
lcd.clear()
lcd.putstr("MicroPython LCD")
