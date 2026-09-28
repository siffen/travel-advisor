from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Destination, Favorite, UserProfile


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "full_name"]

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value.lower().strip()

    def create(self, validated_data):
        full_name = validated_data.pop("full_name", "")
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, full_name=full_name)
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="profile.full_name", allow_blank=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "full_name"]


class FavoriteSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "destination", "created_at"]
