from django.shortcuts import redirect
from functools import wraps
from .models import Vendor


def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if Vendor.objects.filter(user=request.user).exists():
            return redirect("vendor_dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper


def vendor_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("vendor_login")

        if not Vendor.objects.filter(user=request.user).exists():
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper