from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Chat(models.Model):
    participants= models.ManyToManyField(User, related_name='chats')
    created     = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    creator     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_chat', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('chat_details', args=[str(self.id)])
    
    def __str__(self):
        participant_names = ", ".join(str(participant) for participant in self.participants.all())
        return participant_names

class Message(models.Model):
    chat    = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, blank=True, related_name='read_messages')

    class Meta:
        ordering = ['-timestamp']