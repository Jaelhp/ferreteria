from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    path("", views.venta_list, name="venta_list"),
    path("nueva/", views.venta_create, name="venta_create"),
    path("<int:pk>/", views.venta_detail, name="venta_detail"),
    path("<int:pk>/editar/", views.venta_update, name="venta_update"),
    path("<int:pk>/eliminar/", views.venta_delete, name="venta_delete"),
    path("<int:venta_id>/detalles/nuevo/", views.detalle_venta_create, name="detalle_venta_create"),
    path("detalles/<int:pk>/editar/", views.detalle_venta_update, name="detalle_venta_update"),
    path("detalles/<int:pk>/eliminar/", views.detalle_venta_delete, name="detalle_venta_delete"),
]
