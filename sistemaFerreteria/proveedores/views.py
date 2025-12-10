# proveedores/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Proveedor
from .forms import ProveedorForm

# 1. LISTAR (proveedor_list)
class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'proveedores/proveedor_list.html'
    context_object_name = 'proveedores'

# 2. CREAR (proveedor_create)
class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')

# 3. ACTUALIZAR (proveedor_update)
class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')

# 4. ELIMINAR (proveedor_delete)
class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'proveedores/proveedor_confirm_delete.html'
    success_url = reverse_lazy('proveedor_list')
