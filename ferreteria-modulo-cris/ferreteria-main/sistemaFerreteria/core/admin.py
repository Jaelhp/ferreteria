from django.contrib import admin
from .models import Cliente, Proveedor

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'activo')
    search_fields = ('nombre', 'telefono')
    list_filter = ('activo',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'telefono', 'terminos_pago', 'activo')
    search_fields = ('nombre', 'contacto')
    list_filter = ('activo',)