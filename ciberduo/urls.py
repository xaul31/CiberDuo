"""
URL configuration for ciberduo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from grupo_adultoMayor import views as adulto_mayor_views
from grupo_estudiantes import views as estudiantes_views
from grupo_empresarios import views as empresarios_views
from vistaprincipal import views
from usuarios import views as usuarios_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', usuarios_views.login_required(views.vistaprincipal), name='vistaprincipal'),
    path('', usuarios_views.userLoginView, name='login'),
    path('registro/', usuarios_views.userRegistrationView, name='usuarios'),
    path('cerrar-sesion/', usuarios_views.userLogoutView, name='logout'),
    path('adulto-mayor/', usuarios_views.login_required(adulto_mayor_views.inicio), name='adulto_mayor'),
    path('estudiantes/', usuarios_views.login_required(estudiantes_views.inicio), name='estudiantes'),
    path('empresarios/', usuarios_views.login_required(empresarios_views.inicio), name='empresarios'),
]
