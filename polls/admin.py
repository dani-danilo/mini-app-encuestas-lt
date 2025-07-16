"""
Configuración del panel de administración para la aplicación de encuestas.

El admin de Django es una interfaz web automática para gestionar los datos de tu aplicación.
Aquí configuramos cómo se ven y comportan nuestros modelos en el admin.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Question, Choice, Vote


class ChoiceInline(admin.TabularInline):
    """
    Configuración para editar opciones directamente desde la página de la pregunta.
    
    TabularInline muestra las opciones en forma de tabla dentro de la página de edición
    de la pregunta, permitiendo agregar/editar opciones sin salir de la pregunta.
    """
    model = Choice  # El modelo que se va a editar inline
    extra = 3       # Número de campos vacíos adicionales que se muestran por defecto
    fields = ['choice_text']  # Campos que se pueden editar
    

class VoteInline(admin.TabularInline):
    """
    Configuración para ver votos directamente desde la página de la opción.
    """
    model = Vote
    extra = 0  # No mostrar campos vacíos adicionales
    readonly_fields = ['user', 'voter_ip', 'voted_at']  # Campos de solo lectura
    can_delete = False  # No permitir eliminar votos desde aquí
    
    def has_add_permission(self, request, obj=None):
        """No permitir agregar votos desde el admin (solo desde la web)."""
        return False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Configuración personalizada para el modelo Question en el admin.
    
    Esta clase define cómo se ve y comporta Question en el panel de administración.
    """
    
    # Campos que se muestran en la lista principal de preguntas
    list_display = [
        'question_text',           # Texto de la pregunta
        'pub_date',               # Fecha de publicación
        'is_active',              # Si está activa
        'created_by',             # Quién la creó
        'total_votes_display',    # Número total de votos
        'was_published_recently', # Si fue publicada recientemente
    ]
    
    # Campos por los que se puede filtrar en la barra lateral
    list_filter = [
        'pub_date',     # Filtrar por fecha de publicación
        'is_active',    # Filtrar por estado activo/inactivo
        'created_by',   # Filtrar por creador
    ]
    
    # Campo de búsqueda (busca en el texto de la pregunta)
    search_fields = ['question_text']
    
    # Campos que se pueden editar directamente desde la lista (sin entrar al detalle)
    list_editable = ['is_active']
    
    # Organización de campos en la página de edición
    fieldsets = [
        (
            'Información Básica',  # Título del grupo
            {
                'fields': ['question_text', 'is_active'],
                'description': 'Información principal de la encuesta'
            }
        ),
        (
            'Información de Publicación',
            {
                'fields': ['pub_date', 'created_by'],
                'description': 'Cuándo y quién publicó esta encuesta'
            }
        ),
    ]
    
    # Incluir las opciones como inline (editar opciones desde la página de la pregunta)
    inlines = [ChoiceInline]
    
    # Campos de solo lectura (no se pueden editar)
    readonly_fields = ['created_at', 'updated_at']
    
    # Ordenamiento por defecto en la lista
    ordering = ['-pub_date']
    
    # Número de elementos por página
    list_per_page = 20
    
    # Mostrar total de elementos en la parte inferior
    list_max_show_all = 200
    
    def total_votes_display(self, obj):
        """
        Método personalizado para mostrar el total de votos en la lista.
        
        Args:
            obj (Question): La instancia de Question
            
        Returns:
            str: HTML formateado con el número de votos
        """
        total = obj.total_votes()
        if total == 0:
            return format_html('<span style="color: #999;">0 votos</span>')
        elif total < 10:
            return format_html('<span style="color: #ffc107;">{} votos</span>', total)
        else:
            return format_html('<span style="color: #28a745;"><strong>{} votos</strong></span>', total)
    
    total_votes_display.short_description = 'Total de Votos'
    total_votes_display.admin_order_field = 'vote_count'  # Permite ordenar por este campo
    
    def get_queryset(self, request):
        """
        Personaliza la consulta para optimizar el rendimiento.
        
        Esto evita consultas adicionales a la base de datos al mostrar la lista.
        """
        qs = super().get_queryset(request)
        # Precargar las relaciones relacionadas para evitar consultas N+1
        return qs.select_related('created_by').prefetch_related('choice_set__vote_set')
    
    def save_model(self, request, obj, form, change):
        """
        Personaliza el guardado del modelo.
        
        Si no se especifica un creador, asigna el usuario actual.
        """
        if not change:  # Si es un objeto nuevo (no una edición)
            if not obj.created_by:
                obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """
    Configuración personalizada para el modelo Choice en el admin.
    """
    
    # Campos que se muestran en la lista
    list_display = [
        'choice_text',
        'question',
        'vote_count_display',
        'vote_percentage_display',
        'created_at',
    ]
    
    # Campos por los que se puede filtrar
    list_filter = [
        'question',
        'created_at',
    ]
    
    # Campo de búsqueda
    search_fields = ['choice_text', 'question__question_text']
    
    # Campos de solo lectura
    readonly_fields = ['created_at', 'vote_count_display', 'vote_percentage_display']
    
    # Incluir votos como inline
    inlines = [VoteInline]
    
    # Ordenamiento por defecto
    ordering = ['question', 'id']
    
    def vote_count_display(self, obj):
        """Muestra el número de votos para esta opción."""
        count = obj.vote_count()
        if count == 0:
            return format_html('<span style="color: #999;">0</span>')
        else:
            return format_html('<span style="color: #007cba;"><strong>{}</strong></span>', count)
    
    vote_count_display.short_description = 'Votos'
    
    def vote_percentage_display(self, obj):
        """Muestra el porcentaje de votos para esta opción."""
        percentage = obj.vote_percentage()
        if percentage == 0:
            return format_html('<span style="color: #999;">0%</span>')
        else:
            color = '#28a745' if percentage > 50 else '#ffc107' if percentage > 25 else '#dc3545'
            return format_html('<span style="color: {};"><strong>{:.1f}%</strong></span>', color, percentage)
    
    vote_percentage_display.short_description = 'Porcentaje'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """
    Configuración personalizada para el modelo Vote en el admin.
    """
    
    # Campos que se muestran en la lista
    list_display = [
        'get_question_text',
        'choice',
        'get_voter_info',
        'voted_at',
    ]
    
    # Campos por los que se puede filtrar
    list_filter = [
        'voted_at',
        'choice__question',
        'user',
    ]
    
    # Campo de búsqueda
    search_fields = [
        'choice__choice_text', 
        'choice__question__question_text',
        'user__username',
        'voter_ip'
    ]
    
    # Todos los campos son de solo lectura (no se pueden editar votos)
    readonly_fields = ['choice', 'user', 'voter_ip', 'voted_at']
    
    # Ordenamiento por defecto (votos más recientes primero)
    ordering = ['-voted_at']
    
    # Habilitar acciones de eliminación
    actions = ['delete_selected']
    
    # No permitir agregar votos desde el admin
    def has_add_permission(self, request):
        return False
    
    # No permitir editar votos
    def has_change_permission(self, request, obj=None):
        return False
    
    # Permitir eliminar votos (para testing y correcciones)
    def has_delete_permission(self, request, obj=None):
        return True
    
    def get_question_text(self, obj):
        """Obtiene el texto de la pregunta para mostrar en la lista."""
        question_text = obj.choice.question.question_text
        if len(question_text) > 50:
            return question_text[:50] + '...'
        return question_text
    
    get_question_text.short_description = 'Pregunta'
    
    def get_voter_info(self, obj):
        """Muestra información del votante."""
        if obj.user:
            return format_html(
                '<span style="color: #28a745;"><strong>{}</strong></span>', 
                obj.user.username
            )
        else:
            return format_html(
                '<span style="color: #6c757d;">IP: {}</span>', 
                obj.voter_ip
            )
    
    get_voter_info.short_description = 'Votante'


# Personalización del sitio de administración
admin.site.site_header = "Administración de Encuestas"
admin.site.site_title = "Admin Encuestas"
admin.site.index_title = "Panel de Control de Encuestas"
