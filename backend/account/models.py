from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField  


class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    bio=models.TextField(blank=True)
    profile_img=CloudinaryField('avatar', blank=True, null=True)  
   
    created_at=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username


