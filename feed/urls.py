from django.urls import path
from .views import *

urlpatterns = [
    path('feed/', feed, name='feed'),
    path('post/<int:post_id>/', post_detail, name='post'),
    path('post/<int:object_id>/like/', like_object, {'content_type_id': 13}, name='like_post'),
    path('post/<int:post_id>/comment/create/', post_comment, {'content_type_id': 13}, name='post_comment'),
    path('create_post/', create_post, name='create_post'),
    path('comment/<int:object_id>/like/', like_object, {'content_type_id': 15}, name='like_comment'),
    path('photo/<int:object_id>/like/', like_object, {'content_type_id': 12}, name='like_photo'),
]