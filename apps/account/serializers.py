from rest_framework import serializers

from .models import UserDecorator

# from knox


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDecorator
        fields = '__all__'

class CreateUserSerializer(serializers.ModelSerializer):
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

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDecorator
        fields = '__all__'

    def update(self, instance, validated_data):
        password = validated_data.pop('password')

        if password:
            instance.set_password(password)

        instance = super().update(instance, validated_data)

        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password', '')
        user = UserDecorator.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password.')
        attrs['user'] = user
        return attrs
