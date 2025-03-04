# filepath: /c:/Users/Admin/Desktop/django/carbon_connect/main/decorators.py
from django.shortcuts import redirect
from django.contrib import messages

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session or request.session['role'] != 'organization':
            messages.error(request, 'Only Organizations Can List Projects! Please log in.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
