"""
Configuración ASGI para encuestas_project.

ASGI (Asynchronous Server Gateway Interface) es el estándar para aplicaciones Python
asíncronas. Este archivo expone la aplicación ASGI como una variable llamada ``application``.
"""

import os
from django.core.asgi import get_asgi_application

# Configurar la variable de entorno para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encuestas_project.settings')

# Obtener la aplicación ASGI de Django
application = get_asgi_application()
