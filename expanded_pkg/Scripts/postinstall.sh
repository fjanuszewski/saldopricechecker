#!/bin/bash
set -x  # Habilita el modo de depuración para ver cada comando ejecutado

# Obtener la ruta del directorio actual del script
SCRIPT_DIR="$(dirname "$0")"

# Registrar la ejecución del script
echo "Iniciando postinstall.sh" >> /tmp/postinstall.log

# Mover la aplicación a la carpeta /Applications
echo "Moviendo la aplicación a /Applications" >> /tmp/postinstall.log
mv "${SCRIPT_DIR}/SaldoPriceChecker.app" /Applications/

# Crear la carpeta LaunchAgents si no existe
echo "Creando la carpeta ~/Library/LaunchAgents si no existe" >> /tmp/postinstall.log
mkdir -p ~/Library/LaunchAgents

# Copiar el archivo .plist a ~/Library/LaunchAgents/
echo "Copiando el archivo .plist a ~/Library/LaunchAgents/" >> /tmp/postinstall.log
cp "${SCRIPT_DIR}/com.tuapp.saldopricechecker.plist" ~/Library/LaunchAgents/

# Asegurarse de que el archivo .plist tenga los permisos correctos
echo "Estableciendo permisos 644 en ~/Library/LaunchAgents/com.tuapp.saldopricechecker.plist" >> /tmp/postinstall.log
chmod 644 ~/Library/LaunchAgents/com.tuapp.saldopricechecker.plist

# Desactivar el Launch Agent si está cargado
echo "Desactivando el Launch Agent" >> /tmp/postinstall.log
launchctl unload ~/Library/LaunchAgents/com.tuapp.saldopricechecker.plist

# Cargar el Launch Agent
echo "Cargando el Launch Agent" >> /tmp/postinstall.log
launchctl load ~/Library/LaunchAgents/com.tuapp.saldopricechecker.plist

echo "Finalizando postinstall.sh" >> /tmp/postinstall.log