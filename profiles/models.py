from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    status      = models.CharField(max_length=100, blank=True, null=True)
    is_online   = models.BooleanField(default=False)
    photo       = models.ImageField(upload_to='userphoto/', blank=True, null=True)

    def __str__(self):
        return 'Профиль: ' + self.user.username 
    



class FriendRequest(models.Model):
    from_user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at  = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    class Meta:
        unique_together = ['from_user', 'to_user', 'is_accepted']
    def __str__(self):
        return f"{self.from_user.username} to {self.to_user.username}"





