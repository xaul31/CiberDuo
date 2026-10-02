from functools import wraps

from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from . import forms
from .models import Usuario

# Create your views here.


def userRegistrationView(request):
    form = forms.userRegistrationForm()
    registrado = False
    data = {'form': form, 'registrado': registrado}

    if request.method == 'POST':
        form = forms.userRegistrationForm(request.POST)
        if form.is_valid():
            usuario = Usuario(
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
            )
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            registrado = True
            form = forms.userRegistrationForm()

            data = {'form': form, 'registrado': registrado}

    return render(request, 'userRegistration/userRegistration.html', data)


def userLoginView(request):
    form = forms.userLoginForm()
    error = None

    if request.method == 'POST':
        form = forms.userLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            usuario = Usuario.objects.select_related('perfil').filter(email=email).first()
            if usuario and check_password(form.cleaned_data['password'], usuario.password):
                if not usuario.activo:
                    error = 'Tu cuenta está desactivada. Contacta a un administrador.'
                else:
                    request.session['usuario_id'] = usuario.id
                    # Si es administrador, entra directo al panel
                    if usuario.es_admin:
                        request.session['admin_id'] = usuario.id
                        return redirect('panel:dashboard')
                    return redirect('vistaprincipal')
            else:
                error = 'El correo o la contraseña no son correctos.'

    return render(request, 'userLogin/userLogin.html', {'form': form, 'error': error})


def userLogoutView(request):
    request.session.flush()
    return redirect('login')


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')
        if not Usuario.objects.filter(pk=usuario_id, activo=True).exists():
            request.session.flush()
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapped_view