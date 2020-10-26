from django.http import HttpResponse
from django.shortcuts import render, redirect

def unauthenticated_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/whitebricks/home/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_function


