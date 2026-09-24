import sys
import django
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from .models import Visit


def login_view(request):
    """
    Vista de autenticación con interfaz personalizada Coca-Cola
    y fondo blanco.
    """
    if request.user.is_authenticated:
        return redirect('core:hello_world')

    if request.method == 'POST':
        action = request.POST.get('action', 'login')
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if action == 'register':
            email = request.POST.get('email', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()

            if not username or not password:
                messages.error(request, 'Por favor, completa los campos obligatorios.')
            elif password != confirm_password:
                messages.error(request, 'Las contraseñas no coinciden.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, f'El usuario "{username}" ya se encuentra registrado.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, f'¡Usuario "{username}" creado exitosamente! Ahora puedes iniciar sesión.')
                return render(request, 'core/login.html', {
                    'initial_username': username,
                    'active_tab': 'login'
                })

        else:
            if not username or not password:
                messages.error(request, 'Debes ingresar usuario y contraseña.')
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    next_url = request.GET.get('next') or request.POST.get('next') or 'core:hello_world'
                    return redirect(next_url)
                else:
                    messages.error(request, 'Credenciales inválidas. Por favor revisa tu usuario y contraseña.')

    next_url = request.GET.get('next', '')
    return render(request, 'core/login.html', {
        'next': next_url,
        'active_tab': 'login'
    })


def logout_view(request):
    """
    Cierra la sesión del usuario actual y redirige a la página de login.
    """
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('core:login')


@login_required(login_url='core:login')
def hello_world(request):
    """
    Vista de 'Hola Mundo' protegida por autenticación que verifica
    la conexión en tiempo real con MariaDB y el ORM.
    """
    db_status = "Desconectado"
    db_version = "Desconocida"
    db_name = connection.settings_dict.get('NAME', 'mariadb_django')
    db_host = connection.settings_dict.get('HOST', 'db')
    db_port = connection.settings_dict.get('PORT', '3306')
    db_error = None
    visit_count = 0
    recent_visits = []

    try:
        # 1. Consulta directa al motor MariaDB para obtener su versión real
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            row = cursor.fetchone()
            if row:
                db_version = row[0]
        db_status = "Conectado exitosamente"

        # 2. Registrar la visita actual en la base de datos usando el ORM de Django
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if client_ip:
            ip_address = client_ip.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        user_agent = request.META.get('HTTP_USER_AGENT', 'Desconocido')[:250]
        Visit.objects.create(ip_address=ip_address, user_agent=user_agent)

        # 3. Consultar datos guardados
        visit_count = Visit.objects.count()
        recent_visits = Visit.objects.order_by('-timestamp')[:5]

    except Exception as e:
        db_status = "Error de conexión"
        db_error = str(e)

    context = {
        'django_version': django.get_version(),
        'python_version': sys.version.split()[0],
        'db_status': db_status,
        'db_version': db_version,
        'db_name': db_name,
        'db_host': db_host,
        'db_port': db_port,
        'db_error': db_error,
        'visit_count': visit_count,
        'recent_visits': recent_visits,
        'port': '8080',
        'current_user': request.user,
    }
    return render(request, 'core/index.html', context)
