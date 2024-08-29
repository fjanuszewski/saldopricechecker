import requests
import rumps
from collections import deque
from datetime import datetime, timedelta

class PriceCheckerApp(rumps.App):
    def __init__(self):
        super(PriceCheckerApp, self).__init__("Price Checker")
        self.price_threshold = 1.018
        self.notification_enabled = True
        self.event_log = deque(maxlen=10)

        # Lista de intervalos en minutos y sus correspondientes etiquetas
        self.intervals = [
            (15, "Cada 15 minutos"),
            (240, "Cada 4 horas"),
            (480, "Cada 8 horas"),
            (1440, "Cada 24 horas")
        ]

        self.selected_interval = self.intervals[0][1]  # Selección por defecto
        self.update_interval = self.intervals[0][0] * 60  # Convertir a segundos

        # Configurar menú
        self.build_menu()

        # Iniciar el temporizador sin hacer una consulta inicial duplicada
        self.timer = rumps.Timer(self.update_price, self.update_interval)
        self.timer.start()

        # Seleccionar el intervalo por defecto
        self.update_menu_state(self.selected_interval)

    def build_menu(self):
        self.quit_button = None  # Eliminar el botón "Quit" predeterminado

        interval_menu = []
        for interval, label in self.intervals:
            interval_menu.append(rumps.MenuItem(label, callback=self.set_interval(interval, label)))

        self.menu = [
            rumps.MenuItem("Actualizar ahora", callback=self.manual_update),
            rumps.MenuItem("Notificaciones activadas", callback=self.toggle_notifications),
            rumps.MenuItem("Establecer umbral de precio", callback=self.set_price_threshold),
            ("Intervalo de actualización", interval_menu),
            ("Ver eventos", [
                rumps.MenuItem("Mostrar eventos", callback=self.show_events),
                rumps.MenuItem("Limpiar eventos", callback=self.clear_events)
            ]),
            rumps.MenuItem("Salir", callback=self.quit_application)
        ]

        self.menu["Intervalo de actualización"][self.selected_interval].state = True
        # Configurar estado inicial del menú
        self.menu["Notificaciones activadas"].state = self.notification_enabled

    def manual_update(self, sender=None):
        self.update_price()

    def update_timer(self, interval):
        self.timer.stop()
        self.timer.interval = interval
        self.timer.start()

        # Log para el intervalo actualizado
        print(f"Temporizador detenido. Reiniciando con nuevo intervalo: {interval / 60} minutos.")
        print(f"Temporizador reiniciado con el intervalo: {interval / 60} minutos")

    def set_interval(self, interval, label):
        def callback(sender):
            self.update_interval = interval * 60  # Convertir minutos a segundos
            self.update_timer(self.update_interval)
            self.selected_interval = label
            self.update_menu_state(label)
        return callback

    def update_menu_state(self, selected_label):
        # Desmarcar todas las opciones
        for _, label in self.intervals:
            self.menu["Intervalo de actualización"][label].state = False
        
        # Marcar solo la opción seleccionada
        self.menu["Intervalo de actualización"][selected_label].state = True

        # Log para ver qué opción fue marcada
        print(f"Opción de intervalo marcada: {selected_label}")

    def update_price(self, _=None):
        try:
            now = datetime.now()
            next_update = now + timedelta(seconds=self.timer.interval)

            # Log para la fecha y hora de la próxima actualización
            print(f"Haciendo request a las {now.strftime('%Y-%m-%d %H:%M:%S')}. Próxima actualización a las {next_update.strftime('%Y-%m-%d %H:%M:%S')}")

            url = "https://api.saldo.com.ar/v3/systems?include=rates"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                for item in data['included']:
                    if item['id'] == 'payoneer_usdt':
                        price = float(item['attributes']['price'])

                        formatted_price = f"{price:.4f}"

                        min_recent_price = min(self.event_log, key=lambda x: x[1])[1] if self.event_log else float('inf')

                        event_time = now.strftime("%Y-%m-%d %H:%M:%S")
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
