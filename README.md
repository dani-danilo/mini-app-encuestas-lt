# 📊 Aplicación de Encuestas

Una aplicación web desarrollada con Django que permite a los usuarios crear encuestas, votar por opciones y ver los resultados actualizados automáticamente.

## 🚀 Características

- ✅ Crear y gestionar encuestas
- ✅ Votar por opciones
- ✅ Ver resultados actualizados automáticamente
- ✅ Interfaz web intuitiva y moderna
- ✅ Base de datos para almacenar todas las encuestas y votos
- ✅ Actualizaciones automáticas cada 30 segundos

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación principal
- **Django 4.2**: Framework web de Python
- **SQLite**: Base de datos (incluida con Django)
- **HTML/CSS/JavaScript**: Frontend
- **AJAX**: Para actualizar resultados automáticamente

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1. **Python 3.8 o superior**
   - Descarga desde: https://www.python.org/downloads/
   - Verifica la instalación: `python --version`

2. **Git** (opcional, pero recomendado)
   - Descarga desde: https://git-scm.com/

## 🔧 Instalación y Configuración

### Paso 1: Clonar o descargar el proyecto
```bash
# Si usas Git:
git clone <url-del-repositorio>
cd mini-app_encuestas_1

# O simplemente descarga y extrae el archivo ZIP
```

### Paso 2: Crear un entorno virtual (MUY IMPORTANTE)
```bash
# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar la base de datos
```bash
# Crear las tablas de la base de datos
python manage.py makemigrations
python manage.py migrate

# Crear un superusuario (administrador)
python manage.py createsuperuser
```

### Paso 5: Ejecutar el servidor
```bash
python manage.py runserver
```

### Paso 6: Abrir en el navegador
- Aplicación principal: http://127.0.0.1:8000/
- Panel de administración: http://127.0.0.1:8000/admin/

## 📁 Estructura del Proyecto

```
mini-app_encuestas_1/
├── manage.py                 # Comando principal de Django
├── requirements.txt          # Dependencias del proyecto
├── README.md                # Este archivo
├── encuestas_project/       # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py          # Configuraciones del proyecto
│   ├── urls.py              # URLs principales
│   ├── wsgi.py              # Configuración para servidor web
│   └── asgi.py              # Configuración para aplicaciones asíncronas
├── polls/                   # Aplicación de encuestas
│   ├── __init__.py
│   ├── admin.py             # Configuración del panel de admin
│   ├── apps.py              # Configuración de la aplicación
│   ├── models.py            # Modelos de base de datos
│   ├── views.py             # Lógica de las vistas
│   ├── urls.py              # URLs de la aplicación
│   ├── migrations/          # Migraciones de base de datos
│   ├── templates/           # Plantillas HTML
│   └── static/              # Archivos CSS, JS, imágenes
└── db.sqlite3               # Base de datos (se crea automáticamente)
```

## 🎯 Cómo Usar la Aplicación

### Para Usuarios Normales:
1. Ve a http://127.0.0.1:8000/
2. Selecciona una encuesta de la lista
3. Vota por tu opción favorita
4. Ve los resultados actualizarse en tiempo real

### Para Administradores:
1. Ve a http://127.0.0.1:8000/admin/
2. Inicia sesión con tu cuenta de superusuario
3. Crea nuevas encuestas y opciones
4. Ve las estadísticas de votos
5. Elimina votos

## 🔍 Explicación del Código

### Modelos (models.py)
- **Question**: Representa una pregunta de encuesta
- **Choice**: Representa una opción de respuesta
- **Vote**: Almacena cada voto individual

### Vistas (views.py)
- **index**: Muestra todas las encuestas disponibles
- **detail**: Muestra una encuesta específica para votar
- **vote**: Procesa el voto del usuario
- **results**: Muestra los resultados de una encuesta
- **results_json**: Proporciona datos en formato JSON para actualizar resultados automáticamente

### Actualización Automática
- **JavaScript + AJAX**: Actualiza los resultados cada 30 segundos sin recargar la página
- **Animaciones**: Efectos visuales suaves cuando se actualizan los números

## 🐛 Solución de Problemas

### Error: "No module named 'django'"
- Asegúrate de haber activado el entorno virtual
- Ejecuta: `pip install -r requirements.txt`

### Error: "Port already in use"
- Cambia el puerto: `python manage.py runserver 8001`

### La página no carga
- Verifica que el servidor esté ejecutándose
- Revisa la consola en busca de errores

## 📚 Recursos para Aprender Más

- [Documentación oficial de Django](https://docs.djangoproject.com/)
- [Tutorial oficial de Django](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
- [Django Channels Documentation](https://channels.readthedocs.io/)

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:
1. Haz un fork del proyecto
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Haz push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ve el archivo LICENSE para más detalles.

---
💡 **Tip**: Si eres nuevo en Django, te recomiendo seguir el tutorial oficial después de explorar esta aplicación.
