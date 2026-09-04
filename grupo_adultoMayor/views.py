from django.shortcuts import render


def inicio(request):
	respuestas_correctas = {
		'pregunta1': 'b',
		'pregunta2': 'a',
		'pregunta3': 'c',
		'pregunta4': 'b',
		'pregunta5': 'a',
	}
	buenas = None

	if request.method == 'POST':
		buenas = sum(
			request.POST.get(pregunta) == respuesta
			for pregunta, respuesta in respuestas_correctas.items()
		)

	return render(request, 'grupo_adultoMayor/inicio.html', {'buenas': buenas})
