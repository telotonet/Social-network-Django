from rest_framework import serializers
from profiles.serializers import UserSerializer
from .models import Photo, Post, Comment

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    photos = PhotoSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at', 'updated_at', 'author', 'photos']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    photos = PhotoSerializer(many=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'photos']