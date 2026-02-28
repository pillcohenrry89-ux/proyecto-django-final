from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Perfil

def home(request):
    return render(request, 'core/home.html')

@login_required
def libros(request):
    return render(request, 'core/libros.html')

@login_required
def list_libros(request):
    return render(request, 'core/list_libros.html')

@login_required
def perfil(request):
    return render(request, 'core/perfil.html')

@login_required
def admin_usuarios(request):
    # Verificar si el usuario es admin
    if not request.user.is_superuser:
        messages.error(request, '⛔ Acceso denegado. Se requieren permisos de administrador.')
        return redirect('home')
    
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'core/admin_usuarios.html', {'usuarios': usuarios})

@login_required
def crear_usuario(request):
    # Solo administradores pueden crear usuarios
    if not request.user.is_superuser:
        messages.error(request, '⛔ No tienes permiso para crear usuarios.')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        rol = request.POST.get('rol', 'user')
        
        # Crear usuario
        usuario = User.objects.create_user(username=username, email=email, password=password)
        usuario.first_name = request.POST.get('first_name', '')
        usuario.last_name = request.POST.get('last_name', '')
        
        # Asignar rol
        if rol == 'admin':
            usuario.is_superuser = True
            usuario.is_staff = True
        elif rol == 'staff':
            usuario.is_superuser = False
            usuario.is_staff = True
        else:
            usuario.is_superuser = False
            usuario.is_staff = False
        
        usuario.save()
        messages.success(request, f'✅ Usuario {username} creado exitosamente!')
        return redirect('admin_usuarios')
    
    return render(request, 'core/crear_usuario.html')

@login_required
def cambiar_rol(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, '⛔ No tienes permiso.')
        return redirect('home')
    
    usuario = get_object_or_404(User, id=user_id)
    perfil, created = Perfil.objects.get_or_create(usuario=usuario)
    
    if request.method == 'POST':
        nuevo_rol = request.POST.get('rol')
        
        # Actualizar perfil
        perfil.rol = nuevo_rol
        perfil.save()
        
        # Actualizar permisos de Django
        if nuevo_rol == 'admin':
            usuario.is_superuser = True
            usuario.is_staff = True
        elif nuevo_rol == 'staff':
            usuario.is_superuser = False
            usuario.is_staff = True
        else:
            usuario.is_superuser = False
            usuario.is_staff = False
        
        usuario.save()
        messages.success(request, f'✅ {usuario.username} ahora es {perfil.get_rol_display()}')
        return redirect('admin_usuarios')
    
    return render(request, 'core/cambiar_rol.html', {
        'usuario': usuario,
        'perfil': perfil
    })

@login_required
def eliminar_usuario(request, user_id):
    # Verificar si el usuario es admin
    if not request.user.is_superuser:
        messages.error(request, '⛔ No tienes permiso para eliminar usuarios.')
        return redirect('home')
    
    usuario = get_object_or_404(User, id=user_id)
    
    if usuario == request.user:
        messages.error(request, '⛔ No puedes eliminar tu propio usuario.')
        return redirect('admin_usuarios')
    
    if request.method == 'POST':
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f'✅ Usuario {nombre} eliminado.')
        return redirect('admin_usuarios')
    
    return render(request, 'core/eliminar_usuario.html', {'usuario': usuario})