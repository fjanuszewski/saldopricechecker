import csv
import os

class EventLogger:
    def __init__(self, file_path="event_log.csv"):
        self.file_path = file_path

    def save_event(self, event_time, formatted_price, icon):
        """Guardar un solo evento en el archivo CSV."""
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([event_time, formatted_price, icon])

    def load_events(self):
        """Cargar eventos desde el archivo CSV."""
        events = []
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    events.append(tuple(row))
        return events

    def clear_events(self):
        """Eliminar todos los eventos del archivo CSV."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
