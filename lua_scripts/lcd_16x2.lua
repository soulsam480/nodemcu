-- init.lua - NodeMCU I2C LCD Hello World
-- This will run automatically on boot

-- Define GPIO pins for I2C
local sda = 2            -- GPIO2 (D4)
local scl = 1            -- GPIO1 (D3)
local lcd_address = 0x27 -- Default address for PCF8574 I2C adapter

-- Initialize I2C
local id = 0 -- I2C ID
i2c.setup(id, sda, scl, i2c.SLOW)

-- LCD module setup
local lcd = {}

-- Commands
lcd.LCD_CLEARDISPLAY = 0x01
lcd.LCD_RETURNHOME = 0x02
lcd.LCD_ENTRYMODESET = 0x04
lcd.LCD_DISPLAYCONTROL = 0x08
lcd.LCD_FUNCTIONSET = 0x20
lcd.LCD_SETDDRAMADDR = 0x80

-- Flags for display/control
lcd.LCD_DISPLAYON = 0x04
lcd.LCD_CURSOROFF = 0x00
lcd.LCD_BLINKOFF = 0x00
lcd.LCD_ENTRYLEFT = 0x02
lcd.LCD_ENTRYSHIFTDECREMENT = 0x00
lcd.LCD_2LINE = 0x08
lcd.LCD_4BITMODE = 0x00
lcd.LCD_5x8DOTS = 0x00
lcd.LCD_BACKLIGHT = 0x08

-- Pin masks
lcd.En = 0x04 -- Enable bit
lcd.Rs = 0x01 -- Register select bit

-- Function to write to the LCD
function lcd:write4bits(value)
	i2c.start(id)
	i2c.address(id, lcd_address, i2c.TRANSMITTER)
	i2c.write(id, bit.bor(value, self.LCD_BACKLIGHT))
	i2c.stop(id)
end

-- Function to pulse the enable pin
function lcd:pulseEnable(value)
	self:write4bits(bit.bor(value, self.En))        -- Enable high
	tmr.delay(1)                                    -- Enable pulse must be >450ns
	self:write4bits(bit.band(value, bit.bnot(self.En))) -- Enable low
	tmr.delay(50)                                   -- Command needs time to process
end

-- Function to send a command to the LCD
function lcd:send(value, mode)
	local high = bit.band(bit.rshift(value, 4), 0x0F)
	local low = bit.band(value, 0x0F)

	if mode == 0 then -- Command mode
		high = bit.band(high, bit.bnot(self.Rs))
		low = bit.band(low, bit.bnot(self.Rs))
	else -- Data mode
		high = bit.bor(high, self.Rs)
		low = bit.bor(low, self.Rs)
	end

	self:pulseEnable(high)
	self:pulseEnable(low)
end

-- Function to initialize the LCD
function lcd:init()
	tmr.delay(50000) -- Wait for 50ms after power-on

	-- 4-bit initialization sequence
	self:write4bits(0x30)
	tmr.delay(4500)
	self:write4bits(0x30)
	tmr.delay(4500)
	self:write4bits(0x30)
	tmr.delay(150)
	self:write4bits(0x20) -- Switch to 4-bit mode

	-- Configure display
	self:send(bit.bor(self.LCD_FUNCTIONSET, self.LCD_2LINE, self.LCD_5x8DOTS, self.LCD_4BITMODE), 0)

	-- Turn on display, turn off cursor and blink
	self.displaycontrol = bit.bor(self.LCD_DISPLAYON, self.LCD_CURSOROFF, self.LCD_BLINKOFF)
	self:send(bit.bor(self.LCD_DISPLAYCONTROL, self.displaycontrol), 0)

	-- Clear the display
	self:send(self.LCD_CLEARDISPLAY, 0)
	tmr.delay(2000) -- This command takes a long time

	-- Set entry mode
	self.displaymode = bit.bor(self.LCD_ENTRYLEFT, self.LCD_ENTRYSHIFTDECREMENT)
	self:send(bit.bor(self.LCD_ENTRYMODESET, self.displaymode), 0)
end

-- Function to set the cursor position
function lcd:setCursor(col, row)
	local row_offsets = { 0x00, 0x40, 0x14, 0x54 }
	self:send(bit.bor(self.LCD_SETDDRAMADDR, col + row_offsets[row + 1]), 0)
end

-- Function to print text to the LCD
function lcd:print(text)
	for i = 1, #text do
		self:send(string.byte(text, i), 1)
	end
end

-- Initialize the LCD
print("Initializing LCD...")
lcd:init()

-- Show "Hello World" on the first line
lcd:setCursor(0, 0)
lcd:print("Hello World")

-- Show "NodeMCU & I2C" on the second line
lcd:setCursor(0, 1)
lcd:print("NodeMCU & I2C")

print("LCD initialized with Hello World message")
