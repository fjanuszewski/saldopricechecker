import os
import requests
import rumps
from collections import deque
from datetime import datetime

class PriceCheckerApp(rumps.App):
    def __init__(self):
        super(PriceCheckerApp, self).__init__("Price Checker")
        self.price_threshold = 1.018
        self.notification_enabled = True
        self.update_interval = 15 * 60
        self.event_log = deque(maxlen=10)
        
        # Eliminar el botón "Quit" predeterminado
        self.quit_button = None

        self.menu = [
            rumps.MenuItem("Actualizar ahora", callback=self.manual_update),
            rumps.MenuItem("Notificaciones activadas", callback=self.toggle_notifications),
            rumps.MenuItem("Establecer umbral de precio", callback=self.set_price_threshold),
            ("Intervalo de actualización", [
                rumps.MenuItem("Cada 15 minutos", callback=self.set_interval_15_min),
                rumps.MenuItem("Cada 4 horas", callback=self.set_interval_4_hours),
                rumps.MenuItem("Cada 8 horas", callback=self.set_interval_8_hours),
                rumps.MenuItem("Cada 24 horas", callback=self.set_interval_24_hours)
            ]),
            ("Ver eventos", [
                rumps.MenuItem("Mostrar eventos", callback=self.show_events),
                rumps.MenuItem("Limpiar eventos", callback=self.clear_events)
            ]),
            rumps.MenuItem("Salir", callback=self.quit_application)  # Añadir el botón "Salir" personalizado
        ]
        
        self.menu["Notificaciones activadas"].state = self.notification_enabled
        self.menu["Intervalo de actualización"]["Cada 15 minutos"].state = True
        
        self.timer = rumps.Timer(self.update_price, self.update_interval)
        
        # Hacer una consulta inicial después de un breve retardo para evitar posibles bloqueos
        rumps.timer(1)(self.manual_update)

    def manual_update(self, sender=None):
        self.update_price()

    def update_timer(self, interval):
        self.timer.stop()
        self.timer.interval = interval
        self.timer.start()
        
        for item in self.menu["Intervalo de actualización"]:
            item.state = False
        sender = [item for item in self.menu["Intervalo de actualización"] if item.callback == interval][0]
        sender.state = True

    def update_price(self, _=None):
        try:
            url = "https://api.saldo.com.ar/v3/systems?include=rates"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                for item in data['included']:
                    if item['id'] == 'payoneer_usdt':
                        price = float(item['attributes']['price'])

                        formatted_price = f"{price:.4f}"

                        min_recent_price = min(self.event_log, key=lambda x: x[1])[1] if self.event_log else float('inf')

                        event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        icon = "🟡" if price < self.price_threshold else ""
                        self.event_log.append((event_time, formatted_price, icon))

                        if price < self.price_threshold:
                            if price < min_recent_price:
                                self.title = f"🟡 Payoneer USDT: {formatted_price}" 
                            else:
                                self.title = f"🟢 Payoneer USDT: {formatted_price}"
                        else:
                            self.title = f"🔴 Payoneer USDT: {formatted_price}"
                        
                        if self.notification_enabled and price < self.price_threshold:
                            rumps.notification("Alerta de Precio", "Precio Bajo", f"El precio ha bajado a {formatted_price}")

                        break
                else:
                    self.title = "ID 'payoneer_usdt' no encontrado"
            else:
                self.title = f"Error en el request: {response.status_code}"
        except Exception as e:
            self.title = f"Error en la conexión: {str(e)}"

    def set_interval_15_min(self, sender):
        self.update_timer(15 * 60)
        self.update_menu_state(sender)

    def set_interval_4_hours(self, sender):
        self.update_timer(4 * 60 * 60)
        self.update_menu_state(sender)

    def set_interval_8_hours(self, sender):
        self.update_timer(8 * 60 * 60)
        self.update_menu_state(sender)

    def set_interval_24_hours(self, sender):
        self.update_timer(24 * 60 * 60)
        self.update_menu_state(sender)

    def update_menu_state(self, selected_item):
        for item in self.menu["Intervalo de actualización"]:
            item.state = False
        selected_item.state = True

    def toggle_notifications(self, sender):
        self.notification_enabled = not self.notification_enabled
        sender.state = self.notification_enabled

    def set_price_threshold(self, sender):
        response = rumps.Window(
            title="Establecer umbral de precio",
            message="Introduce un nuevo valor para el umbral de precio:",
            default_text=str(self.price_threshold)
        ).run()

        try:
            new_threshold = float(response.text)
            self.price_threshold = new_threshold
            rumps.notification("Umbral de Precio", "Nuevo Umbral Establecido", f"El nuevo umbral de precio es {self.price_threshold}")
        except ValueError:
            rumps.alert("Entrada no válida", "Por favor, introduce un número válido.")
    
    def show_events(self, sender):
        events_str = "\n".join([f"{time} - {icon}{price}" for time, price, icon in self.event_log])
        rumps.alert("Últimos 10 eventos", events_str or "No hay eventos registrados.")

    def clear_events(self, sender):
        self.event_log.clear()
        rumps.notification("Eventos", "Registro de eventos limpiado.", "Todos los eventos han sido eliminados.")
    
    def quit_application(self, sender):
        try:
            rumps.quit_application()
        except Exception as e:
            rumps.alert("Error al salir", f"Error: {str(e)}")

if __name__ == "__main__":
    PriceCheckerApp().run()
