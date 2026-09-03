from django.contrib.auth.hashers import make_password
from django.db import models


class Usuario(models.Model):
	nombre = models.CharField(max_length=150)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=128)
	fecha_registro = models.DateTimeField(auto_now_add=True)

	def set_password(self, raw_password):
		self.password = make_password(raw_password)

	def __str__(self):
		return self.email
