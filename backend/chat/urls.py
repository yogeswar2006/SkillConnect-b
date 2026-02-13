from django.urls import path, include
from .views import get_chat_messages

urlpatterns = [
    path("chats/<str:room_name>/messages/", get_chat_messages),
]
