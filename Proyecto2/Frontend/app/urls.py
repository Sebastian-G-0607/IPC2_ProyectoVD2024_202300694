from django.urls import path
from . import views

# py manage.py runserver

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('iniciarSesion/', views.IniciarSesion, name='iniciarSesion'),
    path('admin/', views.admin, name='admin'),
    path('admin/carga-masiva/', views.adminCarga, name='adminCarga'),
    path('admin/carga-masiva-xml/', views.cargarXML, name='adminCargaXML'),
    path('admin/carga-masiva-enviar/', views.enviarXML, name='enviarXML'),
    path('admin/ver-usuarios/', views.adminVerUsuarios, name="adminVerUsuarios"),
    path('admin/ver-xml/', views.adminVerXML, name="adminVerXML"),
    path('user/', views.user, name='user')
    # path('admin/', views.login, name='login'),
]