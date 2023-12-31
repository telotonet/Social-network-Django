# Generated by Django 4.2.2 on 2023-06-19 23:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatting', '0004_chat_created_chat_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_chat', to=settings.AUTH_USER_MODEL),
        ),
    ]
