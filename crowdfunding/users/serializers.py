from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length = 200)
    email = serializers.CharField(max_length = 200)
    password = serializers.CharField(write_only=True)
    bio=serializers.CharField()
    location=serializers.CharField()
    # is_active=serializers.BooleanField() #eventually turns to true?
    is_mentor=serializers.BooleanField()
    #image = serializers.URLField( null = True)
    #media_link = serializers.URLField( null = True)

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}

#once serializer.save = validated_data got pass in as parameter to then trigger this update
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.is_mentor = validated_data.get('is_mentor', instance.is_mentor)
        instance.save()
        return instance


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