#!/usr/bin/env python
"""
ARCHIVO PRINCIPAL DE GESTIÓN DE DJANGO

Este archivo es como el "control remoto" de tu aplicación Django.
A través de este archivo puedes ejecutar comandos para:
- Crear la base de datos (migrate)
- Ejecutar el servidor (runserver)
- Crear superusuarios (createsuperuser)
- Y muchas otras tareas administrativas
"""

# Importamos las librerías necesarias
import os    # Para trabajar con variables del sistema operativo
import sys   # Para trabajar con argumentos de la línea de comandos


def main():
    """
    FUNCIÓN PRINCIPAL - EL CEREBRO DEL ARCHIVO
    
    Esta función es la que se ejecuta cuando escribes 'python manage.py' en la terminal.
    Se encarga de:
    1. Configurar Django
    2. Ejecutar el comando que le pidas
    """
    
    # PASO 1: Configurar qué archivo de configuración usar
    # Le decimos a Django dónde están nuestras configuraciones
    # 'encuestas_project.settings' es la ruta a nuestro archivo settings.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encuestas_project.settings')
    
    # PASO 2: Intentar importar Django y ejecutar comandos
    try:
        # Importamos la función que ejecuta comandos de Django
        # Esta función es la que entiende comandos como 'runserver', 'migrate', etc.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si Django no está instalado, mostrar un error útil
        # Esto pasa cuando olvidas instalar Django o activar el entorno virtual
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado y "
            "disponible en tu variable de entorno PYTHONPATH? ¿Olvidaste "
            "activar un entorno virtual?"
        ) from exc
    
    # PASO 3: Ejecutar el comando que escribiste en la terminal
    # sys.argv contiene todos los argumentos que escribiste
    # Por ejemplo, si escribes 'python manage.py runserver'
    # sys.argv será ['manage.py', 'runserver']
    execute_from_command_line(sys.argv)


# PUNTO DE ENTRADA DEL PROGRAMA
# Esta línea verifica si este archivo se está ejecutando directamente
# (no importado desde otro archivo)
if __name__ == '__main__':
    # Si se ejecuta directamente, llamar a la función main()
    main()

"""
EJEMPLOS DE USO DE ESTE ARCHIVO:

1. Ejecutar el servidor de desarrollo:
   python manage.py runserver

2. Crear migraciones (cambios en la base de datos):
   python manage.py makemigrations

3. Aplicar migraciones:
   python manage.py migrate

4. Crear un superusuario:
   python manage.py createsuperuser

5. Abrir la consola interactiva de Django:
   python manage.py shell

6. Ejecutar comandos personalizados (como el que creamos):
   python manage.py load_sample_data

NOTA IMPORTANTE:
- Este archivo se crea automáticamente cuando inicias un proyecto Django
- Normalmente NO necesitas modificar este archivo
- Es el punto de entrada para todos los comandos de Django
"""
