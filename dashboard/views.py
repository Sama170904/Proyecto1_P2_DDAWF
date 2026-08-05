from django.shortcuts import render
from frontend_nomina.api_client import APIClient
from authentication.decorators import login_required_api

@login_required_api
def index(request):
    empleados_count = 0
    novedades_count = 0
    nominas_count = 0
    api_status = "Desconectado"
    api_online = False

    # Check API status and fetch metrics
    res_emp = APIClient.get('/empleados/', request)
    if res_emp is not None and res_emp.status_code == 200:
        api_status = "200 OK (En línea)"
        api_online = True
        try:
            empleados_count = len(res_emp.json())
        except Exception:
            empleados_count = 0
    elif res_emp is not None and res_emp.status_code == 401:
        api_status = "Requiere Autenticación"
    
    if api_online:
        res_nov = APIClient.get('/novedades/', request)
        if res_nov and res_nov.status_code == 200:
            try:
                novedades_count = len(res_nov.json())
            except Exception:
                novedades_count = 0

        res_nom = APIClient.get('/nominas/historico/', request)
        if res_nom and res_nom.status_code == 200:
            try:
                nominas_count = len(res_nom.json())
            except Exception:
                nominas_count = 0

    context = {
        'title': "Panel de Control - Sistema de Nómina",
        'empleados_count': empleados_count,
        'novedades_count': novedades_count,
        'nominas_count': nominas_count,
        'api_status': api_status,
        'api_online': api_online,
        'sbu_vigente': 460.00,
        'periodo_actual': "2026-07"
    }

    return render(request, 'dashboard/index.html', context)
