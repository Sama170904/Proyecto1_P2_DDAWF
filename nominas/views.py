import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from frontend_nomina.api_client import APIClient
from authentication.decorators import login_required_api

@login_required_api
def calcular_nomina(request):
    resultados = None
    periodo = request.POST.get('periodo', '2026-07').strip() if request.method == 'POST' else request.GET.get('periodo', '2026-07')

    if request.method == 'POST':
        response = APIClient.post(f'/nominas/calcular/{periodo}', request)
        if response and response.status_code == 200:
            resultados = response.json()
            messages.success(request, f"Nómina para el período '{periodo}' calculada y procesada exitosamente ({len(resultados)} registros).")
        else:
            detail = "Error en la ejecución del cálculo de nómina."
            if response:
                try:
                    detail = response.json().get('detail', detail)
                except Exception:
                    detail = response.text
            messages.error(request, detail)

    return render(request, 'nominas/calcular.html', {
        'title': 'Cálculo Automatizado de Nómina',
        'periodo': periodo,
        'resultados': resultados
    })


@login_required_api
def historico_nominas(request):
    periodo_filter = request.GET.get('periodo', '').strip()
    endpoint = '/nominas/historico/'
    if periodo_filter:
        endpoint += f'?periodo={periodo_filter}'

    response = APIClient.get(endpoint, request)
    nominas = response.json() if (response and response.status_code == 200) else []

    return render(request, 'nominas/historico.html', {
        'title': 'Histórico de Roles de Pago',
        'nominas': nominas,
        'periodo_filter': periodo_filter
    })


@login_required_api
def rol_pagos(request, cedula, periodo):
    response = APIClient.get(f'/nominas/reporte/{cedula}/{periodo}', request)
    if response and response.status_code == 200:
        data = response.json()
        return render(request, 'nominas/rol_pagos.html', {
            'title': f'Rol de Pagos - {cedula} ({periodo})',
            'empleado': data.get('empleado'),
            'nomina': data.get('nomina'),
            'periodo': periodo
        })
    else:
        detail = "No se pudo recuperar el rol de pagos."
        if response:
            try:
                detail = response.json().get('detail', detail)
            except Exception:
                pass
        messages.error(request, detail)
        return redirect('nominas:historico')


@login_required_api
def conciliacion_anticipos(request):
    periodo = request.POST.get('periodo', '2026-07').strip() if request.method == 'POST' else '2026-07'
    reporte = None

    if request.method == 'POST':
        json_raw = request.POST.get('transacciones_json', '').strip()
        try:
            transacciones = json.loads(json_raw)
            if not isinstance(transacciones, list):
                raise ValueError("El JSON debe ser una lista de transacciones bancarias.")
            
            response = APIClient.post(f'/nominas/conciliar-anticipos/{periodo}', request, json_data=transacciones)
            if response and response.status_code == 200:
                reporte = response.json()
                messages.success(request, f"Conciliación bancaria completada para el período {periodo}.")
            else:
                detail = "Error procesando la conciliación."
                if response:
                    try:
                        detail = response.json().get('detail', detail)
                    except Exception:
                        pass
                messages.error(request, detail)
        except Exception as e:
            messages.error(request, f"JSON de transacciones inválido: {e}")

    default_example = json.dumps([
        {
            "cuenta_bancaria": "1234567890",
            "monto": 200.0,
            "referencia": "TRANSF-001"
        }
    ], indent=2)

    return render(request, 'nominas/conciliacion.html', {
        'title': 'Conciliación Bancaria de Anticipos',
        'periodo': periodo,
        'reporte': reporte,
        'default_example': default_example
    })


@login_required_api
def descargar_sat(request, periodo):
    response = APIClient.get(f'/nominas/archivo-sat/{periodo}', request)
    if response and response.status_code == 200:
        http_res = HttpResponse(response.content, content_type='text/plain')
        http_res['Content-Disposition'] = f'attachment; filename=archivo_sat_{periodo}.txt'
        return http_res
    else:
        messages.error(request, f"No se pudo generar el archivo SAT para el período '{periodo}'. Asegúrese de calcular la nómina primero.")
        return redirect('nominas:historico')


@login_required_api
def registrar_pago(request, nomina_id):
    if request.method == 'POST':
        estado = request.POST.get('estado', 'procesado')
        error_mensaje = request.POST.get('error_mensaje', '')

        payload = {
            "estado": estado,
            "error_mensaje": error_mensaje if estado == 'fallido' else None
        }

        response = APIClient.post(f'/nominas/{nomina_id}/registrar-pago', request, json_data=payload)
        if response and response.status_code == 200:
            data = response.json()
            if data.get('alerta_simulada'):
                messages.warning(request, data['alerta_simulada'])
            else:
                messages.success(request, f"Estado de pago de nómina #{nomina_id} actualizado a '{estado}'.")
        else:
            messages.error(request, "No se pudo actualizar el estado de pago.")

    return redirect('nominas:historico')
