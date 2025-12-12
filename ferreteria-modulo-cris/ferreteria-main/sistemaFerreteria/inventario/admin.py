from django.contrib import admin
from .models import MovimientoInventario

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'fecha', 'motivo', 
                    'stock_anterior', 'stock_nuevo')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre', 'motivo', 'referencia')
    readonly_fields = ('fecha',)