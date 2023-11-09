from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['status', 'is_online', 'photo']

class UserSerializer(serializers.ModelSerializer):
    is_friend_request_sent = serializers.BooleanField(required=False)
    is_friend_request_received = serializers.BooleanField(required=False)
    is_friend = serializers.BooleanField(required=False)
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined', 'is_superuser', 'profile', 'is_friend_request_sent', 'is_friend', 'is_friend_request_received']

