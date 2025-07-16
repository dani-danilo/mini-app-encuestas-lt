"""
Modelos de la aplicación de encuestas.

Los modelos definen la estructura de la base de datos y cómo se relacionan los datos.
Cada clase representa una tabla en la base de datos.
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Question(models.Model):
    """
    Modelo que representa una pregunta de encuesta.
    
    Campos:
    - question_text: El texto de la pregunta
    - pub_date: Fecha y hora de publicación
    - created_by: Usuario que creó la pregunta (opcional)
    - is_active: Si la encuesta está activa o no
    """
    
    # Campo de texto para la pregunta (máximo 200 caracteres)
    question_text = models.CharField(
        max_length=200, 
        verbose_name="Texto de la pregunta",
        help_text="Escribe la pregunta que quieres hacer en la encuesta"
    )
    
    # Campo de fecha y hora de publicación
    pub_date = models.DateTimeField(
        verbose_name="Fecha de publicación",
        help_text="Cuándo se publicó esta encuesta"
    )
    
    # Relación con el modelo User (quién creó la pregunta)
    # null=True permite que sea opcional
    # blank=True permite que el campo esté vacío en formularios
    # on_delete=models.SET_NULL significa que si se elimina el usuario, la pregunta se mantiene
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Creado por",
        help_text="Usuario que creó esta encuesta"
    )
    
    # Campo booleano para indicar si la encuesta está activa
    is_active = models.BooleanField(
        default=True,
        verbose_name="¿Está activa?",
        help_text="Las encuestas inactivas no aparecen en la lista principal"
    )
    
    # Campos automáticos de auditoría
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        """
        Metadatos del modelo Question.
        """
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ['-pub_date']  # Ordenar por fecha de publicación (más recientes primero)

    def __str__(self):
        """
        Representación en string del objeto.
        Esto es lo que se muestra en el admin y en otras partes.
        """
        return self.question_text

    def was_published_recently(self):
        """
        Método personalizado que verifica si la pregunta fue publicada recientemente.
        
        Returns:
            bool: True si fue publicada en el último día, False en caso contrario
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def total_votes(self):
        """
        Calcula el total de votos para esta pregunta.
        
        Returns:
            int: Número total de votos
        """
        return Vote.objects.filter(choice__question=self).count()

    def get_results(self):
        """
        Obtiene los resultados de la encuesta en formato diccionario.
        
        Returns:
            dict: Diccionario con los resultados por opción
        """
        results = {}
        total_votes = self.total_votes()
        
        for choice in self.choice_set.all():
            vote_count = choice.vote_count()
            percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            results[choice.id] = {
                'choice_text': choice.choice_text,
                'votes': vote_count,
                'percentage': round(percentage, 2)
            }
        
        return results


class Choice(models.Model):
    """
    Modelo que representa una opción de respuesta para una pregunta.
    
    Campos:
    - question: Relación con la pregunta a la que pertenece
    - choice_text: Texto de la opción
    """
    
    # Relación con Question (una pregunta puede tener muchas opciones)
    # on_delete=models.CASCADE significa que si se elimina la pregunta, 
    # también se eliminan todas sus opciones
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE,
        verbose_name="Pregunta",
        help_text="La pregunta a la que pertenece esta opción"
    )
    
    # Texto de la opción de respuesta
    choice_text = models.CharField(
        max_length=200,
        verbose_name="Texto de la opción",
        help_text="Escribe el texto de esta opción de respuesta"
    )
    
    # Campos automáticos de auditoría
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    class Meta:
        """
        Metadatos del modelo Choice.
        """
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"
        ordering = ['id']  # Ordenar por ID (orden de creación)

    def __str__(self):
        """
        Representación en string del objeto.
        """
        return f"{self.question.question_text[:50]}... - {self.choice_text}"

    def vote_count(self):
        """
        Cuenta el número de votos para esta opción.
        
        Returns:
            int: Número de votos para esta opción
        """
        return self.vote_set.count()

    def vote_percentage(self):
        """
        Calcula el porcentaje de votos para esta opción.
        
        Returns:
            float: Porcentaje de votos (0-100)
        """
        total_votes = self.question.total_votes()
        if total_votes == 0:
            return 0
        return (self.vote_count() / total_votes) * 100


class Vote(models.Model):
    """
    Modelo que representa un voto individual.
    
    Este modelo almacena cada voto por separado, lo que nos permite:
    - Rastrear quién votó (si está autenticado)
    - Prevenir votos duplicados
    - Obtener estadísticas detalladas
    - Auditar los votos
    
    Campos:
    - choice: La opción por la que se votó
    - voter_ip: IP del votante (para prevenir votos duplicados de IPs anónimas)
    - user: Usuario que votó (si está autenticado)
    - voted_at: Cuándo se realizó el voto
    """
    
    # Relación con la opción elegida
    choice = models.ForeignKey(
        Choice, 
        on_delete=models.CASCADE,
        verbose_name="Opción elegida",
        help_text="La opción por la que votó el usuario"
    )
    
    # IP del votante (para usuarios anónimos)
    voter_ip = models.GenericIPAddressField(
        verbose_name="IP del votante",
        help_text="Dirección IP desde donde se realizó el voto"
    )
    
    # Usuario que votó (opcional, para usuarios autenticados)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Usuario",
        help_text="Usuario que realizó el voto (si está autenticado)"
    )
    
    # Fecha y hora del voto
    voted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y hora del voto"
    )

    class Meta:
        """
        Metadatos del modelo Vote.
        """
        verbose_name = "Voto"
        verbose_name_plural = "Votos"
        ordering = ['-voted_at']  # Ordenar por fecha de voto (más recientes primero)
        
        # Índices para mejorar el rendimiento de las consultas
        indexes = [
            models.Index(fields=['choice', 'voted_at']),
            models.Index(fields=['voter_ip', 'choice']),
        ]
        
        # Restricciones simplificadas para evitar votos duplicados
        # Nota: Para restricciones más complejas que involucren relaciones,
        # es mejor manejarlas en la lógica de las vistas
        constraints = [
            # Un usuario autenticado no puede votar dos veces por la misma opción
            models.UniqueConstraint(
                fields=['choice', 'user'],
                condition=models.Q(user__isnull=False),
                name='unique_user_vote_per_choice'
            ),
            # Una IP no puede votar dos veces por la misma opción (para usuarios anónimos)
            models.UniqueConstraint(
                fields=['choice', 'voter_ip'],
                condition=models.Q(user__isnull=True),
                name='unique_ip_vote_per_choice'
            ),
        ]

    def __str__(self):
        """
        Representación en string del objeto.
        """
        voter = self.user.username if self.user else f"IP: {self.voter_ip}"
        return f"{voter} votó por '{self.choice.choice_text}' en '{self.choice.question.question_text[:30]}...'"

    def get_question(self):
        """
        Obtiene la pregunta asociada con este voto.
        
        Returns:
            Question: La pregunta a la que pertenece la opción votada
        """
        return self.choice.question
