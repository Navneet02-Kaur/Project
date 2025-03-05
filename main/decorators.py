# filepath: /c:/Users/Admin/Desktop/django/carbon_connect/main/decorators.py
from django.shortcuts import redirect
from django.contrib import messages

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Please log in to access this page.')
            return redirect(f"/login?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper
