from rest_framework.serializers import ModelSerializer
from account.models import CustomUser
from rest_framework import serializers

class QueryUsersSerializer(ModelSerializer):
    
    class Meta:
        model=CustomUser
        fields=['id','username','email','profile_img']