DEFAULT_THRESHOLD = 1.018
DEFAULT_INTERVAL = 15 * 60  # 15 minutos en segundos

INTERVALS = [
    (15, "Cada 15 minutos"),
    (240, "Cada 4 horas"),
    (480, "Cada 8 horas"),
    (1440, "Cada 24 horas")
]

API_URL = "https://api.saldo.com.ar/v3/systems?include=rates"

LANGUAGES = [
    ("es", "Español"),
    ("en", "English"),
    ("pt", "Português"),
    ("it", "Italiano"),
    ("fr", "Français"),
    ("zh", "中文")
]
