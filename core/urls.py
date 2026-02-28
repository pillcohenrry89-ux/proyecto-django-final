from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('libros/', views.libros, name='libros'),
    path('list-libros/', views.list_libros, name='list_libros'),
    path('perfil/', views.perfil, name='perfil'),
    path('gestion/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('gestion/usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('cambiar-rol/<int:user_id>/', views.cambiar_rol, name='cambiar_rol'),
    path('eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]