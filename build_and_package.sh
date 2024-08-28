#!/bin/bash

# Configuración
APP_NAME="SaldoPriceChecker"
PKG_NAME="SaldoPriceChecker.pkg"
SOURCE_SCRIPT="SaldoPriceChecker.py"
PLIST_FILE="com.tuapp.saldopricechecker.plist"
SCRIPTS_DIR="./scripts"
DIST_DIR="./dist"
VENV_PATH="./path/to/venv"  # Asegúrate de reemplazar esto con la ruta correcta a tu entorno virtual

# Activar el entorno virtual
source "$VENV_PATH/bin/activate"

# Paso 1: Compilar la aplicación en una aplicación .app usando PyInstaller
pyinstaller --onefile --windowed --name "$APP_NAME" --icon=resources/icon.icns "$SOURCE_SCRIPT"

# Paso 2: Mover el archivo .app generado al directorio dist/
mv "./dist/$APP_NAME.app" "$DIST_DIR/$APP_NAME.app"

# Paso 3: Crear el paquete intermedio utilizando pkgbuild
pkgbuild --install-location /Applications --component ./dist/SaldoPriceChecker.app --scripts ./scripts --identifier com.tuapp.saldopricechecker --version 1.0 ./dist/SaldoPriceChecker-pkg.pkg

# Paso 4: Crear el instalador final utilizando productbuild
productbuild --distribution "$SCRIPTS_DIR/distribution.xml" --package-path "$DIST_DIR" --resources "$SCRIPTS_DIR" "$DIST_DIR/$PKG_NAME"

# Limpieza de archivos innecesarios
rm -rf ./build
rm -rf ./__pycache__
rm -rf ./*.spec
rm -rf ./dist/*.app
rm "$DIST_DIR/$APP_NAME-pkg.pkg"

# Resultado
echo "El paquete ha sido creado en $DIST_DIR/$PKG_NAME"
