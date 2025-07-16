"""
Vistas de la aplicación de encuestas.

Las vistas contienen la lógica que maneja las peticiones HTTP y devuelve respuestas.
Cada vista representa una página o funcionalidad específica de la aplicación.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count, F
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import Question, Choice, Vote


def get_client_ip(request):
    """
    Obtiene la dirección IP del cliente que hace la petición.
    
    Args:
        request: Objeto HttpRequest de Django
        
    Returns:
        str: Dirección IP del cliente
    """
    # Primero verifica si viene a través de un proxy
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        # IP directa
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    """
    Vista principal que muestra la lista de encuestas disponibles.
    
    Esta vista:
    1. Obtiene todas las encuestas activas
    2. Las ordena por fecha de publicación (más recientes primero)
    3. Implementa paginación para manejar muchas encuestas
    4. Renderiza la plantilla con la lista de encuestas
    
    Args:
        request: Objeto HttpRequest de Django
        
    Returns:
        HttpResponse: Página HTML con la lista de encuestas
    """
    
    # Obtener todas las preguntas activas, ordenadas por fecha de publicación
    # select_related('created_by') optimiza las consultas a la base de datos
    # prefetch_related('choice_set') precarga las opciones relacionadas
    question_list = Question.objects.filter(
        is_active=True,
        pub_date__lte=timezone.now()  # Solo encuestas ya publicadas
    ).select_related('created_by').prefetch_related('choice_set').order_by('-pub_date')
    
    # Implementar paginación (5 encuestas por página)
    paginator = Paginator(question_list, 5)
    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)
    
    # Agregar información adicional a cada pregunta
    for question in questions:
        question.total_votes_count = question.total_votes()
        question.choices_count = question.choice_set.count()
    
    # Contexto que se pasa a la plantilla
    context = {
        'questions': questions,
        'title': 'Encuestas Disponibles',
        'total_questions': question_list.count(),
    }
    
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """
    Vista que muestra los detalles de una encuesta específica para votar.
    
    Esta vista:
    1. Obtiene la pregunta por su ID
    2. Verifica si el usuario ya votó
    3. Muestra las opciones disponibles para votar
    
    Args:
        request: Objeto HttpRequest de Django
        question_id: ID de la pregunta a mostrar
        
    Returns:
        HttpResponse: Página HTML con los detalles de la encuesta
    """
    
    # Obtener la pregunta o mostrar error 404 si no existe
    # select_related y prefetch_related optimizan las consultas
    question = get_object_or_404(
        Question.objects.select_related('created_by').prefetch_related('choice_set'),
        pk=question_id,
        is_active=True  # Solo mostrar encuestas activas
    )
    
    # Verificar si el usuario ya votó en esta encuesta
    user_has_voted = False
    user_vote_choice = None
    client_ip = get_client_ip(request)
    
    # Verificar si ya existe un voto desde esta IP (independientemente del usuario)
    existing_vote = Vote.objects.filter(
        choice__question=question,
        voter_ip=client_ip
    ).first()
    
    # Si es usuario autenticado, también verificar por usuario
    if request.user.is_authenticated and not existing_vote:
        existing_vote = Vote.objects.filter(
            choice__question=question,
            user=request.user
        ).first()
    
    if existing_vote:
        user_has_voted = True
        user_vote_choice = existing_vote.choice
    
    # Contexto para la plantilla
    context = {
        'question': question,
        'user_has_voted': user_has_voted,
        'user_vote_choice': user_vote_choice,
        'total_votes': question.total_votes(),
    }
    
    return render(request, 'polls/detail_simple.html', context)


@require_POST
def vote(request, question_id):
    """
    Vista que procesa el voto de un usuario.
    
    Esta vista:
    1. Valida que se haya seleccionado una opción
    2. Verifica que el usuario no haya votado antes
    3. Registra el voto en la base de datos
    4. Redirige a la página de resultados
    
    Args:
        request: Objeto HttpRequest de Django
        question_id: ID de la pregunta en la que se vota
        
    Returns:
        HttpResponseRedirect: Redirección a la página de resultados o error
    """
    
    # Obtener la pregunta
    question = get_object_or_404(Question, pk=question_id, is_active=True)
    
    # Obtener la opción seleccionada del formulario
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # Si no se seleccionó una opción válida, mostrar error
        messages.error(request, 'Por favor selecciona una opción válida.')
        return render(request, 'polls/detail_simple.html', {
            'question': question,
            'error_message': "No seleccionaste una opción.",
        })
    
    # Verificar si el usuario ya votó
    client_ip = get_client_ip(request)
    
    # Verificar si ya existe un voto desde esta IP (independientemente del usuario)
    existing_vote = Vote.objects.filter(
        choice__question=question,
        voter_ip=client_ip
    ).first()
    
    # Si es usuario autenticado, también verificar por usuario
    if request.user.is_authenticated and not existing_vote:
        existing_vote = Vote.objects.filter(
            choice__question=question,
            user=request.user
        ).first()
    
    if existing_vote:
        # Si ya votó, mostrar mensaje y redirigir a resultados
        messages.warning(request, 'Ya has votado en esta encuesta.')
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
    # Crear el nuevo voto
    try:
        new_vote = Vote(
            choice=selected_choice,
            voter_ip=client_ip,
            user=request.user if request.user.is_authenticated else None
        )
        new_vote.save()
        
        # Mensaje de éxito
        messages.success(request, f'¡Gracias por votar! Tu voto por "{selected_choice.choice_text}" ha sido registrado.')
        
        # Redirigir a la página de resultados
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        
    except Exception as e:
        # Si hay algún error al guardar el voto
        messages.error(request, 'Hubo un error al procesar tu voto. Por favor inténtalo de nuevo.')
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Hubo un error al procesar tu voto.",
        })


def results(request, question_id):
    """
    Vista que muestra los resultados de una encuesta.
    
    Esta vista:
    1. Obtiene la pregunta y sus opciones
    2. Calcula los votos y porcentajes para cada opción
    3. Muestra los resultados en tiempo real
    
    Args:
        request: Objeto HttpRequest de Django
        question_id: ID de la pregunta de la que mostrar resultados
        
    Returns:
        HttpResponse: Página HTML con los resultados
    """
    
    # Obtener la pregunta con todas sus opciones y votos
    question = get_object_or_404(
        Question.objects.prefetch_related('choice_set__vote_set'),
        pk=question_id
    )
    
    # Calcular estadísticas para cada opción
    choices_with_stats = []
    total_votes = question.total_votes()
    
    for choice in question.choice_set.all():
        vote_count = choice.vote_count()
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        
        choices_with_stats.append({
            'choice': choice,
            'votes': vote_count,
            'percentage': round(percentage, 1),
        })
    
    # Verificar si el usuario actual votó
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(
                choice__question=question,
                user=request.user
            ).choice
        except Vote.DoesNotExist:
            pass
    else:
        client_ip = get_client_ip(request)
        try:
            user_vote = Vote.objects.get(
                choice__question=question,
                voter_ip=client_ip,
                user__isnull=True
            ).choice
        except Vote.DoesNotExist:
            pass
    
    # Contexto para la plantilla
    context = {
        'question': question,
        'choices_with_stats': choices_with_stats,
        'total_votes': total_votes,
        'user_vote': user_vote,
    }
    
    return render(request, 'polls/results_simple.html', context)


def live_results_api(request, question_id):
    """
    API endpoint que devuelve los resultados en tiempo real en formato JSON.
    
    Esta vista es llamada por JavaScript para actualizar los resultados
    sin recargar la página completa.
    
    Args:
        request: Objeto HttpRequest de Django
        question_id: ID de la pregunta
        
    Returns:
        JsonResponse: Resultados en formato JSON
    """
    
    try:
        question = get_object_or_404(Question, pk=question_id)
        
        # Obtener resultados actualizados
        results = question.get_results()
        total_votes = question.total_votes()
        
        # Preparar la respuesta JSON
        response_data = {
            'success': True,
            'total_votes': total_votes,
            'results': results,
            'question_text': question.question_text,
            'timestamp': timezone.now().isoformat(),
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


class QuestionListView(generic.ListView):
    """
    Vista basada en clase para mostrar la lista de preguntas.
    
    Esta es una alternativa a la vista function-based 'index'.
    Las vistas basadas en clase proporcionan más funcionalidad automática.
    """
    
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'questions'
    paginate_by = 5
    
    def get_queryset(self):
        """
        Personaliza la consulta para obtener solo encuestas activas y publicadas.
        """
        return Question.objects.filter(
            is_active=True,
            pub_date__lte=timezone.now()
        ).select_related('created_by').prefetch_related('choice_set').order_by('-pub_date')
    
    def get_context_data(self, **kwargs):
        """
        Agrega contexto adicional a la plantilla.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Encuestas Disponibles'
        context['total_questions'] = self.get_queryset().count()
        
        # Agregar estadísticas a cada pregunta
        for question in context['questions']:
            question.total_votes_count = question.total_votes()
            question.choices_count = question.choice_set.count()
        
        return context


def about(request):
    """
    Vista simple que muestra información sobre la aplicación.
    
    Args:
        request: Objeto HttpRequest de Django
        
    Returns:
        HttpResponse: Página HTML con información de la aplicación
    """
    
    context = {
        'title': 'Acerca de la Aplicación',
        'description': 'Sistema de encuestas en tiempo real desarrollado con Django',
    }
    
    return render(request, 'polls/about.html', context)
