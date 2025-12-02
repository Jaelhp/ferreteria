from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import admin_required, vendedor_required, caja_required, proveedor_required

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.get_full_name() or user.username}')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'core/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')

@login_required
def home(request):
    return render(request, 'core/home.html', {
        'usuario': request.user
    })

@admin_required
def vista_admin(request):
    return render(request, 'core/vista_admin.html')

@vendedor_required
def vista_vendedor(request):
    return render(request, 'core/vista_vendedor.html')

@caja_required
def vista_caja(request):
    return render(request, 'core/vista_caja.html')

@proveedor_required
def vista_proveedor(request):
    return render(request, 'core/vista_proveedor.html')