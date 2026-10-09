from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('perfil/<slug:slug>/', views.perfil, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('preguntas/', views.lista_preguntas, name='lista_preguntas'),
    path('preguntas/crear/', views.crear_pregunta, name='crear_pregunta'),
    path('preguntas/<int:pregunta_id>/editar/', views.editar_pregunta, name='editar_pregunta'),
    path('preguntas/<int:pregunta_id>/eliminar/', views.eliminar_pregunta, name='eliminar_pregunta'),
]