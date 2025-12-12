from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    unidad_medida = models.CharField(max_length=20, default="unidad")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, 
                                      validators=[MinValueValidator(Decimal('0.01'))])
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, 
                                       validators=[MinValueValidator(Decimal('0.00'))])
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def necesita_reposicion(self):
        return self.stock_actual <= self.stock_minimo

    class Meta:
        verbose_name_plural = "Productos"