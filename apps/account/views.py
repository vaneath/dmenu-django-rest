from django.contrib.auth import login
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.settings import knox_settings
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import DateTimeField
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from .models import UserDecorator
from .serializers import (CreateUserSerializer, LoginSerializer,
                          UpdateUserSerializer, UserSerializer)


class RegisterUserAPI(CreateAPIView):
  query_set = UserDecorator.objects.all()
  serializer_class = CreateUserSerializer
  permission_classes = (AllowAny,)

class UpdateUserAPI(UpdateAPIView):
  query_set = UserDecorator.objects.all()
  serializer_class = UpdateUserSerializer

class LoginView(APIView):
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES

    def get_context(self):
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_token_limit_per_user(self):
        return knox_settings.TOKEN_LIMIT_PER_USER

    def get_user_serializer_class(self):
        return UserSerializer  # Use your custom UserSerializer

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def get_post_response_data(self, request, token, instance):
        user_serializer = self.get_user_serializer_class()

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }

        if user_serializer is not None:
            data["user"] = user_serializer(
                request.user,
                context=self.get_context()
            ).data

        return data

    def post(self, request, format=None):
        token_limit_per_user = self.get_token_limit_per_user()

        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)

            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )

        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)
        return Response(data)
