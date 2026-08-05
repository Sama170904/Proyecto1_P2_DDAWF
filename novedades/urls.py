from django.urls import path
from . import views

app_name = 'novedades'

urlpatterns = [
    path('', views.lista_novedades, name='list'),
    path('nueva/', views.crear_novedad, name='create'),
]
