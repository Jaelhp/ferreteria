from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin-panel/', views.vista_admin, name='vista_admin'),
    path('vendedor-panel/', views.vista_vendedor, name='vista_vendedor'),
    path('caja-panel/', views.vista_caja, name='vista_caja'),
    path('proveedor-panel/', views.vista_proveedor, name='vista_proveedor'),
]