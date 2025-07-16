# Generado por Django 4.2.7 el 2025-07-16 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(help_text='Escribe la pregunta que quieres hacer en la encuesta', max_length=200, verbose_name='Texto de la pregunta')),
                ('pub_date', models.DateTimeField(help_text='Cuándo se publicó esta encuesta', verbose_name='Fecha de publicación')),
                ('is_active', models.BooleanField(default=True, help_text='Las encuestas inactivas no aparecen en la lista principal', verbose_name='¿Está activa?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('created_by', models.ForeignKey(blank=True, help_text='Usuario que creó esta encuesta', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
            ],
            options={
                'verbose_name': 'Pregunta',
                'verbose_name_plural': 'Preguntas',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(help_text='Escribe el texto de esta opción de respuesta', max_length=200, verbose_name='Texto de la opción')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('question', models.ForeignKey(help_text='La pregunta a la que pertenece esta opción', on_delete=django.db.models.deletion.CASCADE, to='polls.question', verbose_name='Pregunta')),
            ],
            options={
                'verbose_name': 'Opción',
                'verbose_name_plural': 'Opciones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter_ip', models.GenericIPAddressField(help_text='Dirección IP desde donde se realizó el voto', verbose_name='IP del votante')),
                ('voted_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora del voto')),
                ('choice', models.ForeignKey(help_text='La opción por la que votó el usuario', on_delete=django.db.models.deletion.CASCADE, to='polls.choice', verbose_name='Opción elegida')),
                ('user', models.ForeignKey(blank=True, help_text='Usuario que realizó el voto (si está autenticado)', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Voto',
                'verbose_name_plural': 'Votos',
                'ordering': ['-voted_at'],
                'indexes': [models.Index(fields=['choice', 'voted_at'], name='polls_vote_choice__73b9d2_idx'), models.Index(fields=['voter_ip', 'choice'], name='polls_vote_voter_i_115b01_idx')],
            },
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(condition=models.Q(('user__isnull', False)), fields=('choice', 'user'), name='unique_user_vote_per_choice'),
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(condition=models.Q(('user__isnull', True)), fields=('choice', 'voter_ip'), name='unique_ip_vote_per_choice'),
        ),
    ]
