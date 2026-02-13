from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class SkillSerializer(ModelSerializer):
    class Meta:
        model=Skills
        fields=['id','name']

class UserSKillAddSerializer(ModelSerializer):
    skill_name=serializers.CharField(source='skill.name',read_only=True)              
    class Meta:
        model=UserSkill
        fields='__all__' 
        read_only_fields=['user']       
                
class WorkOfferSerializer(ModelSerializer):
    sender_username=serializers.CharField(source='offered_by.username',read_only=True)
    sender_profile_img=serializers.ImageField(source='offered_by.profile_img',read_only=True)
    
    
    
    class Meta:
        model=WorkOffers
        fields=['id','name','description','offered_by','sender_username','sender_profile_img','created_at']
        read_only_fields=['offered_by'] 

