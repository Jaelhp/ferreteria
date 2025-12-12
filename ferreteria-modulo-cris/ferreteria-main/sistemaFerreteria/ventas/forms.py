from django import forms
from .models import Venta, DetalleVenta


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ["numero_venta", "cliente", "notas"]


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ["producto", "cantidad", "precio_unitario"]
