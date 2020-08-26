from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length = 200)
    email = serializers.CharField(max_length = 200)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value