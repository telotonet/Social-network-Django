from django.contrib import admin
from django.urls import path
from .views import chat_details, chat_list, get_chat_messages, create_chat, chat_add_friend

urlpatterns = [
    path('chats/', chat_list, name='chat_list'),
    path('chat/create/<int:user_id>/', create_chat, name='create_chat'),
    path('chat/<int:chat_id>/', chat_details, name='chat_details'),
    path('chat/<int:chat_id>/messages/', get_chat_messages, name='get_chat_messages'),
    path('chat/<int:chat_id>/add_user/<int:user_id>/', chat_add_friend, name='chat_add_friend'),

]