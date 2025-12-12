from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'precio_venta', 
                    'stock_actual', 'stock_minimo', 'necesita_reposicion', 'activo')
    search_fields = ('codigo', 'nombre')
    list_filter = ('categoria', 'activo')
    
    def necesita_reposicion(self, obj):
        return obj.necesita_reposicion
    necesita_reposicion.boolean = True