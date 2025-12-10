# proveedores/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProveedorListView.as_view(), name='proveedor_list'),
    path('crear/', views.ProveedorCreateView.as_view(), name='proveedor_create'),
    path('editar/<int:pk>/', views.ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('eliminar/<int:pk>/', views.ProveedorDeleteView.as_view(), name='proveedor_delete'),
]