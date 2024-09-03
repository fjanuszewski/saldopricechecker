import os
import sys
import json

class Localizer:
    def __init__(self, language="es"):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_path, "messages.json")
        with open(file_path, "r") as file:
            self.messages = json.load(file)
        self.language = language

    def get(self, key):
        return self.messages[self.language].get(key, key)

    def set_language(self, language):
        """Cambiar el idioma en vivo."""
        self.language = language
