from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('perfil/<slug:slug>/', views.perfil, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
]