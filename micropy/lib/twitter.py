import requests
import time
from lib.secrets import Secrets


class Twitter:
    def __init__(self, lcd):
        self.lcd = lcd
        self.secrets = Secrets()

    def get_feed(self):
        headers = {
            "X-Auth-Key": self.secrets.get("twitter_key"),
        }

        self.lcd.clear()
        self.lcd.cycle_str("fetching tweets")

        feed_url = "{}/api/parse?url=https://rsshub.app/twitter/user/sidhant&jq=$.items%5B*%5D.title".format(
            self.secrets.get("base_rss_url")
        )

        response = requests.get(feed_url, headers=headers, timeout=10)

        if response.status_code != 200:
            self.lcd.clear()
            self.lcd.cycle_str("Unable to load tweets")
            return

        data = response.json()

        self.lcd.clear()
        self.lcd.cycle_str("showing tweets")

        for index, item in enumerate(data):
            self.lcd.clear()
            self.lcd.cycle_str("showing tweet [{}] |>".format(index))
            time.sleep(1)

            self.lcd.clear()
            self.lcd.cycle_str(item)
            time.sleep(1)

        self.lcd.clear()
        self.lcd.cycle_str("done showing tweets")

    def fetch(self):
        return self.get_feed()
