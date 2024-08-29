import json

class Localizer:
    def __init__(self, language="es"):
        with open("messages.json", "r") as file:
            self.messages = json.load(file)
        self.language = language

    def get(self, key):
        return self.messages[self.language].get(key, key)

    def set_language(self, language):
        """Cambiar el idioma en vivo."""
        self.language = language
