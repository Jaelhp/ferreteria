from django.urls import path
from . import views

app_name = "compras"

urlpatterns = [
    path("", views.compra_list, name="compra_list"),
    path("nueva/", views.compra_create, name="compra_create"),
    path("<int:pk>/", views.compra_detail, name="compra_detail"),
    path("<int:pk>/editar/", views.compra_update, name="compra_update"),
    path("<int:pk>/eliminar/", views.compra_delete, name="compra_delete"),
    path("<int:compra_id>/detalles/nuevo/", views.detalle_compra_create, name="detalle_compra_create"),
    path("detalles/<int:pk>/editar/", views.detalle_compra_update, name="detalle_compra_update"),
    path("detalles/<int:pk>/eliminar/", views.detalle_compra_delete, name="detalle_compra_delete"),
]
