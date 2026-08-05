from django.shortcuts import render, redirect
from django.contrib import messages
from frontend_nomina.api_client import APIClient

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        response = APIClient.post('/auth/login', json_data={"email": email, "password": password})
        if response and response.status_code == 200:
            data = response.json()
            request.session['access_token'] = data.get('access_token')
            request.session['user_email'] = email
            request.session['user_data'] = data.get('user', {})
            messages.success(request, f"¡Bienvenido de nuevo, {email}!")
            return redirect('dashboard:index')
        else:
            error_msg = "Credenciales incorrectas o servidor no disponible."
            if response:
                try:
                    error_msg = response.json().get('detail', error_msg)
                except Exception:
                    pass
            messages.error(request, error_msg)

    return render(request, 'security/login.html')


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        response = APIClient.post('/auth/signup', json_data={"email": email, "password": password})
        if response and response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            if token:
                request.session['access_token'] = token
                request.session['user_email'] = email
                request.session['user_data'] = data.get('user', {})
                messages.success(request, "Cuenta creada exitosamente. Has iniciado sesión.")
                return redirect('dashboard:index')
            else:
                messages.success(request, "Cuenta registrada exitosamente. Por favor inicie sesión.")
                return redirect('login')
        else:
            error_msg = "No se pudo registrar la cuenta."
            if response:
                try:
                    error_msg = response.json().get('detail', error_msg)
                except Exception:
                    pass
            messages.error(request, error_msg)

    return render(request, 'security/signup.html')


def logout_view(request):
    request.session.flush()
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')
