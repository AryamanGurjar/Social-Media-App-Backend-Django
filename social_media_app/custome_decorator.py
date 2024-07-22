import uuid
from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from user_auth.models import User


def validate_registered_user_uuid(view_func):
    """
    Checks than only registered user is allowed to do task in the platform.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            uuid_obj = uuid.UUID(user_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid UUID format'}, status=400)
        registered_user = get_object_or_404(User, id=uuid_obj)
        return view_func(request, *args, **kwargs)

    return wrapper
