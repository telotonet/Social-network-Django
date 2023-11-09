from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.generic.http import AsyncHttpConsumer
from asgiref.sync import sync_to_async
import json
import asyncio
from django.contrib.auth import get_user_model
from django.utils import timezone
from chatting.models import Chat, Message


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    connected_users = dict()
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)
        self.room_group_name = f'chat_room_{self.chat_id}'
        user = self.scope["user"]
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        is_user_in_chat = await sync_to_async(self.chat.participants.filter(id=user.id).exists)()
        if user.is_authenticated and is_user_in_chat:
            connected_users_dict = self.connected_users.get(f'{self.chat_id}')
            if connected_users_dict:
                connected_users_dict.append(user.id)
            else:
                connected_users_dict = self.connected_users[f'{self.chat_id}'] = []
                connected_users_dict.append(user.id)

            # Чтение всех непрочитанных сообщений для данного пользователя
            unread_messages = await sync_to_async(list)(self.chat.messages.exclude(read_by=user).filter(read_by__isnull=True))
            for message in unread_messages:
                for user_id in self.connected_users.get(f'{self.chat_id}', []):
                    if user_id != message.sender_id:
                        await self.update_message_read(user_id, message.id)
                await sync_to_async(message.read_by.add)(user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                'type': 'user_joined',
                'connected_users': self.connected_users.get(f'{self.chat_id}'),
                }
             )   

            await self.accept()
        else:
            await self.close()


    async def disconnect(self, close_code):
        user = self.scope.get('user') 
        self.connected_users.get(f'{self.chat_id}').remove(self.scope['user'].id)   # Удаление пользователя из хранилища
        if self.connected_users.get(f'{self.chat_id}') == []:                       # Удаление пользователя из хранилища
            del self.connected_users[f'{self.chat_id}']                             # Удаление пользователя из хранилища

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'user_joined',
            'connected_users': self.connected_users.get(f'{self.chat_id}'),
            }
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_typing',
                'typing_username': user.username,
                'typing_user_id': user.pk,
                'is_typing': False,
            })


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = self.scope.get('user')
        typing = text_data_json.get('typing')   
        if typing:
            if typing=='start_typing':
                typing = True
            else:
                typing = False
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_typing',
                    'typing_username': user.username,
                    'typing_user_id': user.pk,
                    'is_typing': typing,
                })


        is_message = text_data_json.get('message')
        if (is_message and user is not None):
            message = text_data_json['message']
            sender_id = None
            new_message = None
            if user is not None and user.is_authenticated:
                sender_id = user.id
                if self.chat_id is not None:
                    new_message = await self.save_message(self.chat_id, sender_id, message)
            user_from_db = await sync_to_async(User.objects.prefetch_related('profile').values('id', 'username', 'profile__status', 'profile__is_online', 'profile__photo').get)(pk=user.id)
            serialized_user = await sync_to_async(json.dumps)(user_from_db)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'user': serialized_user,
                    'message': message,
                    'sender_id': user.id,
                    'message_id': new_message.id,
                    'timestamp': str(timezone.now().strftime('%H:%M')),
                }
            )


    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        sender_id = event['sender_id']
        message_id = event['message_id']
        await self.send(text_data=json.dumps({
            "new_message": {
                'message': message,
                'user': user,
                'message_id': message_id,
                'timestamp': event['timestamp'],
            }
        }))
        # Обновление состояния прочтения сообщения для всех участников в группе
        for user_id in self.connected_users.get(f'{self.chat_id}', []):
            if user_id != sender_id:
                await self.update_message_read(user_id, message_id)


    async def update_message_read(self, user_id, message):
        recipient = await sync_to_async(User.objects.get)(id=user_id)
        msg = await sync_to_async(Message.objects.get)(pk=message)
        await sync_to_async(msg.read_by.add)(recipient)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message_read',
                'message_id': message,
            }
        )


    async def message_read(self, event):
        message_id = event['message_id']
        await self.send(text_data=json.dumps({
            "message_read": {
                'message_id': message_id,
            }
        }))

    
    async def user_joined(self, event):
        connected_users = event['connected_users']
        await self.send(text_data=json.dumps({
            "user_joined": {
                'connected_users': connected_users,
            }
        }))


    async def save_message(self, chat_id, sender_id, content):
        message = await sync_to_async(Message.objects.create)(chat_id=chat_id, sender_id=sender_id, content=content)
        return message


    async def chat_typing(self, event):
        username = event['typing_username']
        is_typing = event['is_typing']
        typing_user_id = event['typing_user_id']
        await self.send(text_data=json.dumps({
            "typing": {
                'username': username,
                'typing_user_id': typing_user_id,
                'is_typing': is_typing,
            }
        }))