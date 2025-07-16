"""
Comando personalizado de Django para cargar datos de ejemplo en la aplicación.

Este comando crea encuestas de muestra para poder probar la aplicación
inmediatamente después de la instalación.

Uso: python manage.py load_sample_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from polls.models import Question, Choice
import datetime


class Command(BaseCommand):
    """
    Comando para cargar datos de ejemplo en la base de datos.
    
    Crea varias encuestas con sus respectivas opciones para poder
    probar la funcionalidad de la aplicación.
    """
    
    help = 'Carga datos de ejemplo para probar la aplicación de encuestas'
    
    def add_arguments(self, parser):
        """
        Agrega argumentos opcionales al comando.
        """
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Elimina todos los datos existentes antes de cargar los nuevos',
        )
        
        parser.add_argument(
            '--user',
            type=str,
            help='Username del usuario que será marcado como creador de las encuestas',
            default='admin'
        )
    
    def handle(self, *args, **options):
        """
        Método principal que ejecuta el comando.
        """
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando carga de datos de ejemplo...')
        )
        
        # Si se especifica --delete, eliminar datos existentes
        if options['delete']:
            self.stdout.write('🗑️  Eliminando datos existentes...')
            Question.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('✅ Datos existentes eliminados')
            )
        
        # Buscar el usuario especificado
        try:
            creator = User.objects.get(username=options['user'])
            self.stdout.write(
                self.style.SUCCESS(f'👤 Usuario encontrado: {creator.username}')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f'⚠️  Usuario "{options["user"]}" no encontrado. Las encuestas se crearán sin autor.')
            )
            creator = None
        
        # Datos de ejemplo para las encuestas
        sample_questions = [
            {
                'question_text': '¿Cuál es tu lenguaje de programación favorito?',
                'choices': [
                    'Python',
                    'JavaScript',
                    'Java',
                    'C++',
                    'Go'
                ]
            },
            {
                'question_text': '¿Qué framework web prefieres para Python?',
                'choices': [
                    'Django',
                    'Flask',
                    'FastAPI',
                    'Pyramid'
                ]
            },
            {
                'question_text': '¿Cuál es tu sistema operativo preferido para desarrollo?',
                'choices': [
                    'Windows',
                    'macOS',
                    'Linux Ubuntu',
                    'Linux Arch',
                    'Linux CentOS'
                ]
            },
            {
                'question_text': '¿Qué base de datos usas más frecuentemente?',
                'choices': [
                    'PostgreSQL',
                    'MySQL',
                    'SQLite',
                    'MongoDB',
                    'Redis'
                ]
            },
            {
                'question_text': '¿Cuál es tu editor de código favorito?',
                'choices': [
                    'VS Code',
                    'PyCharm',
                    'Sublime Text',
                    'Vim',
                    'Atom'
                ]
            },
            {
                'question_text': '¿Qué metodología de desarrollo prefieres?',
                'choices': [
                    'Agile/Scrum',
                    'Kanban',
                    'Waterfall',
                    'DevOps',
                    'Lean'
                ]
            },
            {
                'question_text': '¿Cuál es tu horario de trabajo más productivo?',
                'choices': [
                    'Temprano en la mañana (6-10 AM)',
                    'Media mañana (10 AM - 12 PM)',
                    'Tarde (2-6 PM)',
                    'Noche (8 PM - 12 AM)',
                    'Madrugada (12-6 AM)'
                ]
            }
        ]
        
        # Crear las encuestas
        created_questions = 0
        for i, question_data in enumerate(sample_questions):
            # Calcular fecha de publicación (escalonada en días anteriores)
            pub_date = timezone.now() - datetime.timedelta(days=len(sample_questions) - i - 1)
            
            # Crear la pregunta
            question = Question.objects.create(
                question_text=question_data['question_text'],
                pub_date=pub_date,
                created_by=creator,
                is_active=True
            )
            
            # Crear las opciones para esta pregunta
            for choice_text in question_data['choices']:
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text
                )
            
            created_questions += 1
            self.stdout.write(
                f'✅ Encuesta creada: "{question.question_text}" con {len(question_data["choices"])} opciones'
            )
        
        # Mensaje de finalización
        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS(
                f'🎉 ¡Datos de ejemplo cargados exitosamente!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'📊 Se crearon {created_questions} encuestas con sus respectivas opciones.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'🚀 Ya puedes usar la aplicación en: http://127.0.0.1:8000/'
            )
        )
        self.stdout.write('='*60)
        
        # Instrucciones adicionales
        self.stdout.write('\n📋 Instrucciones:')
        self.stdout.write('   1. Ejecuta: python manage.py runserver')
        self.stdout.write('   2. Ve a: http://127.0.0.1:8000/')
        self.stdout.write('   3. Vota en las encuestas y ve los resultados')
        self.stdout.write('   4. Accede al admin: http://127.0.0.1:8000/admin/')
        self.stdout.write('\n💡 Tip: Puedes ejecutar este comando con --delete para recrear los datos')
