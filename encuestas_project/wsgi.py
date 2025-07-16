"""
CONFIGURACIÓN WSGI PARA EL PROYECTO ENCUESTAS

¿Qué es WSGI?
WSGI (Web Server Gateway Interface) es el estándar que permite que servidores web
como Apache, Nginx o Gunicorn puedan ejecutar aplicaciones Django.

¿Cuándo se usa este archivo?
- Cuando despliegas tu aplicación en producción (Heroku, AWS, etc.)
- Para servidores web reales (no el servidor de desarrollo)
- Con servicios como Gunicorn, uWSGI, etc.

¿Necesitas modificar este archivo?
- Para desarrollo: NO, usa 'python manage.py runserver'
- Para producción: Posiblemente sí, según el servidor que uses

Este archivo expone la aplicación WSGI como una variable llamada 'application'.
"""

# Importar herramientas del sistema operativo
import os

# Importar la función de Django que crea la aplicación WSGI
from django.core.wsgi import get_wsgi_application

# CONFIGURAR EL ARCHIVO DE SETTINGS DE DJANGO
# Le decimos a Django dónde encontrar nuestras configuraciones
# Esto debe apuntar al mismo archivo settings.py que usamos en desarrollo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encuestas_project.settings')

# CREAR LA APLICACIÓN WSGI
# Esta línea crea el objeto que los servidores web usarán para ejecutar Django
# Es como el "punto de entrada" de tu aplicación para servidores de producción
application = get_wsgi_application()

"""
EJEMPLOS DE USO EN PRODUCCIÓN:

1. CON GUNICORN (servidor Python popular):
   gunicorn encuestas_project.wsgi:application

2. CON HEROKU (plataforma en la nube):
   - Heroku detecta automáticamente este archivo
   - Se especifica en el archivo Procfile: web: gunicorn encuestas_project.wsgi

3. CON APACHE Y MOD_WSGI:
   - Se configura en el archivo de virtual host de Apache
   - Apunta a este archivo como punto de entrada

4. CON NGINX Y UWSGI:
   - uWSGI usa este archivo para ejecutar Django
   - Nginx hace de proxy reverso

ESTRUCTURA TÍPICA DE DESPLIEGUE:

Internet → Nginx (servidor web) → Gunicorn (servidor WSGI) → Django (este archivo)

NOTAS IMPORTANTES:

1. NO modifiques este archivo a menos que sepas exactamente qué haces
2. Para desarrollo local, sigue usando 'python manage.py runserver'
3. En producción, asegúrate de que DEBUG=False en settings.py
4. Este archivo se crea automáticamente cuando inicias un proyecto Django

VARIABLES DE ENTORNO IMPORTANTES:

- DJANGO_SETTINGS_MODULE: Apunta al archivo de configuración
- DEBUG: Debe ser False en producción
- SECRET_KEY: Debe ser diferente en producción
- DATABASE_URL: Configuración de base de datos de producción
"""
