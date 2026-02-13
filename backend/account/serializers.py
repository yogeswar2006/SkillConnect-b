from .models import *
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','username','password','email','bio','profile_img','created_at','last_login']
        read_only_fields=['id','created_at']
        extra_kwargs = {'password': {'write_only': True}} 
        
    def create(self, validated_data):
          password=validated_data.pop('password',None)
          user=CustomUser(**validated_data)
          if password:
              user.set_password(password)
          user.save()
          
          return user   
       
    def update(self, instance, validated_data):
         for key,value in validated_data.items():
             if key=='password':
                  instance.set_password(value)
             else:
                 setattr(instance,key,value)     
         instance.save()
         return instance  