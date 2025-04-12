i2c.setup(0, 4, 5, i2c.SLOW) -- SDA=GPIO4 (D2), SCL=GPIO5 (D1)
for addr = 0, 127 do
	i2c.start(0)
	local c = i2c.address(0, addr, i2c.TRANSMITTER)
	i2c.stop(0)
	if c then
		print("I2C device found at address 0x" .. string.format("%02X", addr))
	end
end
