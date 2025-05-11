import requests
from lib.secrets import Secrets


class Weather:
    def __init__(self, lcd):
        self.lcd = lcd
        self.secrets = Secrets()

    def get_loc(self):
        # Make a GET request
        response = requests.get("http://www.geoplugin.net/json.gp")

        location_data = response.json()

        self.lat = location_data["geoplugin_latitude"]
        self.lon = location_data["geoplugin_longitude"]

        self.lcd.clear()
        self.lcd.putstr("Fetching weather...")

    def get_weather(self):
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&exclude=hourly,daily,alerts,minutely&units=metric".format(
                self.lat,
                self.lon,
                self.secrets.get("weather_key"),
            )
        )

        data = response.json()
        self.city = data["name"]
        self.weather = data["weather"][0]["main"]
        self.desc = data["weather"][0]["description"]
        self.temp = data["main"]["temp"]

        self.lcd.clear()
        self.lcd.cycle_str(
            "City: %s has %s weather with %d degrees."
            % (self.city, self.weather, self.temp),
            2,
        )

    def fetch(self):
        self.get_loc()
        self.get_weather()
