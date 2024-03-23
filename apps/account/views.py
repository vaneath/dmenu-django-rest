from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_auth.registration.views import RegisterView
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from apps.authtoken.serializers import AuthTokenSerializerDecorator

from .models import UserDecorator
from .serializers import (LoginUserSerializer, RegisterUserSerializer,
                          UserSerializer)


class RegisterView(RegisterView):

    def get_response_data(self, user):
        return AuthTokenSerializerDecorator(data={'user': user, 'token': self.token}).data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        self.token = create_knox_token(None, user, None)
        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None)
        return user

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
