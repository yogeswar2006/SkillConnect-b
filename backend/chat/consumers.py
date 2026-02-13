from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async



class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("USER:", self.scope["user"])
        print("WS USER:", self.scope["user"])
        print("IS AUTH:", self.scope["user"].is_authenticated)
        print(self.scope["user"].id)


        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        _, id1, id2 = room_name.split("_")
        ids = sorted([int(id1), int(id2)])
        print(ids)
        if user.id not in ids:
            await self.close()
            return

        self.room_group_name = f"chat_{ids[0]}_{ids[1]}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
    async def receive(self, text_data):
            data = json.loads(text_data)

            message_type = data["message_type"]
            content = data["content"]

            await self.save_message(message_type, content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message_type": message_type,
                    "content": content,
                    "sender_id": self.scope["user"].id,
                    "sender_username":self.scope["user"].username,
                }
            )
    async def disconnect(self, close_code):
      if hasattr(self, "room_group_name"):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

            
    @database_sync_to_async
    def save_message(self, message_type, content):
        from .models import Message, ChatRoom
        _, id1, id2 = self.room_group_name.split("_")
        room = ChatRoom.objects.get(user1_id=id1, user2_id=id2)

        return Message.objects.create(
            room=room,
            sender=self.scope["user"],
            message_type=message_type,
            content=content
        )
                
    async def chat_message(self, event):
       await self.send(text_data=json.dumps(event))
              
