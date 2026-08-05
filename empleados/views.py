from django.shortcuts import render, redirect
from django.contrib import messages
from frontend_nomina.api_client import APIClient
from authentication.decorators import login_required_api

@login_required_api
def lista_empleados(request):
    empleados = []
    error = None

    response = APIClient.get('/empleados/', request)
    if response and response.status_code == 200:
        empleados = response.json()
    else:
        if response and response.status_code == 401:
            messages.warning(request, "Sesión no autenticada en Supabase/API. Inicie sesión para ver los empleados.")
        else:
            error = "No se pudieron obtener los empleados del backend."

    return render(request, 'empleados/list.html', {
        'empleados': empleados,
        'error': error,
        'title': 'Gestión de Empleados'
    })


@login_required_api
def crear_empleado(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula', '').strip()
        nombres = request.POST.get('nombres', '').strip()
        sueldo_basico = float(request.POST.get('sueldo_basico', 0))
        cuenta_bancaria = request.POST.get('cuenta_bancaria', '').strip()
        aporte_iess = float(request.POST.get('aporte_iess', 0.0945))
        bonificaciones = float(request.POST.get('bonificaciones', 0))
        prestamos = float(request.POST.get('prestamos', 0))
        decimos = request.POST.get('decimos') == 'on' or request.POST.get('decimos') == 'true' or request.POST.get('decimos') == 'True'
        fondos_reserva = request.POST.get('fondos_reserva') == 'on' or request.POST.get('fondos_reserva') == 'true' or request.POST.get('fondos_reserva') == 'True'

        if sueldo_basico < 460.0:
            messages.error(request, "El sueldo básico no puede ser menor al Salario Básico Unificado ($460.00).")
            return render(request, 'empleados/form.html', {'title': 'Nuevo Empleado', 'post_data': request.POST})

        form_data = {
            "cedula": cedula,
            "nombres": nombres,
            "sueldo_basico": sueldo_basico,
            "cuenta_bancaria": cuenta_bancaria,
            "aporte_iess": aporte_iess,
            "bonificaciones": bonificaciones,
            "prestamos": prestamos,
            "decimos": decimos,
            "fondos_reserva": fondos_reserva
        }

        # Call FastAPI POST /empleados_form/ or /empleados/
        response = APIClient.post('/empleados/', request, json_data=form_data)
        if response and response.status_code in [200, 201]:
            messages.success(request, f"Empleado '{nombres}' registrado exitosamente.")
            return redirect('empleados:list')
        else:
            detail = "Error al crear el empleado."
            if response:
                try:
                    detail = response.json().get('detail', detail)
                except Exception:
                    detail = response.text
            messages.error(request, detail)

    return render(request, 'empleados/form.html', {'title': 'Nuevo Empleado', 'post_data': {}})


@login_required_api
def editar_empleado(request, cedula):
    res = APIClient.get(f'/empleados/{cedula}', request)
    empleado = None
    if res and res.status_code == 200:
        empleado = res.json()
    else:
        messages.error(request, "Empleado no encontrado.")
        return redirect('empleados:list')

    if request.method == 'POST':
        nombres = request.POST.get('nombres', '').strip()
        sueldo_basico = float(request.POST.get('sueldo_basico', 0))
        cuenta_bancaria = request.POST.get('cuenta_bancaria', '').strip()
        aporte_iess = float(request.POST.get('aporte_iess', 0.0945))
        bonificaciones = float(request.POST.get('bonificaciones', 0))
        prestamos = float(request.POST.get('prestamos', 0))
        decimos = request.POST.get('decimos') == 'on' or request.POST.get('decimos') == 'true' or request.POST.get('decimos') == 'True'
        fondos_reserva = request.POST.get('fondos_reserva') == 'on' or request.POST.get('fondos_reserva') == 'true' or request.POST.get('fondos_reserva') == 'True'

        update_data = {
            "id": empleado.get('id'),
            "cedula": cedula,
            "nombres": nombres,
            "sueldo_basico": sueldo_basico,
            "cuenta_bancaria": cuenta_bancaria,
            "aporte_iess": aporte_iess,
            "bonificaciones": bonificaciones,
            "prestamos": prestamos,
            "decimos": decimos,
            "fondos_reserva": fondos_reserva
        }

        response = APIClient.put(f'/empleados/{cedula}', request, json_data=update_data)
        if response and response.status_code == 200:
            messages.success(request, f"Empleado '{nombres}' actualizado correctamente.")
            return redirect('empleados:list')
        else:
            detail = "Error al actualizar empleado."
            if response:
                try:
                    detail = response.json().get('detail', detail)
                except Exception:
                    pass
            messages.error(request, detail)

    return render(request, 'empleados/form.html', {
        'title': f'Editar Empleado ({cedula})',
        'empleado': empleado
    })


@login_required_api
def eliminar_empleado(request, cedula):
    if request.method == 'POST':
        response = APIClient.delete(f'/empleados/{cedula}', request)
        if response and response.status_code == 200:
            messages.success(request, f"Empleado {cedula} eliminado correctamente.")
        else:
            messages.error(request, "No se pudo eliminar el empleado.")
    return redirect('empleados:list')
