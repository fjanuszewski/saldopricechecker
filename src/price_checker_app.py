# price_checker_app.py

import rumps
from datetime import datetime, timedelta
from collections import deque
from api_manager import APIManager
from menu_manager import MenuManager
from localizer import Localizer
from constants import DEFAULT_THRESHOLD, DEFAULT_INTERVAL
from event_logger import EventLogger  # Importamos la nueva clase

class PriceCheckerApp(rumps.App):
    def __init__(self, language="es"):
        self.localizer = Localizer(language)
        super(PriceCheckerApp, self).__init__(self.localizer.get("app_name"))
        self.quit_button = None
        self.price_threshold = DEFAULT_THRESHOLD
        self.notification_enabled = True
        self.update_interval = DEFAULT_INTERVAL
        self.event_log = deque(maxlen=10)

        # Instanciar EventLogger para manejar el almacenamiento de eventos
        self.event_logger = EventLogger()
        self.load_events()  # Cargar eventos al iniciar la aplicación

        # API Manager
        self.api_manager = APIManager()

        # Menu Manager
        self.menu_manager = MenuManager(self, self.localizer)

        # Temporizador
        self.timer = rumps.Timer(self.update_price, self.update_interval)
        self.start_timer()

    def update_menu_language(self):
        """Actualizar los textos del menú al cambiar el idioma."""
        self.menu_manager.build_menu()

    def load_events(self):
        """Cargar eventos desde el archivo CSV y añadirlos al log de eventos."""
        loaded_events = self.event_logger.load_events()
        for event in loaded_events:
            self.event_log.append(event)

    def save_event(self, event_time, formatted_price, icon):
        """Guardar un evento tanto en el log de eventos como en el archivo CSV."""
        self.event_log.append((event_time, formatted_price, icon))
        self.event_logger.save_event(event_time, formatted_price, icon)

    def set_interval(self, interval, label):
        def callback(sender):
            self.update_interval = interval * 60  # Convertir minutos a segundos
            self.update_timer(self.update_interval)
            self.menu_manager.update_menu_state(label)
        return callback

    def start_timer(self):
        self.timer.start()
        print(f"[INFO] Temporizador iniciado con un intervalo de {self.update_interval / 60} minutos.")


    def stop_timer(self):
        self.timer.stop()

    def restart_timer(self):
        self.stop_timer()
        self.start_timer()

    def manual_update(self):
        self.update_price()

    def update_price(self, sender=None):
        now = datetime.now()
        next_update = now + timedelta(seconds=self.timer.interval)
        print(f"[INFO] Haciendo request a las {now.strftime('%Y-%m-%d %H:%M:%S')}. Próxima actualización a las {next_update.strftime('%Y-%m-%d %H:%M:%S')}")

        data = self.api_manager.get_price_data()
        price = self.api_manager.extract_payoneer_usdt_price(data)

        if price:
            formatted_price = f"{price:.4f}"
            min_recent_price = min(self.event_log, key=lambda x: x[1])[1] if self.event_log else float('inf')
            event_time = now.strftime("%Y-%m-%d %H:%M:%S")
            icon = "🟡" if price < self.price_threshold else ""

            # Guardar el evento usando la nueva clase EventLogger
            self.save_event(event_time, formatted_price, icon)

            if price < self.price_threshold:
                if price < min_recent_price:
                    self.title = f"🟡 Payoneer USDT: {formatted_price}" 
                else:
                    self.title = f"🟢 Payoneer USDT: {formatted_price}"
            else:
                self.title = f"🔴 Payoneer USDT: {formatted_price}"
            
            if self.notification_enabled and price < self.price_threshold:
                rumps.notification(self.localizer.get("price_alert"), self.localizer.get("price_low"), f"El precio ha bajado a {formatted_price}")
        
        # Confirmación de que el método se ha ejecutado
        print("[INFO] Método update_price ejecutado correctamente.")

    def update_timer(self, interval):
        self.timer.stop()
        self.timer.interval = interval
        self.timer.start()

        print(f"Temporizador detenido. Reiniciando con nuevo intervalo: {interval / 60} minutos.")
        print(f"Temporizador reiniciado con el intervalo: {interval / 60} minutos")

    def toggle_notifications(self, sender=None):
        self.notification_enabled = not self.notification_enabled
        self.menu_manager.toggle_notification_state()


    def set_price_threshold(self):
        response = rumps.Window(
            title=self.localizer.get("set_price_threshold"),
            message=self.localizer.get("enter_new_threshold"),
            default_text=str(self.price_threshold)
        ).run()

        try:
            new_threshold = float(response.text)
            self.price_threshold = new_threshold
            rumps.notification(self.localizer.get("price_alert"), self.localizer.get("new_threshold_set"), f"El nuevo umbral de precio es {self.price_threshold}")
        except ValueError:
            rumps.alert(self.localizer.get("invalid_input"), self.localizer.get("enter_new_threshold"))

    def show_events(self, sender):
        events_str = "\n".join([f"{time} - {icon}{price}" for time, price, icon in self.event_log])
        rumps.alert(self.localizer.get("events_list_title"), events_str or self.localizer.get("no_events_recorded"))

    def clear_events(self, sender):
        self.event_log.clear()
        self.event_logger.clear_events()  # También limpiamos el archivo CSV
        rumps.notification(self.localizer.get("events_cleared"), "Todos los eventos han sido eliminados.")

    def quit_application(self, sender):
        try:
            rumps.quit_application()
        except Exception as e:
            rumps.alert("Error al salir", f"Error: {str(e)}")
