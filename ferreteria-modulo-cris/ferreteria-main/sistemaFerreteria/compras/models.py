from django.db import models
from django.core.validators import MinValueValidator
from core.models import Proveedor
from productos.models import Producto

class Compra(models.Model):
    numero_compra = models.CharField(max_length=20, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='compras')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Compra {self.numero_compra} - {self.proveedor.nombre}"

    def calcular_total(self):
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = total
        self.save()
        return total

    class Meta:
        verbose_name_plural = "Compras"
        ordering = ['-fecha']


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.compra.calcular_total()

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    class Meta:
        verbose_name_plural = "Detalles de Compra"