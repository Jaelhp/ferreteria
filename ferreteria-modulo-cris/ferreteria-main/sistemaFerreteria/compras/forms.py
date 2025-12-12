from django import forms
from .models import Compra, DetalleCompra


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ["numero_compra", "proveedor", "notas"]


class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ["producto", "cantidad", "precio_unitario"]
