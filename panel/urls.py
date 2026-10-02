from django.urls import path
from django.views.generic import RedirectView

from usuarios import views as usuarios_views

from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', RedirectView.as_view(pattern_name='login'), name='login'),
    path('logout/', usuarios_views.userLogoutView, name='logout'),

    path('usuarios/', views.usuario_lista, name='usuario_lista'),
    path('usuarios/nuevo/', views.usuario_form, name='usuario_nuevo'),
    path('usuarios/<int:pk>/editar/', views.usuario_form, name='usuario_editar'),
    path('usuarios/<int:pk>/activo/', views.usuario_toggle, name='usuario_toggle'),
    path('usuarios/<int:pk>/eliminar/', views.usuario_eliminar, name='usuario_eliminar'),

    path('preguntas/', views.pregunta_lista, name='pregunta_lista'),
    path('preguntas/nueva/', views.pregunta_form, name='pregunta_nueva'),
    path('preguntas/<int:pk>/editar/', views.pregunta_form, name='pregunta_editar'),
    path('preguntas/<int:pk>/eliminar/', views.pregunta_eliminar, name='pregunta_eliminar'),

    path('perfiles/', views.perfil_lista, name='perfil_lista'),
    path('perfiles/nuevo/', views.perfil_form, name='perfil_nuevo'),
    path('perfiles/<int:pk>/editar/', views.perfil_form, name='perfil_editar'),
    path('perfiles/<int:pk>/eliminar/', views.perfil_eliminar, name='perfil_eliminar'),

    path('amenazas/', views.amenaza_lista, name='amenaza_lista'),
    path('amenazas/nueva/', views.amenaza_form, name='amenaza_nueva'),
    path('amenazas/<int:pk>/editar/', views.amenaza_form, name='amenaza_editar'),
    path('amenazas/<int:pk>/eliminar/', views.amenaza_eliminar, name='amenaza_eliminar'),
]