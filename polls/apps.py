"""
CONFIGURACIÓN DE LA APLICACIÓN POLLS

Este archivo define cómo se configura nuestra aplicación 'polls' dentro del proyecto Django.
Es como el "acta de nacimiento" de nuestra aplicación.

¿Qué hace este archivo?
- Le dice a Django cómo se llama nuestra aplicación
- Define configuraciones específicas para esta aplicación
- Se ejecuta automáticamente cuando Django inicia
"""

# Importamos la clase base para configurar aplicaciones Django
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """
    CLASE DE CONFIGURACIÓN PARA LA APLICACIÓN POLLS
    
    Esta clase hereda de AppConfig y define cómo Django debe tratar
    a nuestra aplicación de encuestas.
    """
    
    # CONFIGURACIÓN DEL TIPO DE CAMPO ID AUTOMÁTICO
    # Esto le dice a Django qué tipo de campo usar para las claves primarias
    # BigAutoField permite IDs más grandes que el AutoField normal
    # Es útil si esperas tener muchos registros en tu base de datos
    default_auto_field = 'django.db.models.BigAutoField'
    
    # NOMBRE DE LA APLICACIÓN
    # Este debe coincidir exactamente con el nombre de la carpeta de tu aplicación
    # Django usa este nombre para identificar la aplicación en todo el proyecto
    name = 'polls'
    
    # NOMBRE LEGIBLE DE LA APLICACIÓN (opcional)
    # Puedes agregar un nombre más amigable que aparezca en el admin
    verbose_name = 'Sistema de Encuestas'
    
    def ready(self):
        """
        MÉTODO QUE SE EJECUTA CUANDO LA APLICACIÓN ESTÁ LISTA
        
        Este método se llama automáticamente cuando Django termina de
        configurar la aplicación. Es útil para:
        - Importar señales (signals)
        - Registrar tareas programadas
        - Inicializar configuraciones especiales
        
        Por ahora no necesitamos nada especial, pero es bueno saber que existe.
        """
        # Aquí podrías importar señales u otras configuraciones
        # Por ejemplo: from . import signals
        pass

"""
NOTAS IMPORTANTES PARA PRINCIPIANTES:

1. ¿Por qué existe este archivo?
   - Django necesita saber cómo configurar cada aplicación
   - Permite personalizar el comportamiento específico de la aplicación
   - Se ejecuta automáticamente al iniciar Django

2. ¿Cuándo se modifica?
   - Normalmente no necesitas modificar este archivo
   - Se puede personalizar para configuraciones avanzadas
   - El archivo se crea automáticamente con 'python manage.py startapp'

3. ¿Qué pasa si lo borras?
   - Django usará configuraciones por defecto
   - Pero es mejor mantenerlo para futuras personalizaciones

4. ¿Dónde se usa esta configuración?
   - En settings.py, cuando agregamos 'polls' a INSTALLED_APPS
   - Django busca automáticamente la clase de configuración
"""
