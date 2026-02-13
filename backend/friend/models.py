from django.db import models
 

# Create your models here.

class FriendRequest(models.Model):
    sender = models.ForeignKey("account.CustomUser", related_name='sent_requests',  on_delete=models.CASCADE)
    receiver = models.ForeignKey("account.CustomUser",related_name='received_requests',on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[
            ("PENDING",'pending'),
            ("ACCEPTED",'accepted'),
            ("DECLINED",'declined')
        ],
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('sender','receiver')
    
    
    