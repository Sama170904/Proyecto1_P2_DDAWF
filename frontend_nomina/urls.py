from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('empleados/', include('empleados.urls')),
    path('novedades/', include('novedades.urls')),
    path('nominas/', include('nominas.urls')),
    path('', include('dashboard.urls')),
]
