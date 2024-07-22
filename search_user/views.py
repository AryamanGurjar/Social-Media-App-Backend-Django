from rest_framework import generics

from user_auth.models import User

from .constants import EMAIL_IDENTIFIER
from .serializers import UserSerializer


from social_media_app.utils import CustomPageNumberPagination

from social_media_app.custome_decorator import validate_registered_user_uuid


class UserSearchView(generics.ListAPIView):
    """
    Searching for a user using it's email_id or name.
    """
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    @validate_registered_user_uuid
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        if EMAIL_IDENTIFIER in keyword:
            return User.objects.filter(email__iexact=keyword)
        return User.objects.filter(name__icontains=keyword)

    def get_serializer(self, *args, **kwargs):
        keyword = self.request.query_params.get('keyword', '')
        if EMAIL_IDENTIFIER in keyword:
            fields = ['email', 'name']
        else:
            fields = ['name']

        return self.get_serializer_class()(*args, fields=fields, **kwargs)