from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['fullName', 'email', 'phone', 'avatar']
        read_only_fields = ['avatar']


class ProfileAvatarSerializer(serializers.ModelSerializer):
    url = serializers.ModelField(model_field=Profile()._meta.get_field('avatar'))

    class Meta:
        model = Profile
        fields = ['url', 'avatar']


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'username': {'read_only': True},
            # 'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)
