from django.shortcuts import render


def inicio(request):
	return render(request, 'grupo_adultoMayor/inicio.html')
