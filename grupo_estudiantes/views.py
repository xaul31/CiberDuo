from django.shortcuts import render


def inicio(request):
	respuestas_correctas = {
		'pregunta1': 'b',
		'pregunta2': 'c',
		'pregunta3': 'a',
		'pregunta4': 'b',
		'pregunta5': 'b',
	}
	buenas = None

	if request.method == 'POST':
		buenas = sum(
			request.POST.get(pregunta) == respuesta
			for pregunta, respuesta in respuestas_correctas.items()
		)

	return render(request, 'grupo_estudiantes/inicio.html', {'buenas': buenas})
