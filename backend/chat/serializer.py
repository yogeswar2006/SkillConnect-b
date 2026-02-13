from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(source="sender.id")

    class Meta:
        model = Message
        fields = ["id", "sender_id", "message_type", "content", "timestamp"]
