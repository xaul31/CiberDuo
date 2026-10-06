from django.db import models
from django.conf import settings

# Create your models here.

class Perfil(models.Model):
    nombre = models.CharField(max_length=60)
    slug = models.CharField(unique=True, max_length=60)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'perfil'



class TipoAmenaza(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tipo_amenaza'

class Medio(models.Model):
    nombre = models.CharField(max_length=80)
    orden = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'medio'

class Pregunta(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    tipo_amenaza = models.ForeignKey(TipoAmenaza, on_delete=models.CASCADE)
    medio = models.ForeignKey(Medio, on_delete=models.CASCADE)
    enunciado = models.TextField()
    mensaje_simulado = models.TextField()
    explicacion = models.TextField()
    puntos = models.IntegerField()
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pregunta'


class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.TextField()
    es_correcta = models.BooleanField(default=False)
    retroalimentacion = models.TextField()
    orden = models.IntegerField()

    class Meta:
        db_table = 'opcion'


class RegistroRespuesta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registro_respuesta'

