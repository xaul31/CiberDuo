from django.contrib import admin
from django.urls import include, path
from grupo_adultoMayor import views as adulto_mayor_views
from grupo_estudiantes import views as estudiantes_views
from grupo_empresarios import views as empresarios_views
from vistaprincipal import views
from usuarios import views as usuarios_views
from contenido import views as contenido_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('panel.urls')),
    path('dashboard/', usuarios_views.login_required(views.vistaprincipal), name='vistaprincipal'),
    path('', usuarios_views.userLoginView, name='login'),
    path('registro/', usuarios_views.userRegistrationView, name='usuarios'),
    path('cerrar-sesion/', usuarios_views.userLogoutView, name='logout'),
    path('adulto-mayor/', usuarios_views.login_required(adulto_mayor_views.inicio), name='adulto_mayor'),
    path('estudiantes/', usuarios_views.login_required(estudiantes_views.inicio), name='estudiantes'),
    path('empresarios/', usuarios_views.login_required(empresarios_views.inicio), name='empresarios'),
    path('probar/<slug:perfil_slug>/', usuarios_views.login_required(contenido_views.cuestionario), name='cuestionario'),
]