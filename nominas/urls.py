from django.urls import path
from . import views

app_name = 'nominas'

urlpatterns = [
    path('calcular/', views.calcular_nomina, name='calcular'),
    path('historico/', views.historico_nominas, name='historico'),
    path('reporte/<str:cedula>/<str:periodo>/', views.rol_pagos, name='rol_pagos'),
    path('conciliacion/', views.conciliacion_anticipos, name='conciliacion'),
    path('sat/<str:periodo>/', views.descargar_sat, name='descargar_sat'),
    path('<int:nomina_id>/registrar-pago/', views.registrar_pago, name='registrar_pago'),
]
