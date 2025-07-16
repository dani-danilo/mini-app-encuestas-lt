"""
Configuración de URLs principal para el proyecto encuestas_project.

Este archivo define las URLs principales del proyecto y conecta las aplicaciones.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración de Django: /admin/
    # Aquí puedes gestionar encuestas, usuarios y ver estadísticas
    path('admin/', admin.site.urls),
    
    # URLs de la aplicación de encuestas: /
    # Incluye todas las URLs definidas en polls/urls.py
    path('', include('polls.urls')),
    
    # URLs alternativas para la aplicación: /polls/
    # Permite acceder a las encuestas también desde /polls/
    # Comentamos esta línea para evitar namespace duplicado
    # path('polls/', include('polls.urls')),
]

# En modo de desarrollo, servir archivos estáticos y media
# Esto es necesario para que se vean las imágenes, CSS y JS
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
Explicación de la configuración:

1. path('admin/', admin.site.urls):
   - Conecta el panel de administración de Django
   - Accesible en: http://127.0.0.1:8000/admin/

2. path('', include('polls.urls')):
   - Incluye todas las URLs de la aplicación polls
   - La cadena vacía '' significa que las URLs de polls estarán en la raíz
   - Ejemplo: http://127.0.0.1:8000/ → polls.views.index

3. path('polls/', include('polls.urls')):
   - Alternativa que permite acceder a las encuestas desde /polls/
   - Ejemplo: http://127.0.0.1:8000/polls/ → misma vista que /

4. include():
   - Función que permite incluir URLs de otras aplicaciones
   - Mantiene las aplicaciones modulares y organizadas

5. static():
   - Solo en desarrollo (DEBUG=True)
   - Permite servir archivos CSS, JavaScript e imágenes
   - En producción se usa un servidor web como Nginx

Estructura final de URLs:
- / → Lista de encuestas
- /5/ → Detalle de encuesta #5
- /5/vote/ → Votar en encuesta #5
- /5/results/ → Resultados de encuesta #5
- /admin/ → Panel de administración
- /polls/ → Alternativa a la raíz
"""
