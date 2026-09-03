from django.shortcuts import render


def inicio(request):
	return render(request, 'grupo_empresarios/inicio.html')
