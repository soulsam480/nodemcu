-- Configure I2C (SDA on GPIO4/D2, SCL on GPIO5/D1)
local SDA = 4 -- GPIO4 (D2 on NodeMCU)
local SCL = 5 -- GPIO5 (D1 on NodeMCU)
i2c.setup(0, SDA, SCL, i2c.SLOW)

-- SSD1306 OLED display settings
local oled_addr = 0x3D -- Common I2C address for SSD1306 OLEDs. Adjust if needed.

-- SSD1306 OLED initialization and drawing functions
local function oled_init()
	-- Initialize the SSD1306 display
	i2c.start(0)
	i2c.address(0, oled_addr, i2c.TRANSMITTER)
	i2c.write(0, 0xAE) -- Set display off
	i2c.write(0, 0xD5) -- Set display clock division
	i2c.write(0, 0x80) -- The suggested ratio 0x80
	i2c.write(0, 0xA8) -- Multiplex ratio
	i2c.write(0, 0x3F)
	i2c.write(0, 0xD3) -- Set display offset
	i2c.write(0, 0x00) -- No offset
	i2c.write(0, 0x40) -- Set start line
	i2c.write(0, 0x8D) -- Charge pump
	i2c.write(0, 0x14) -- Enable charge pump
	i2c.write(0, 0x20) -- Memory mode
	i2c.write(0, 0x00) -- Horizontal addressing
	i2c.write(0, 0xA1) -- Segment re-map
	i2c.write(0, 0xC8) -- COM output scan direction
	i2c.write(0, 0xDA) -- COM pins hardware configuration
	i2c.write(0, 0x12) -- Disable COM left/right remap
	i2c.write(0, 0x81) -- Set contrast control
	i2c.write(0, 0xCF) -- Contrast value
	i2c.write(0, 0xD9) -- Set pre-charge period
	i2c.write(0, 0xF1) -- Pre-charge
	i2c.write(0, 0xDB) -- Set vcomh deselect level
	i2c.write(0, 0x40) -- vcomh deselect level
	i2c.write(0, 0xA6) -- Entire display ON
	i2c.write(0, 0xA4) -- Entire display OFF (until reset)
	i2c.write(0, 0xAF) -- Turn on display
	i2c.stop(0)
end

local function oled_clear()
	i2c.start(0)
	i2c.address(0, oled_addr, i2c.TRANSMITTER)
	for y = 0, 7 do
		i2c.write(0, 0xB0 + y) -- Set page address
		i2c.write(0, 0x00) -- Set column address lower byte
		i2c.write(0, 0x10) -- Set column address higher byte
		for x = 0, 127 do
			i2c.write(0, 0x00) -- Clear pixels
		end
	end
	i2c.stop(0)
end

-- Draw text on the OLED display
local function oled_draw_text(x, y, text)
	i2c.start(0)
	i2c.address(0, oled_addr, i2c.TRANSMITTER)
	i2c.write(0, 0xB0 + y) -- Set page address
	i2c.write(0, 0x00 + x) -- Set column address lower byte
	i2c.write(0, 0x10) -- Set column address higher byte (0x10 because we're addressing bytes, so multiply by 8 and add a little more)

	for i = 1, #text do
		local char = text:sub(i, i)
		-- ASCII lookup in font (simplified example)
		-- Replace with actual ASCII-to-dotmap lookup
		i2c.write(0, string.byte(char))
	end
	i2c.stop(0)
end

-- Main initialization and display "Hello, World!"
function init()
	oled_init()
	oled_clear()
	oled_draw_text(0, 0, "Hello")
	oled_draw_text(0, 1, "World!")
end

tmr.create():alarm(1000, tmr.ALARM_SINGLE, init)
