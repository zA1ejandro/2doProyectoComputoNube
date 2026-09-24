from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Crea usuarios por defecto para pruebas si no existen en la base de datos MariaDB.'

    def handle(self, *args, **options):
        User = get_user_model()

        # Usuario administrador / superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@cocacola.com', 'admin123')
            self.stdout.write(self.style.SUCCESS(' Superusuario "admin" (clave: admin123) creado exitosamente.'))
        else:
            self.stdout.write(' Usuario "admin" ya existe.')

        # Usuario estándar de prueba
        if not User.objects.filter(username='coca_user').exists():
            User.objects.create_user('coca_user', 'usuario@cocacola.com', 'coca123')
            self.stdout.write(self.style.SUCCESS(' Usuario "coca_user" (clave: coca123) creado exitosamente.'))
        else:
            self.stdout.write(' Usuario "coca_user" ya existe.')
