from django.shortcuts import render


def inicio(request):
	return render(request, 'grupo_estudiantes/inicio.html')
