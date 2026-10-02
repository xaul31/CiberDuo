from django.contrib.auth.hashers import check_password, make_password
from django.db import models

ADMIN_SLUG = 'administrador'


class Usuario(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    perfil = models.ForeignKey(
        'contenido.Perfil',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def es_admin(self):
        """Es administrador si su perfil es el perfil 'administrador'."""
        return self.perfil_id is not None and self.perfil.slug == ADMIN_SLUG

    def __str__(self):
        return self.email