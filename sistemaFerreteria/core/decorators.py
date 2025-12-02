from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps

def role_required(*roles):
    """
    Decorador para restringir acceso por rol de usuario
    Uso: @role_required('administrador', 'vendedor')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.rol in roles or request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                else:
                    from django.contrib import messages
                    messages.error(request, 'No tienes permisos para acceder a esta sección')
                    return redirect('home')
            return redirect('login')
        return wrapper
    return decorator

def admin_required(view_func):
    """
    Decorador para vistas que solo puede acceder el administrador
    """
    return role_required('administrador')(view_func)

def vendedor_required(view_func):
    """
    Decorador para vistas accesibles por vendedor y administrador
    """
    return role_required('administrador', 'vendedor')(view_func)

def caja_required(view_func):
    """
    Decorador para vistas accesibles por caja y administrador
    """
    return role_required('administrador', 'caja')(view_func)

def proveedor_required(view_func):
    """
    Decorador para vistas accesibles por proveedor y administrador
    """
    return role_required('administrador', 'proveedor')(view_func)