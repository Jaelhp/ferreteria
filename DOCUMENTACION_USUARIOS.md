# Sistema de Usuarios y Permisos - Ferretería

## Configuración Implementada

### 1. Modelo de Usuario Personalizado
- Se extendió `AbstractUser` para crear un modelo `Usuario` con campo de rol
- Roles disponibles: Administrador, Vendedor, Caja, Proveedor

### 2. Sistema de Autenticación
- Login: `/login/`
- Logout: `/logout/`
- Home: `/` (requiere autenticación)

### 3. Decoradores de Protección por Rol

#### Decoradores disponibles:
- `@login_required` - Solo usuarios autenticados
- `@role_required('rol1', 'rol2')` - Roles específicos
- `@admin_required` - Solo administradores
- `@vendedor_required` - Vendedores y administradores
- `@caja_required` - Caja y administradores
- `@proveedor_required` - Proveedores y administradores

#### Ejemplo de uso:
```python
from core.decorators import vendedor_required

@vendedor_required
def mi_vista(request):
    return render(request, 'template.html')
```

### 4. Permisos por Rol

| Rol | Permisos |
|-----|----------|
| Administrador | Acceso completo a todos los módulos |
| Vendedor | Productos (consulta), Ventas (registro) |
| Caja | Ventas (procesamiento de pagos) |
| Proveedor | Compras (registro de entregas) |

### 5. Estructura de Archivos Creados/Modificados
```
core/
├── models.py (Usuario, Cliente, Proveedor)
├── views.py (login, logout, home, vistas protegidas)
├── decorators.py (decoradores de permisos)
├── admin.py (registro de modelos)
└── templates/
    └── core/
        ├── base.html
        ├── login.html
        ├── home.html
        ├── vista_admin.html
        ├── vista_vendedor.html
        ├── vista_caja.html
        └── vista_proveedor.html

sistemaFerreteria/
├── settings.py (AUTH_USER_MODEL, LOGIN_URL configurados)
└── urls.py (rutas de autenticación)
```

### 6. Configuración en settings.py
```python
AUTH_USER_MODEL = 'core.Usuario'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
```

## Cómo Usar

### Crear usuarios desde el admin:
1. Acceder a `/admin/`
2. Ir a "Usuarios"
3. Crear usuario y asignar rol correspondiente

### Proteger una vista nueva:
```python
from core.decorators import vendedor_required

@vendedor_required
def nueva_vista(request):
    # Tu código aquí
    return render(request, 'template.html')
```

## Comandos Útiles
```bash
# Crear superusuario
python manage.py createsuperuser

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejecutar servidor
python manage.py runserver
```

## Próximos Pasos Sugeridos

1. Implementar las vistas completas para cada módulo (productos, ventas, compras, inventario)
2. Agregar formularios específicos para cada rol
3. Implementar reportes según permisos
4. Agregar validaciones adicionales en formularios según rol
