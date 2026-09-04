from django.shortcuts import render


def inicio(request):
	respuestas_correctas = {
		'pregunta1': 'b',
		'pregunta2': 'c',
		'pregunta3': 'a',
		'pregunta4': 'b',
		'pregunta5': 'c',
	}
	buenas = None

	if request.method == 'POST':
		buenas = sum(
			request.POST.get(pregunta) == respuesta
			for pregunta, respuesta in respuestas_correctas.items()
		)

	return render(request, 'grupo_empresarios/inicio.html', {'buenas': buenas})
