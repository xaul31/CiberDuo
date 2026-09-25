from django.shortcuts import get_object_or_404, render

from .models import Perfil


def cuestionario(request, perfil_slug):
    """Muestra las preguntas de un perfil leyéndolas desde la base de datos
    (modelos Perfil / TipoAmenaza / Pregunta / Opcion) y corrige el intento."""

    perfil = get_object_or_404(Perfil, slug=perfil_slug, activo=True)
    preguntas = (
        perfil.preguntas
        .filter(activa=True)
        .prefetch_related('opciones')
    )

    resultado = None  # None = todavía no envía el formulario

    if request.method == 'POST':
        correctas = 0
        detalle = []  # para mostrar qué falló, opcional en el template

        for pregunta in preguntas:
            opcion_elegida_id = request.POST.get(f'pregunta_{pregunta.id}')
            opcion_correcta = pregunta.opcion_correcta
            es_correcta = (
                opcion_elegida_id is not None
                and opcion_correcta is not None
                and str(opcion_correcta.id) == opcion_elegida_id
            )
            if es_correcta:
                correctas += 1

            detalle.append({
                'pregunta': pregunta,
                'opcion_elegida_id': opcion_elegida_id,
                'es_correcta': es_correcta,
            })

        resultado = {
            'correctas': correctas,
            'total': preguntas.count(),
            'detalle': detalle,
        }

    return render(
        request,
        'contenido/cuestionario.html',
        {
            'perfil': perfil,
            'preguntas': preguntas,
            'resultado': resultado,
        },
    )