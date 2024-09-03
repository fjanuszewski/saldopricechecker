import csv
import os

class EventLogger:
    def __init__(self, file_name="event_log.csv"):
        self.file_name = file_name
        self.file_path = self._get_log_file_path()

    def _get_log_file_path(self):
        """Obtiene la ruta completa para el archivo de log en Application Support."""
        app_support_dir = os.path.expanduser("~/Library/Application Support/SaldoPriceChecker")
        os.makedirs(app_support_dir, exist_ok=True)  # Crea el directorio si no existe
        return os.path.join(app_support_dir, self.file_name)

    def save_event(self, event_time, formatted_price, icon):
        """Guardar un solo evento en el archivo CSV."""
        try:
            print(f"Guardando evento en {self.file_path}")  # Mensaje de depuración
            with open(self.file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([event_time, formatted_price, icon])
            print(f"Evento guardado correctamente")  # Mensaje de depuración
        except Exception as e:
            print(f"Error al guardar evento en el archivo {self.file_path}: {e}")


    def load_events(self):
        """Cargar eventos desde el archivo CSV."""
        events = []
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, mode='r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        events.append(tuple(row))
            except Exception as e:
                print(f"Error al cargar eventos desde el archivo {self.file_path}: {e}")
        return events

    def clear_events(self):
        """Eliminar todos los eventos del archivo CSV."""
        if os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
            except Exception as e:
                print(f"Error al eliminar el archivo {self.file_path}: {e}")
