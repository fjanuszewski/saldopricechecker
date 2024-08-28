# SaldoPriceChecker

SaldoPriceChecker es una aplicación para macOS que monitorea los precios de Payoneer USDT desde una API externa y notifica al usuario si el precio baja de un umbral especificado.

## Requisitos

- Python 3.6 o superior
- `pip` para instalar paquetes de Python
- `pyinstaller` para compilar la aplicación
- Entorno virtual de Python

## Instalación

1. **Clona este repositorio en tu máquina local:**
```git clone https://github.com/tuusuario/saldopricechecker.git cd saldopricechecker```

2. **Configura y activa un entorno virtual de Python:**
```python3 -m venv ./path/to/venv source ./path/to/venv/bin/activate```

3. **Instala las dependencias necesarias:**
```pip install -r requirements.txt```


4. **Compila la aplicación en una aplicación macOS (.app) usando PyInstaller:**

```./build_and_package.sh```



Este script hará lo siguiente:
- Compilar la aplicación utilizando `pyinstaller`.
- Crear un paquete instalador `.pkg` utilizando `pkgbuild` y `productbuild`.
- Crear el instalador final en el directorio `dist`.

## Uso

Después de instalar la aplicación mediante el `.pkg` generado, la aplicación se ejecutará automáticamente y estará disponible en la barra de menús.

### Funcionalidades:

- **Actualizar ahora:** Realiza una consulta inmediata para obtener el precio actual.
- **Notificaciones activadas:** Activa o desactiva las notificaciones.
- **Establecer umbral de precio:** Permite definir el umbral de precio para las alertas.
- **Intervalo de actualización:** Permite seleccionar el intervalo de tiempo para las actualizaciones automáticas (15 minutos, 4 horas, 8 horas, 24 horas).
- **Ver eventos:** Muestra los últimos 10 eventos registrados.
- **Salir:** Cierra la aplicación y detiene la ejecución del Launch Agent.

### Iniciar Manualmente la Aplicación

Si deseas iniciar manualmente la aplicación después de haberla cerrado, simplemente abre la carpeta `Applications` y haz doble clic en `SaldoPriceChecker.app`.

## Personalización del Icono

El icono de la aplicación puede ser personalizado utilizando un archivo `.icns` específico. Puedes cambiar el icono actual reemplazando el archivo `resources/icon.icns` con tu propio archivo `.icns` antes de compilar.

## Desinstalación

Para desinstalar la aplicación, puedes ejecutar el siguiente script:

```./scripts_uninstall/postuninstall.sh```


Este script removerá la aplicación de `/Applications` y también eliminará el Launch Agent.
