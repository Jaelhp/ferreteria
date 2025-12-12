from django.contrib import admin
from .models import Venta, DetalleVenta

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    fields = ('producto', 'cantidad', 'precio_unitario', 'subtotal')
    readonly_fields = ('subtotal',)


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('numero_venta', 'cliente', 'fecha', 'total')
    search_fields = ('numero_venta', 'cliente__nombre')
    list_filter = ('fecha',)
    inlines = [DetalleVentaInline]
    readonly_fields = ('total',)