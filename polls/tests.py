"""
ARCHIVO DE PRUEBAS PARA LA APLICACIÓN POLLS

Este archivo contiene pruebas automáticas para verificar que nuestra aplicación
funcione correctamente. Las pruebas son como "exámenes" que le hacemos a nuestro código.

¿Por qué son importantes las pruebas?
- Verifican que el código funcione como esperamos
- Detectan errores antes de que los usuarios los encuentren
- Permiten cambiar código con confianza
- Documentan cómo debe comportarse el código

¿Cómo ejecutar las pruebas?
En la terminal: python manage.py test polls
"""

# Importamos las herramientas necesarias para crear pruebas
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

# Importamos nuestros modelos para probarlos
from .models import Question, Choice, Vote


class QuestionModelTest(TestCase):
    """
    PRUEBAS PARA EL MODELO QUESTION
    
    Estas pruebas verifican que el modelo Question funcione correctamente.
    """
    
    def test_was_published_recently_with_future_question(self):
        """
        PRUEBA: was_published_recently() debe devolver False para preguntas futuras
        
        Verificamos que una pregunta con fecha futura no se considere "reciente"
        """
        # Crear una fecha 30 días en el futuro
        time = timezone.now() + datetime.timedelta(days=30)
        
        # Crear una pregunta con esa fecha futura
        future_question = Question(pub_date=time)
        
        # Verificar que NO se considere reciente
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        """
        PRUEBA: was_published_recently() debe devolver False para preguntas muy antiguas
        """
        # Crear una fecha de hace más de 1 día
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        
        # Crear una pregunta antigua
        old_question = Question(pub_date=time)
        
        # Verificar que NO se considere reciente
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        """
        PRUEBA: was_published_recently() debe devolver True para preguntas recientes
        """
        # Crear una fecha de hace 23 horas (menos de 1 día)
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        
        # Crear una pregunta reciente
        recent_question = Question(pub_date=time)
        
        # Verificar que SÍ se considere reciente
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTest(TestCase):
    """
    PRUEBAS PARA LA VISTA INDEX (página principal)
    
    Estas pruebas verifican que la página principal funcione correctamente.
    """
    
    def test_no_questions(self):
        """
        PRUEBA: Si no hay preguntas, debe mostrar un mensaje apropiado
        """
        # Hacer una petición GET a la página principal
        response = self.client.get(reverse('polls:index'))
        
        # Verificar que la respuesta sea exitosa (código 200)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que el mensaje "No hay encuestas" aparezca
        self.assertContains(response, "No hay encuestas disponibles")
        
        # Verificar que la lista de preguntas esté vacía
        self.assertQuerysetEqual(response.context['questions'], [])
    
    def test_past_question(self):
        """
        PRUEBA: Las preguntas del pasado deben aparecer en la página principal
        """
        # Crear una pregunta del pasado
        question = create_question(question_text="Pregunta del pasado.", days=-30)
        
        # Hacer petición a la página principal
        response = self.client.get(reverse('polls:index'))
        
        # Verificar que la pregunta aparezca
        self.assertQuerysetEqual(
            response.context['questions'],
            [question],
        )
    
    def test_future_question(self):
        """
        PRUEBA: Las preguntas futuras NO deben aparecer en la página principal
        """
        # Crear una pregunta futura
        create_question(question_text="Pregunta futura.", days=30)
        
        # Hacer petición a la página principal
        response = self.client.get(reverse('polls:index'))
        
        # Verificar que no aparezcan preguntas
        self.assertContains(response, "No hay encuestas disponibles")
        self.assertQuerysetEqual(response.context['questions'], [])


class QuestionDetailViewTest(TestCase):
    """
    PRUEBAS PARA LA VISTA DETAIL (página de votación)
    """
    
    def test_future_question(self):
        """
        PRUEBA: No se debe poder acceder a preguntas futuras
        """
        # Crear una pregunta futura
        future_question = create_question(question_text="Pregunta futura.", days=5)
        
        # Intentar acceder a su página de detalle
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        
        # Debería devolver error 404 (no encontrado)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
        PRUEBA: Se debe poder acceder a preguntas del pasado
        """
        # Crear una pregunta del pasado
        past_question = create_question(question_text="Pregunta del pasado.", days=-5)
        
        # Acceder a su página de detalle
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        
        # Debería funcionar correctamente
        self.assertContains(response, past_question.question_text)


class VoteTest(TestCase):
    """
    PRUEBAS PARA EL SISTEMA DE VOTACIÓN
    """
    
    def setUp(self):
        """
        CONFIGURACIÓN INICIAL PARA LAS PRUEBAS
        
        Este método se ejecuta antes de cada prueba individual.
        Aquí creamos datos básicos que necesitaremos en las pruebas.
        """
        # Crear una pregunta de prueba
        self.question = create_question("¿Pregunta de prueba?", days=-1)
        
        # Crear algunas opciones para la pregunta
        self.choice1 = Choice.objects.create(
            question=self.question,
            choice_text="Opción 1"
        )
        self.choice2 = Choice.objects.create(
            question=self.question,
            choice_text="Opción 2"
        )
    
    def test_vote_increases_count(self):
        """
        PRUEBA: Votar debe aumentar el contador de votos
        """
        # Contar votos iniciales
        initial_votes = self.choice1.vote_count()
        
        # Simular un voto
        Vote.objects.create(
            choice=self.choice1,
            voter_ip="192.168.1.1"
        )
        
        # Verificar que el contador aumentó
        self.assertEqual(self.choice1.vote_count(), initial_votes + 1)
    
    def test_vote_via_post_request(self):
        """
        PRUEBA: Votar a través de una petición POST debe funcionar
        """
        # Hacer una petición POST para votar
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.post(url, {'choice': self.choice1.id})
        
        # Verificar que redirige a la página de resultados
        self.assertRedirects(
            response,
            reverse('polls:results', args=(self.question.id,))
        )
        
        # Verificar que el voto se registró
        self.assertEqual(self.choice1.vote_count(), 1)


# FUNCIONES AUXILIARES PARA LAS PRUEBAS

def create_question(question_text, days):
    """
    FUNCIÓN AUXILIAR: Crear una pregunta para pruebas
    
    Args:
        question_text (str): El texto de la pregunta
        days (int): Días desde hoy (negativo = pasado, positivo = futuro)
    
    Returns:
        Question: La pregunta creada
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


"""
CÓMO EJECUTAR ESTAS PRUEBAS:

1. Ejecutar todas las pruebas:
   python manage.py test

2. Ejecutar solo las pruebas de polls:
   python manage.py test polls

3. Ejecutar una clase específica de pruebas:
   python manage.py test polls.tests.QuestionModelTest

4. Ejecutar una prueba específica:
   python manage.py test polls.tests.QuestionModelTest.test_was_published_recently_with_future_question

INTERPRETANDO LOS RESULTADOS:

- . (punto) = Prueba pasó exitosamente
- F = Prueba falló (FAIL)
- E = Error en la prueba (ERROR)

EJEMPLO DE SALIDA:
..........
----------------------------------------------------------------------
Ran 10 tests in 0.123s

OK

CONSEJOS PARA PRINCIPIANTES:

1. Escribe pruebas ANTES de escribir código (TDD - Test Driven Development)
2. Una prueba debe verificar UNA cosa específica
3. Usa nombres descriptivos para las pruebas
4. Las pruebas deben ser independientes entre sí
5. Ejecuta las pruebas frecuentemente mientras desarrollas
"""
