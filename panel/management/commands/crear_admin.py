from getpass import getpass

from django.core.management.base import BaseCommand, CommandError

from contenido.models import Perfil
from usuarios.models import ADMIN_SLUG, Usuario


class Command(BaseCommand):
    help = 'Crea (o promueve) un usuario administrador para el panel /panel/.'

    def add_arguments(self, parser):
        parser.add_argument('--nombre', default='Administrador')
        parser.add_argument('--email', required=True)
        parser.add_argument('--password')

    def handle(self, *args, **opts):
        password = opts['password'] or getpass('Contraseña: ')
        if not password:
            raise CommandError('La contraseña no puede estar vacía.')

        perfil, _ = Perfil.objects.get_or_create(
            slug=ADMIN_SLUG,
            defaults={
                'nombre': 'Administrador',
                'descripcion': 'Acceso al panel de administración.',
                'orden': 99,
                'activo': False,  # no aparece como grupo público
            },
        )

        usuario, creado = Usuario.objects.get_or_create(
            email=opts['email'],
            defaults={'nombre': opts['nombre']},
        )
        usuario.perfil = perfil
        usuario.activo = True
        usuario.set_password(password)
        usuario.save()

        self.stdout.write(self.style.SUCCESS(
            f'Administrador {"creado" if creado else "actualizado"}: {usuario.email}'
        ))