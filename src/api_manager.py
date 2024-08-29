import requests
from constants import API_URL

class APIManager:
    def __init__(self):
        self.api_url = API_URL

    def get_price_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al conectar con la API: {str(e)}")
            return None

    def extract_payoneer_usdt_price(self, data):
        if data:
            for item in data.get('included', []):
                if item['id'] == 'payoneer_usdt':
                    return float(item['attributes']['price'])
        print("ID 'payoneer_usdt' no encontrado")
        return None
