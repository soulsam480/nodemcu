local SDA = 4
local SCL = 5
i2c.setup(0, SDA, SCL, i2c.SLOW)

-- Try address 0x3C (and optionally 0x3D if 0x3C doesn't work)
local i2c_addr = 0x3C

-- Basic OLED initialization (simplified example)
i2c.start(0)
i2c.address(0, i2c_addr, i2c.TRANSMITTER)
i2c.write(0, 0xAE) -- Display off
i2c.write(0, 0x20) -- Horizontal addressing
i2c.write(0, 0x00)
i2c.stop(0)

-- To test if it works, you can also see if the display at least turns on or shows pixels
i2c.start(0)
i2c.address(0, i2c_addr, i2c.TRANSMITTER)
i2c.write(0, 0x21) -- Set column address
i2c.write(0, 0x00) -- Start column
i2c.write(0, 0x7F) -- End column

i2c.start(0)
i2c.address(0, i2c_addr, i2c.TRANSMITTER)
i2c.write(0, 0x22) -- Set page address
i2c.write(0, 0x00) -- Start page

i2c.start(0)
i2c.address(0, i2c_addr, i2c.TRANSMITTER)
for i = 0, 127 do
	i2c.write(0, 0xFF) -- Fill pixels
end
i2c.stop(0)

i2c.start(0)
i2c.address(0, i2c_addr, i2c.TRANSMITTER)
i2c.write(0, 0xAF) -- Turn on display
i2c.stop(0)
