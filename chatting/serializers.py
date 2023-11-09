from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message
from profiles.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Message
        fields= ['id', 'sender', 'content', 'timestamp', 'read_by']