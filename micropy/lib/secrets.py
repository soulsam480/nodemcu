import json
import builtins


class Secrets:
    def __init__(self):
        secrets = json.load(builtins.open("lib/.secrets.json", "r"))
        self.secrets = secrets

    def get(self, key):
        return self.secrets.get(key)
