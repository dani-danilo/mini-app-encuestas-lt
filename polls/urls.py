"""
Configuración de URLs para la aplicación polls.

Este archivo define todas las URLs (rutas) de la aplicación de encuestas
y las conecta con sus respectivas vistas.
"""

from django.urls import path
from . import views

# Namespace de la aplicación para evitar conflictos con otras aplicaciones
app_name = 'polls'

urlpatterns = [
    # URL principal: /
    # Muestra la lista de todas las encuestas disponibles
    path('', views.index, name='index'),
    
    # URL alternativa usando vista basada en clase: /list/
    # Misma funcionalidad que index pero usando Class-Based View
    path('list/', views.QuestionListView.as_view(), name='question_list'),
    
    # URL para ver detalles de una encuesta específica: /5/
    # Donde 5 es el ID de la pregunta
    path('<int:question_id>/', views.detail, name='detail'),
    
    # URL para procesar votos: /5/vote/
    # Procesa el voto enviado desde el formulario de la encuesta
    path('<int:question_id>/vote/', views.vote, name='vote'),
    
    # URL para ver resultados de una encuesta: /5/results/
    # Muestra los resultados con gráficos y estadísticas
    path('<int:question_id>/results/', views.results, name='results'),
    
    # API endpoint para obtener resultados en tiempo real: /5/live-results/
    # Devuelve datos JSON para actualizar resultados sin recargar la página
    path('<int:question_id>/live-results/', views.live_results_api, name='live_results_api'),
    
    # Página de información sobre la aplicación: /about/
    path('about/', views.about, name='about'),
]

"""
Explicación de los patrones de URL:

1. '' (string vacío): 
   - Representa la URL raíz de la aplicación
   - Ejemplo: http://127.0.0.1:8000/

2. '<int:question_id>/':
   - <int:...> captura un número entero de la URL
   - question_id es el nombre del parámetro que se pasa a la vista
   - Ejemplo: http://127.0.0.1:8000/5/ → question_id=5

3. 'vote/':
   - String literal que debe aparecer exactamente en la URL
   - Ejemplo: http://127.0.0.1:8000/5/vote/

4. name='...':
   - Nombre interno de la URL para referenciarla en plantillas y vistas
   - Se usa con reverse() o en plantillas como {% url 'polls:index' %}

5. app_name = 'polls':
   - Crea un namespace para evitar conflictos con otras aplicaciones
   - Permite usar 'polls:index' en lugar de solo 'index'

Flujo típico de uso:
1. Usuario visita / → ve lista de encuestas (index)
2. Usuario hace clic en una encuesta → va a /5/ (detail)
3. Usuario vota → POST a /5/vote/ (vote) → redirige a /5/results/ (results)
4. JavaScript llama a /5/live-results/ cada pocos segundos para actualizar datos
"""
