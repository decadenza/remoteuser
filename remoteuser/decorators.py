from functools import wraps
from django.http import HttpResponseForbidden

def write_permission_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.has_write_permission:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            return HttpResponseForbidden()

    return wraps(view_func)(_decorator)