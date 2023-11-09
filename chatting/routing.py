from django.urls import re_path, path
from chatting.consumers import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
