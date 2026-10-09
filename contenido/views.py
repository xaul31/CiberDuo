from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Perfil, Pregunta, Opcion, RegistroRespuesta, TipoAmenaza, Medio
from django.contrib.admin.views.decorators import staff_member_required

def inicio(request):
    perfiles = Perfil.objects.filter(activo=True)
    return render(request, 'contenido/inicio.html', {'perfiles': perfiles})


def perfil(request, slug):
    perfil = Perfil.objects.get(slug=slug)

    preguntas = Pregunta.objects.filter(perfil=perfil, activa=True)

    resultado = None
    retroalimentacion = None
    puntos_obtenidos = 0
    mensaje_puntos = None

    if request.method == 'POST':
        pregunta_id = request.POST.get('pregunta')
        opcion_id = request.POST.get('opcion')

        pregunta_respondida = Pregunta.objects.get(id=pregunta_id, perfil=perfil)

        opcion = Opcion.objects.get(id=opcion_id,pregunta=pregunta_respondida)

        if request.user.is_authenticated:
            ya_acertada = RegistroRespuesta.objects.filter( usuario= request.user, pregunta=pregunta_respondida, opcion__es_correcta=True).exists()


            RegistroRespuesta.objects.create(usuario=request.user,pregunta=pregunta_respondida,opcion=opcion)

        retroalimentacion = opcion.retroalimentacion

        if opcion.es_correcta:
            resultado = "¡Respuesta correcta!"
            if ya_acertada:
                puntos_obtenidos = 0
                mensaje_puntos = "Ya habías completado correctamente esta pregnta."
            else:
                puntos_obtenidos = pregunta_respondida.puntos
                mensaje_puntos = "Has obtenido nuevos puntos."
        else:
            resultado = "Respuesta incorrecta."
            puntos_obtenidos = 0




    return render(request, 'contenido/perfil.html', {'perfil': perfil, 'preguntas': preguntas, 'resultado': resultado, 'retroalimentacion': retroalimentacion, 'puntos_obtenidos': puntos_obtenidos, 'mensaje_puntos': mensaje_puntos})



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

@staff_member_required
def lista_preguntas(request):
    preguntas = Pregunta.objects.all()
    perfiles = Perfil.objects.all()
    busqueda = request.GET.get('buscar', '')
    perfil_id = request.GET.get('perfil', '')

    if busqueda:
        preguntas = preguntas.filter(enunciado__icontains=busqueda)

    if perfil_id:
        preguntas = preguntas.filter(perfil_id=perfil_id)

    return render(request, 'contenido/lista_preguntas.html', {'preguntas': preguntas, 'perfiles': perfiles, 'busqueda': busqueda, 'perfil_id': perfil_id})

@staff_member_required
def crear_pregunta(request):

    perfiles = Perfil.objects.all()
    tipos_amenaza = TipoAmenaza.objects.all()
    medios = Medio.objects.all()

    if request.method == 'POST':
        perfil_id = request.POST.get('perfil')
        tipo_amenaza_id = request.POST.get('tipo_amenaza')
        medio_id = request.POST.get('medio')
        enunciado = request.POST.get('enunciado')
        mensaje_simulado = request.POST.get('mensaje_simulado')
        explicacion = request.POST.get('explicacion')
        puntos = request.POST.get('puntos')

        perfil = Perfil.objects.get(id=perfil_id)
        tipo_amenaza = TipoAmenaza.objects.get(id=tipo_amenaza_id)
        medio = Medio.objects.get(id=medio_id)

        Pregunta.objects.create(
            perfil=perfil,
            tipo_amenaza=tipo_amenaza,
            medio=medio,
            enunciado=enunciado,
            mensaje_simulado=mensaje_simulado,
            explicacion=explicacion,
            puntos=puntos,
            activa=True
        )

        return redirect('lista_preguntas')

    return render(request, 'contenido/crear_pregunta.html', {'perfiles': perfiles, 'tipos_amenaza': tipos_amenaza, 'medios': medios})



@staff_member_required
def editar_pregunta(request, pregunta_id):
    pregunta = Pregunta.objects.get(id=pregunta_id)
    perfiles = Perfil.objects.all()
    tipos_amenaza = TipoAmenaza.objects.all()
    medios = Medio.objects.all()

    if request.method == 'POST':
        perfil_id = request.POST.get('perfil')
        tipo_amenaza_id = request.POST.get('tipo_amenaza')
        medio_id = request.POST.get('medio')

        pregunta.perfil = Perfil.objects.get(id=perfil_id)
        pregunta.tipo_amenaza = TipoAmenaza.objects.get(id=tipo_amenaza_id)
        pregunta.medio = Medio.objects.get(id=medio_id)

        pregunta.enunciado = request.POST.get('enunciado')
        pregunta.mensaje_simulado = request.POST.get('mensaje_simulado')
        pregunta.explicacion = request.POST.get('explicacion')
        pregunta.puntos = request.POST.get('puntos')

        pregunta.save()

        return redirect('lista_preguntas')

    return render(request, 'contenido/editar_pregunta.html', {'pregunta': pregunta, 'perfiles': perfiles, 'tipos_amenaza': tipos_amenaza, 'medios': medios})


@staff_member_required
def eliminar_pregunta(request, pregunta_id):

    pregunta = Pregunta.objects.get(id=pregunta_id)

    if request.method == 'POST':
        pregunta.delete()
        return redirect('lista_preguntas')

    return render(request, 'contenido/eliminar_pregunta.html', {'pregunta': pregunta})