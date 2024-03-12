from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import UserDecorator

# from knox


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDecorator
        fields = ['first_name', 'last_name', 'email']

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDecorator
        fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if UserDecorator.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email address already exists.')
        return attrs
    
    def create(self, validated_data):
        user = UserDecorator.objects.create_user(**validated_data)
        return user

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDecorator
        fields = ['first_name', 'last_name', 'email']
