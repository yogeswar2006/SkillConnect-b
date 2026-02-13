from channels.generic.websocket import AsyncWebsocketConsumer
import json



class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
         user = self.scope["user"]
         
         if user.is_anonymous:
             await self.close()
             return
         
         self.group_name = f"user_{user.id}"
         
         await self.channel_layer.group_add(
             self.group_name,
             self.channel_name
         )
         
         await self.accept()
         
    async def friend_request(self,event):
        
        await self.send(text_data=json.dumps({
            "type":"FRIEND REQUEST",
            "id": event["id"],
            "sender_id":event["sender_id"],
            "sender_username":event['sender_username'],
            "sender_profile_image":event['sender_profile_image']
        }))
        
    async def friend_request_accepted(self,event):
        await self.send(text_data=json.dumps({
            "type":"FRIEND_REQUEST_ACCEPTED",
            "by_user_id":event["by_user_id"],
            "by_username": event["by_username"],
        }))    