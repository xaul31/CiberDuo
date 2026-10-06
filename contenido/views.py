from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Perfil, Pregunta, Opcion, RegistroRespuesta

def inicio(request):
    perfiles = Perfil.objects.filter(activo=True)
    return render(request, 'contenido/inicio.html', {'perfiles': perfiles})


def perfil(request, slug):
    perfil = Perfil.objects.get(slug=slug)

    preguntas = Pregunta.objects.filter(perfil=perfil, activa=True)

    resultado = None
    retroalimentacion = None

    if request.method == 'POST':
        pregunta_id = request.POST.get('pregunta')
        opcion_id = request.POST.get('opcion')

        pregunta_respondida = Pregunta.objects.get(id=pregunta_id)

        opcion = Opcion.objects.get(
            id=opcion_id,
            pregunta=pregunta_respondida
        )

        if request.user.is_authenticated:
            RegistroRespuesta.objects.create(
                usuario=request.user,
                pregunta=pregunta_respondida,
                opcion=opcion
            )

        retroalimentacion = opcion.retroalimentacion

        if opcion.es_correcta:
            resultado = "¡Respuesta correcta!"
        else:
            resultado = "Respuesta incorrecta."




    return render(request, 'contenido/perfil.html', {'perfil': perfil, 'preguntas': preguntas, 'resultado': resultado, 'retroalimentacion': retroalimentacion})



def registro(request):
    mensaje = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            mensaje = "El nombre de usuario ya está en uso."
        else:
            User.objects.create_user(username=username, password=password)

            return redirect('inicio')

    return render(request, 'contenido/registro.html', {'mensaje': mensaje})


def iniciar_sesion(request):
    mensaje = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect('inicio')
        else:
            mensaje = "Nombre de usuario o contraseña incorrectos."

    return render(request, 'contenido/login.html', {'mensaje': mensaje})


def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')
