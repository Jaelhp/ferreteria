# proveedores/models.py
from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre/Razón Social")
    # unique=True es vital para evitar RUCs duplicados
    ruc = models.CharField(max_length=15, unique=True, verbose_name="RUC")
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre