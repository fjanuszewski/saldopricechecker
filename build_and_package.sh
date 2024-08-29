#!/bin/bash

# Configuración
APP_NAME="SaldoPriceChecker"
PKG_NAME="SaldoPriceChecker.pkg"
SOURCE_SCRIPT="SaldoPriceChecker.py"
PLIST_FILE="com.tuapp.saldopricechecker.plist"
SCRIPTS_DIR="./scripts"
DIST_DIR="./dist"
VENV_PATH="./venv"  # Ruta al entorno virtual

# Crear el entorno virtual si no existe
if [ ! -d "$VENV_PATH" ]; then
    echo "Creando el entorno virtual en $VENV_PATH..."
    python3 -m venv "$VENV_PATH"
fi

# Activar el entorno virtual
echo "Activando el entorno virtual..."
source "$VENV_PATH/bin/activate"

# Instalar PyInstaller y Pillow si no están instalados
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller no está instalado. Instalando PyInstaller..."
    pip install pyinstaller
fi

if ! python -c "import PIL" &> /dev/null; then
    echo "Pillow no está instalado. Instalando Pillow..."
    pip install pillow
fi

# Paso 1: Compilar la aplicación en una aplicación .app usando PyInstaller
echo "Compilando la aplicación con PyInstaller..."
pyinstaller --onefile --windowed --name "$APP_NAME" --icon=resources/icon.icns "$SOURCE_SCRIPT"

# Paso 2: Mover el archivo .app generado al directorio dist/
echo "Moviendo la aplicación .app al directorio de distribución..."
mv "./dist/$APP_NAME.app" "$DIST_DIR/$APP_NAME.app"

# Paso 3: Crear el paquete intermedio utilizando pkgbuild
echo "Creando el paquete intermedio con pkgbuild..."
pkgbuild --install-location /Applications --component "./dist/$APP_NAME.app" --scripts "$SCRIPTS_DIR" --identifier com.tuapp.saldopricechecker --version 1.0 "./dist/SaldoPriceChecker-pkg.pkg"

# Paso 4: Crear el instalador final utilizando productbuild
echo "Creando el instalador final con productbuild..."
productbuild --distribution "$SCRIPTS_DIR/distribution.xml" --package-path "$DIST_DIR" --resources "$SCRIPTS_DIR" "$DIST_DIR/$PKG_NAME"

# Limpieza de archivos innecesarios
echo "Limpiando archivos innecesarios..."
rm -rf ./build
rm -rf ./__pycache__
rm -rf ./*.spec
rm -rf ./dist/*.app
rm "$DIST_DIR/$APP_NAME-pkg.pkg"

# Resultado
echo "El paquete ha sido creado en $DIST_DIR/$PKG_NAME"
