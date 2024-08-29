from price_checker_app import PriceCheckerApp

def main():
    # Crear una instancia de PriceCheckerApp
    app = PriceCheckerApp(language="es")  # Puedes cambiar "es" por "en" para cambiar el idioma

    # Iniciar el temporizador
    app.start_timer()

    # La aplicación Rumps necesita correr el loop principal
    app.menu_manager.app.run()

if __name__ == "__main__":
    main()
