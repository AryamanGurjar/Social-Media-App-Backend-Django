from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer, LoginSerializer

class RegisterUserView(generics.CreateAPIView):
    """Register User."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginUserView(generics.GenericAPIView):
    """
    Handle User Login.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_id = str(user.id)
        return Response({'id':user_id }, status=status.HTTP_200_OK)