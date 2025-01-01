from django.urls import path
from . import views

# py manage.py runserver

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('iniciarSesion/', views.IniciarSesion, name='iniciarSesion'),
    path('logout', views.cerrarSesion, name='cerrarSesion'),
    path('admin/', views.admin, name='admin'),
    path('admin/carga-masiva/', views.adminCarga, name='adminCarga'),
    path('admin/carga-masiva-xml/', views.cargarXML, name='adminCargaXML'),
    path('admin/carga-masiva-enviar/', views.enviarXML, name='enviarXML'),
    path('admin/ver-usuarios/', views.adminVerUsuarios, name="adminVerUsuarios"),
    path('admin/ver-xml/', views.adminVerXML, name="adminVerXML"),
    path('admin/estadisticas/', views.adminVerEstadisticas, name="adminEstadisticas"),
    path('user/', views.user, name='user'),
    path('user/ayuda/', views.userAyuda, name='userAyuda'),
    path('user/cargar-imagen/', views.userCrearImg, name='userCrearImg'),
    path('user/cargar-imagen-xml/', views.userCargarXMLImagen, name='userCargarXML'),
    path('user/enviar-imagen-xml/', views.enviarXMLImagen, name='userenviarXML'),
    path('user/editar-imagen/', views.userEditarImg, name='userEditarImg'),
    path('user/editar-imagen-XML/', views.EditarImagenMatriz, name='userEditarImgXML'),
    path('user/ver-galeria/', views.userVerImagenes, name='userVerImagenes'),
]