# proveedores/forms.py
from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'ruc', 'telefono', 'email', 'direccion', 'activo']