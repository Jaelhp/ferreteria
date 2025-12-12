from django.contrib import admin
from .models import Compra, DetalleCompra

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1
    fields = ('producto', 'cantidad', 'precio_unitario', 'subtotal')
    readonly_fields = ('subtotal',)


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('numero_compra', 'proveedor', 'fecha', 'total')
    search_fields = ('numero_compra', 'proveedor__nombre')
    list_filter = ('fecha',)
    inlines = [DetalleCompraInline]
    readonly_fields = ('total',)