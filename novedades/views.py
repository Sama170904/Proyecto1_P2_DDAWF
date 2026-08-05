from django.shortcuts import render, redirect
from django.contrib import messages
from frontend_nomina.api_client import APIClient
from authentication.decorators import login_required_api

@login_required_api
def lista_novedades(request):
    novedades = []
    error = None

    response = APIClient.get('/novedades/', request)
    if response and response.status_code == 200:
        novedades = response.json()
    else:
        error = "No se pudieron consultar las novedades."

    return render(request, 'novedades/list.html', {
        'novedades': novedades,
        'error': error,
        'title': 'Novedades Mensuales de Nómina'
    })


@login_required_api
def crear_novedad(request):
    # Fetch employees list for dropdown selection
    res_emp = APIClient.get('/empleados/', request)
    empleados = res_emp.json() if (res_emp and res_emp.status_code == 200) else []

    if request.method == 'POST':
        empleado_cedula = request.POST.get('empleado_cedula', '').strip()
        periodo = request.POST.get('periodo', '2026-07').strip()
        anticipos = float(request.POST.get('anticipos', 0.0))
        prestamo_iess = float(request.POST.get('prestamo_iess', 0.0))
        descuentos = float(request.POST.get('descuentos', 0.0))
        reembolsos = float(request.POST.get('reembolsos', 0.0))

        payload = {
            "empleado_cedula": empleado_cedula,
            "periodo": periodo,
            "anticipos": anticipos,
            "prestamo_iess": prestamo_iess,
            "descuentos": descuentos,
            "reembolsos": reembolsos
        }

        response = APIClient.post('/novedades/', request, json_data=payload)
        if response and response.status_code in [200, 201]:
            messages.success(request, f"Novedad registrada para el empleado {empleado_cedula} en el período {periodo}.")
            return redirect('novedades:list')
        else:
            detail = "No se pudo registrar la novedad."
            if response:
                try:
                    detail = response.json().get('detail', detail)
                except Exception:
                    detail = response.text
            messages.error(request, detail)

    return render(request, 'novedades/form.html', {
        'title': 'Registrar Novedad Mensual',
        'empleados': empleados
    })
