#!/bin/bash

# Eliminar la aplicación
sudo rm -rf /Applications/SaldoPriceChecker.app

# Eliminar el Launch Agent
rm ~/Library/LaunchAgents/com.tuapp.saldopricechecker.plist

# Eliminar archivos de log
rm ~/Library/Logs/saldopricechecker.log
rm ~/Library/Logs/saldopricechecker_error.log

# Mensaje de confirmación
echo "SaldoPriceChecker ha sido desinstalado correctamente."
