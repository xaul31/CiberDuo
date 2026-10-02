from functools import wraps

from django.shortcuts import redirect

from usuarios.models import Usuario


def admin_required(view_func):
    """Solo deja pasar a usuarios activos con perfil 'administrador'."""

    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        admin_id = request.session.get('admin_id')
        admin = (
            Usuario.objects.select_related('perfil')
            .filter(pk=admin_id, activo=True)
            .first()
            if admin_id else None
        )
        if admin is None or not admin.es_admin:
            request.session.pop('admin_id', None)
            return redirect('login')
        request.admin = admin
        return view_func(request, *args, **kwargs)

    return wrapped