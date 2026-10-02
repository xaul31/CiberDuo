from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from contenido.models import Perfil, Pregunta, TipoAmenaza
from usuarios.models import Usuario

from .decorators import admin_required
from .forms import (
    OpcionFormSet,
    PanelLoginForm,
    PerfilForm,
    PreguntaForm,
    TipoAmenazaForm,
    UsuarioForm,
)


# ---------------------------------------------------------------- sesión

def login_view(request):
    if request.session.get('admin_id'):
        return redirect('panel:dashboard')

    form = PanelLoginForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        usuario = (
            Usuario.objects.select_related('perfil')
            .filter(email=form.cleaned_data['email'])
            .first()
        )
        if (
            usuario
            and usuario.check_password(form.cleaned_data['password'])
            and usuario.activo
            and usuario.es_admin
        ):
            request.session['admin_id'] = usuario.id
            return redirect('panel:dashboard')
        error = 'Credenciales inválidas o sin permisos de administrador.'

    return render(request, 'panel/login.html', {'form': form, 'error': error})


def logout_view(request):
    request.session.pop('admin_id', None)
    return redirect('panel:login')


# ---------------------------------------------------------------- dashboard

@admin_required
def dashboard(request):
    contexto = {
        'seccion': 'dashboard',
        'total_usuarios': Usuario.objects.count(),
        'usuarios_activos': Usuario.objects.filter(activo=True).count(),
        'total_preguntas': Pregunta.objects.count(),
        'preguntas_activas': Pregunta.objects.filter(activa=True).count(),
        'total_perfiles': Perfil.objects.count(),
        'total_amenazas': TipoAmenaza.objects.count(),
        'ultimos_usuarios': Usuario.objects.select_related('perfil').order_by('-fecha_registro')[:5],
        'preguntas_por_perfil': Perfil.objects.annotate(n=Count('preguntas')),
    }
    return render(request, 'panel/dashboard.html', contexto)


# ---------------------------------------------------------------- usuarios

@admin_required
def usuario_lista(request):
    usuarios = Usuario.objects.select_related('perfil')
    q = request.GET.get('q', '').strip()
    perfil = request.GET.get('perfil', '')
    activo = request.GET.get('activo', '')

    if q:
        usuarios = usuarios.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
    if perfil == 'none':
        usuarios = usuarios.filter(perfil__isnull=True)
    elif perfil:
        usuarios = usuarios.filter(perfil_id=perfil)
    if activo in ('1', '0'):
        usuarios = usuarios.filter(activo=(activo == '1'))

    return render(request, 'panel/usuario_lista.html', {
        'seccion': 'usuarios',
        'usuarios': usuarios,
        'perfiles': Perfil.objects.all(),
        'q': q, 'perfil_sel': perfil, 'activo_sel': activo,
    })


@admin_required
def usuario_form(request, pk=None):
    usuario = get_object_or_404(Usuario, pk=pk) if pk else None
    form = UsuarioForm(request.POST or None, instance=usuario)

    if request.method == 'POST' and form.is_valid():
        if usuario and usuario.pk == request.admin.pk:
            nuevo = form.save(commit=False)
            nuevo_perfil = nuevo.perfil
            if not nuevo.activo or nuevo_perfil is None or nuevo_perfil.slug != 'administrador':
                messages.error(request, 'No puedes desactivarte ni quitarte el perfil de administrador a ti mismo.')
                return render(request, 'panel/form.html', _ctx_form(form, 'usuarios', usuario, 'usuario'))
        form.save()
        messages.success(request, 'Usuario guardado.')
        return redirect('panel:usuario_lista')

    return render(request, 'panel/form.html', _ctx_form(form, 'usuarios', usuario, 'usuario'))


