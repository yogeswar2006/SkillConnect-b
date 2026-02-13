from django.shortcuts import render
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatRoom,Message
from .serializer import MessageSerializer
# Create your views here.



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_chat_messages(request, room_name):
    _, id1, id2 = room_name.split("_")
    ids = sorted([int(id1), int(id2)])

    if request.user.id not in ids:
        return Response(status=403)

    room, _ = ChatRoom.objects.get_or_create(
        user1_id=ids[0],
        user2_id=ids[1]
    )

    messages = Message.objects.filter(room=room).order_by("timestamp")
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
