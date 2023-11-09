from django.dispatch import receiver
from django.db.models.signals import post_save
from profiles.models import FriendRequest
from chatting.models import Message
from notifications.models import Notification

# @receiver(post_save, sender=FriendRequest)
# @receiver(post_save, sender=Message)
# def create_notification(sender, instance, created, **kwargs):
#     if created:
#         # Определение сообщения в зависимости от типа уведомления
#         if isinstance(instance, FriendRequest):
#             message = f"У вас новая заявка в друзья от {instance.from_user.username}."
#         elif isinstance(instance, Message):
#             message = f"У вас новое сообщение от {instance.from_user.username}."

#         # Создание уведомления
#         Notification.objects.create(
#             user=instance.to_user,
#             message=message
#         )