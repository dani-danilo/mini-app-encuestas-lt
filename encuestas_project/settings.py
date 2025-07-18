"""
Django settings for encuestas_project project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Construir rutas dentro del proyecto así: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Configuraciones de desarrollo rápido - no adecuadas para producción
# Ver https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: mantén la clave secreta usada en producción en secreto!
SECRET_KEY = 'django-insecure-^ewgyte-ox^71j%az&^syu)^v_x4l4mb*h0zvxf@%9rbrhv@gw'

# ADVERTENCIA DE SEGURIDAD: no ejecutes con debug activado en producción!
DEBUG = True

ALLOWED_HOSTS = []


# Definición de aplicaciones
# Esta sección define todas las aplicaciones que usa nuestro proyecto Django

INSTALLED_APPS = [
    # Aplicaciones predeterminadas de Django
    'django.contrib.admin',        # Panel de administración
    'django.contrib.auth',         # Sistema de autenticación
    'django.contrib.contenttypes', # Sistema de tipos de contenido
    'django.contrib.sessions',     # Manejo de sesiones
    'django.contrib.messages',     # Sistema de mensajes
    'django.contrib.staticfiles',  # Manejo de archivos estáticos (CSS, JS, imágenes)
    
    # Nuestra aplicación personalizada
    'polls',                       # La aplicación de encuestas que creamos
]

MIDDLEWARE = [
    # Middleware para seguridad básica
    'django.middleware.security.SecurityMiddleware',
    
    # Middleware para sesiones de usuario
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # Middleware común para funcionalidades básicas
    'django.middleware.common.CommonMiddleware',
    
    # Middleware para protección CSRF (Cross-Site Request Forgery)
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Middleware para autenticación de usuarios
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # Middleware para sistema de mensajes
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Middleware para protección contra clickjacking
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'encuestas_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'encuestas_project.wsgi.application'


# Base de datos
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validación de contraseñas
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization (Configuración de idioma y zona horaria)
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# Configuramos el idioma a español
LANGUAGE_CODE = 'es-es'

# Configuramos la zona horaria (puedes cambiarla según tu ubicación)
TIME_ZONE = 'America/Mexico_City'

# Habilita la internacionalización (soporte para múltiples idiomas)
USE_I18N = True

# Habilita el uso de zonas horarias
USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Tipo de campo de clave primaria por defecto
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CONFIGURACIONES ADICIONALES PARA NUESTRA APLICACIÓN DE ENCUESTAS
# =============================================================================

# Configuración adicional para archivos estáticos
# Directorio donde se almacenan los archivos estáticos en producción
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Directorios adicionales donde Django busca archivos estáticos
# Comentamos esto por ahora para evitar warnings, se puede crear después
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]

# Configuración para archivos multimedia (uploads de usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# CONFIGURACIÓN FINAL
# =============================================================================
# El proyecto está configurado y listo para usar con Django básico.
