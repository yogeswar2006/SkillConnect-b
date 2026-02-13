

from django.urls import path,re_path,include

from .consumers import ChatConsumer


websocket_urlpatterns =[
    re_path(
    r"ws/chat/(?P<room_name>chat_\d+_\d+)/$",
    ChatConsumer.as_asgi()
)
]