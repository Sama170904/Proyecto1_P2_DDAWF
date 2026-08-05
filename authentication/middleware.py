from django.shortcuts import redirect
from django.contrib import messages

class LoginRequiredMiddleware:
    """
    Middleware que protege todas las rutas del sistema excepto la autenticación.
    Si el usuario no tiene 'access_token' en su sesión, es redirigido al Login.
    """
    EXEMPT_PATHS = [
        '/auth/login/',
        '/auth/signup/',
        '/auth/logout/',
        '/admin/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Permitir rutas exentas y archivos estáticos
        if any(path.startswith(exempt) for exempt in self.EXEMPT_PATHS) or path.startswith('/static/'):
            return self.get_response(request)

        # Verificar si existe token en la sesión
        if not request.session.get('access_token'):
            messages.warning(request, "Debe iniciar sesión para acceder al sistema.")
            return redirect('login')

        return self.get_response(request)
