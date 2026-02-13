from django.db import models
from django.conf import settings




# Create your models here.


                            # Work domain Flow
class Skills(models.Model):
   
    name=models.CharField(max_length=200,unique=True)
  
    def __str__(self):
        return self.name
                                   
                            
class UserSkill(models.Model):
    
    class Proficiency(models.IntegerChoices):
        BEGINNER=1,'beginner'
        INTERMEDIATE=2,'intermediate'
        PRO=3,'pro'
        
    
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="user_skills")
    skill=models.ForeignKey(Skills,on_delete=models.CASCADE,related_name="user_skills")
    proficiency_level=models.IntegerField(choices=Proficiency.choices, default=Proficiency.BEGINNER)
    description=models.TextField()
    years_of_experience=models.IntegerField()
    added_at=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user.username} added {self.skill.name} skill"

class WorkOffers(models.Model):
    offered_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="user_offers")
    description=models.TextField()
    name=models.CharField(max_length=300)
    # price=models.PositiveBigIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    # skills_required=models.ForeignKey(Skills,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.offered_by.username} offered {self.name} job"   
    
    
    # Not now(Future)
class WorkRequests(models.Model):
    class Status(models.IntegerChoices): # one of the way to use enums(Choices)😊
        ACCEPTED=1,"accepted"
        PENDING=2,"pending"
    
    
    requested_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=300)
    description=models.TextField()
    budget=models.DecimalField(max_digits=6,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.IntegerField(choices=Status.choices,default=Status.PENDING) 
    
    def __str__(self):
        return f"{self.requested_by.username} requested {self.name} work"      
                 
                 
           # Not now(Future)                      
class WorkMatches(models.Model):
    class Status(models.IntegerChoices): # one of the way to use enums(Choices)😊
        ACCEPTED=1,"accepted"
        DECLINED=2,"declined"
        PENDING=3,"pending"
    
    offered=models.ForeignKey(WorkOffers,on_delete=models.CASCADE)
    status=models.IntegerField(choices=Status.choices,default=Status.PENDING)
    matched_at=models.DateTimeField(auto_now_add=True)
    requested=models.ForeignKey(WorkRequests,on_delete=models.CASCADE)
    
                                       