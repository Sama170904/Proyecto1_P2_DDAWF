from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def login_required_api(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('access_token'):
            messages.warning(request, "Debe iniciar sesión para acceder a este módulo.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
