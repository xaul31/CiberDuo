from django.db import models


class Perfil(models.Model):
    """Grupo objetivo de la plataforma: Adulto Mayor, Estudiante, Microempresario."""

    nombre = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(
        max_length=60,
        unique=True,
        help_text='Se usa en la URL, por ejemplo: adulto-mayor',
    )
    descripcion = models.TextField(blank=True)
    orden = models.PositiveSmallIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        return self.nombre


class TipoAmenaza(models.Model):
    """Categoría de ataque: phishing, vishing, smishing, ransomware, Wi-Fi pública, etc."""

    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'tipo de amenaza'
        verbose_name_plural = 'tipos de amenaza'

    def __str__(self):
        return self.nombre


class Pregunta(models.Model):
    """Escenario simulado que se le presenta al usuario de un perfil."""

    class Medio(models.TextChoices):
        SMS = 'sms', 'SMS'
        CORREO = 'correo', 'Correo electrónico'
        LLAMADA = 'llamada', 'Llamada telefónica'
        WHATSAPP = 'whatsapp', 'WhatsApp'
        REDES = 'redes', 'Redes sociales'
        WEB = 'web', 'Sitio web'
        WIFI = 'wifi', 'Red Wi-Fi'
        PRESENCIAL = 'presencial', 'Presencial / equipo compartido'
        OTRO = 'otro', 'Otro'

    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name='preguntas',
    )
    tipo_amenaza = models.ForeignKey(
        TipoAmenaza,
        on_delete=models.PROTECT,
        related_name='preguntas',
    )
    enunciado = models.TextField(help_text='La situación y la pregunta que ve el usuario.')
    medio = models.CharField(max_length=20, choices=Medio.choices, default=Medio.OTRO)
    mensaje_simulado = models.TextField(
        blank=True,
        help_text='Opcional: texto del SMS, correo o mensaje falso que se le muestra al usuario.',
    )
    explicacion = models.TextField(
        blank=True,
        help_text='Por qué la respuesta correcta es la más segura.',
    )
    puntos = models.PositiveSmallIntegerField(default=10)
    orden = models.PositiveSmallIntegerField(default=0)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['perfil', 'orden', 'id']
        verbose_name = 'pregunta'
        verbose_name_plural = 'preguntas'

    def __str__(self):
        return f'[{self.perfil}] {self.enunciado[:60]}'

    @property
    def opcion_correcta(self):
        return self.opciones.filter(es_correcta=True).first()


class Opcion(models.Model):
    """Alternativa de respuesta de una pregunta. Solo una debe ser la correcta (se valida en el admin)."""

    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='opciones',
    )
    texto = models.CharField(max_length=300)
    es_correcta = models.BooleanField(default=False)
    retroalimentacion = models.TextField(
        blank=True,
        help_text='Opcional: qué pasa si el usuario elige esta opción.',
    )
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['pregunta', 'orden', 'id']
        verbose_name = 'opción'
        verbose_name_plural = 'opciones'

    def __str__(self):
        return self.texto[:60]