from apps.authtoken.serializers import AuthTokenSerializerDecorator
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .models import UserDecorator
from .serializers import (LoginUserSerializer, RegisterUserSerializer,
                          UserSerializer)


class RegisterView(CreateAPIView):
  query_set = UserDecorator.objects.all()
  serializer_class = RegisterUserSerializer
  permission_classes = (AllowAny,)

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def get_user_serializer_class(self):
      return LoginUserSerializer
    
    def post(self, request, format=None):
        serializer = AuthTokenSerializerDecorator(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
