from machine import Pin, I2C
import ssd1306
import time


class I2cOled:
    def __init__(self, width=128, height=64, i2c_addr=0x3C, scl_pin=5, sda_pin=4):
        self.i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.display = ssd1306.SSD1306_I2C(width, height, self.i2c, addr=i2c_addr)
        self.cols = width // 8
        self.lines = height // 8
        self.cursor_x = 0
        self.cursor_y = 0
        self.clear()

    def clear(self):
        self.cursor_x = 0
        self.cursor_y = 0
        self.display.fill(0)
        self.display.show()

    def home(self):
        self.cursor_x = 0
        self.cursor_y = 0

    def move_to(self, line, column):
        self.cursor_x = min(column, self.cols - 1)
        self.cursor_y = min(line, self.lines - 1)

    def putstr(self, string):
        for char in string:
            if char == "\n":
                self.cursor_y += 1
                if self.cursor_y >= self.lines:
                    self.cursor_y = 0
                self.cursor_x = 0
                continue

            if self.cursor_x >= self.cols:
                self.cursor_x = 0
                self.cursor_y += 1
                if self.cursor_y >= self.lines:
                    self.cursor_y = 0

            self.display.text(char, self.cursor_x * 8, self.cursor_y * 8, 1)
            self.cursor_x += 1

        self.display.show()

    def cycle_str(self, string, loop=1):
        total = self.lines * self.cols
        idx = 0

        if loop == 0:
            return

        if len(string) > total:
            while idx < len(string):
                self.clear()
                self.putstr(string[idx : idx + total])
                idx += total
                time.sleep(2)
            if loop > 1:
                self.cycle_str(string, loop - 1)
        else:
            self.putstr(string)
