import rumps
from constants import INTERVALS, LANGUAGES

class MenuManager:
    def __init__(self, app, localizer):
        self.app = app
        self.localizer = localizer
        self.intervals = INTERVALS
        self.selected_interval = self.intervals[0][1]  # Selección por defecto
        self.selected_language = LANGUAGES[0][0]  # Selección de idioma por defecto
        self.build_menu()

    def build_menu(self):
        # Limpiar el menú antes de reconstruirlo
        self.app.menu.clear()

        self.app.quit_button = None  # Eliminar el botón "Quit" predeterminado

        interval_menu = []
        for interval, label in self.intervals:
            # Aquí configuramos el callback para cada intervalo
            menu_item = rumps.MenuItem(label, callback=self.app.set_interval(interval, label))
            interval_menu.append(menu_item)

        language_menu = []
        for lang_code, lang_name in LANGUAGES:
            menu_item = rumps.MenuItem(lang_name, callback=self.set_language(lang_code))
            language_menu.append(menu_item)

        # Construimos el menú completo sin el botón "Quit"
        self.app.menu = [
            rumps.MenuItem(self.localizer.get("update_now"), callback=self.app.manual_update),
            rumps.MenuItem(self.localizer.get("notifications_enabled"), callback=self.app.toggle_notifications),
            rumps.MenuItem(self.localizer.get("set_price_threshold"), callback=self.app.set_price_threshold),
            (self.localizer.get("update_interval"), interval_menu),
            (self.localizer.get("view_events"), [
                rumps.MenuItem(self.localizer.get("show_events"), callback=self.app.show_events),
                rumps.MenuItem(self.localizer.get("clear_events"), callback=self.app.clear_events),
            ]),
            (self.localizer.get("language"), language_menu),
            rumps.MenuItem(self.localizer.get("exit"), callback=self.app.quit_application)
        ]

        # Establecemos el estado inicial en el menú de intervalos e idiomas
        self.update_menu_state(self.selected_interval)
        self.update_language_state(self.selected_language)

    def update_menu_state(self, selected_label):
        # Desmarcar todas las opciones en "Intervalo de actualización"
        for _, label in self.intervals:
            self.app.menu[self.localizer.get("update_interval")][label].state = False

        # Marcar solo la opción seleccionada
        self.app.menu[self.localizer.get("update_interval")][selected_label].state = True
        self.selected_interval = selected_label
        print(f"Opción de intervalo marcada: {selected_label}")

    def update_language_state(self, selected_language):
        # Desmarcar todas las opciones en "Selector de idioma"
        for lang_code, lang_name in LANGUAGES:
            self.app.menu[self.localizer.get("language")][lang_name].state = False

        # Marcar solo la opción seleccionada
        lang_name = next(name for code, name in LANGUAGES if code == selected_language)
        self.app.menu[self.localizer.get("language")][lang_name].state = True
        self.selected_language = selected_language
        print(f"Idioma seleccionado: {lang_name}")

    def set_language(self, lang_code):
        def callback(sender):
            self.app.localizer.set_language(lang_code)
            self.update_language_state(lang_code)
            self.app.update_menu_language()  # Actualizar el idioma del menú en vivo
        return callback

    def toggle_notification_state(self):
        """Actualizar el estado de la opción de notificaciones en el menú."""
        menu_item = self.app.menu[self.localizer.get("notifications_enabled")]
        menu_item.state = self.app.notification_enabled
        
        # Reproducir un sonido cuando se activan las notificaciones
        if self.app.notification_enabled:
            rumps.notification(self.localizer.get("notifications_enabled"), "", "🔔 Notificaciones activadas")
