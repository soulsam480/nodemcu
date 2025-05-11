from machine import Pin, I2C
import time


# --- LCD API Base Class ---
class LcdApi:

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0
        self.clear()

    def total_chars(self):
        return self.num_lines * self.num_columns

    def clear(self):
        self.cursor_x = 0
        self.cursor_y = 0
        self.hal_write_command(0x01)
        time.sleep_ms(2)
        self.hal_write_command(0x02)
        time.sleep_ms(2)

    def home(self):
        self.cursor_x = 0
        self.cursor_y = 0
        self.hal_write_command(0x02)
        time.sleep_ms(2)

    def move_to(self, line, column):
        if line >= self.num_lines:
            line = self.num_lines - 1
        if column >= self.num_columns:
            column = self.num_columns - 1

        self.cursor_x = column
        self.cursor_y = line

        # Calculate DDRAM address for the position
        addr = column
        if line == 1:
            addr += 0x40  # Line 1 starts at 0x40
        elif line == 2:
            addr += 0x14  # For 20x4 displays, line 2
        elif line == 3:
            addr += 0x54  # For 20x4 displays, line 3

        self.hal_write_command(0x80 | addr)

    def putstr(self, string):
        for char in string:
            # Check if we need to move to the next line
            if self.cursor_x >= self.num_columns:
                self.cursor_x = 0
                self.cursor_y += 1
                if self.cursor_y >= self.num_lines:
                    self.cursor_y = 0  # Wrap around to the top
                self.move_to(self.cursor_y, self.cursor_x)

            # Write the character and update cursor position
            self.hal_write_data(ord(char))
            self.cursor_x += 1

    def cycle_str(self, string, loop=1):
        # here we need to check if string has more than 32 chars
        # then we need to split in 32 char sets and then render one by one
        last_ind = 0

        if loop == 0:
            return

        if len(string) > 32:
            while last_ind < len(string):
                self.clear()
                self.putstr(string[last_ind:last_ind + 32])
                last_ind += 32
                time.sleep(2)

            if loop > 1:
                self.cycle_str(string, loop - 1)
        else:
            self.putstr(string)


# --- I2C LCD Class ---
class I2cLcd(LcdApi):
    LCD_BACKLIGHT = 0x08
    ENABLE = 0x04

    def __init__(self, i2c_addr, num_lines, num_columns):
        self.i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
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

    def backlight_on(self):
        self.backlight = self.LCD_BACKLIGHT
        self.i2c.writeto(self.i2c_addr, bytes([self.backlight]))

    def backlight_off(self):
        self.backlight = 0
        self.i2c.writeto(self.i2c_addr, bytes([self.backlight]))
