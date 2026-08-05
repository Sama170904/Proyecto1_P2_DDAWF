from django.urls import path
from . import views

app_name = 'empleados'

urlpatterns = [
    path('', views.lista_empleados, name='list'),
    path('nuevo/', views.crear_empleado, name='create'),
    path('<str:cedula>/editar/', views.editar_empleado, name='edit'),
    path('<str:cedula>/eliminar/', views.eliminar_empleado, name='delete'),
]
