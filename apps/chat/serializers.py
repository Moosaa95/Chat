from rest_framework import serializers
from .models import User, Token

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        # Hash the password before saving
        from django.contrib.auth.hashers import make_password
        user = User.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password']),
            tokens=4000
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class ChatSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, max_length=1000)


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']