@admin_required
@require_POST
def usuario_toggle(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario.pk == request.admin.pk:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
    else:
        usuario.activo = not usuario.activo
        usuario.save(update_fields=['activo'])
        messages.success(request, f'{usuario.email} ahora está {"activo" if usuario.activo else "inactivo"}.')
    return redirect(request.META.get('HTTP_REFERER') or 'panel:usuario_lista')


@admin_required
def usuario_eliminar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario.pk == request.admin.pk:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('panel:usuario_lista')
    return _eliminar(request, usuario, 'usuarios', 'panel:usuario_lista', f'al usuario {usuario.email}')


# ---------------------------------------------------------------- preguntas

@admin_required
def pregunta_lista(request):
    preguntas = Pregunta.objects.select_related('perfil', 'tipo_amenaza').annotate(n_opciones=Count('opciones'))
    q = request.GET.get('q', '').strip()
    perfil = request.GET.get('perfil', '')
    amenaza = request.GET.get('amenaza', '')
    activa = request.GET.get('activa', '')

    if q:
        preguntas = preguntas.filter(enunciado__icontains=q)
    if perfil:
        preguntas = preguntas.filter(perfil_id=perfil)
    if amenaza:
        preguntas = preguntas.filter(tipo_amenaza_id=amenaza)
    if activa in ('1', '0'):
        preguntas = preguntas.filter(activa=(activa == '1'))

    return render(request, 'panel/pregunta_lista.html', {
        'seccion': 'preguntas',
        'preguntas': preguntas,
        'perfiles': Perfil.objects.all(),
        'amenazas': TipoAmenaza.objects.all(),
        'q': q, 'perfil_sel': perfil, 'amenaza_sel': amenaza, 'activa_sel': activa,
    })


@admin_required
def pregunta_form(request, pk=None):
    pregunta = get_object_or_404(Pregunta, pk=pk) if pk else None
    form = PreguntaForm(request.POST or None, instance=pregunta)
    formset = OpcionFormSet(request.POST or None, instance=pregunta)

    if request.method == 'POST' and form.is_valid():
        # el formset necesita la pregunta ya creada para validarse
        with transaction.atomic():
            pregunta = form.save()
            formset = OpcionFormSet(request.POST, instance=pregunta)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Pregunta guardada.')
                return redirect('panel:pregunta_lista')
            transaction.set_rollback(True)
        if pk is None:
            pregunta = None
            formset = OpcionFormSet(request.POST, instance=None)
            formset.is_valid()

    ctx = _ctx_form(form, 'preguntas', pregunta, 'pregunta')
    ctx['formset'] = formset
    return render(request, 'panel/pregunta_form.html', ctx)


@admin_required
def pregunta_eliminar(request, pk):
    pregunta = get_object_or_404(Pregunta, pk=pk)
    return _eliminar(request, pregunta, 'preguntas', 'panel:pregunta_lista', 'esta pregunta y sus opciones')


# ---------------------------------------------------------------- perfiles

@admin_required
def perfil_lista(request):
    perfiles = Perfil.objects.annotate(n_preguntas=Count('preguntas', distinct=True), n_usuarios=Count('usuarios', distinct=True))
    return render(request, 'panel/perfil_lista.html', {'seccion': 'perfiles', 'perfiles': perfiles})


@admin_required
def perfil_form(request, pk=None):
    perfil = get_object_or_404(Perfil, pk=pk) if pk else None
    form = PerfilForm(request.POST or None, instance=perfil)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfil guardado.')
        return redirect('panel:perfil_lista')
    return render(request, 'panel/form.html', _ctx_form(form, 'perfiles', perfil, 'perfil'))


@admin_required
def perfil_eliminar(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    if perfil.pk == request.admin.perfil_id:
        messages.error(request, 'No puedes eliminar tu propio perfil de administrador.')
        return redirect('panel:perfil_lista')
    return _eliminar(
        request, perfil, 'perfiles', 'panel:perfil_lista',
        f'el perfil "{perfil.nombre}" (se borrarán también sus preguntas; los usuarios quedarán sin perfil)',
    )


# ---------------------------------------------------------------- tipos de amenaza

@admin_required
def amenaza_lista(request):
    amenazas = TipoAmenaza.objects.annotate(n_preguntas=Count('preguntas'))
    return render(request, 'panel/amenaza_lista.html', {'seccion': 'amenazas', 'amenazas': amenazas})


@admin_required
def amenaza_form(request, pk=None):
    amenaza = get_object_or_404(TipoAmenaza, pk=pk) if pk else None
    form = TipoAmenazaForm(request.POST or None, instance=amenaza)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Tipo de amenaza guardado.')
        return redirect('panel:amenaza_lista')
    return render(request, 'panel/form.html', _ctx_form(form, 'amenazas', amenaza, 'tipo de amenaza'))


@admin_required
def amenaza_eliminar(request, pk):
    amenaza = get_object_or_404(TipoAmenaza, pk=pk)
    return _eliminar(request, amenaza, 'amenazas', 'panel:amenaza_lista', f'el tipo de amenaza "{amenaza.nombre}"')


# ---------------------------------------------------------------- helpers

def _ctx_form(form, seccion, objeto, nombre):
    return {
        'seccion': seccion,
        'form': form,
        'objeto': objeto,
        'titulo': f'Editar {nombre}' if objeto else f'Nuevo {nombre}',
        'volver': f'panel:{_LISTAS[seccion]}',
    }


_LISTAS = {
    'usuarios': 'usuario_lista',
    'preguntas': 'pregunta_lista',
    'perfiles': 'perfil_lista',
    'amenazas': 'amenaza_lista',
}


def _eliminar(request, objeto, seccion, destino, descripcion):
    if request.method == 'POST':
        try:
            objeto.delete()
            messages.success(request, 'Registro eliminado.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar: todavía hay preguntas que lo usan.')
        return redirect(destino)
    return render(request, 'panel/confirmar_eliminar.html', {
        'seccion': seccion,
        'descripcion': descripcion,
        'volver': destino,
    })