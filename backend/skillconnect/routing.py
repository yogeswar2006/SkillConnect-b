from chat.routing import websocket_urlpatterns as chat_ws
from friend.routing import websocket_urlpatterns as friend_ws

websocket_urlpatterns = chat_ws + friend_ws
