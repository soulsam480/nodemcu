## Zoro's ESP8266 Board Projects

### firmware

- first tried using nodemcu lua firmware, it worked but couldn't make displays
  work
- now tried micropython, works beautifully and code seems simple

### Scripts

- lua sciripts in lua_scripts folder
- python scripts in micropy folder

### How to flash

- download binary and flash using esptool

```bash
esptool.py --port /dev/PORT --baud 460800 write_flash --flash_size=detect 0 ~/path/to/.bin
```

- here change the port and binary file

### How to run python code

- to run directly

```bash
ampy --port /dev/PORT run path/to/.py
```

- see ampy docs

### How to load scripts to board

```bash
ampy --port /dev/cu.wchusbserial57660205031 put micropy/lib/weather.py lib/weather.py
```

### Secrets needed to run the app

- create a file inside lib/.secrets.json
- keys
  - weather_key
  - twitter_key
