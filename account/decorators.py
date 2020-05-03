from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func

def allowed_users(allowed_rolls=[]):
    def decorators(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_rolls:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('you are not authorised to view this page')
        return wrapper_func
    return decorators


def admin_only(view_func):
    def wrapper_function(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customers':
            return redirect('user_page')
        if group == 'admin':
            return view_func(request,*args,**kwargs)
    return wrapper_function